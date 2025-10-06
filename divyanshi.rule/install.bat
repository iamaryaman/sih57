@echo off
REM Legal Metrology Compliance System - Installation Script for Windows
REM Run this batch file to install all required dependencies

echo.
echo ==========================================================
echo   Legal Metrology Compliance System - Installation
echo ==========================================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found: 
python --version

REM Check if pip is installed
echo Checking pip installation...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pip...
    python -m ensurepip --upgrade
)

echo pip version:
pip --version

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Create virtual environment (optional but recommended)
echo.
echo Creating virtual environment (recommended)...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install required packages
echo.
echo Installing required packages...
echo This may take a few minutes...

pip install Flask>=2.3.0
pip install pandas>=2.0.0
pip install matplotlib>=3.7.0
pip install numpy>=1.24.0
pip install requests>=2.31.0
pip install jsonschema>=4.19.0
pip install python-dateutil>=2.8.0
pip install colorama>=0.4.6
pip install Werkzeug>=2.3.0

REM Install optional packages
echo.
echo Installing optional packages...
pip install PyPDF2>=3.0.0
pip install openpyxl>=3.1.0
pip install rich>=13.5.0
pip install tqdm>=4.66.0

REM Create required directories
echo.
echo Creating required directories...
if not exist reports mkdir reports
if not exist uploads mkdir uploads
if not exist templates mkdir templates

echo.
echo Testing installation...
python -c "import flask, pandas, matplotlib.pyplot, json, re; print('All core libraries imported successfully!')"

if %errorlevel% eq 0 (
    echo.
    echo ==========================================================
    echo   Installation Complete!
    echo ==========================================================
    echo.
    echo Next steps:
    echo 1. Run the demo: python demo.py
    echo 2. Start web interface: python web_app.py  
    echo 3. Open browser to: http://localhost:5000
    echo.
    echo Documentation: README.md
    echo.
    echo To activate virtual environment later:
    echo   venv\Scripts\activate.bat
    echo.
) else (
    echo.
    echo WARNING: Installation test failed.
    echo Some libraries may not be installed correctly.
    echo.
)

pause