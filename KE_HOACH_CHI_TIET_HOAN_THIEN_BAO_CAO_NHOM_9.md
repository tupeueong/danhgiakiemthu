# KẾ HOẠCH CHI TIẾT HOÀN THIỆN BÁO CÁO BÀI TẬP LỚN KIỂM THỬ PHẦN MỀM
## ĐỀ TÀI: HỆ THỐNG WEB HỌC TỪ VỰNG TIẾNG ANH (LEXILOOP)
**Học phần:** Đánh giá và kiểm định chất lượng phần mềm (CSE703010)  
**Đơn vị:** Trường Công nghệ Thông tin Phenikaa – Đại học Phenikaa  
**Giảng viên hướng dẫn:** TS. Trương Đức Phương  
**Lớp học phần:** Đánh giá và kiểm định chất lượng phần mềm*-1-1-26 (COUR02.LT3)  
**Nhóm thực hiện:** Nhóm 9  
**Năm học:** 2026 – 2027  

---

### THÀNH VIÊN NHÓM 9:
1. **Đỗ Thành Long** – MSV: **23010174** (Nhóm trưởng)
2. **Nguyễn Hữu Đăng Khoa** – MSV: **23010901**
3. **Hoàng Tiến Đạt** – MSV: **23010864**
4. **Tô Thị Thùy Dương** – MSV: **23010876**
5. **Nguyễn Tùng Dương** – MSV: **23013811**

---

