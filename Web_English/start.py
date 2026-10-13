"""Start Lexiloop locally and open it in the default browser."""

import socket
import sys
from threading import Timer
import webbrowser

LOCAL_HOST = "127.0.0.1"
LOCAL_PORT = 5000
LOCAL_URL = f"http://{LOCAL_HOST}:{LOCAL_PORT}"


def port_is_in_use(host: str = LOCAL_HOST, port: int = LOCAL_PORT) -> bool:
    """Return True when another process is already serving the local address."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
        connection.settimeout(0.4)
        return connection.connect_ex((host, port)) == 0


if __name__ == "__main__":
    if port_is_in_use():
        print(f"Không thể khởi động: {LOCAL_URL} đang được một tiến trình khác sử dụng.")
        print("Hãy dừng cửa sổ Lexiloop cũ bằng Ctrl+C, rồi chạy lại run.bat.")
        sys.exit(1)

    from app import app

    Timer(1.0, lambda: webbrowser.open(LOCAL_URL)).start()
    print(f"Lexiloop đang chạy tại {LOCAL_URL}")
    print("Nhấn Ctrl+C trong cửa sổ này để dừng.")
    app.run(host=LOCAL_HOST, port=LOCAL_PORT, debug=False)
