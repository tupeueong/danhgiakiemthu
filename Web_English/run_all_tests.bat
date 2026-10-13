@echo off
chcp 65001 > nul
echo ======================================================================
echo    NHOM 9 - CHUONG TRINH CHAY TOAN BO TEST SUITE DUA AN LEXILOOP
echo ======================================================================
cd /d "%~dp0"
.venv\Scripts\python tests\run_all_tests.py
echo.
echo ======================================================================
echo    DA HOAN TAT KIEM THU! Nhấn phím bất kỳ để đóng...
echo ======================================================================
pause > nul
