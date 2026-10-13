"""Kiểm thử Fuzzing & Độ bền vững (Fuzzing & Robustness Testing)
Chuyên trách: Member 5 - Nguyễn Tùng Dương
Mục tiêu: Đảm bảo server không sập (Crash 500) trước các đầu vào dị biệt hoặc độc hại.
"""

import pytest


def test_fuzzing_unicode_and_emojis(client):
    """Kiểm thử ký tự Emoji và Unicode kết hợp."""
    payload = {
        "english": "test_emoji_🚀_🔥",
        "phonetic": "/test/",
        "vietnamese": "nghĩa có emoji 🌟 và dấu kết hợp e\u0301",
        "part_of_speech": "noun",
        "examples": ["This is an emoji test 💡."],
        "collocations": ["deep test 🎯"],
    }
    res = client.post("/api/words", json=payload)
    assert res.status_code == 201
    word = res.get_json()["word"]
    assert "🚀" in word["english"]
    assert "🌟" in word["vietnamese"]


def test_fuzzing_super_long_strings(client):
    """Kiểm thử chuỗi siêu dài (10.000 ký tự) không làm sập server."""
    long_text = "A" * 10000
    res = client.post(
        "/api/words",
        json={"english": long_text, "vietnamese": "nghĩa dài", "part_of_speech": "noun"},
    )
    # Backend phải cắt ngắn hoặc từ chối hợp lệ, không được sập 500
    assert res.status_code in [201, 400]


def test_fuzzing_xss_injection_payloads(client):
    """Kiểm thử chuỗi tiêm nhiễm mã kịch bản XSS."""
    xss_payload = "<script>alert('XSS_ATTACK')</script>"
    res = client.post(
        "/api/words",
        json={"english": "sanitization", "vietnamese": xss_payload, "part_of_speech": "noun"},
    )
    assert res.status_code == 201
    # Dữ liệu được lưu dạng chuỗi an toàn, không thực thi script


def test_fuzzing_sql_injection_payloads(client):
    """Kiểm thử chuỗi tiêm nhiễm mã SQL Injection."""
    sql_injection = "' OR '1'='1' -- ; DROP TABLE words;"
    res = client.get(f"/api/words?q={sql_injection}")
    # SQLAlchemy ORM tham số hóa truy vấn, chặn đứng SQL Injection hoàn toàn
    assert res.status_code == 200
    assert isinstance(res.get_json()["items"], list)
