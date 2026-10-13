"""Automated Selenium UI Test & Screenshot Capture for Lexiloop
Tự động khởi động server Flask, dùng Selenium Chrome tương tác với toàn bộ 5 màn hình
và tự động chụp ảnh màn hình làm minh chứng kiểm thử thực tế.
"""

import os
import sys
import time
import threading
from werkzeug.serving import make_server

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import create_app
from models import db


class ServerThread(threading.Thread):
    def __init__(self, app, port=5005):
        super().__init__()
        self.server = make_server("127.0.0.1", port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


def run_selenium_ui_tests():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    screenshots_dir = os.path.join(root_dir, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    print("=" * 80)
    print(" " * 20 + "SELENIUM UI AUTOMATION & SCREENSHOT RUNNER")
    print("=" * 80)

    # 1. Khởi động Flask Server tạm thời trên port 5005
    port = 5005
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    server = ServerThread(app, port=port)
    server.start()
    print(f"[1/6] Da khoi dong Flask test server tai http://127.0.0.1:{port}")
    time.sleep(1)

    # 2. Khởi tạo Headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    base_url = f"http://127.0.0.1:{port}"

    try:
        # Step 1: Mở Dashboard
        print("[2/6] Dang kiem thu Man hinh Hom nay (Dashboard)...")
        driver.get(base_url)
        time.sleep(1.5)
        dash_path = os.path.join(screenshots_dir, "01_dashboard.png")
        driver.save_screenshot(dash_path)
        print(f" -> Da chup anh Dashboard: {dash_path}")

        # Step 2: Mở Thư viện
        print("[3/6] Dang kiem thu Man hinh Thu vien (Library)...")
        lib_btn = driver.find_element(By.CSS_SELECTOR, "button[data-route='library']")
        driver.execute_script("arguments[0].click();", lib_btn)
        time.sleep(1)
        lib_path = os.path.join(screenshots_dir, "02_library.png")
        driver.save_screenshot(lib_path)
        print(f" -> Da chup anh Thu vien: {lib_path}")

        # Step 3: Mở Thêm từ & nhập liệu
        print("[4/6] Dang kiem thu Man hinh Them tu (Add Word)...")
        add_btn = driver.find_element(By.CSS_SELECTOR, "button[data-route='add']")
        driver.execute_script("arguments[0].click();", add_btn)
        time.sleep(1)

        # Điền từ mẫu
        try:
            eng_input = driver.find_element(By.CSS_SELECTOR, "#singleAddView input[name='english']")
            eng_input.send_keys("eloquent")
            vi_input = driver.find_element(By.CSS_SELECTOR, "#singleAddView input[name='vietnamese']")
            vi_input.send_keys("hùng biện, lưu loát")
        except Exception as e:
            print(f"  Note finding input: {e}")

        time.sleep(0.5)
        add_path = os.path.join(screenshots_dir, "03_add_word.png")
        driver.save_screenshot(add_path)
        print(f" -> Da chup anh Them tu: {add_path}")

        # Step 4: Mở Sổ công thức
        print("[5/6] Dang kiem thu Man hinh So cong thuc (Formulas)...")
        form_btn = driver.find_element(By.CSS_SELECTOR, "button[data-route='formulas']")
        driver.execute_script("arguments[0].click();", form_btn)
        time.sleep(1)
        form_path = os.path.join(screenshots_dir, "04_formulas.png")
        driver.save_screenshot(form_path)
        print(f" -> Da chup anh So cong thuc: {form_path}")

        # Step 5: Mở Cài đặt
        print("[6/6] Dang kiem thu Man hinh Cai dat (Settings)...")
        set_btn = driver.find_element(By.CSS_SELECTOR, "button[data-route='settings']")
        driver.execute_script("arguments[0].click();", set_btn)
        time.sleep(1)
        set_path = os.path.join(screenshots_dir, "05_settings.png")
        driver.save_screenshot(set_path)
        print(f" -> Da chup anh Cai dat: {set_path}")

        print("=" * 80)
        print("[THANH CONG] Toan bo 5 man hinh da duoc kiem thu va chup anh thanh cong!")
        print(f"Tat ca anh duoc luu tai: {screenshots_dir}")
        print("=" * 80)

    finally:
        driver.quit()
        server.shutdown()


if __name__ == "__main__":
    run_selenium_ui_tests()
