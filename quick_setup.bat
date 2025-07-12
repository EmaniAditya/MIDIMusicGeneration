@echo off
REM Quick setup script for Windows systems
REM This script automatically creates a virtual environment and installs all dependencies

echo =====================================================
echo   MIDI Music Generation - Quick Setup
echo =====================================================
echo.

REM Check for Python
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
    echo Python found
) else (
    echo Python not found. Please install Python 3.x
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check Python version
%PYTHON_CMD% -c "import sys; sys.exit(0) if sys.version_info >= (3, 6) else sys.exit(1)"
if %ERRORLEVEL% NEQ 0 (
    echo Python 3.6+ is required. Please upgrade your Python installation.
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...

REM Check if venv module is available
%PYTHON_CMD% -m venv --help >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Virtual environment module not available. 
    echo Please reinstall Python with the "Add Python to environment variables" 
    echo and "Install for all users" options checked.
    pause
    exit /b 1
)

REM Create the virtual environment
%PYTHON_CMD% -m venv venv

REM Activate the virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment created and activated
) else (
    echo Failed to create virtual environment
    pause
    exit /b 1
)

REM Install packages
echo Installing Python packages...
pip install --upgrade pip
pip install -r requirements.txt

REM Check installation status
if %ERRORLEVEL% NEQ 0 (
    echo Some packages failed to install. Please check the error messages above.
    echo You might need to install them manually.
) else (
    echo Python packages installed successfully
)

REM Create directories
echo Creating required directories...
if not exist MIDI\Models mkdir MIDI\Models
if not exist MIDI\Output\MIDI mkdir MIDI\Output\MIDI
if not exist MIDI\Output\MP3 mkdir MIDI\Output\MP3
if not exist MIDI\Result mkdir MIDI\Result

REM Create run script
echo Creating run script...
echo @echo off > run_app.bat
echo REM Run the MIDI Music Generation application >> run_app.bat
echo call venv\Scripts\activate.bat >> run_app.bat
echo python Main_GUI.py >> run_app.bat
echo. >> run_app.bat
echo pause >> run_app.bat

echo.
echo =====================================================
echo   Setup Complete!
echo =====================================================
echo.
echo To run the application:
echo   1. Double-click run_app.bat
echo   OR
echo   2. Manually:
echo      venv\Scripts\activate
echo      python Main_GUI.py
echo.

pause 