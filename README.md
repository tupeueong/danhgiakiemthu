# ĐỀ TÀI: ĐÁNH GIÁ VÀ KIỂM THỬ CHẤT LƯỢNG HỆ THỐNG WEB HỌC TỪ VỰNG TIẾNG ANH (LEXILOOP)

* **Học phần:** Đánh giá và kiểm định chất lượng phần mềm (CSE703010)
* **Giảng viên hướng dẫn:** TS. Trương Đức Phương
* **Đơn vị:** Trường Công nghệ Thông tin - Trường Đại học Phenikaa
* **Nhóm thực hiện:** Nhóm 9
* **Năm học:** 2026 - 2027

---

## 1. Cấu trúc thư mục dự án

```text
danhgiakiemthu/
├── docx/                                            # Thư mục lưu trữ văn bản báo cáo đồ án
│   ├── Báo_cáo_Nhóm_5_Testing.docx                 # Báo cáo mẫu tham chiếu chuẩn mực
│   └── Báo_cáo_Nhóm_9_Testing.docx                 # Báo cáo kiểm thử chính thức của Nhóm 9
│
├── KE_HOACH_CHI_TIET_HOAN_THIEN_BAO_CAO_NHOM_9.md   # Bản kế hoạch tổng thể & lộ trình triển khai
│
├── Web_English/                                     # Toàn bộ mã nguồn hệ thống & bộ kiểm thử tự động
│   ├── app.py                                       # Backend Flask REST API
│   ├── models.py                                    # CSDL SQLAlchemy & 8 thực thể dữ liệu
│   ├── srs.py                                       # Thuật toán lặp lại ngắt quãng SRS (Spaced Repetition)
│   ├── static/                                      # Giao diện Vanilla CSS & Vanilla JS (app.js)
│   ├── templates/                                   # Giao diện HTML (index.html)
│   ├── screenshots/                                 # 5 ảnh chụp minh chứng E2E tự động từ Selenium
│   ├── htmlcov/                                     # Báo cáo trực quan độ phủ mã nguồn (Code Coverage 93%)
│   ├── TEST_EXECUTION_SUMMARY.md                    # Báo cáo tổng hợp số liệu thực thi test
│   └── tests/                                       # Hệ thống kiểm thử phân rã theo 5 thành viên
│       ├── member1_blackbox/                        # 60 TCs Hộp đen 5 màn hình chính
│       ├── member2_study_sessions/                  # 55 TCs Hộp đen 3 phiên học tập
│       ├── member3_api_postman/                     # 15 REST API Postman Collection & Runner
│       ├── member4_whitebox_coverage/               # 46 TCs Hộp trắng, Basis Path CFG V(G)=4
│       ├── member5_advanced_stress/                 # 15 TCs Race condition, Stress 1000 từ, Defect Log
│       ├── run_all_tests.py                         # Master Test Runner điều phối toàn bộ test
│       └── test_ui_selenium_automation.py           # Kịch bản E2E Selenium Headless Chrome
│
└── unnecessary_files/                               # Thư mục gom các tệp tin tạm thời & bản nháp
    ├── README.md                                    # Giải thích mục đích các file lưu trữ tạm
    ├── doc9_content.txt                             # Trích xuất outline thô
    ├── inspect_docs.py                              # Script phân tích cấu trúc Word
    └── nhom_5_*.txt                                 # Các phân đoạn dữ liệu nháp bóc tách từ báo cáo mẫu
```

---

## 2. Kết quả thực thi kiểm thử tóm tắt

* **Tổng số kiểm thử tự động:** **67/67 Test Cases PASSED (100% Đạt)**
* **Độ phủ mã nguồn (Code Coverage):** **93% Statement Coverage**
  * `models.py`: **100%**
  * `srs.py`: **100%**
  * `app.py`: **92%**
* **REST API:** **15/15 Endpoints Đạt (100%)**
* **Hiệu năng & Chịu tải:** Bulk import 1.000 từ trong ~1.6s; Search Latency < 45ms.
* **Bảng lỗi phát hiện (Defect Log):** Ghi nhận 15 lỗi thực tế (12 Fixed, 3 Monitored).
