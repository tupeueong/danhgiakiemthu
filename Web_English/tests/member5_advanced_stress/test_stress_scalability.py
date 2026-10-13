"""Kiểm thử Chịu tải & Khả năng mở rộng (Stress & Scalability Testing)
Chuyên trách: Member 5 - Nguyễn Tùng Dương
Mục tiêu: Đánh giá độ trễ và thông lượng khi kho từ vựng phát triển lớn.
"""

import time
import pytest
from models import Word, db


def test_stress_bulk_insert_and_search_latency(client):
    """Chèn 1.000 từ vựng và đo thời gian truy vấn tìm kiếm."""
    items = []
    for i in range(1, 1001):
        items.append(
            {
                "english": f"vocabulary_{i:04d}",
                "phonetic": f"/vəˈkæbjələri_{i}/",
                "vietnamese": f"từ vựng mẫu số {i}",
                "part_of_speech": "noun",
                "examples": [f"This is example sentence number {i} for stress test."],
            }
        )

    # 1. Đo thời gian Bulk Insert 1000 từ
    start_insert = time.time()
    res = client.post("/api/words/bulk", json={"items": items})
    insert_latency = (time.time() - start_insert) * 1000
    assert res.status_code == 201
    assert res.get_json()["added"] == 1000
    print(f"\n[BENCHMARK] Thoi gian them 1.000 tu vung: {insert_latency:.2f} ms")

    # 2. Đo độ trễ tìm kiếm (Search Latency) với index
    start_search = time.time()
    res_search = client.get("/api/words?q=vocabulary_0500")
    search_latency = (time.time() - start_search) * 1000
    assert res_search.status_code == 200
    assert len(res_search.get_json()["items"]) == 1
    print(f"[BENCHMARK] Do tre tim kiem (Search Latency): {search_latency:.2f} ms")
    assert search_latency < 500  # Phải phản hồi dưới 500ms

    # 3. Đo độ trễ tổng hợp thống kê Stats
    start_stats = time.time()
    res_stats = client.get("/api/stats")
    stats_latency = (time.time() - start_stats) * 1000
    assert res_stats.status_code == 200
    assert res_stats.get_json()["total"] == 1000
    print(f"[BENCHMARK] Do tre thong ke (Stats Latency): {stats_latency:.2f} ms")
    assert stats_latency < 300

    # 4. Đo độ trễ xuất file CSV 1000 dòng
    start_csv = time.time()
    res_csv = client.get("/api/export.csv")
    csv_latency = (time.time() - start_csv) * 1000
    assert res_csv.status_code == 200
    print(f"[BENCHMARK] Do tre xuat CSV (Export CSV Latency): {csv_latency:.2f} ms")
    assert csv_latency < 2500  # Chấp nhận dưới 2.5s khi xuất toàn bộ 1000 bản ghi kèm metadata

