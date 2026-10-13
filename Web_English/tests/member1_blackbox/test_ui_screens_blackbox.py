import json
import pytest
from models import FormulaNote, Setting, Word, WordProgress, db


def test_dashboard_stats_contract(client, add_word):
    """TC_DASH_01 -> TC_DASH_05: Kiểm tra số liệu thống kê trả về cho Dashboard."""
    # Ban đầu rỗng
    res = client.get("/api/stats")
    assert res.status_code == 200
    data = res.get_json()
    assert data["total"] == 0
    assert data["new"] == 0
    assert data["learning"] == 0
    assert data["learned"] == 0
    assert data["due"] == 0
    assert data["difficult"] == 0

    # Thêm 1 từ mới
    word = add_word(english="innovative", vietnamese="sáng tạo", part_of_speech="adjective")
    res = client.get("/api/stats")
    data = res.get_json()
    assert data["total"] == 1
    assert data["new"] == 1


def test_library_search_and_filters_contract(client, add_word):
    """TC_LIB_01 -> TC_LIB_10: Kiểm tra API tìm kiếm và lọc trạng thái của Thư viện."""
    add_word(english="resilient", vietnamese="kiên cường", part_of_speech="adjective")
    add_word(english="persist", vietnamese="kiên trì", part_of_speech="verb")

    # Tìm kiếm theo từ tiếng Anh
    res = client.get("/api/words?q=resilient")
    assert res.status_code == 200
    items = res.get_json()["items"]
    assert len(items) == 1
    assert items[0]["english"] == "resilient"

    # Tìm kiếm hoa thường
    res = client.get("/api/words?q=RESILIENT")
    assert res.status_code == 200
    assert len(res.get_json()["items"]) == 1

    # Tìm kiếm theo nghĩa tiếng Việt
    res = client.get("/api/words?q=kiên")
    assert res.status_code == 200
    assert len(res.get_json()["items"]) == 2

    # Lọc theo state
    res = client.get("/api/words?state=new")
    assert res.status_code == 200
    assert len(res.get_json()["items"]) == 2

    # Tìm từ không tồn tại
    res = client.get("/api/words?q=nonexistent123")
    assert res.status_code == 200
    assert len(res.get_json()["items"]) == 0


def test_add_word_validation_and_pos_normalization(client):
    """TC_ADD_01 -> TC_ADD_06: Kiểm tra validate bắt buộc và alias loại từ."""
    # Bỏ trống English
    res = client.post("/api/words", json={"english": "", "vietnamese": "nghĩa", "part_of_speech": "noun"})
    assert res.status_code == 400
    assert "tiếng anh" in res.get_json()["error"].lower()

    # Bỏ trống Vietnamese
    res = client.post("/api/words", json={"english": "apple", "vietnamese": "", "part_of_speech": "noun"})
    assert res.status_code == 400
    assert "nghĩa" in res.get_json()["error"].lower()

    # Alias POS: 'v' -> 'verb'
    res = client.post(
        "/api/words",
        json={"english": "analyze", "vietnamese": "phân tích", "part_of_speech": "v"},
    )
    assert res.status_code == 201
    assert res.get_json()["word"]["part_of_speech"] == "verb"


def test_bulk_import_contract(client):
    """TC_ADD_10 -> TC_ADD_15: Kiểm tra import hàng loạt 7 cột."""
    items = [
        {"english": "accurate", "phonetic": "/ˈækjərət/", "vietnamese": "chính xác", "part_of_speech": "adj", "examples": ["It is accurate."]},
        {"english": "benchmark", "phonetic": "/ˈbentʃmɑːk/", "vietnamese": "tiêu chuẩn", "part_of_speech": "noun", "examples": ["A new benchmark."]},
    ]
    res = client.post("/api/words/bulk", json={"items": items})
    assert res.status_code == 201
    data = res.get_json()
    assert data["added"] == 2
    assert len(data["skipped"]) == 0

    # Import lại để kiểm tra tự động bỏ qua từ trùng
    res = client.post("/api/words/bulk", json={"items": items})
    data = res.get_json()
    assert data["added"] == 0
    assert len(data["skipped"]) == 2


def test_formula_notes_crud_contract(client):
    """TC_FORM_01 -> TC_FORM_08: Kiểm tra CRUD sổ công thức và tính độc lập."""
    # Thêm công thức
    res = client.post("/api/formulas", json={"content": "S + V + O (Cấu trúc câu đơn)"})
    assert res.status_code == 201
    formula = res.get_json()["formula"]
    fid = formula["id"]
    assert formula["content"] == "S + V + O (Cấu trúc câu đơn)"

    # Cập nhật công thức
    res = client.put(f"/api/formulas/{fid}", json={"content": "S + V + O (Cập nhật)"})
    assert res.status_code == 200
    assert res.get_json()["formula"]["content"] == "S + V + O (Cập nhật)"

    # Xóa công thức
    res = client.delete(f"/api/formulas/{fid}")
    assert res.status_code == 200

    # Kiểm tra đã xóa
    res = client.get("/api/formulas")
    assert res.get_json()["total"] == 0


def test_settings_voice_contract(client):
    """TC_SET_01 -> TC_SET_06: Kiểm tra lưu và đọc cấu hình giọng đọc."""
    res = client.get("/api/settings")
    assert res.status_code == 200
    assert res.get_json()["voice_name"] == "Microsoft Zira - English (United States)"

    # Đổi giọng sang Mark
    res = client.put(
        "/api/settings",
        json={"voice_name": "Microsoft Mark - English (United States)"},
    )
    assert res.status_code == 200
    assert res.get_json()["voice_name"] == "Microsoft Mark - English (United States)"

    # Thử đổi giọng không được hỗ trợ
    res = client.put("/api/settings", json={"voice_name": "Invalid Voice XYZ"})
    assert res.status_code == 400
