# HƯỚNG DẪN KIỂM THỬ: THÀNH VIÊN 1 - HOÀNG TIẾN ĐẠT (23010864)
## CHUYÊN TRÁCH: KIỂM THỬ HỘP ĐEN 5 MÀN HÌNH CHÍNH (UI BLACK-BOX 1)

### 1. Phạm vi phụ trách
- **Màn hình Hôm nay (`dashboard`)**: 12 Test Cases (`TC_DASH_01` -> `TC_DASH_12`)
- **Màn hình Thư viện (`library`)**: 15 Test Cases (`TC_LIB_01` -> `TC_LIB_15`)
- **Màn hình Thêm từ (`add`)**: 18 Test Cases (`TC_ADD_01` -> `TC_ADD_18`)
- **Màn hình Sổ công thức (`formulas`)**: 8 Test Cases (`TC_FORM_01` -> `TC_FORM_08`)
- **Màn hình Cài đặt (`settings`)**: 7 Test Cases (`TC_SET_01` -> `TC_SET_07`)
**Tổng cộng:** 60 Test Cases.

### 2. Các file trong thư mục
- `test_cases_ui_screens.json`: Dữ liệu 60 test cases có đầy đủ ID, Steps, Input, Expected, Actual, Status.
- `test_ui_screens_blackbox.py`: Script tự động hóa kiểm tra các hành vi và hợp đồng API tương ứng.

### 3. Cách chạy kiểm thử
1. **Kiểm thử thủ công trên trình duyệt:**
   - Chạy ứng dụng bằng `run.bat` hoặc lệnh:
     ```cmd
     .venv\Scripts\python start.py
     ```
   - Mở trình duyệt `http://127.0.0.1:5000`.
   - Thực hiện từng bước kiểm thử theo file `test_cases_ui_screens.json`.
   - Chụp ảnh minh chứng cho từng màn hình, lưu vào thư mục `screenshots/member1/`.
2. **Kiểm thử tự động bằng Pytest:**
   ```powershell
   .venv\Scripts\python -m pytest tests/member1_blackbox/test_ui_screens_blackbox.py -v
   ```

### 4. Kết quả bàn giao cho Báo cáo
- Bảng Test Case Hộp đen đưa vào Chương 3 (Mục 3.2, 3.3, 3.4, 3.5, 3.6).
- Ghi nhận lỗi `TC_DASH_12` (lỗi responsive trên mobile) đưa vào Bảng Defect Log ở Chương 7.
