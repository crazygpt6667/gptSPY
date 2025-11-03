@echo on
echo Installing SecureConnect Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher and try again.
    pause
    exit /b 1
)

echo Installing required packages...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Failed to install required packages.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo Installation complete!
echo.
echo Starting SecureConnect Application...
python main.py

pause