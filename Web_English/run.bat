@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Lexiloop chua duoc cai dat. Hay xem README.md de chay buoc cai dat lan dau.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" start.py
if errorlevel 1 (
  echo.
  pause
)
endlocal
