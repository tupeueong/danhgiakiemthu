"""Script tự động chạy đo Code Coverage và xuất báo cáo HTML
Phục vụ Member 4 (Nguyễn Hữu Đăng Khoa) lấy số liệu cho Chương 4 của Báo cáo.
"""

import subprocess
import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def run():
    print("=" * 80)
    print(" " * 20 + "DANG KHOA - CODE COVERAGE MEASUREMENT")
    print("=" * 80)

    # Chạy pytest với coverage
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--cov=app",
        "--cov=models",
        "--cov=srs",
        "--cov-report=term-missing",
        "--cov-report=html",
        "tests/",
    ]

    result = subprocess.run(cmd)
    print("=" * 80)
    if result.returncode == 0:
        print("[SUCCESS] Tat ca cac test suite da PASS 100%!")
        print("Bao cao HTML da duoc sinh tai: Web_English/htmlcov/index.html")
    else:
        print(f"[NOTE] Ket qua chay voi returncode: {result.returncode}")
    print("=" * 80)


if __name__ == "__main__":
    run()
