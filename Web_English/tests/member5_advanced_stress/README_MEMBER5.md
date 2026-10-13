# HƯỚNG DẪN KIỂM THỬ: THÀNH VIÊN 5 - NGUYỄN TÙNG DƯƠNG (23013811)
## CHUYÊN TRÁCH: KIỂM THỬ NÂNG CAO, CHỊU TẢI & QUẢN LÝ DEFECT LOG

### 1. Phạm vi phụ trách
- Kiểm thử Tranh chấp đồng thời (Concurrency & Race Condition): `test_concurrency_race_condition.py`.
- Kiểm thử Chịu tải & Khả năng mở rộng (Stress & Latency Benchmark): `test_stress_scalability.py`.
- Kiểm thử Độ bền vững & Fuzzing (Unicode, Emoji, XSS, SQLi): `test_fuzzing_robustness.py`.
- Tổng hợp và quản lý Bảng Defect Log (Chương 7): `generate_defect_log.py`.

### 2. Các file trong thư mục
- `test_concurrency_race_condition.py`: Mô phỏng multi-threads cùng nộp 1 attempt_id, kiểm tra Idempotency và chế độ WAL.
- `test_stress_scalability.py`: Tự động chèn 1.000 từ vựng và đo độ trễ (latency ms) của các truy vấn.
- `test_fuzzing_robustness.py`: Kiểm thử dữ liệu dị biệt, chuỗi 10.000 ký tự và an toàn bảo mật.
- `generate_defect_log.py`: Script tự động sinh `defect_log.json` và `defect_log.md` chứa 15 lỗi thực tế.

### 3. Cách chạy kiểm thử
1. **Chạy toàn bộ kiểm thử nâng cao:**
   ```powershell
   .venv\Scripts\python -m pytest tests/member5_advanced_stress/ -v -s
   ```
   *(Tham số `-s` để in các thông số benchmark độ trễ ms ra terminal)*.
2. **Sinh bảng Defect Log:**
   ```powershell
   .venv\Scripts\python tests/member5_advanced_stress/generate_defect_log.py
   ```

### 4. Kết quả bàn giao cho Báo cáo
- Dữ liệu Benchmark độ trễ và mô phỏng tranh chấp đưa vào Chương 6 (Kiểm thử nâng cao).
- Bảng Defect Log 15 lỗi hoàn chỉnh đưa vào Chương 7 (Mục 7.2).
