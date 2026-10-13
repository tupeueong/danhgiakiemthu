# Lexiloop

Ứng dụng web học từ vựng chạy riêng trên máy, lưu dữ liệu bằng SQLite và phát
âm bằng các giọng có sẵn trong Chrome/Windows.

## Chức năng

- Thư viện chứa toàn bộ từ vựng đã thêm.
- **Sổ công thức** là khu vực ghi chú độc lập: mỗi công thức có một ô nội dung, giữ nguyên
  các dòng khi hiển thị và có thể thêm, sửa hoặc xoá. Các ghi chú này không tham gia bài tập
  hay lịch SRS của từ vựng.
- Mỗi từ trong Thư viện hiển thị nhanh tối đa hai ví dụ, hai
  collocation và hai word pattern; bấm vào mục để xem hoặc chỉnh sửa đầy đủ.
- Thêm từng từ hoặc dán nhiều dòng từ Excel, Google Sheets, TSV, `|` hay CSV.
- Ngoài nghĩa và loại từ, mỗi mục có thể lưu danh sách `Collocation` và
  `Word pattern`. Khi thêm hoặc sửa, nhập mỗi collocation/pattern trên một dòng.
  Các danh sách này được hiện trong màn làm quen khi có dữ liệu, nhưng không làm
  bảng thư viện trở nên rối.
- Mỗi từ có thể có nhiều câu ví dụ. Khi thêm hoặc sửa một từ, nhập mỗi câu trên
  một dòng; khi nhập hàng loạt, ngăn các câu trong cột `Examples` bằng ` || `.
  Mỗi lần làm quen hoặc làm bài điền câu, ứng dụng chọn ngẫu nhiên một ví dụ.
  Nếu không câu nào chứa đúng từ tiếng Anh, bài điền câu tự chuyển thành bài gõ từ.
- Một từ có nhiều loại từ được lưu thành nhiều mục riêng, ví dụ `record · noun`
  và `record · verb`. Mỗi mục có nghĩa, phiên âm, ví dụ và tiến độ SRS riêng.
  Có thể viết tắt `n`, `v`, `adj`, `adv` khi nhập; ứng dụng chuẩn hoá sang tên
  đầy đủ. Trong câu hỏi, loại từ luôn được hiển thị để phân biệt đúng mục đang học.
- Câu hỏi trắc nghiệm loại bỏ những đáp án nhiễu mơ hồ: mục có cùng từ tiếng
  Anh không làm nghĩa sai cho nhau, và các từ có cùng nghĩa không làm đáp án sai
  trong bài chọn từ.
- Sáu lượt ghi nhớ từ mới với câu hỏi chọn nghĩa, chọn từ, gõ từ, nghe và điền
  câu ví dụ. Sau khi chấm các câu không phải bài nghe, từ tiếng Anh sẽ được đọc
  lại bằng giọng đã chọn.
- Lịch SRS: 4 giờ → 12 giờ → 24 giờ → 6 ngày → 12 ngày → 48 ngày → 96 ngày
  → 6 tháng. Phần ôn SRS xoay vòng bốn dạng: chọn nghĩa, gõ từ, chọn từ và
  nghe rồi gõ; không sử dụng dạng nghe rồi chọn. Một câu sai trong giai đoạn ôn
  sẽ đặt lại lịch về 4 giờ và hiển thẻ xem lại đầy đủ từ, phiên âm,
  nghĩa, loại từ, cách dùng và ví dụ trước khi tiếp tục.
- Ôn siêu tốc chỉ lấy những từ đã học xong và đang đến hạn: 8 giây mỗi câu,
  bắt đầu với 3 tim, sai hoặc hết giờ mất 1 tim và đặt lại lịch về 4 giờ; đúng
  15 câu liên tiếp nhận thêm 1 tim. Nếu không tạo được ít nhất hai đáp án rõ
  ràng cho một từ, từ đó được bỏ qua và giữ nguyên lịch thay vì chuyển sang bài gõ.
- Ba lựa chọn giọng: Microsoft Mark, Microsoft Zira và Google US English.
- Tìm kiếm, lọc, sửa, xoá, đặt lại tiến độ và xuất CSV.

## Định dạng thêm hàng loạt

Định dạng 7 cột mới, theo đúng thứ tự:

```text
English    Phonetic    Vietnamese    Part of speech    Examples    Collocation    Word pattern
```

Các cột được ngăn bằng phím `Tab`. Nhiều mục trong các cột `Examples`,
`Collocation` và `Word pattern` đều được ngăn bằng ` || `. Danh sách 5 cột cũ
kết thúc ở `Examples` vẫn nhập được bình thường; hai danh sách mới sẽ được để
trống. Lexiloop cũng đọc lại được các tệp CSV xuất từ phiên bản cũ, phiên bản
một collocation/pattern và phiên bản danh sách hiện tại.

Trong tệp CSV do Lexiloop xuất, mỗi collocation và word pattern được giữ trên
một dòng bên trong ô CSV. Vì vậy nội dung thật có chứa `||` vẫn được nhập lại
nguyên vẹn.

## Cài đặt lần đầu trên Windows

Mở CMD trong thư mục `D:\IELTS\Prep` rồi chạy:

```cmd
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

Các thư viện chỉ được cài trong `.venv\Lib\site-packages` của project.

## Chạy Lexiloop

Cách đơn giản nhất: nhấp đúp `run.bat`.

Hoặc chạy bằng CMD:

```cmd
cd /d D:\IELTS\Prep
.venv\Scripts\python start.py
```

`start.py` khởi động server và tự mở `http://127.0.0.1:5000` trong trình duyệt.
Giữ cửa sổ CMD đang chạy; nhấn `Ctrl+C` để dừng Lexiloop.

`app.py` chứa ứng dụng Flask và được `start.py` sử dụng nội bộ. Người dùng bình
thường không cần chạy trực tiếp `app.py`.

## Dữ liệu

Dữ liệu nằm trong `instance\vocabulary.db`. Hãy dừng Lexiloop trước khi sao lưu
tệp này.

## Kiểm thử

```cmd
cd /d D:\IELTS\Prep
.venv\Scripts\python -m pytest tests -q
```

Kiểm thử sử dụng database tạm và không thay đổi `instance\vocabulary.db`.
