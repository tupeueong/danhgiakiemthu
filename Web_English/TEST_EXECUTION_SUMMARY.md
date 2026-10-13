# BÁO CÁO TỔNG HỢP KẾT QUẢ THỰC THI KIỂM THỬ HỆ THỐNG
## ĐỀ TÀI: WEB HỌC TỪ VỰNG TIẾNG ANH (LEXILOOP) - NHÓM 9

- **Thời gian thực thi:** 2026-10-13 20:50:48
- **Tổng thời gian chạy:** 17.62 giây
- **Trạng thái:** TẤT CẢ TEST CASES ĐÃ ĐẠT (100% PASS)

### 1. BẢNG TỔNG HỢP KIỂM THỬ THEO 5 THÀNH VIÊN

| Thành Viên | Vai Trò & Phân Hệ Phụ Trách | Số Test Cases | Kết Quả Thực Thi | File Báo Cáo / Script |
|---|---|---|---|---|
| **Hoàng Tiến Đạt** | Thành viên 1: Hộp đen 5 màn hình chính | 60 TCs | **60/60 PASS (100%)** | `tests/member1_blackbox/` |
| **Tô Thị Thùy Dương** | Thành viên 2: Hộp đen 3 phiên học tập | 55 TCs | **55/55 PASS (100%)** | `tests/member2_study_sessions/` |
| **Đỗ Thành Long** | Thành viên 3 (Lead): REST API & Postman | 15 APIs | **15/15 PASS (100%)** | `tests/member3_api_postman/` |
| **Nguyễn Hữu Đăng Khoa** | Thành viên 4: White-box, CFG & Coverage | 46 TCs | **46/46 PASS (100%)** | `tests/member4_whitebox_coverage/` |
| **Nguyễn Tùng Dương** | Thành viên 5: Concurrency, Stress & Defect Log | 15 TCs | **15/15 PASS (100%)** | `tests/member5_advanced_stress/` |

### 2. KẾT QUẢ ĐỘ PHỦ MÃ NGUỒN (CODE COVERAGE)

- **`models.py`:** **100%** (95/95 dòng lệnh)
- **`srs.py`:** **100%** (39/39 dòng lệnh)
- **`app.py`:** **92%** (488/533 dòng lệnh)
- **Tổng thể toàn bộ dự án:** **93% Statement Coverage**
- Báo cáo chi tiết dạng đồ họa HTML: `htmlcov/index.html`

### 3. THÔNG SỐ HIỆU NĂNG & CHỊU TẢI (STRESS BENCHMARK)

- Thời gian chèn hàng loạt 1.000 từ vựng: **~1.605 ms**
- Độ trễ tìm kiếm (Search Latency có Index): **24.25 ms** (< 50ms)
- Độ trễ thống kê tổng hợp (Stats Latency): **25.56 ms** (< 50ms)
- Độ trễ xuất tệp CSV 1.000 dòng: **843.64 ms** (< 1.000ms)

### 4. TỔNG HỢP LỖI PHÁT HIỆN (DEFECT LOG)

- Tổng số lỗi ghi nhận: **15 lỗi thực tế** (xem chi tiết tại `tests/member5_advanced_stress/defect_log.md`)
- Đã khắc phục (Fixed): **12 lỗi**
- Lỗi giao diện & phần cứng được ghi nhận theo dõi: **3 lỗi**
