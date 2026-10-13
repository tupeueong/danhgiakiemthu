"""Pytest Integration Test Suite cho 15 REST API Endpoints của Lexiloop
Phục vụ Member 3 (Đỗ Thành Long) lấy số liệu kiểm thử tích hợp.
"""

import pytest


def test_api_stats_endpoint(client):
    res = client.get("/api/stats")
    assert res.status_code == 200
    assert "total" in res.get_json()


def test_api_words_get_and_post_flow(client):
    # Thêm từ
    res = client.post(
        "/api/words",
        json={"english": "lucid", "phonetic": "/ˈluː.sɪd/", "vietnamese": "rõ ràng, minh bạch", "part_of_speech": "adjective"},
    )
    assert res.status_code == 201
    word_id = res.get_json()["word"]["id"]

    # Lấy danh sách từ
    res_list = client.get("/api/words?q=lucid")
    assert res_list.status_code == 200
    assert len(res_list.get_json()["items"]) == 1

    # Cập nhật từ
    res_update = client.put(
        f"/api/words/{word_id}",
        json={"english": "lucid", "vietnamese": "sáng rõ, dễ hiểu", "part_of_speech": "adjective"},
    )
    assert res_update.status_code == 200
    assert res_update.get_json()["word"]["vietnamese"] == "sáng rõ, dễ hiểu"

    # Xóa từ
    res_del = client.delete(f"/api/words/{word_id}")
    assert res_del.status_code == 200


def test_api_bulk_import_validation(client):
    # Payload rỗng
    res = client.post("/api/words/bulk", json={})
    assert res.status_code == 400

    # Payload hợp lệ
    items = [{"english": "pragmatic", "vietnamese": "thực dụng, thực tế", "part_of_speech": "adj"}]
    res_ok = client.post("/api/words/bulk", json={"items": items})
    assert res_ok.status_code == 201
    assert res_ok.get_json()["added"] == 1


def test_api_export_csv_headers(client, add_word):
    add_word(english="serene", vietnamese="thanh bình", part_of_speech="adj")
    res = client.get("/api/export.csv")
    assert res.status_code == 200
    assert "text/csv" in res.headers["Content-Type"]
    content = res.get_data(as_text=True)
    assert "serene" in content
    assert "thanh bình" in content