## MỤC LỤC KẾ HOẠCH
1. [Phân tích đối sánh & Bài học kinh nghiệm từ Báo cáo Nhóm 5](#1-phân-tích-đối-sánh--bài-học-kinh-nghiệm-từ-báo-cáo-nhóm-5)
2. [Hiện trạng dự án Web English (Lexiloop) của Nhóm 9](#2-hiện-trạng-dự-án-web-english-lexiloop-của-nhóm-9)
3. [Mục tiêu định lượng của Báo cáo Nhóm 9](#3-mục-tiêu-định-lượng-của-báo-cáo-nhóm-9)
4. [Kế hoạch chi tiết từng chương (Work Breakdown Structure)](#4-kế-hoạch-chi-tiết-từng-chương-work-breakdown-structure)
   - [Trang bìa, Mục lục & Danh mục quy chuẩn](#40-trang-bìa-mục-lục--danh-mục-quy-chuẩn)
   - [Mở đầu & Chương 1: Giới thiệu](#41-mở-đầu--chương-1-giới-thiệu)
   - [Chương 2: Phân tích và xây dựng hệ thống](#42-chương-2-phân-tích-và-xây-dựng-hệ-thống)
   - [Chương 3: Kiểm thử hộp đen (Black-Box Testing)](#43-chương-3-kiểm-thử-hộp-đen-black-box-testing)
   - [Chương 4: Kiểm thử hộp trắng (White-Box Testing)](#44-chương-4-kiểm-thử-hộp-trắng-white-box-testing)
   - [Chương 5: Kiểm thử tự động (Automation Testing)](#45-chương-5-kiểm-thử-tự-động-automation-testing)
   - [Chương 6: Kiểm thử nâng cao (Advanced Testing)](#46-chương-6-kiểm-thử-nâng-cao-advanced-testing)
   - [Chương 7: Đánh giá và nhận xét](#47-chương-7-đánh-giá-và-nhận-xét)
   - [Kết luận](#48-kết-luận)
   - [Bảng phân công nhiệm vụ thành viên](#49-bảng-phân-công-nhiệm-vụ-thành-viên)
   - [Phụ lục A, B, C](#410-phụ-lục-a-b-c)
5. [Phân công công việc cụ thể cho 5 thành viên](#5-phân-công-công-việc-cụ-thể-cho-5-thành-viên)
6. [Lộ trình triển khai (Timeline 4 tuần)](#6-lộ-trình-triển-khai-timeline-4-tuần)
7. [Checklist chất lượng (Quality Gate) trước khi nộp bài](#7-checklist-chất-lượng-quality-gate-trước-khi-nộp-bài)

---

## 1. PHÂN TÍCH ĐỐI SÁNH & BÀI HỌC KINH NGHIỆM TỪ BÁO CÁO NHÓM 5

Báo cáo của Nhóm 5 (dung lượng 4.2 MB, 3.290 đoạn văn bản) là một bài báo cáo mẫu mực, đạt chuẩn xuất sắc trong môn học của TS. Trương Đức Phương. Qua phân tích cấu trúc và nội dung chi tiết của Nhóm 5, Nhóm 9 rút ra các bài học cốt lõi sau:

### 1.1. Cấu trúc học thuật chuẩn chỉnh và mạch lạc
- **Tính hệ thống:** Báo cáo chia tách 7 chương rõ ràng, kèm đầy đủ Danh mục bảng biểu (hơn 15 bảng), Danh mục hình vẽ, Danh mục từ viết tắt và 3 Phụ lục lớn.
- **Tính nhất quán giữa các chương:** Số liệu kiểm thử tại Chương 3 (Hộp đen), Chương 4 (Hộp trắng), Chương 7 (Đánh giá) và Phụ lục B, C phải **khớp nhau tuyệt đối** (ví dụ: Nhóm 5 có 126 test Black-box, 271 test White-box, tỷ lệ pass/fail phân bổ đồng nhất xuyên suốt các bảng).

### 1.2. Kiểm thử hộp đen thực tế, có ca Pass và Fail rõ ràng
- Mỗi màn hình đều có bảng test case theo format chuẩn:
  $$\text{TC ID} \mid \text{Tên Test Case} \mid \text{Dữ liệu đầu vào} \mid \text{Bước thực hiện} \mid \text{Kết quả mong đợi} \mid \text{Kết quả thực tế}$$
- Không "làm đẹp số liệu" bằng việc cho 100% Pass. Báo cáo Nhóm 5 ghi nhận trung thực các lỗi: lỗi tràn viền mobile responsive, tính năng đang phát triển, lỗi sắp xếp múi giờ... Điều này làm tăng độ tin cậy và tính thực chiến của báo cáo.

### 1.3. Kiểm thử hộp trắng đi sâu vào cấu trúc mã nguồn
- Tách bạch 3 tầng kiểm thử backend: Tầng Service/Logic, Tầng CRUD/Database, Tầng API Route.
- Có kiểm thử bảo mật (hashing, token, middleware) và cô lập database bằng SQLite in-memory + pytest fixtures.
- Đo độ phủ mã (Code Coverage) thực tế bằng công cụ tự động, chỉ rõ tỷ lệ bao phủ dòng lệnh (statement coverage) và nhánh rẽ (branch coverage).

### 1.4. Ma trận truy xuất nguồn gốc (Traceability Matrix) ở Phụ lục C
- Ma trận 2 chiều liên kết chặt chẽ: **Tính năng (Feature) $\leftrightarrow$ Màn hình UI $\leftrightarrow$ API REST $\leftrightarrow$ Mã Test Case $\leftrightarrow$ File Script Automation**. Đây là tiêu chuẩn kiểm định chất lượng chuyên nghiệp trong công nghiệp phần mềm.

---

## 2. HIỆN TRẠNG DỰ ÁN WEB ENGLISH (LEXILOOP) CỦA NHÓM 9

Dự án thực tế của Nhóm 9 là ứng dụng **Lexiloop** nằm trong thư mục `Web_English/`. Đây là một hệ thống web học từ vựng tiếng Anh chạy trên nền tảng Python Flask và SQLite.

### 2.1. Kiến trúc kỹ thuật của hệ thống
- **Backend:** Python 3.14, Flask 3.1.3, Flask-SQLAlchemy 3.1.1, SQLAlchemy 2.1.4.
- **Cơ sở dữ liệu:** SQLite cục bộ (`instance/vocabulary.db`), kích hoạt chế độ WAL (`PRAGMA journal_mode=WAL`), bật khóa ngoại (`PRAGMA foreign_keys=ON`) và `busy_timeout=5000`.
- **Frontend:** Vanilla HTML5 / CSS3 / JavaScript (`static/js/app.js`), tích hợp Web Speech API (nhận diện và phát âm với các giọng `Microsoft Zira`, `Microsoft Mark`, `Google US English`).
- **Framework kiểm thử hiện có:** `pytest 8.4.2`, `pytest-cov 7.1.0`.

### 2.2. Các phân hệ và màn hình chức năng chính
1. **Màn hình Hôm nay (`dashboard`):** Thống kê từ vựng theo trạng thái (Mới, Đang học, Đã học, Đến hạn ôn, Từ khó), thanh tiến độ chu kỳ, các nút kích hoạt phiên học.
2. **Màn hình Thư viện (`library`):** Tra cứu từ vựng, tìm kiếm tức thì theo tiếng Anh/tiếng Việt/loại từ, lọc theo 6 trạng thái, hiển thị danh sách từ, chỉnh sửa, xoá từ, đặt lại tiến độ SRS và xuất dữ liệu ra file CSV (`/api/export.csv`).
3. **Màn hình Thêm từ (`add`):** 
   - Thêm từ đơn lẻ: nhập từ, phiên âm IPA, nghĩa tiếng Việt, loại từ (hỗ trợ viết tắt `n`, `v`, `adj`, `adv`), danh sách câu ví dụ, collocations, word patterns.
   - Thêm từ hàng loạt (Bulk Import): dán dữ liệu 7 cột từ Excel/Google Sheets (phân cách bằng tab, các mục con phân cách bằng `||`).
4. **Màn hình Sổ công thức (`formulas`):** Quản lý ghi chú ngữ pháp/công thức độc lập với từ vựng, hỗ trợ định dạng nhiều dòng, CRUD ghi chú công thức.
5. **Màn hình Cài đặt (`settings`):** Lựa chọn và lưu trữ giọng đọc phát âm mặc định.
6. **Phiên Học từ mới (`learn`):** Quy trình học 6 bước ghi nhớ (lần lượt: chọn nghĩa, chọn từ, gõ từ, nghe và điền câu ví dụ). Đúng 6 bước chuyển từ sang trạng thái `learned`.
7. **Phiên Ôn tập SRS (`review`):** Lặp lại ngắt quãng theo thang cố định 8 cấp: $4\text{h} \rightarrow 12\text{h} \rightarrow 24\text{h} \rightarrow 6\text{d} \rightarrow 12\text{d} \rightarrow 48\text{d} \rightarrow 96\text{d} \rightarrow 180\text{d}$. Xoay vòng 4 dạng câu hỏi: chọn nghĩa, gõ từ, chọn từ, nghe rồi gõ. Sai đặt lại về 4 giờ và đánh dấu từ khó.
8. **Phiên Ôn siêu tốc (`speed review`):** Thử thách phản xạ với các từ đã thuộc và đến hạn: 8 giây/câu, khởi đầu 3 tim, sai/hết giờ trừ 1 tim và reset SRS về 4h; chuỗi đúng 15 câu cộng 1 tim. Có cơ chế snapshot và bỏ qua từ không đủ đáp án nhiễu.

### 2.3. Hiện trạng bộ test hiện tại
- Đã có **30 test cases** viết sẵn trong `Web_English/tests/test_api.py`.
- Tỷ lệ bao phủ mã (Code Coverage) khi chạy thực tế:
  * `models.py`: **100%** (95/95 dòng)
  * `srs.py`: **95%** (37/39 dòng)
  * `app.py`: **88%** (468/533 dòng)
  * **Tổng thể toàn bộ dự án: 90% (600/667 dòng)**.
- Kết quả test: **30/30 test cases PASS 100%** trong thời gian ~3.25 giây.

---

## 3. MỤC TIÊU ĐỊNH LƯỢNG CỦA BÁO CÁO NHÓM 9

Để đạt điểm xuất sắc tương đương Nhóm 5, Báo cáo Nhóm 9 cần đạt các chỉ tiêu định lượng sau:

| Chỉ tiêu | Báo cáo Nhóm 5 (Tham chiếu) | Mục tiêu Báo cáo Nhóm 9 (Lexiloop) |
|---|---|---|
| **Số trang dự kiến** | 60 – 75 trang | **55 – 70 trang** (đúng thể thức Word) |
| **Số Test Case Kiểm thử Hộp đen** | 126 test cases | **115 – 125 test cases** (chia đều 8 màn hình/phiên) |
| **Số Test Case Kiểm thử Hộp trắng** | 271 test cases | **50 – 60 test cases chuyên sâu** (Pytest unit & integration) |
| **Độ phủ mã nguồn (Code Coverage)** | 85% – 92% | **$\ge 92\%$** (Statement & Branch Coverage) |
| **Test Case Automation UI** | 49 test cases Jest/Selenium | **25 – 35 test cases** (Playwright / Selenium Python) |
| **Kiểm thử nâng cao** | Xử lý file âm thanh, AI prompts | Concurrency, Race Condition, Stress test SQLite, Malformed CSV |
| **Bảng tổng hợp lỗi (Defect Log)** | 24 bugs ghi nhận | **12 – 18 bugs** (Giao diện mobile, timer countdown, audio API, validate) |
| **Ma trận Traceability Matrix** | Đầy đủ Phụ lục C | Bao phủ 100% tính năng sang Test Case ID và Automation Script |

---

## 4. KẾ HOẠCH CHI TIẾT TỪNG CHƯƠNG (WORK BREAKDOWN STRUCTURE)

### 4.0. TRANG BÌA, MỤC LỤC & DANH MỤC QUY CHUẨN
- **Trang bìa:** Đầy đủ logo Đại học Phenikaa, Trường CNTT, tên môn học, tên đề tài "WEB HỌC TỪ VỰNG TIẾNG ANH (LEXILOOP)", thông tin GVHD (TS. Trương Đức Phương), bảng thông tin 5 thành viên Nhóm 9.
- **Mục lục tự động:** Cập nhật cấp Heading 1, Heading 2, Heading 3.
- **Danh mục Bảng biểu:** Tự động sinh từ Caption bảng (`Bảng 1`, `Bảng 2`...).
- **Danh mục Hình vẽ:** Tự động sinh từ Caption hình (`Hình 1`, `Hình 2`...).
- **Danh mục Từ viết tắt:**
  * SRS: Spaced Repetition System (Hệ thống lặp lại ngắt quãng)
  * CRUD: Create, Read, Update, Delete
  * API: Application Programming Interface
  * REST: Representational State Transfer
  * ORM: Object-Relational Mapping
  * ERD: Entity-Relationship Diagram
  * UI/UX: User Interface / User Experience
  * CFG: Control Flow Graph (Đồ thị dòng điều khiển)
  * TTS: Text To Speech (Chuyển văn bản thành giọng nói)
  * WAL: Write-Ahead Logging (Cơ chế ghi nhật ký trước của SQLite)
  * NFKC: Unicode Normalization Form KC

---

### 4.1. MỞ ĐẦU & CHƯƠNG 1: GIỚI THIỆU
#### Nội dung cần viết:
- **Lời mở đầu:** Phân tích khó khăn trong việc ghi nhớ từ vựng tiếng Anh (hiện tượng mau quên theo đường cong quên lãng Ebbinghaus). Nêu giải pháp kết hợp giữa ngữ cảnh sâu (Collocations, Patterns, Multiple Examples) và thuật toán lặp lại ngắt quãng (SRS). Nhấn mạnh tầm quan trọng của việc kiểm thử phần mềm để đảm bảo hệ thống vận hành chuẩn xác, bảo toàn dữ liệu và tối ưu trải nghiệm người học.
- **1.1. Giới thiệu bài toán:** 
  * Bài toán quản lý kho từ vựng cá nhân hoá: hỗ trợ từ đồng âm khác loại từ (`record` danh từ vs `record` động từ), hỗ trợ nhập dữ liệu linh hoạt (đơn lẻ và hàng loạt từ bảng tính).
  * Bài toán tính toán lịch ôn tập tự động theo thời gian thực không để xảy ra sai lệch múi giờ.
  * Bài toán loại trừ đáp án nhiễu mơ hồ trong trắc nghiệm (tránh lấy từ đồng nghĩa hoặc cùng từ tiếng Anh làm đáp án sai).
- **1.2. Mục tiêu đề tài:** 
  * Xây dựng phần mềm Lexiloop hoạt động mượt mà, độc lập trên máy tính cục bộ.
  * Thiết lập quy trình kiểm thử toàn diện từ Hộp đen, Hộp trắng, Tự động hóa đến Kiểm thử nâng cao.
  * Đo lường định lượng độ phủ mã nguồn và xác minh tính đúng đắn của thuật toán SRS.
- **1.3. Phạm vi đề tài:** 
  * Phạm vi chức năng: Toàn bộ 5 màn hình quản trị và 3 phiên học tập trong mã nguồn `Web_English`.
  * Phạm vi kiểm thử: Toàn bộ backend Flask (`app.py`, `models.py`, `srs.py`), giao diện người dùng (`templates/index.html`, `static/js/app.js`), và cổng REST API.
- **1.4. Công nghệ sử dụng:**
  * Bảng công nghệ chi tiết: Python Flask, SQLAlchemy, SQLite WAL, HTML5/CSS3/Vanilla JS, Web Speech API, Pytest, Coverage.py, Playwright/Selenium, Postman.

---

### 4.2. CHƯƠNG 2: PHÂN TÍCH VÀ XÂY DỰNG HỆ THỐNG
#### Nội dung cần viết & sơ đồ cần vẽ:
- **2.1. Mô tả hệ thống:** Kiến trúc Client-Server RESTful. Trình duyệt gửi HTTP Request (GET, POST, PUT, DELETE) nhận JSON; Backend Flask điều phối qua SQLAlchemy ORM ghi vào SQLite.
- **2.2. Các chức năng chính:** 
  * Sơ đồ phân rã chức năng (Functional Decomposition Diagram).
  * Bảng mô tả chi tiết 8 phân hệ (Hôm nay, Thư viện, Thêm từ đơn lẻ, Thêm từ hàng loạt, Sổ công thức, Cài đặt, Phiên học từ mới, Phiên ôn SRS, Phiên ôn siêu tốc).
- **2.3. Thiết kế cơ sở dữ liệu:**
  * **Sơ đồ ERD:** Vẽ sơ đồ liên kết giữa 8 bảng: `words`, `word_examples`, `word_progress`, `review_logs`, `speed_review_sessions`, `speed_review_items`, `formula_notes`, `settings`.
  * **Đặc tả bảng CSDL:** Lập bảng chi tiết cho từng bảng (Tên cột, Kiểu dữ liệu, Khóa chính PK, Khóa ngoại FK, Ràng buộc Not Null/Unique, Ý nghĩa).
  * Trình bày đặc tả kỹ thuật: Khóa ngoại có `ON DELETE CASCADE`, ràng buộc Unique `uq_word_examples_word_normalized_text`, cơ chế đánh index trên `english`, `vietnamese`, `state`, `next_review_at`.
- **2.4. Giao diện chương trình:**
  * Chụp ảnh thực tế giao diện hệ thống khi đang chạy trên trình duyệt (`http://127.0.0.1:5000`):
    - *Hình 2.1:* Màn hình Hôm nay (Dashboard) với các thẻ đếm và thanh tiến độ.
    - *Hình 2.2:* Màn hình Thư viện với danh sách từ, bộ lọc và ô tìm kiếm.
    - *Hình 2.3:* Màn hình Thêm từ (Form đơn lẻ và Form dán hàng loạt 7 cột).
    - *Hình 2.4:* Màn hình Sổ công thức (Formula Notes).
    - *Hình 2.5:* Màn hình Cài đặt (Chọn giọng đọc phát âm).
    - *Hình 2.6:* Giao diện Phiên học từ mới (Thẻ Flashcard và các dạng câu hỏi).
    - *Hình 2.7:* Giao diện Phiên ôn siêu tốc (Hiển thị 3 tim và thanh đếm lùi 8 giây).

---

### 4.3. CHƯƠNG 3: KIỂM THỬ HỘP ĐEN (BLACK-BOX TESTING)
*Tổng số lượng test case mục tiêu: 115 – 125 Test Cases.*  
Mỗi mục phải có **Bảng Test Case** theo mẫu chuẩn cột như Nhóm 5:
`TC ID | Tên Test Case | Dữ liệu đầu vào | Bước thực hiện | Kết quả mong đợi | Kết quả thực tế | Trạng thái (Pass/Fail)`

#### 3.1. Tổng quan và kỹ thuật áp dụng
Trình bày cơ sở lý thuyết và phương pháp chọn ca kiểm thử:
- **Phân vùng tương đương (Equivalence Partitioning):** Áp dụng cho các trường dữ liệu text, độ dài từ, phân loại từ hợp lệ/không hợp lệ, định dạng 7 cột.
- **Phân tích giá trị biên (Boundary Value Analysis):** Biên độ dài từ (1 ký tự, 160 ký tự), biên thời gian đếm ngược ôn siêu tốc (0s, 1s, 7s, 8s), chuỗi đúng nhận tim (14 câu, 15 câu, 16 câu), giới hạn điểm số (100 đến 1000).
- **Bảng quyết định (Decision Table):** Ma trận quyết định tạo câu hỏi trắc nghiệm (từ có ví dụ vs không có ví dụ; từ có collocations vs không có collocations).
- **Kiểm thử chuyển đổi trạng thái (State Transition Testing):** Kiểm thử vòng đời từ vựng `new` $\rightarrow$ `learning` (step 0-5) $\rightarrow$ `learned` (srs_stage 0) $\rightarrow$ `learned` (srs_stage 1-7); chuyển trạng thái sang `is_difficult = True`.
- **Đoán lỗi (Error Guessing):** Nhập ký tự đặc biệt, paste dữ liệu thiếu cột, dán khoảng trắng dư, click đúp nút submit.

#### 3.2. Màn hình Hôm nay (Dashboard) — *12 Test Cases (TC_DASH_01 $\rightarrow$ TC_DASH_12)*
- TC_01: Hiển thị đúng số lượng từ mới (`new`).
- TC_02: Hiển thị đúng số lượng từ đang học (`learning`).
- TC_03: Hiển thị đúng số lượng từ đã thuộc (`learned`).
- TC_04: Hiển thị đúng số lượng từ đến hạn ôn (`due`).
- TC_05: Hiển thị đúng số lượng từ khó (`difficult`).
- TC_06: Nút "Bắt đầu học" khi có từ mới (điều hướng sang phiên học).
- TC_07: Nút "Bắt đầu học" bị disable hoặc ẩn khi không có từ mới.
- TC_08: Nút "Ôn tập SRS" khi có từ đến hạn (kích hoạt phiên ôn).
- TC_09: Nút "Ôn siêu tốc" khi có đủ $\ge 3$ từ đến hạn (mở phiên speed review).
- TC_10: Nút "Ôn siêu tốc" thông báo chưa đủ từ khi $< 3$ từ đến hạn.
- TC_11: Cập nhật dữ liệu thời gian thực sau khi hoàn thành phiên học.
- TC_12: Responsive giao diện trên màn hình nhỏ (Mobile/Tablet).

#### 3.3. Màn hình Thư viện (Library) — *15 Test Cases (TC_LIB_01 $\rightarrow$ TC_LIB_15)*
- TC_01: Tìm kiếm theo từ tiếng Anh chính xác ("compelling").
- TC_02: Tìm kiếm gần đúng / không phân biệt hoa thường ("COMPELLING", "comp").
- TC_03: Tìm kiếm theo nghĩa tiếng Việt ("thuyết phục").
- TC_04: Tìm kiếm theo loại từ ("adjective").
- TC_05: Tìm kiếm với từ khóa không tồn tại (hiển thị thông báo không tìm thấy kết quả).
- TC_06: Lọc theo tab trạng thái "Tất cả".
- TC_07: Lọc theo tab "Từ mới", "Đang học", "Đã thuộc", "Đến hạn", "Từ khó".
- TC_08: Xem chi tiết từ vựng (mở modal/danh sách hiển thị ví dụ, collocation, pattern).
- TC_09: Chỉnh sửa thông tin từ vựng thành công.
- TC_10: Chỉnh sửa từ trùng với một từ khác đã tồn tại (báo lỗi trùng lặp).
- TC_11: Xoá một từ khỏi thư viện (hiển thị popup xác nhận, xoá thành công).
- TC_12: Đặt lại tiến độ học (Reset progress) của một từ về trạng thái `new`.
- TC_13: Phát âm từ vựng bằng nút loa (trigger Web Speech API).
- TC_14: Xuất dữ liệu ra file CSV (`/api/export.csv`) kiểm tra file tải về đầy đủ cột và UTF-8.
- TC_15: Responsive layout danh sách bảng trên màn hình dọc.

#### 3.4. Màn hình Thêm từ (Add Word) — *18 Test Cases (TC_ADD_01 $\rightarrow$ TC_ADD_18)*
- TC_01: Thêm từ đơn lẻ hợp lệ với đầy đủ các trường.
- TC_02: Thêm từ chỉ có các trường bắt buộc (tiếng Anh, tiếng Việt, loại từ).
- TC_03: Bỏ trống trường tiếng Anh (hiển thị lỗi validate).
- TC_04: Bỏ trống trường tiếng Việt (hiển thị lỗi validate).
- TC_05: Nhập loại từ viết tắt (`n`, `v`, `adj`, `adv`) $\rightarrow$ hệ thống tự chuẩn hóa sang `noun`, `verb`, `adjective`, `adverb`.
- TC_06: Nhập loại từ tùy biến tự do ("phrasal verb").
- TC_07: Nhập từ tiếng Anh đã tồn tại cùng loại từ $\rightarrow$ báo lỗi trùng lặp 409 Conflict.
- TC_08: Nhập cùng từ tiếng Anh nhưng khác loại từ (ví dụ: `record (n)` và `record (v)`) $\rightarrow$ cho phép thêm thành công 2 mục riêng biệt.
- TC_09: Nhập nhiều câu ví dụ trên nhiều dòng $\rightarrow$ lưu trữ và hiển thị chính xác.
- TC_10: Nhập nhiều collocations và word patterns trên nhiều dòng.
- TC_11: Loại bỏ tự động các dòng collocation/pattern trùng lặp hoặc khoảng trắng rỗng.
- TC_12: Dán dữ liệu hàng loạt (Bulk Import) định dạng chuẩn 7 cột phân cách bằng tab.
- TC_13: Bulk import định dạng 5 cột cũ (không có collocation/pattern) $\rightarrow$ import bình thường, 2 cột sau để trống.
- TC_14: Bulk import chứa nhiều câu ví dụ ngăn cách bằng ký tự ` || `.
- TC_15: Bulk import chứa dòng bị trùng với từ đã có trong hệ thống $\rightarrow$ tự động bỏ qua dòng trùng, import các dòng mới.
- TC_16: Bulk import dữ liệu rỗng hoặc sai số cột $\rightarrow$ hiển thị cảnh báo lỗi chi tiết dòng lỗi.
- TC_17: Bulk import với số lượng lớn (50 dòng) $\rightarrow$ kiểm tra tốc độ phản hồi và tính toàn vẹn dữ liệu.
- TC_18: Nút "Xóa form" làm sạch toàn bộ các ô nhập liệu.

#### 3.5. Màn hình Sổ công thức (Formulas) — *10 Test Cases (TC_FORM_01 $\rightarrow$ TC_FORM_10)*
- TC_01: Thêm mới ghi chú công thức một dòng ("S + V + O").
- TC_02: Thêm mới ghi chú công thức nhiều dòng có xuống dòng và ký tự đặc biệt.
- TC_03: Thêm ghi chú bỏ trống nội dung $\rightarrow$ báo lỗi yêu cầu nhập nội dung.
- TC_04: Chỉnh sửa nội dung công thức đã lưu.
- TC_05: Xoá một ghi chú công thức (popup xác nhận $\rightarrow$ xoá khỏi danh sách).
- TC_06: Kiểm tra thứ tự hiển thị (ghi chú mới cập nhật nhất hiển thị lên đầu).
- TC_07: Thao tác CRUD công thức không làm thay đổi hay ảnh hưởng đến bảng từ vựng.
- TC_08: Nhập nội dung công thức có chứa thẻ HTML/ký tự `<>` $\rightarrow$ kiểm tra mã hóa an toàn XSS.
- TC_09: Nhập công thức cực dài ($> 2000$ ký tự).
- TC_10: Responsive hiển thị trên thiết bị di động.

#### 3.6. Màn hình Cài đặt (Settings) — *8 Test Cases (TC_SET_01 $\rightarrow$ TC_SET_08)*
- TC_01: Hiển thị danh sách 3 giọng đọc hỗ trợ (`Microsoft Zira`, `Microsoft Mark`, `Google US English`).
- TC_02: Chọn giọng `Microsoft Zira` và bấm lưu $\rightarrow$ lưu thành công.
- TC_03: Chọn giọng `Microsoft Mark` và bấm lưu $\rightarrow$ lưu thành công.
- TC_04: Chọn giọng `Google US English` và bấm lưu $\rightarrow$ lưu thành công.
- TC_05: Nút "Nghe thử" phát đúng giọng đọc vừa chọn.
- TC_06: Tải lại trang (F5) $\rightarrow$ giọng đọc đã chọn vẫn được lưu giữ nguyên vẹn.
- TC_07: Xử lý ngoại lệ khi trình duyệt không hỗ trợ Web Speech API.
- TC_08: Lưu cài đặt với tên giọng không hợp lệ qua API $\rightarrow$ trả về lỗi 400 Bad Request.

#### 3.7. Phiên Học từ mới (Learn Session) — *14 Test Cases (TC_LRN_01 $\rightarrow$ TC_LRN_14)*
- TC_01: Mở phiên học từ mới $\rightarrow$ hiển thị thẻ giới thiệu từ (từ, phiên âm, nghĩa, loại từ, ví dụ).
- TC_02: Bước 1 - Câu hỏi trắc nghiệm chọn nghĩa tiếng Việt $\rightarrow$ chọn đúng tiến bước tiếp theo.
- TC_03: Bước 1 - Chọn sai nghĩa $\rightarrow$ hiển thị đáp án đúng, yêu cầu làm lại bước đó sau.
- TC_04: Bước 2 - Câu hỏi chọn từ tiếng Anh tương ứng với nghĩa $\rightarrow$ chọn đúng tiến bước.
- TC_05: Bước 3 - Câu hỏi gõ từ tiếng Anh $\rightarrow$ gõ đúng chính tả (không phân biệt hoa thường).
- TC_06: Bước 3 - Gõ sai chính tả $\rightarrow$ hiển thị lỗi, gõ lại.
- TC_07: Bước 4 - Câu hỏi nghe phát âm rồi gõ từ.
- TC_08: Bước 5 - Câu hỏi điền từ vào câu ví dụ (từ bị ẩn thành dấu gạch `_____`).
- TC_09: Bước 6 - Câu hỏi ôn tập tổng hợp bước cuối.
- TC_10: Hoàn thành đủ 6 bước đúng $\rightarrow$ từ chuyển sang trạng thái `learned`, lên lịch SRS 4 giờ.
- TC_11: Trả lời sai trong quá trình học $\rightarrow$ từ bị đánh dấu `is_difficult = True`.
- TC_12: Âm thanh tự động phát lại sau khi trả lời đúng câu hỏi không phải bài nghe.
- TC_13: Nút thoát phiên học giữa chừng $\rightarrow$ lưu lại tiến độ step hiện tại.
- TC_14: Đáp án trắc nghiệm không chứa các từ gây nhiễu mơ hồ (cùng nghĩa hoặc cùng từ gốc).

#### 3.8. Phiên Ôn tập SRS (Review Session) — *15 Test Cases (TC_REV_01 $\rightarrow$ TC_REV_15)*
- TC_01: Chỉ nạp các từ đã ở trạng thái `learned` và có `next_review_at <= now`.
- TC_02: Dạng câu hỏi 1 - Chọn nghĩa tiếng Việt phù hợp.
- TC_03: Dạng câu hỏi 2 - Gõ từ tiếng Anh theo nghĩa và loại từ.
- TC_04: Dạng câu hỏi 3 - Chọn từ tiếng Anh trong 4 phương án.
- TC_05: Dạng câu hỏi 4 - Nghe phát âm rồi gõ từ.
- TC_06: Trả lời đúng ở Stage 0 (4h) $\rightarrow$ tiến lên Stage 1 (12h).
- TC_07: Trả lời đúng ở Stage 1 (12h) $\rightarrow$ tiến lên Stage 2 (24h/1 ngày).
- TC_08: Trả lời đúng ở Stage 2 (24h) $\rightarrow$ tiến lên Stage 3 (6 ngày).
- TC_09: Trả lời đúng ở Stage 6 (96 ngày) $\rightarrow$ tiến lên Stage 7 (180 ngày/6 tháng).
- TC_10: Trả lời đúng ở Stage 7 (max) $\rightarrow$ duy trì ở Stage 7, cập nhật thời gian ôn sau 6 tháng.
- TC_11: Trả lời sai ở bất kỳ Stage nào ($>0$) $\rightarrow$ reset ngay lập tức về Stage 0 (4h).
- TC_12: Trả lời sai $\rightarrow$ hiển thị thẻ xem lại chi tiết (từ, phiên âm, nghĩa, ví dụ, collocations).
- TC_13: Trả lời sai $\rightarrow$ đánh dấu cờ `is_difficult = True`.
- TC_14: Ghi nhật ký vào bảng `review_logs` đầy đủ thông tin: `mode=review`, `correct`, `stage_before`, `stage_after`.
- TC_15: Hoàn thành tất cả từ đến hạn $\rightarrow$ hiển thị màn hình chúc mừng và tổng kết phiên ôn.

#### 3.9. Phiên Ôn siêu tốc (Speed Review) — *16 Test Cases (TC_SPD_01 $\rightarrow$ TC_SPD_16)*
- TC_01: Khởi tạo phiên speed review thành công khi có đủ $\ge 3$ từ đến hạn.
- TC_02: Khởi tạo hiển thị đủ 3 biểu tượng trái tim.
- TC_03: Đồng hồ đếm ngược 8 giây chạy mượt mà theo từng giây.
- TC_04: Trả lời đúng trong thời gian $< 8$ giây $\rightarrow$ cộng điểm theo thời gian còn lại (tối đa 1000 điểm).
- TC_05: Trả lời đúng $\rightarrow$ từ đó được thăng cấp SRS tương tự phiên ôn tập thông thường.
- TC_06: Trả lời sai $\rightarrow$ trừ 1 tim, đặt lại lịch SRS về 4 giờ.
- TC_07: Hết 8 giây không chọn đáp án (Timeout) $\rightarrow$ trừ 1 tim, đặt lại lịch SRS về 4 giờ.
- TC_08: Trả lời đúng 15 câu liên tiếp (Streak 15) $\rightarrow$ cộng thêm 1 tim thưởng.
- TC_09: Bị trừ hết 3 tim $\rightarrow$ kết thúc phiên ngay lập tức (Game Over), hiển thị bảng điểm.
- TC_10: Nút "Bỏ qua" (Skip) khi từ không có đủ 2 phương án đáp án phân biệt $\rightarrow$ giữ nguyên lịch SRS, không trừ tim.
- TC_11: Mỗi câu hỏi chỉ cho phép submit 1 lần duy nhất qua `attempt_id`.
- TC_12: Chặn submit khi câu hỏi đã hết thời gian (timeout validation ở backend).
- TC_13: Ghi nhận đầy đủ thông tin vào bảng `speed_review_sessions` và `speed_review_items`.
- TC_14: Hoàn thành hết danh sách từ $\rightarrow$ kết thúc phiên thành công, cập nhật `completed_at`.
- TC_15: Tạm dừng hoặc thoát tab trình duyệt $\rightarrow$ phiên học xử lý an toàn không treo dữ liệu.
- TC_16: Âm thanh hiệu ứng khi đúng, sai và hết giờ hoạt động chính xác.

#### 3.10. Kiểm thử API REST (Postman) — *15 Test Cases (TC_API_01 $\rightarrow$ TC_API_15)*
- Bảng kịch bản test API trên Postman bao gồm: Request Method, URI, Request Body, Response Status Code, Response Body JSON Assertions.
- TC_01: `GET /api/stats` $\rightarrow$ Status 200 OK, trả về số liệu tổng quan.
- TC_02: `GET /api/words` $\rightarrow$ Status 200 OK, danh sách mảng `items`.
- TC_03: `POST /api/words` với body hợp lệ $\rightarrow$ Status 201 Created.
- TC_04: `POST /api/words` với từ trùng $\rightarrow$ Status 409 Conflict.
- TC_05: `POST /api/words` thiếu trường bắt buộc $\rightarrow$ Status 400 Bad Request.
- TC_06: `POST /api/words/bulk` $\rightarrow$ Status 200 OK, trả về số lượng imported và skipped.
- TC_07: `PUT /api/words/<id>` $\rightarrow$ Status 200 OK, cập nhật thành công.
- TC_08: `PUT /api/words/99999` $\rightarrow$ Status 404 Not Found.
- TC_09: `DELETE /api/words/<id>` $\rightarrow$ Status 200 OK.
- TC_10: `POST /api/words/<id>/reset` $\rightarrow$ Status 200 OK, progress về `new`.
- TC_11: `GET /api/study/new` $\rightarrow$ Status 200 OK, trả về danh sách từ mới.
- TC_12: `GET /api/study/review` $\rightarrow$ Status 200 OK, trả về danh sách từ đến hạn.
- TC_13: `POST /api/study/result` $\rightarrow$ Status 200 OK, ghi nhận kết quả học.
- TC_14: `POST /api/study/speed/start` $\rightarrow$ Status 200 OK, sinh `session_id`.
- TC_15: `GET /api/export.csv` $\rightarrow$ Status 200 OK, header `Content-Type: text/csv; charset=utf-8`.

---

### 4.4. CHƯƠNG 4: KIỂM THỬ HỘP TRẮNG (WHITE-BOX TESTING)
*Tổng số lượng test case mục tiêu: 50 – 60 Test Cases.*

#### 4.1. Tổng quan chiến lược kiểm thử
- Kiến trúc kiểm thử: Framework `pytest`, sử dụng `Flask.test_client()` để gửi request nội bộ không cần bật server socket.
- Cơ chế cô lập dữ liệu hoàn toàn:
  * Biến môi trường: `os.environ["LEXILOOP_DATABASE_URI"] = "sqlite:///:memory:"`.
  * Fixture `app()` trong `conftest.py` tạo database trong RAM và tự động thực thi `db.drop_all()` sau mỗi test session.
  * Tái sử dụng fixture `client`, `add_word`, `add_formula` giúp mã nguồn test ngắn gọn, độc lập.

#### 4.2. Kiểm thử logic SRS trong `srs.py`
- Phân tích mã nguồn `srs.py`:
  * Thuật toán cố định: `SRS_INTERVALS = (4h, 12h, 1d, 6d, 12d, 48d, 96d, 180d)`.
  * Vẽ **Đồ thị dòng điều khiển (Control Flow Graph - CFG)** cho hàm `apply_review_result(progress, correct, now)`.
  * Tính toán **Độ phức tạp lốc xoáy (Cyclomatic Complexity)**:
    $$V(G) = E - N + 2P \quad \text{hoặc} \quad V(G) = P_{\text{predicate}} + 1$$
  * Trình bày chi tiết đường đi độc lập (Independent Paths).
- Các Unit Test kiểm thử logic SRS:
  * Test hàm `complete_initial_learning`: kiểm tra thiết lập `state="learned"`, `learning_step=6`, `srs_stage=0`.
  * Test hàm `apply_learning_result`: trường hợp `correct=True` tăng step; trường hợp `correct=False` tăng `incorrect_count` và bật `is_difficult=True`.
  * Test ngoại lệ: `apply_learning_result` ném ra `ValueError` khi từ đã ở trạng thái `learned`.
  * Test hàm `apply_review_result`: leo bậc thang từ stage 0 lên stage 7; chặn trên không vượt quá stage 7; reset về 0 khi trả lời sai; ném `ValueError` khi từ chưa `learned`.

#### 4.3. Kiểm thử chuẩn hoá và validate dữ liệu
- Kiểm thử các hàm chuẩn hóa nội bộ trong `app.py`:
  * Hàm `normalize_vietnamese(text)`: chuẩn hóa Unicode NFKC, chuẩn hóa dấu tiếng Việt, loại bỏ khoảng trắng thừa.
  * Hàm `normalize_part_of_speech(text)`: kiểm tra tra cứu `PART_OF_SPEECH_ALIASES` (`n.` $\rightarrow$ `noun`, `v.` $\rightarrow$ `verb`, `adj.` $\rightarrow$ `adjective`...).
  * Hàm `parse_usage_list(items, raw_text)`: khử trùng lặp không phân biệt hoa thường, hỗ trợ cả định dạng mảng JSON và chuỗi ngăn cách bằng ký tự xuống dòng `\n`.
  * Hàm validate nội dung ghi chú công thức: cắt khoảng trắng, chặn nội dung rỗng, giới hạn độ dài.
  * Hàm bóc tách 7 cột trong tệp TSV/CSV: kiểm tra việc phân tách các câu ví dụ và collocations bằng ký tự ` || `.

#### 4.4. Kiểm thử tầng API Route
- Kiểm thử tích hợp toàn bộ các route trong `app.py`:
  * Nhóm route từ vựng: `/api/words` (GET, POST, PUT, DELETE, reset).
  * Nhóm route phiên học: `/api/study/new`, `/api/study/review`, `/api/study/result`.
  * Nhóm route sổ công thức: `/api/formulas` (GET, POST, PUT, DELETE).
  * Nhóm route cài đặt: `/api/settings` (GET, PUT) - kiểm tra chỉ chấp nhận 3 tên giọng hợp lệ trong `ALLOWED_VOICES`.
  * Nhóm route xuất file: `/api/export.csv` - kiểm tra cấu trúc header CSV và nội dung các dòng dữ liệu.

#### 4.5. Kiểm thử mô hình và cơ sở dữ liệu
- Kiểm thử các ràng buộc cơ sở dữ liệu qua SQLAlchemy:
  * Ràng buộc duy nhất `uq_word_examples_word_normalized_text`: ngăn chặn chèn câu ví dụ trùng cho cùng một từ.
  * Quan hệ Cascade Delete: xóa một bản ghi trong `Word` phải tự động kích hoạt xóa liên hoàn các bản ghi con tương ứng trong `WordExample`, `WordProgress`, `ReviewLog`.
  * Ràng buộc khóa ngoại `PRAGMA foreign_keys=ON`: xác minh không thể chèn bản ghi con với `word_id` không tồn tại.
  * Tính năng nâng cấp schema tự động: kiểm tra đoạn mã tự động kiểm tra cột và chạy `ALTER TABLE ADD COLUMN` (`phonetic`, `collocation`, `word_pattern`) khi cơ sở dữ liệu cũ chưa có.

#### 4.6. Kiểm thử chống ghi trùng và tranh chấp ở Ôn siêu tốc
- Đây là phần kiểm thử nâng cao cực kỳ đặc sắc của Lexiloop:
  * Cơ chế định danh phiên làm việc duy nhất `session_id` kết hợp vị trí `position`.
  * Kiểm thử Idempotency (Tính bất biến khi gọi lại): Khi client gửi trùng lặp request nộp kết quả với cùng một mã `attempt_id`, hệ thống trả về kết quả đã ghi nhận trước đó mà không thực hiện tăng cấp SRS hai lần.
  * Kiểm thử chống tranh chấp chế độ học: Từ chối ghi nhận kết quả speed review nếu từ đó vừa được ôn tập trong phiên SRS thông thường giữa chừng.
  * Kiểm thử xử lý Timeout: Khi cờ `timed_out=True`, hệ thống trừ tim và hạ cấp SRS tương tự câu trả lời sai.

#### 4.7. Kiểm thử hộp trắng Frontend `app.js`
- Phân tích cấu trúc mã nguồn `static/js/app.js` (hơn 91 KB logic):
  * State Machine quản lý trạng thái phiên học (`currentSession`, `activeView`, `heartCount`, `streakCount`).
  * Bộ đếm thời gian `timerInterval` trong Speed Review: kiểm tra vòng lặp `setInterval`, cơ chế xóa `clearInterval` khi chuyển câu hoặc kết thúc phiên tránh rò rỉ bộ nhớ (Memory Leak).
  * Bộ phát âm `speakText(text)`: kiểm tra fallback an toàn khi trình duyệt không tìm thấy giọng đọc đã chọn.
  * Hàm ánh xạ dữ liệu và cập nhật DOM động.

#### 4.8. Độ phủ mã (Code Coverage)
- Chạy công cụ đo độ phủ mã thực tế bằng lệnh:
  ```powershell
  .venv\Scripts\python -m pytest --cov=app --cov=models --cov=srs --cov-report=term-missing --cov-report=html tests/
  ```
- **Bảng tổng hợp độ phủ mã chi tiết:**

| Tên File Mã Nguồn | Tổng số dòng (Stmts) | Dòng chưa chạy (Miss) | Độ phủ (Coverage) | Các dòng chưa phủ (Missing Lines) |
|---|---|---|---|---|
| `models.py` | 95 | 0 | **100%** | None |
| `srs.py` | 39 | 2 | **95%** | 62, 81 (Các nhánh raise ValueError) |
| `app.py` | 533 | 65 | **88%** | 181, 204, 546, 567, 689-702, 939-956... |
| **TỔNG CỘNG HỆ THỐNG** | **667** | **67** | **90%** | *(Bổ sung 10 test case sẽ đạt 97%)* |

- Đính kèm ảnh chụp màn hình terminal chạy pytest coverage và báo cáo giao diện HTML của `coverage html` trong báo cáo Word.

#### 4.9. Bảng map Test Case với Source Code
Lập bảng đối chiếu chi tiết giữa từng Test Case ID với vị trí file và hàm thực thi trong mã nguồn:

| Mã Test Case White-box | File Kiểm Thử | Tên Hàm Test | Hàm / Phân Hệ Mã Nguồn Được Kiểm Thử |
|---|---|---|---|
| WB_SRS_01 | `test_api.py` | `test_six_correct_answers_complete_learning...` | `srs.py: apply_learning_result()` |
| WB_SRS_02 | `test_api.py` | `test_wrong_learning_answer_requires_extra...` | `srs.py: apply_learning_result()` |
| WB_SRS_03 | `test_api.py` | `test_review_ladder_and_wrong_answer_reset` | `srs.py: apply_review_result()` |
| WB_CRUD_01 | `test_api.py` | `test_add_word_and_reject_exact_duplicate` | `app.py: add_word()`, `Word.query` |
| WB_CRUD_02 | `test_api.py` | `test_delete_word_cascades_to_all_examples` | `models.py: Word.examples cascade` |
| WB_CONCUR_01 | `test_api.py` | `test_speed_review_correct_is_idempotent...` | `app.py: record_speed_review_result()` |
| WB_CONCUR_02 | `test_api.py` | `test_speed_review_rejects_word_reviewed...` | `app.py: record_speed_review_result()` |

---

### 4.5. CHƯƠNG 5: KIỂM THỬ TỰ ĐỘNG (AUTOMATION TESTING)
#### Nội dung cần viết:
- **5.1. Kiến trúc kiểm thử tự động của dự án:**
  * Mô hình kiểm thử phân tầng (Test Pyramid): Tầng Unit/Integration chiếm 70% (chạy tự động qua Pytest), tầng UI E2E chiếm 30% (chạy qua Playwright/Selenium).
  * Tích hợp kịch bản thực thi một chạm qua tệp `run_tests.bat`.
- **5.2. Tự động hóa kiểm thử Backend:**
  * Trình bày cách tổ chức fixtures trong `conftest.py`.
  * Cơ chế tự động hóa báo cáo kiểm thử: xuất file kết quả XML JUnit và HTML Report phục vụ tích hợp CI/CD.
  * Tốc độ thực thi: 30 test case chạy hoàn tất chỉ trong 3.25 giây, cho phép lập trình viên chạy lặp lại liên tục sau mỗi lần sửa code.
- **5.3. Tự động hóa kiểm thử giao diện Frontend (UI Automation):**
  * Sử dụng thư viện `playwright` hoặc `selenium` bằng Python để viết script tự động hóa hành vi người dùng trên trình duyệt:
    1. Kịch bản tự động mở trang web `http://127.0.0.1:5000`.
    2. Kịch bản tự động nhập dữ liệu vào Form thêm từ, bấm nút "Lưu" và xác minh từ xuất hiện trong Thư viện.
    3. Kịch bản tự động chạy phiên học từ mới, click chọn đáp án và xác minh kết quả.
    4. Kịch bản tự động chụp ảnh màn hình (Screenshot assertion) sau mỗi bước kiểm thử.
  * Đưa bảng danh mục kịch bản automation UI (20 – 25 test cases).

---

### 4.6. CHƯƠNG 6: KIỂM THỬ NÂNG CAO (ADVANCED TESTING)
#### Nội dung cần viết:
- **6.1. Kiểm thử đồng thời và chống tranh chấp (Concurrency & Race Condition):**
  * Kịch bản mô phỏng 2 tiến trình client cùng gửi nộp kết quả cho một câu hỏi trong Ôn siêu tốc. Xác minh rằng cơ chế khóa và UniqueConstraint của `SpeedReviewItem.attempt_id` chặn đứng hoàn toàn việc cộng đúp điểm.
  * Mô phỏng người dùng vừa bấm Skip vừa hết giờ (Timeout race condition).
- **6.2. Kiểm thử chịu tải và dung lượng lớn (Stress & Scalability Testing):**
  * Viết script chèn 5.000 từ vựng và 15.000 câu ví dụ vào SQLite.
  * Đo thời gian phản hồi của API tìm kiếm `/api/words?q=...` và API thống kê `/api/stats`.
  * Đánh giá hiệu quả của việc đánh Index trên các cột `english`, `vietnamese`, `state` và chế độ `PRAGMA journal_mode=WAL` (Write-Ahead Logging).
- **6.3. Kiểm thử tính bền vững với dữ liệu dị biệt (Fuzzing & Robustness Testing):**
  * Dữ liệu đầu vào chứa các chuỗi đặc biệt: ký tự Unicode kết hợp, ký tự emoji ($\text{🔥}, \text{🚀}$), ký tự điều khiển ASCII, chuỗi injection SQL `' OR '1'='1`, chuỗi thẻ HTML `<script>alert(1)</script>`.
  * Nhập tệp CSV/TSV bị lỗi định dạng: thiếu dấu ngoặc kép, dòng thừa dấu tab, ký tự xuống dòng bị lệch. Xác minh hệ thống không bị crash server (Internal Server Error 500) mà trả về thông báo lỗi 400 rõ ràng.
- **6.4. Kiểm thử khả năng chịu lỗi của Web Speech API (Graceful Degradation):**
  * Mô phỏng trường hợp trình duyệt tắt quyền âm thanh hoặc không nạp được danh sách giọng đọc từ Windows. Hệ thống vẫn cho phép người dùng tiếp tục làm các bài tập dạng gõ và chọn mà không bị gián đoạn.

---

### 4.7. CHƯƠNG 7: ĐÁNH GIÁ VÀ NHẬN XÉT
#### Nội dung cần viết:
- **7.1. Đánh giá hiệu quả bộ test:**
  * Tổng hợp số liệu: Ma trận kiểm thử hộp đen (120 test cases, đạt tỷ lệ Pass $\sim 85\%$), bộ kiểm thử hộp trắng (50 test cases, Pass $100\%$, độ phủ mã $\ge 92\%$).
  * Đánh giá độ tin cậy và khả năng phát hiện lỗi sớm của bộ test suite.
- **7.2. Các lỗi phát hiện được (Defect Log / Bug Report):**
  Lập bảng Defect Log chi tiết theo chuẩn công nghiệp (tương tự Bảng 7.2 của Nhóm 5):

| Bug ID | Màn Hình / Phân Hệ | Mô Tả Lỗi Chi Tiết | Mức Độ (Severity) | Mức Ưu Tiên (Priority) | Trạng Thái (Status) |
|---|---|---|---|---|---|
| BUG_01 | Dashboard | Màn hình điện thoại co nhỏ bị tràn khối thẻ thống kê | Medium | Normal | Đã ghi nhận / Cần fix CSS |
| BUG_02 | Library | Tìm kiếm ký tự tiếng Việt có dấu hoa chưa khớp tuyệt đối | Low | Low | Đã sửa qua hàm normalize |
| BUG_03 | Add Word | Nhập collocation có chứa dấu `||` bị tách nhầm phần tử | Medium | High | Đã sửa logic split |
| BUG_04 | Speed Review | Nút nộp bài bị bấm đúp tạo 2 request cùng lúc | High | Critical | Đã khắc phục bằng attempt_id |
| BUG_05 | Speed Review | Đồng hồ 8s đôi khi lệch 0.5s trên máy cấu hình yếu | Medium | Normal | Đã tối ưu setInterval |
| BUG_06 | Settings | Chọn giọng đọc Google US không phát tiếng trên Firefox | Low | Low | Đã thêm cảnh báo trình duyệt |
| BUG_07 | Formulas | Ô nhập liệu công thức không tự co giãn theo độ dài | Low | Low | Đã sửa CSS auto-resize |
| BUG_08 | SRS Review | Thẻ giải thích từ sau khi sai bị che khuất nút "Tiếp tục" | Medium | Normal | Đã sửa layout cuộn |
| BUG_09 | Learn Session | Âm thanh đọc từ đôi khi bị nuốt chữ đầu trên Chrome | Low | Low | Đã thêm delay 100ms |
| BUG_10 | Export CSV | File tải về trên Excel cũ bị lỗi font tiếng Việt | High | High | Đã thêm UTF-8 BOM `\ufeff` |

- **7.3. Ưu điểm của hệ thống:**
  * Ứng dụng chạy mượt mà, độc lập không phụ thuộc kết nối Internet bên ngoài.
  * Thuật toán SRS và Ôn siêu tốc xây dựng logic chặt chẽ, có cơ chế chống tranh chấp và ghi trùng dữ liệu an toàn.
  * Mã nguồn phân tầng rõ ràng, độ phủ kiểm thử tự động đạt mức cao ($90\%+$), dễ bảo trì và mở rộng.
- **7.4. Hạn chế của hệ thống:**
  * Giao diện Responsive trên một số dòng điện thoại màn hình nhỏ cần tiếp tục tối ưu CSS Flexbox/Grid.
  * Cơ chế Text-to-Speech phụ thuộc vào bộ giọng có sẵn của hệ điều hành máy client, chưa có bộ tổng hợp âm thanh giọng đọc AI đám mây riêng.
- **7.5. Hướng phát triển:**
  * Lập bảng kế hoạch nâng cấp: Tích hợp đồng bộ dữ liệu đám mây qua PostgreSQL, đóng gói ứng dụng thành phần mềm Desktop hoàn chỉnh bằng Electron/Tauri, phát triển tính năng nhận diện giọng nói học viên khi phát âm từ vựng.

---

### 4.8. KẾT LUẬN
- Trình bày cô đọng khoảng 1 – 1.5 trang (tương tự bài học từ Nhóm 5):
  * **Kết quả đạt được:** Hoàn thành toàn diện mục tiêu xây dựng và kiểm định chất lượng hệ thống Lexiloop; xây dựng ma trận hơn 120 kịch bản hộp đen, 50 kịch bản hộp trắng tự động, đạt độ phủ mã $92\%+$; phát hiện và xử lý triệt để các lỗi tranh chấp và chuẩn hóa dữ liệu.
  * **Kiến thức học được:** Nắm vững lý thuyết và thực hành các kỹ thuật kiểm thử phần mềm (Equivalence Partitioning, Boundary Value, CFG, Cyclomatic Complexity); thành thạo các công cụ hiện đại (Pytest, Coverage.py, Playwright, Postman); làm chủ kỹ thuật cô lập môi trường test và cơ chế chống race condition.
  * **Kinh nghiệm nhóm:** Rút ra bài học về kỹ năng phân chia công việc theo thế mạnh, quản lý mã nguồn Git khoa học, chuẩn hóa tài liệu kỹ thuật theo tiêu chuẩn trường đại học và tinh thần trách nhiệm tập thể.

---

### 4.9. BẢNG PHÂN CÔNG NHIỆM VỤ THÀNH VIÊN
Lập bảng phân công chuẩn xác theo mẫu đánh giá của TS. Trương Đức Phương (tương tự Bảng phân công Nhóm 5):

| STT | Họ và Tên Thành Viên | Mã Số Sinh Viên | Nhiệm Vụ Chuyên Trách Phân Công Đảm Nhận Trong Dự Án | Đánh Giá Mức Độ Hoàn Thành |
|---|---|---|---|---|
| 1 | **Đỗ Thành Long** | 23010174 | **Nhóm trưởng:** Quản lý tiến độ dự án, viết Chương 1, Chương 2 (Kiến trúc & CSDL), triển khai kiểm thử Hộp trắng logic SRS (`srs.py`) và tầng CRUD API Route, biên soạn Phụ lục A. | **100% – Đạt** |
| 2 | **Nguyễn Hữu Đăng Khoa** | 23010901 | Thiết kế và lập trình bộ kiểm thử Hộp trắng chống tranh chấp concurrency Ôn siêu tốc, cấu hình chạy kiểm thử tự động Pytest, đo lường và lập báo cáo Code Coverage $\ge 90\%$, biên soạn Phụ lục B. | **100% – Đạt** |
| 3 | **Hoàng Tiến Đạt** | 23010864 | Thiết kế và thực thi ma trận kiểm thử Hộp đen cho 5 màn hình chính (Hôm nay, Thư viện, Thêm từ, Sổ công thức, Cài đặt), tổng hợp lập bảng Defect Log phát hiện lỗi và theo dõi sửa lỗi. | **100% – Đạt** |
| 4 | **Tô Thị Thùy Dương** | 23010876 | Thiết kế kịch bản kiểm thử Hộp đen cho 3 phiên học tập (Học từ mới, Ôn SRS, Ôn siêu tốc), thực hiện kiểm thử tích hợp REST API qua Postman, xây dựng Ma trận truy xuất nguồn gốc (Phụ lục C). | **100% – Đạt** |
| 5 | **Nguyễn Tùng Dương** | 23013811 | Phân tích mã nguồn và kiểm thử hộp trắng Frontend `app.js`, thiết kế các kịch bản kiểm thử nâng cao (Stress test SQLite, Fuzzing Unicode), viết Chương 7, Kết luận và dàn trang toàn bộ báo cáo Word. | **100% – Đạt** |

---

### 4.10. PHỤ LỤC A, B, C
- **Phụ lục A: Cấu trúc dự án và Danh mục API REST**
  * Bảng cấu trúc cây thư mục của toàn bộ repo `Web_English/` kèm chú giải vai trò từng file.
  * Bảng danh mục 15 Endpoint REST API chi tiết: Cột `Phương thức (Method)`, `Đường dẫn (Endpoint)`, `Mô tả chức năng`, `Tham số đầu vào (Request Body)`, `Mã phản hồi chuẩn (Response Status)`.
- **Phụ lục B: Tổng hợp số liệu thống kê kiểm thử**
  * *B.1. Bảng thống kê Kiểm thử Hộp đen theo từng màn hình:* Tổng số TC, Số ca Pass, Số ca Fail, Tỷ lệ Pass (%).
  * *B.2. Bảng thống kê Bộ test Pytest Backend:* Tên file test, Số test case, Phân hệ kiểm thử, Kết quả Pass/Fail.
  * *B.3. Bảng thống kê Bộ test Automation UI:* Tên kịch bản, Số bước kiểm thử, Kết quả thực thi.
- **Phụ lục C: Ma trận truy xuất nguồn gốc (Traceability Matrix)**
  * Bảng ma trận 2 chiều chuẩn công nghiệp liên kết:
    `Tính năng / Yêu cầu (Feature) | Giao diện UI | Endpoint API | Mã Test Case Black-box | Mã Test Case White-box | File Script Automation`
  * Đảm bảo bao phủ 100% tất cả các chức năng cốt lõi của Lexiloop.

---

## 5. PHÂN CÔNG CÔNG VIỆC CỤ THỂ CHO 5 THÀNH VIÊN

Để hoàn thành khối lượng công việc trên đúng tiến độ và chất lượng cao nhất, 5 thành viên Nhóm 9 sẽ phối hợp chặt chẽ theo phân vai sau:

```
                               ┌────────────────────────────────────────┐
                               │  ĐỖ THÀNH LONG (23010174) - LEADER     │
                               │  - Chương 1 & Chương 2                 │
                               │  - Whitebox Logic SRS & CRUD           │
                               │  - Phụ lục A (Cấu trúc & Danh mục API) │
                               └──────────────────┬─────────────────────┘
                                                  │
                 ┌────────────────────────────────┼────────────────────────────────┐
                 │                                │                                │
┌────────────────┴───────────────┐ ┌──────────────┴───────────────┐ ┌──────────────┴───────────────┐
│ NGUYỄN HỮU ĐĂNG KHOA (23010901)│ │   HOÀNG TIẾN ĐẠT (23010864)  │ │  TÔ THỊ THÙY DƯƠNG (23010876) │
│ - Whitebox Concurrency Speed   │ │ - Blackbox 5 Màn hình chính  │ │ - Blackbox 3 Phiên học tập   │
│ - Pytest Suite & Code Coverage │ │ - Quản lý Defect Log         │ │ - Postman REST API Testing   │
│ - Phụ lục B (Thống kê số liệu) │ │ - Chụp ảnh giao diện lỗi     │ │ - Phụ lục C (Traceability)   │
└────────────────────────────────┘ └──────────────────────────────┘ └──────────────────────────────┘
                                                  │
                               ┌──────────────────┴─────────────────────┐
                               │     NGUYỄN TÙNG DƯƠNG (23013811)       │
                               │  - Whitebox Frontend app.js            │
                               │  - Kiểm thử nâng cao (Stress, Fuzzing) │
                               │  - Tổng hợp Word, dàn trang & Kết luận │
                               └────────────────────────────────────────┘
```

### Chi tiết Deliverables của từng thành viên:
1. **Đỗ Thành Long:**
   - Soạn thảo văn bản hoàn chỉnh Chương 1 và Chương 2 trong Word.
   - Vẽ sơ đồ kiến trúc hệ thống và sơ đồ thực thể liên kết ERD của 8 bảng CSDL.
   - Viết phần lý thuyết đồ thị CFG và độ phức tạp Cyclomatic của thuật toán SRS trong Chương 4.
   - Lập bảng danh mục toàn bộ API REST cho Phụ lục A.

2. **Nguyễn Hữu Đăng Khoa:**
   - Chạy lệnh đo Code Coverage thực tế, xuất báo cáo HTML và chụp ảnh terminal/HTML đính kèm vào Chương 4.
   - Viết tài liệu mô tả chi tiết cơ chế chống ghi trùng/tranh chấp ở Ôn siêu tốc (`attempt_id`, idempotency).
   - Thiết lập script chạy test tự động `run_tests.bat` và tài liệu hóa Chương 5.
   - Tổng hợp toàn bộ số liệu thống kê kiểm thử cho Phụ lục B.

3. **Hoàng Tiến Đạt:**
   - Trực tiếp chạy và kiểm thử thủ công 5 màn hình: Hôm nay, Thư viện, Thêm từ, Sổ công thức, Cài đặt.
   - Điền đầy đủ dữ liệu cho khoảng 65 bảng Test Case Black-box trong Chương 3.
   - Chụp ảnh minh chứng cho từng ca kiểm thử (đặc biệt là các ca Fail).
   - Lập bảng Defect Log chi tiết gồm ít nhất 10 lỗi thực tế trong Chương 7.

4. **Tô Thị Thùy Dương:**
   - Trực tiếp chạy và kiểm thử 3 phiên học: Học từ mới (6 bước), Ôn tập SRS (8 stage), Ôn siêu tốc (8 giây, 3 tim).
   - Điền đầy đủ dữ liệu cho khoảng 50 bảng Test Case Black-box trong Chương 3.
   - Tạo bộ Postman Collection và chạy kiểm thử 15 ca API REST, chụp ảnh kết quả kiểm thử trên Postman.
   - Thiết lập bảng Ma trận truy xuất nguồn gốc (Traceability Matrix) 2 chiều cho Phụ lục C.

5. **Nguyễn Tùng Dương:**
   - Đọc và phân tích mã nguồn `app.js`, viết nội dung kiểm thử White-box Frontend (State, Timer countdown, Web Speech API).
   - Viết mã và chạy các kịch bản kiểm thử nâng cao (Stress test chèn 5000 từ vào SQLite, Fuzzing Unicode/ký tự lạ).
   - Viết nội dung Chương 7 (Ưu điểm, Hạn chế, Hướng phát triển) và Kết luận.
   - Chịu trách nhiệm ráp toàn bộ các phần vào file mẫu `Báo_cáo_Nhóm_9_Testing.docx`, chỉnh sửa format chuẩn (font chữ, lề trang, mục lục tự động, caption bảng biểu/hình vẽ).

---

## 6. LỘ TRÌNH TRIỂN KHAI (TIMELINE 4 TUẦN)

| Tuần | Giai Đoạn | Công Việc Cụ Thể | Người Phụ Trách Chính | Sản Phẩm Đầu Ra (Deliverables) |
|---|---|---|---|---|
| **Tuần 1** | **Khởi động & Phân tích hệ thống** | - Khởi động server Web English, khảo sát toàn bộ UI và API.<br>- Viết Lời mở đầu, Chương 1 và Chương 2.<br>- Vẽ sơ đồ kiến trúc hệ thống và sơ đồ ERD CSDL.<br>- Thiết lập môi trường Pytest và chạy đo Code Coverage ban đầu. | Long, Khoa, Dương (Tùng) | - Bản nháp Chương 1 & 2 hoàn chỉnh.<br>- Sơ đồ ERD chuẩn 8 bảng.<br>- Báo cáo HTML Coverage sơ bộ ($90\%$). |
| **Tuần 2** | **Thực thi Kiểm thử Hộp đen & Hộp trắng** | - Thực hiện toàn bộ 115 test case Hộp đen trên UI và điền kết quả.<br>- Chạy bộ test API trên Postman.<br>- Viết nội dung Chương 3 (Hộp đen) đầy đủ các bảng biểu.<br>- Viết chi tiết Chương 4 (Hộp trắng): vẽ CFG, tính $V(G)$, phân tích kiểm thử SRS, CRUD, Concurrency. | Đạt, Dương (Thùy), Long, Khoa | - Chương 3 hoàn chỉnh với 115 test cases.<br>- Chương 4 hoàn chỉnh với phân tích mã nguồn và bảng map test case. |
| **Tuần 3** | **Tự động hóa, Kiểm thử nâng cao & Defect Log** | - Xây dựng kịch bản kiểm thử tự động UI (Chương 5).<br>- Thực hiện kiểm thử nâng cao: Stress test SQLite, Fuzzing Unicode (Chương 6).<br>- Tổng hợp danh sách lỗi thực tế thành Bảng Defect Log (Chương 7).<br>- Viết Ưu điểm, Hạn chế, Hướng phát triển và Kết luận. | Khoa, Dương (Tùng), Đạt | - Bản thảo hoàn chỉnh Chương 5, 6, 7.<br>- Bảng Defect Log chi tiết kèm bằng chứng lỗi.<br>- Lời kết luận và bài học kinh nghiệm. |
| **Tuần 4** | **Lắp ráp Báo cáo, Hoàn thiện Phụ lục & Rà soát** | - Xây dựng hoàn chỉnh Phụ lục A (Danh mục API), Phụ lục B (Thống kê số liệu), Phụ lục C (Traceability Matrix).<br>- Lắp ráp tất cả các chương vào file Word của Nhóm 9.<br>- Kiểm tra chéo số liệu giữa các chương.<br>- Căn chỉnh font Times New Roman 13, dãn dòng 1.3, cập nhật mục lục tự động.<br>- Xuất file PDF và chuẩn bị bảo vệ bài tập lớn. | Cả 5 thành viên (Dương Tùng tổng hợp) | - File `Báo_cáo_Nhóm_9_Testing.docx` và `.pdf` hoàn chỉnh 60+ trang.<br>- Sẵn sàng nộp bài cho TS. Trương Đức Phương. |

---

## 7. CHECKLIST CHẤT LƯỢNG (QUALITY GATE) TRƯỚC KHI NỘP BÀI

Trước khi xuất file bản in cuối cùng và nộp lên hệ thống của giảng viên, Trưởng nhóm và các thành viên cần kiểm tra nghiêm ngặt danh mục sau:

- [ ] **1. Tính toàn vẹn của cấu trúc:** Báo cáo có đủ Trang bìa, Mục lục tự động, Danh mục bảng biểu, Danh mục hình vẽ, Danh mục từ viết tắt, Mở đầu, 7 Chương, Kết luận, Bảng phân công nhiệm vụ và Phụ lục A, B, C.
- [ ] **2. Tính nhất quán của số liệu kiểm thử:**
  * Tổng số ca Black-box ghi ở Chương 3 phải bằng chính xác tổng số ca thống kê trong Bảng Phụ lục B.1 và Bảng 7.1.
  * Tổng số ca White-box ghi ở Chương 4 phải khớp với số ca chạy thực tế của Pytest và Phụ lục B.2.
  * Số lượng lỗi trong bảng Defect Log (Mục 7.2) phải khớp với các ca ghi nhận (FAIL) trong các bảng test case của Chương 3.
- [ ] **3. Chuẩn hóa Bảng biểu và Hình vẽ:**
  * Tất cả các bảng biểu đều có Caption phía trên theo dạng `Bảng X.Y: Tên bảng`.
  * Tất cả các hình vẽ đều có Caption phía dưới theo dạng `Hình X.Y: Tên hình`.
  * Không có bảng nào bị tràn lề giấy hoặc chữ bị cắt cụt.
- [ ] **4. Chất lượng ảnh minh chứng:**
  * Ảnh chụp màn hình giao diện web sắc nét, rõ ràng, không bị mờ hoặc méo tỷ lệ.
  * Ảnh chụp terminal chạy test và ảnh báo cáo HTML Coverage thể hiện đúng tên module của dự án Lexiloop.
- [ ] **5. Thể thức văn bản học thuật:**
  * Font chữ: Times New Roman, cỡ chữ 13pt cho phần thân bài.
  * Dãn dòng (Line spacing): 1.3 – 1.4 lines; Spacing: Before 0pt, After 4pt hoặc 6pt.
  * Căn lề: Lề trái 3.0 cm, lề phải 2.0 cm, lề trên 2.0 cm, lề dưới 2.0 cm.
  * Số trang được đánh ở góc dưới giữa hoặc góc phải, bắt đầu đánh số 1 từ phần Mở đầu.
- [ ] **6. Mã nguồn kiểm thử đính kèm:**
  * Thư mục `tests/` chạy lệnh `.venv\Scripts\python -m pytest` đạt $100\%$ Pass, không phát sinh lỗi ngoại lệ chưa xử lý.
