"""Kiểm thử Tranh chấp & Tính bất biến (Concurrency, Race Condition & Idempotency)
Chuyên trách: Member 5 - Nguyễn Tùng Dương
Mục tiêu: Xác minh cơ chế chống ghi trùng (Idempotency) và chống xung đột phiên làm việc.
"""

from datetime import UTC, datetime, timedelta
import pytest
from models import ReviewLog, SpeedReviewItem, SpeedReviewSession, Word, WordProgress, db


def test_speed_review_idempotency_prevents_double_submission(client, add_word, monkeypatch):
    """Xác minh cơ chế Idempotency: Khi client gửi lặp lại request nộp kết quả
    với cùng 1 attempt_id (ví dụ do mạng lag hoặc bấm đúp), hệ thống chỉ xử lý 1 lần,
    các lần sau trả về duplicate=True mà không tăng điểm hay trừ tim hai lần."""
    words = [
        add_word(english="concurrency", vietnamese="tính đồng thời"),
        add_word(english="thread", vietnamese="luồng xử lý"),
        add_word(english="mutex", vietnamese="khóa loại trừ"),
    ]
    # Hoàn thành 6 bước học
    for w in words:
        for _ in range(6):
            client.post("/api/study/result", json={"word_id": w["id"], "mode": "learn", "correct": True})

    # Tua thời gian để đến hạn
    due_time = datetime.now(UTC).replace(tzinfo=None) + timedelta(hours=5)
    monkeypatch.setattr("app.utc_now", lambda: due_time)
    monkeypatch.setattr("srs.utc_now", lambda: due_time)

    # Khởi tạo phiên
    res = client.post("/api/study/speed/start")
    assert res.status_code == 201
    resp_data = res.get_json()
    session_id = resp_data["session_id"]
    item = resp_data["items"][0]
    word_id = item["id"]

    payload = {
        "session_id": session_id,
        "word_id": word_id,
        "attempt_id": "attempt-race-idempotent-001",
        "correct": True,
        "timed_out": False,
        "question_type": "speed-meaning-choice",
    }

    # Lần nộp 1: Thành công
    res1 = client.post("/api/study/speed/result", json=payload)
    assert res1.status_code == 200
    assert res1.get_json()["word"]["progress"]["srs_stage"] == 1

    # Lần nộp 2 (Bấm đúp cùng attempt_id): Phải trả về duplicate=True
    res2 = client.post("/api/study/speed/result", json=payload)
    assert res2.status_code == 200
    assert res2.get_json().get("duplicate") is True
    # Stage vẫn là 1, không bị tăng lên 2
    assert res2.get_json()["word"]["progress"]["srs_stage"] == 1

    # Lần nộp 3 (Cố tình nộp attempt_id khác cho cùng 1 câu đã trả lời): Chặn 409 Conflict
    res3 = client.post(
        "/api/study/speed/result",
        json={**payload, "attempt_id": "attempt-different-fraud-002"},
    )
    assert res3.status_code == 409
    assert "đã được chấm" in res3.get_json()["error"]


def test_rapid_sequential_requests_transaction_integrity(client, add_word):
    """Xác minh tính toàn vẹn giao dịch của SQLite khi nhận chuỗi request liên tiếp nhanh."""
    w = add_word(english="integrity", vietnamese="tính toàn vẹn")
    for i in range(10):
        res = client.get(f"/api/words?q=integrity")
        assert res.status_code == 200

    res_stats = client.get("/api/stats")
    assert res_stats.status_code == 200
