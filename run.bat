@echo off
python main.py
if %errorlevel% neq 0 (
    echo.
    echo [!] Something went wrong. Check if Python is installed.
    pause
)
pause