import datetime
import pytest
from models import ReviewLog, SpeedReviewSession, Word, WordProgress, db
from srs import SRS_INTERVALS


def test_learn_session_six_steps_and_completion(client, add_word):
    """TC_LRN_01 -> TC_LRN_10: Kiểm tra quy trình học từ mới 6 bước."""
    word = add_word(english="thrive", vietnamese="phát triển mạnh", part_of_speech="verb")
    wid = word["id"]

    # Kiểm tra nạp danh sách học
    res = client.get("/api/study/new")
    assert res.status_code == 200
    items = res.get_json()["items"]
    assert any(w["id"] == wid for w in items)

    # Thực hiện 5 lần đúng liên tiếp (learning step tăng từ 0 lên 5)
    for step in range(1, 6):
        res = client.post(
            "/api/study/result",
            json={"word_id": wid, "mode": "learn", "correct": True, "question_type": "typing"},
        )
        assert res.status_code == 200
        progress = res.get_json()["word"]["progress"]
        assert progress["state"] == "learning"
        assert progress["learning_step"] == step

    # Lần thứ 6 đúng -> hoàn tất chuyển sang 'learned'
    res = client.post(
        "/api/study/result",
        json={"word_id": wid, "mode": "learn", "correct": True, "question_type": "typing"},
    )
    assert res.status_code == 200
    progress = res.get_json()["word"]["progress"]
    assert progress["state"] == "learned"
    assert progress["learning_step"] == 6
    assert progress["srs_stage"] == 0


def test_learn_session_wrong_answer_marks_difficult(client, add_word):
    """TC_LRN_11: Kiểm tra khi trả lời sai, từ bị đánh dấu khó."""
    word = add_word(english="obscure", vietnamese="mơ hồ", part_of_speech="adjective")
    wid = word["id"]

    res = client.post(
        "/api/study/result",
        json={"word_id": wid, "mode": "learn", "correct": False, "question_type": "multiple_choice"},
    )
    assert res.status_code == 200
    progress = res.get_json()["word"]["progress"]
    assert progress["is_difficult"] is True
    assert progress["incorrect_count"] == 1


def test_srs_review_ladder_and_reset(client, add_word, monkeypatch):
    """TC_REV_01 -> TC_REV_11: Kiểm tra thang 8 cấp bậc SRS và reset về 4 giờ."""
    word = add_word(english="pioneer", vietnamese="người tiên phong", part_of_speech="noun")
    wid = word["id"]

    # Hoàn thành học từ mới để vào stage 0
    for _ in range(6):
        client.post("/api/study/result", json={"word_id": wid, "mode": "learn", "correct": True})

    # Giả lập thời gian trôi qua để từ đến hạn ôn
    future_time = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) + datetime.timedelta(hours=5)
    monkeypatch.setattr("app.utc_now", lambda: future_time)
    monkeypatch.setattr("srs.utc_now", lambda: future_time)

    # Ôn tập lần 1 đúng -> Stage 0 lên Stage 1
    res = client.post("/api/study/result", json={"word_id": wid, "mode": "review", "correct": True})
    assert res.status_code == 200
    assert res.get_json()["word"]["progress"]["srs_stage"] == 1

    # Ôn tập lần 2 đúng -> Stage 1 lên Stage 2
    res = client.post("/api/study/result", json={"word_id": wid, "mode": "review", "correct": True})
    assert res.status_code == 200
    assert res.get_json()["word"]["progress"]["srs_stage"] == 2

    # Ôn tập lần 3 SAI -> Reset ngay về Stage 0 (4h)
    res = client.post("/api/study/result", json={"word_id": wid, "mode": "review", "correct": False})
    assert res.status_code == 200
    progress = res.get_json()["word"]["progress"]
    assert progress["srs_stage"] == 0
    assert progress["is_difficult"] is True


def test_speed_review_session_flow(client, add_word, monkeypatch):
    """TC_SPD_01 -> TC_SPD_11: Kiểm tra luồng Ôn siêu tốc, timeout và idempotency."""
    # Tạo 3 từ đã learned
    words = []
    for eng, vi in [("cat", "con mèo"), ("dog", "con chó"), ("bird", "con chim")]:
        w = add_word(english=eng, vietnamese=vi, part_of_speech="noun")
        words.append(w)
        for _ in range(6):
            client.post("/api/study/result", json={"word_id": w["id"], "mode": "learn", "correct": True})

    # Tua thời gian để 3 từ đến hạn
    due_time = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) + datetime.timedelta(hours=5)
    monkeypatch.setattr("app.utc_now", lambda: due_time)
    monkeypatch.setattr("srs.utc_now", lambda: due_time)

    # Bắt đầu session
    res = client.post("/api/study/speed/start")
    assert res.status_code == 201
    resp_data = res.get_json()
    session_id = resp_data["session_id"]
    items = resp_data["items"]
    assert len(items) == 3

    # Nộp kết quả câu 1 đúng
    item1 = items[0]
    res = client.post(
        "/api/study/speed/result",
        json={
            "session_id": session_id,
            "word_id": item1["id"],
            "attempt_id": "attempt-unique-001",
            "correct": True,
            "timed_out": False,
        },
    )
    assert res.status_code == 200

    # Nộp trùng attempt_id (kiểm tra Idempotency)
    res_dup = client.post(
        "/api/study/speed/result",
        json={
            "session_id": session_id,
            "word_id": item1["id"],
            "attempt_id": "attempt-unique-001",
            "correct": True,
            "timed_out": False,
        },
    )
    assert res_dup.status_code == 200
    assert res_dup.get_json().get("duplicate") is True
