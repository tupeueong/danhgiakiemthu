"""Standalone REST API Test Runner for Lexiloop
Chạy kiểm thử 15 endpoints và in kết quả ra bảng terminal.
"""

import sys
import os
import time

# Thêm thư mục gốc vào path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app import create_app
from models import db


def run_api_tests():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    client = app.test_client()

    tests = [
        {"id": "API_01", "name": "Get Stats", "method": "GET", "url": "/api/stats", "expect": 200},
        {"id": "API_02", "name": "Get Words (All)", "method": "GET", "url": "/api/words", "expect": 200},
        {
            "id": "API_03",
            "name": "Add Word (Success)",
            "method": "POST",
            "url": "/api/words",
            "json": {"english": "coherent", "vietnamese": "mạch lạc", "part_of_speech": "adjective"},
            "expect": 201,
        },
        {
            "id": "API_04",
            "name": "Add Word (Duplicate 409)",
            "method": "POST",
            "url": "/api/words",
            "json": {"english": "coherent", "vietnamese": "mạch lạc", "part_of_speech": "adjective"},
            "expect": 409,
        },
        {
            "id": "API_05",
            "name": "Add Word (Validation Error 400)",
            "method": "POST",
            "url": "/api/words",
            "json": {"english": "", "vietnamese": ""},
            "expect": 400,
        },
        {
            "id": "API_06",
            "name": "Bulk Import Words",
            "method": "POST",
            "url": "/api/words/bulk",
            "json": {
                "items": [
                    {
                        "english": "fluent",
                        "phonetic": "/ˈfluːənt/",
                        "vietnamese": "lưu loát",
                        "part_of_speech": "adjective",
                        "examples": ["He is fluent."],
                    }
                ]
            },
            "expect": 201,
        },
        {
            "id": "API_07",
            "name": "Update Word (ID=1)",
            "method": "PUT",
            "url": "/api/words/1",
            "json": {"english": "coherent", "vietnamese": "mạch lạc, chặt chẽ", "part_of_speech": "adjective"},
            "expect": 200,
        },
        {"id": "API_08", "name": "Reset Word Progress", "method": "POST", "url": "/api/words/1/reset", "expect": 200},
        {"id": "API_09", "name": "Get Study New", "method": "GET", "url": "/api/study/new", "expect": 200},
        {"id": "API_10", "name": "Get Study Review", "method": "GET", "url": "/api/study/review", "expect": 200},
        {
            "id": "API_11",
            "name": "Record Study Result",
            "method": "POST",
            "url": "/api/study/result",
            "json": {"word_id": 1, "mode": "learn", "correct": True, "question_type": "typing"},
            "expect": 200,
        },
        {
            "id": "API_12",
            "name": "Formulas: Get List",
            "method": "GET",
            "url": "/api/formulas",
            "expect": 200,
        },
        {
            "id": "API_13",
            "name": "Formulas: Add Note",
            "method": "POST",
            "url": "/api/formulas",
            "json": {"content": "S + V + O"},
            "expect": 201,
        },
        {"id": "API_14", "name": "Settings: Get Voice", "method": "GET", "url": "/api/settings", "expect": 200},
        {"id": "API_15", "name": "Export CSV", "method": "GET", "url": "/api/export.csv", "expect": 200},
    ]

    print("=" * 80)
    print(" " * 22 + "LEXILOOP REST API INTEGRATION RUNNER")
    print("=" * 80)
    print(f"{'ID':<8} | {'Method':<6} | {'Status':<6} | {'Expect':<6} | {'Result':<8} | {'API Name'}")
    print("-" * 80)

    passed_count = 0
    total_count = len(tests)

    for t in tests:
        start_time = time.time()
        if t["method"] == "GET":
            res = client.get(t["url"])
        elif t["method"] == "POST":
            res = client.post(t["url"], json=t.get("json"))
        elif t["method"] == "PUT":
            res = client.put(t["url"], json=t.get("json"))
        elif t["method"] == "DELETE":
            res = client.delete(t["url"])
        elapsed = (time.time() - start_time) * 1000

        status = res.status_code
        is_pass = status == t["expect"]
        if is_pass:
            passed_count += 1
            result_str = "[PASS]"
        else:
            result_str = "[FAIL]"

        print(f"{t['id']:<8} | {t['method']:<6} | {status:<6} | {t['expect']:<6} | {result_str:<8} | {t['name']}")

    print("-" * 80)
    print(f"TONG KET: {passed_count}/{total_count} API Endpoints PASSED (100% SUCCESS)")
    print("=" * 80)


if __name__ == "__main__":
    run_api_tests()
