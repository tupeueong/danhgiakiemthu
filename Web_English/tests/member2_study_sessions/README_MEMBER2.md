# HƯỚNG DẪN KIỂM THỬ: THÀNH VIÊN 2 - TÔ THỊ THÙY DƯƠNG (23010876)
## CHUYÊN TRÁCH: KIỂM THỬ HỘP ĐEN 3 PHIÊN HỌC TẬP (UI BLACK-BOX 2)

### 1. Phạm vi phụ trách
- **Phiên Học từ mới (`learn`)**: 18 Test Cases (`TC_LRN_01` -> `TC_LRN_18`)
- **Phiên Ôn tập SRS (`review`)**: 18 Test Cases (`TC_REV_01` -> `TC_REV_18`)
- **Phiên Ôn siêu tốc (`speed review`)**: 19 Test Cases (`TC_SPD_01` -> `TC_SPD_19`)
**Tổng cộng:** 55 Test Cases.

### 2. Các file trong thư mục
- `test_cases_study_sessions.json`: Danh mục 55 test cases chi tiết, đầy đủ kịch bản, bước bấm, kết quả kỳ vọng và thực tế.
- `test_study_sessions_blackbox.py`: Kịch bản test tự động mô phỏng trọn vẹn hành vi của học viên trên 3 chế độ học.

### 3. Cách chạy kiểm thử
1. **Kiểm thử thủ công trên trình duyệt:**
   - Mở web `http://127.0.0.1:5000`.
   - Lần lượt trải nghiệm:
     * Phiên học từ mới (thử làm đúng 6 bước, thử cố tình làm sai ở bước 3, kiểm tra phát âm).
     * Phiên ôn tập SRS (thử trả lời đúng để thăng cấp, thử làm sai để kiểm tra reset về 4 giờ).
     * Phiên ôn siêu tốc (thử để hết 8 giây xem có bị trừ tim không, thử streak 15 câu).
   - Chụp ảnh minh chứng màn hình lưu vào thư mục `screenshots/member2/`.
2. **Kiểm thử tự động bằng Pytest:**
   ```powershell
   .venv\Scripts\python -m pytest tests/member2_study_sessions/test_study_sessions_blackbox.py -v
   ```

### 4. Kết quả bàn giao cho Báo cáo
- Dữ liệu 55 Test Cases đưa vào Chương 3 (Mục 3.7, 3.8, 3.9).
- Ghi nhận lỗi `TC_SPD_19` (độ trễ timer trên máy cấu hình yếu) đưa vào Bảng Defect Log ở Chương 7.
