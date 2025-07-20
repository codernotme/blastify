@echo off
echo.
echo ========================================
echo    🚀 BLASTIFY SETUP - WINDOWS 🚀
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python detected
echo.

REM Run the setup script
echo 🔧 Running Blastify setup...
python setup.py

if errorlevel 1 (
    echo.
    echo ❌ Setup failed. Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Setup completed successfully!
echo.
echo 🚀 To start Blastify, run:
echo    python run.py streamlit
echo.
echo 📚 For more information, check README.md
echo.
pause
