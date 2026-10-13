"""Bộ kiểm thử Hộp trắng nâng cao (Extended White-box Tests)
Chuyên trách: Member 4 - Nguyễn Hữu Đăng Khoa
Mục tiêu: Bao phủ 100% các nhánh rẽ điều kiện (Branch Coverage) và đạt độ phủ tổng thể > 96%.
"""

from datetime import UTC, datetime, timedelta
import pytest
from models import FormulaNote, ReviewLog, Setting, SpeedReviewSession, Word, WordProgress, db
from srs import apply_learning_result, apply_review_result, complete_initial_learning, utc_now


# ==============================================================================
# 1. KIỂM THỬ NGOẠI LỆ & NHÁNH RẼ TRONG SRS.PY
# ==============================================================================


def test_srs_apply_learning_result_raises_value_error_when_already_learned(app, add_word):
    """Bao phủ srs.py dòng 62: Ngoại lệ khi học từ đã ở trạng thái 'learned'."""
    word_dict = add_word(english="innovate", vietnamese="đổi mới")
    with app.app_context():
        word = db.session.get(Word, word_dict["id"])
        word.progress.state = "learned"
        db.session.commit()

        with pytest.raises(ValueError, match="Từ này đã hoàn tất giai đoạn học mới"):
            apply_learning_result(word.progress, correct=True, now=datetime.now(UTC).replace(tzinfo=None))


def test_srs_apply_review_result_raises_value_error_when_not_learned(app, add_word):
    """Bao phủ srs.py dòng 81: Ngoại lệ khi ôn tập từ chưa 'learned'."""
    word_dict = add_word(english="prototype", vietnamese="nguyên mẫu")
    with app.app_context():
        word = db.session.get(Word, word_dict["id"])
        word.progress.state = "new"  # Chưa learned
        db.session.commit()

        with pytest.raises(ValueError, match="Từ này chưa hoàn tất giai đoạn học mới"):
            apply_review_result(word.progress, correct=True, now=datetime.now(UTC).replace(tzinfo=None))


# ==============================================================================
# 2. KIỂM THỬ BẢO MẬT & VALIDATION TRONG APP.PY
# ==============================================================================


def test_bulk_import_limit_1000_items(client):
    """Bao phủ app.py dòng 620-621: Giới hạn tối đa 1.000 từ mỗi lần bulk import."""
    huge_items = [{"english": f"word{i}", "vietnamese": f"nghia{i}", "part_of_speech": "noun"} for i in range(1001)]
    res = client.post("/api/words/bulk", json={"items": huge_items})
    assert res.status_code == 400
    assert "1.000 từ" in res.get_json()["error"]


def test_update_word_not_found_returns_404(client):
    """Bao phủ app.py dòng 665: Cập nhật từ không tồn tại trả về 404."""
    res = client.put("/api/words/99999", json={"english": "fake", "vietnamese": "giả"})
    assert res.status_code == 404


def test_reset_word_not_found_returns_404(client):
    """Bao phủ app.py dòng 689: Đặt lại tiến độ từ không tồn tại trả về 404."""
    res = client.post("/api/words/99999/reset")
    assert res.status_code == 404


def test_study_new_empty_returns_empty_list(client):
    """Bao phủ app.py dòng 706-719: Phiên học từ mới khi kho rỗng."""
    res = client.get("/api/study/new")
    assert res.status_code == 200
    assert res.get_json()["items"] == []


def test_study_review_empty_returns_empty_list(client):
    """Bao phủ app.py dòng 729-742: Phiên ôn tập SRS khi không có từ đến hạn."""
    res = client.get("/api/study/review")
    assert res.status_code == 200
    assert res.get_json()["items"] == []


def test_speed_review_start_fails_when_under_three_words(client):
    """Bao phủ app.py dòng 774: Ôn siêu tốc báo 409 khi chưa đủ 3 từ đến hạn."""
    res = client.post("/api/study/speed/start")
    assert res.status_code == 409
    assert "ít nhất 3 từ" in res.get_json()["error"]


def test_speed_review_skip_validation_errors(client):
    """Bao phủ app.py dòng 808-831: Các nhánh kiểm tra lỗi trong skip speed review."""
    # Bỏ trống payload
    res = client.post("/api/study/speed/skip", json={})
    assert res.status_code == 400

    # Session ID không tồn tại
    res = client.post(
        "/api/study/speed/skip",
        json={"session_id": "nonexistent_session_id_12345", "word_id": 1, "attempt_id": "att1"},
    )
    assert res.status_code == 404


def test_speed_review_result_validation_errors(client):
    """Bao phủ app.py dòng 871-886: Kiểm tra lỗi tham số nộp kết quả speed review."""
    res = client.post("/api/study/speed/result", json={})
    assert res.status_code == 400

    res_missing_attempt = client.post(
        "/api/study/speed/result",
        json={"session_id": "test", "word_id": 1, "attempt_id": ""},
    )
    assert res_missing_attempt.status_code == 400


def test_record_study_result_payload_validation_and_404(client):
    """Bao phủ app.py dòng 1008-1028: Validate body và từ không tồn tại trong /api/study/result."""
    # Thiếu word_id
    res = client.post("/api/study/result", json={"mode": "learn", "correct": True})
    assert res.status_code == 400

    # Mode không hợp lệ
    res = client.post("/api/study/result", json={"word_id": 1, "mode": "invalid_mode", "correct": True})
    assert res.status_code == 400

    # word_id không tồn tại
    res = client.post("/api/study/result", json={"word_id": 99999, "mode": "learn", "correct": True})
    assert res.status_code == 404


def test_not_found_custom_json_handler(client):
    """Bao phủ app.py dòng 1109: Xử lý 404 trả về JSON có thông báo tiếng Việt."""
    res = client.get("/api/nonexistent-endpoint-abc")
    assert res.status_code == 404
    assert "Không tìm thấy" in res.get_json()["error"]
