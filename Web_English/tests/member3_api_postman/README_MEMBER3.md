# HƯỚNG DẪN KIỂM THỬ: THÀNH VIÊN 3 - ĐỖ THÀNH LONG (23010174)
## CHUYÊN TRÁCH: KIỂM THỬ TÍCH HỢP REST API QUA POSTMAN & TRACEABILITY MATRIX

### 1. Phạm vi phụ trách
- Toàn bộ 15 Endpoints REST API của hệ thống Lexiloop.
- Xây dựng file Postman Collection chuẩn JSON v2.1.
- Chạy Postman Collection Runner, chụp ảnh kết quả response.
- Xây dựng Ma trận truy xuất nguồn gốc hai chiều (Phụ lục C của Báo cáo).

### 2. Các file trong thư mục
- `Lexiloop_API.postman_collection.json`: File bộ sưu tập Postman chứa 15 API, kèm assertions kiểm tra status code và schema.
- `test_api_runner.py`: Script Python độc lập chạy test nhanh 15 API và in bảng tổng kết.
- `test_api_integration.py`: File Pytest tích hợp.

### 3. Cách chạy kiểm thử
1. **Chạy bằng Postman Desktop:**
   - Mở phần mềm Postman $\rightarrow$ bấm nút **Import** $\rightarrow$ chọn file `Lexiloop_API.postman_collection.json`.
   - Đảm bảo server Web English đang chạy trên `http://127.0.0.1:5000`.
   - Bấm chuột phải vào Collection $\rightarrow$ chọn **Run collection** $\rightarrow$ bấm **Run Lexiloop API Collection**.
   - Quan sát kết quả Passed 100% và chụp ảnh màn hình Postman Runner lưu vào `screenshots/member3/`.
2. **Chạy bằng Terminal (Python):**
   ```powershell
   .venv\Scripts\python tests/member3_api_postman/test_api_runner.py
   ```

### 4. Kết quả bàn giao cho Báo cáo
- Danh mục API đưa vào Phụ lục A (Bảng danh mục API chi tiết).
- Bảng kết quả kiểm thử API đưa vào Chương 3 (Mục 3.10).
- Ma trận Truy xuất nguồn gốc Feature - UI - API - Test Case đưa vào Phụ lục C.
