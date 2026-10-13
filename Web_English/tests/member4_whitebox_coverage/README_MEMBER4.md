# HƯỚNG DẪN KIỂM THỬ: THÀNH VIÊN 4 - NGUYỄN HỮU ĐĂNG KHOA (23010901)
## CHUYÊN TRÁCH: KIỂM THỬ HỘP TRẮNG, ĐO ĐỘ PHỦ MÃ NGUỒN & VẼ ĐỒ THỊ CFG

### 1. Phạm vi phụ trách
- Kiểm thử Hộp trắng toàn diện backend (Pytest).
- Đo Code Coverage (Statement & Branch Coverage) cho `app.py`, `models.py`, `srs.py`.
- Lập bảng Basis Path Testing (Đường đi cơ sở) và tính toán Độ phức tạp Cyclomatic $V(G)$.
- Tổng hợp Phụ lục B (Số liệu thống kê kiểm thử) cho Báo cáo.

### 2. Các file trong thư mục
- `test_whitebox_extended.py`: Bộ 12 test cases mở rộng phủ các nhánh lỗi, validate và ngoại lệ.
- `test_whitebox_cfg_basis_path.py`: Bộ 4 test cases tương ứng 4 đường đi độc lập của thuật toán SRS.
- `run_coverage.py`: Script 1 chạm tự động chạy đo Coverage và xuất báo cáo HTML.

### 3. Phân tích Đồ thị dòng điều khiển (CFG) cho hàm `apply_review_result`
- **Mã nguồn:** `srs.py`
- **Các đỉnh (Nodes - N):**
  * N1: Bắt đầu hàm, kiểm tra `progress.state != 'learned'`
  * N2: Ném ngoại lệ `ValueError`
  * N3: Gán `before = progress.srs_stage`, cập nhật `last_reviewed_at`, rẽ nhánh `if correct:`
  * N4: Nhánh Đúng: Tăng `correct_count`, tính `srs_stage = min(before + 1, 7)`
  * N5: Nhánh Sai: Tăng `incorrect_count`, `is_difficult = True`, `srs_stage = 0`
  * N6: Cập nhật `next_review_at = now + SRS_INTERVALS[...]`, return `(before, srs_stage)`
- **Các cạnh (Edges - E):** 8 cạnh nối giữa các nút.
- **Tính toán Độ phức tạp Cyclomatic:**
  $$V(G) = E - N + 2P = 8 - 6 + 2(1) = 4$$
  Hoặc tính theo số lượng vị từ điều kiện (Predicate Nodes):
  $$V(G) = P + 1 = 3 + 1 = 4$$
- **4 Đường đi độc lập (Basis Paths):**
  * **Path 1:** N1 $\rightarrow$ N2 (Ném ngoại lệ)
  * **Path 2:** N1 $\rightarrow$ N3 $\rightarrow$ N4 $\rightarrow$ N6 (Đúng, tăng cấp SRS)
  * **Path 3:** N1 $\rightarrow$ N3 $\rightarrow$ N4 (biên cực đại Stage 7) $\rightarrow$ N6 (Đúng ở Stage 7, giữ nguyên)
  * **Path 4:** N1 $\rightarrow$ N3 $\rightarrow$ N5 $\rightarrow$ N6 (Sai, reset về Stage 0)

### 4. Cách chạy và lấy số liệu Coverage
Chạy lệnh trong terminal:
```powershell
.venv\Scripts\python tests/member4_whitebox_coverage/run_coverage.py
```
- Mở file `Web_English/htmlcov/index.html` trên trình duyệt để chụp ảnh giao diện độ phủ xanh lá (93%+) đưa vào Chương 4 của Báo cáo.
