"""Script sinh Bảng Defect Log (Bảng lỗi phát hiện được)
Chuyên trách: Member 5 - Nguyễn Tùng Dương
Tổng hợp danh sách các lỗi phát hiện trong quá trình kiểm thử để đưa vào Chương 7 của Báo cáo.
"""

import json
import os

DEFECTS = [
    {
        "id": "BUG_01",
        "module": "Dashboard",
        "title": "Lỗi tràn viền khối thống kê trên màn hình mobile",
        "severity": "Medium",
        "priority": "Normal",
        "status": "Đã ghi nhận (Cần tối ưu CSS)",
        "description": "Khi co nhỏ màn hình xuống kích thước 375x667, các khối thẻ từ mới và đang học bị tràn viền bên phải do flex-wrap chưa cấu hình co giãn.",
    },
    {
        "id": "BUG_02",
        "module": "Ôn siêu tốc",
        "title": "Timer 8 giây bị trễ 0.3s trên máy cấu hình yếu",
        "severity": "Medium",
        "priority": "Normal",
        "status": "Đã ghi nhận (Cần tối ưu setInterval)",
        "description": "Khi chạy nhiều tác vụ nặng, hàm setInterval trong JavaScript bị nghẽn luồng dẫn đến thời gian mỗi câu thực tế dài hơn 8 giây.",
    },
    {
        "id": "BUG_03",
        "module": "Ôn siêu tốc",
        "title": "Người dùng bấm đúp nút nộp bài tạo 2 request",
        "severity": "High",
        "priority": "Critical",
        "status": "Đã khắc phục (Fixed qua attempt_id)",
        "description": "Client gửi 2 request nộp kết quả cùng lúc. Đã khắc phục thành công nhờ cơ chế Idempotency kiểm tra attempt_id ở backend.",
    },
    {
        "id": "BUG_04",
        "module": "Thêm từ",
        "title": "Nhập collocation có chứa ký tự || bị tách nhầm",
        "severity": "Medium",
        "priority": "High",
        "status": "Đã khắc phục (Fixed)",
        "description": "Trong bulk import, ký tự || dùng làm dấu phân cách cột con. Nếu nội dung câu thật chứa || thì bị tách đôi. Đã fix qua logic regex.",
    },
    {
        "id": "BUG_05",
        "module": "Thư viện",
        "title": "Tìm kiếm tiếng Việt có dấu hoa bị sót từ",
        "severity": "Low",
        "priority": "Low",
        "status": "Đã khắc phục (Fixed)",
        "description": "Tìm từ khóa chữ hoa có dấu tiếng Việt (ví dụ: 'THUYẾT PHỤC') chưa khớp tuyệt đối do hàm lower() mặc định. Đã fix qua normalize NFKC.",
    },
    {
        "id": "BUG_06",
        "module": "Cài đặt",
        "title": "Giọng đọc Google US không phát tiếng trên trình duyệt Firefox",
        "severity": "Low",
        "priority": "Low",
        "status": "Đã ghi nhận (Phụ thuộc OS)",
        "description": "Trình duyệt Firefox trên một số bản Windows không nạp được giọng Google US English của Chrome. Hệ thống tự động fallback sang giọng mặc định.",
    },
    {
        "id": "BUG_07",
        "module": "Sổ công thức",
        "title": "Ô nhập công thức không tự động co giãn theo chiều dọc",
        "severity": "Low",
        "priority": "Low",
        "status": "Đã khắc phục (Fixed CSS)",
        "description": "Khi dán ghi chú dài 20 dòng, ô textarea xuất hiện thanh cuộn gây khó nhìn. Đã fix bằng thuộc tính CSS auto-resize.",
    },
    {
        "id": "BUG_08",
        "module": "Ôn tập SRS",
        "title": "Thẻ xem lại từ khi làm sai bị che khuất nút Tiếp tục",
        "severity": "Medium",
        "priority": "Normal",
        "status": "Đã khắc phục (Fixed)",
        "description": "Khi từ có quá nhiều ví dụ và collocations, popup kéo dài xuống dưới che mất nút 'Tiếp tục'. Đã thêm thuộc tính overflow-y: auto.",
    },
    {
        "id": "BUG_09",
        "module": "Học từ mới",
        "title": "Âm thanh đọc từ bị nuốt âm tiết đầu trên Chrome",
        "severity": "Low",
        "priority": "Low",
        "status": "Đã khắc phục (Fixed)",
        "description": "Do Web Speech API khởi động chưa kịp buffer, âm đầu bị cắt ngắn. Đã khắc phục bằng cách thêm độ trễ 100ms trước khi gọi speak().",
    },
    {
        "id": "BUG_10",
        "module": "Xuất CSV",
        "title": "Mở tệp CSV trên phần mềm Excel cũ bị lỗi font tiếng Việt",
        "severity": "Medium",
        "priority": "High",
        "status": "Đã khắc phục (Fixed qua UTF-8 BOM)",
        "description": "File CSV xuất bằng utf-8 thường bị Excel nhận nhầm bảng mã ANSI. Đã bổ sung ký tự UTF-8 BOM (\\ufeff) ở đầu file để Excel hiển thị chuẩn.",
    },
    {
        "id": "BUG_11",
        "module": "Thêm từ",
        "title": "Nhập khoảng trắng đầu đuôi không được làm sạch tự động",
        "severity": "Low",
        "priority": "Normal",
        "status": "Đã khắc phục (Fixed)",
        "description": "Người dùng copy paste từ vựng vô tình dính khoảng trắng '  diligent  ' làm sai lệch việc tìm kiếm. Đã thêm hàm strip() toàn diện.",
    },
    {
        "id": "BUG_12",
        "module": "Ôn siêu tốc",
        "title": "Trạng thái tim không đổi màu ngay khi mất mạng",
        "severity": "Low",
        "priority": "Low",
        "status": "Đã ghi nhận",
        "description": "Khi client mất kết nối mạng cục bộ, hiệu ứng tim bị giật 0.5s trước khi popup lỗi hiện lên.",
    },
    {
        "id": "BUG_13",
        "module": "Học từ mới",
        "title": "Câu ví dụ không chứa đúng từ tiếng Anh làm kẹt bài điền từ",
        "severity": "High",
        "priority": "Critical",
        "status": "Đã khắc phục (Fixed)",
        "description": "Nếu người dùng nhập ví dụ không có chứa từ gốc, bài điền từ không thể tạo chỗ trống. Đã fix: tự động chuyển sang bài gõ từ thông thường.",
    },
    {
        "id": "BUG_14",
        "module": "Thư viện",
        "title": "Xoá từ chưa có hộp thoại xác nhận thứ hai khi đang học",
        "severity": "Medium",
        "priority": "Normal",
        "status": "Đã khắc phục (Fixed)",
        "description": "Bấm xoá chỉ có 1 popup confirm đơn giản. Đã bổ sung cảnh báo rõ ràng rằng tiến độ SRS của từ cũng sẽ bị xoá vĩnh viễn.",
    },
    {
        "id": "BUG_15",
        "module": "Cơ sở dữ liệu",
        "title": "Chưa bật PRAGMA foreign_keys trên một số phiên bản SQLite",
        "severity": "High",
        "priority": "Critical",
        "status": "Đã khắc phục (Fixed qua event connect)",
        "description": "SQLite mặc định tắt ràng buộc khóa ngoại. Đã fix bằng việc lắng nghe sự kiện connect của SQLAlchemy để kích hoạt PRAGMA foreign_keys=ON.",
    },
]


def generate():
    out_dir = os.path.dirname(__file__)

    # 1. Xuất file JSON
    json_path = os.path.join(out_dir, "defect_log.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(DEFECTS, f, ensure_ascii=False, indent=2)

    # 2. Xuất bảng Markdown cho Báo cáo
    md_path = os.path.join(out_dir, "defect_log.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# BẢNG TỔNG HỢP CÁC LỖI PHÁT HIỆN ĐƯỢC (DEFECT LOG)\n\n")
        f.write("| Mã Bug | Phân Hệ / Màn Hình | Tên Lỗi & Mô Tả Chi Tiết | Mức Độ (Severity) | Mức Ưu Tiên (Priority) | Trạng Thái (Status) |\n")
        f.write("|---|---|---|---|---|---|\n")
        for b in DEFECTS:
            f.write(f"| **{b['id']}** | {b['module']} | **{b['title']}**: {b['description']} | {b['severity']} | {b['priority']} | {b['status']} |\n")

    print(f"[DEFECT LOG] Da xuat thanh cong {len(DEFECTS)} bugs tai:")
    print(f" - {json_path}")
    print(f" - {md_path}")


if __name__ == "__main__":
    generate()
