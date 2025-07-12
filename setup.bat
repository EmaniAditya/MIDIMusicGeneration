@echo off
REM MIDI Music Generation Project Setup Script for Windows
REM This script installs all required dependencies for the project

echo =====================================================
echo   MIDI Music Generation - Dependency Installer
echo =====================================================
echo.

REM Check for Python
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
    echo Python found
) else (
    echo Python not found. Please install Python 3.x
    exit /b 1
)

REM Check Python version
%PYTHON_CMD% -c "import sys; sys.exit(0) if sys.version_info >= (3, 6) else sys.exit(1)"
if %ERRORLEVEL% NEQ 0 (
    echo Python 3.6+ is required. Please upgrade your Python installation.
    exit /b 1
)

REM Check for pip
%PYTHON_CMD% -m pip --version >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PIP_CMD=%PYTHON_CMD% -m pip
    echo pip found
) else (
    echo pip not found. Installing pip...
    %PYTHON_CMD% -m ensurepip --default-pip
    set PIP_CMD=%PYTHON_CMD% -m pip
)

REM Offer to create a virtual environment
echo.
echo Creating a virtual environment is RECOMMENDED to avoid dependency conflicts.
echo Would you like to create a virtual environment? (y/n)
set /p create_venv=

if /i "%create_venv%" EQU "y" (
    echo Creating virtual environment...
    
    REM Check if venv is available
    %PYTHON_CMD% -m venv --help >nul 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo Virtual environment module not available. 
        echo Please reinstall Python with the "Add Python to environment variables" and 
        echo "Install for all users" options checked.
        exit /b 1
    )
    
    %PYTHON_CMD% -m venv venv
    
    REM Activate the virtual environment
    if exist venv\Scripts\activate.bat (
        call venv\Scripts\activate.bat
        echo Virtual environment created and activated
        
        REM Update variables to use the virtualenv python and pip
        set PYTHON_CMD=python
        set PIP_CMD=pip
    ) else (
        echo Failed to create virtual environment
        exit /b 1
    )
) else (
    echo Proceeding without a virtual environment (not recommended).
)

echo.
echo Installing required Python packages...
%PIP_CMD% install --upgrade pip
%PIP_CMD% install tensorflow keras numpy opencv-python Pillow mido pygame midi2audio openpyxl prettytable music21

REM Check if installation was successful
if %ERRORLEVEL% NEQ 0 (
    echo Some packages failed to install. Please check the error messages above.
    echo You might need to install them manually.
) else (
    echo Python packages installed successfully
)

echo.
echo Checking for system dependencies...

REM FluidSynth (for MIDI to audio conversion)
echo NOTE: FluidSynth is required for MIDI to audio conversion.
echo Please download and install FluidSynth from https://www.fluidsynth.org/
echo or use the Windows binary from https://github.com/FluidSynth/fluidsynth/releases

REM Create required directories
echo.
echo Creating required directories...
if not exist MIDI\Models mkdir MIDI\Models
if not exist MIDI\Output\MIDI mkdir MIDI\Output\MIDI
if not exist MIDI\Output\MP3 mkdir MIDI\Output\MP3
if not exist MIDI\Result mkdir MIDI\Result

echo.
echo =====================================================
echo   Setup Complete!
echo =====================================================
echo.

REM Create a convenience script
if /i "%create_venv%" EQU "y" (
    echo Creating convenience batch file...
    echo @echo off > run_app.bat
    echo REM Convenience script to run the MIDI Music Generation app >> run_app.bat
    echo call venv\Scripts\activate.bat >> run_app.bat
    echo python Main_GUI.py >> run_app.bat
    echo. >> run_app.bat
    echo pause >> run_app.bat
    
    echo To run the application:
    echo   1. Either double-click run_app.bat
    echo   2. Or manually activate the virtual environment:
    echo      venv\Scripts\activate
    echo      python Main_GUI.py
) else (
    echo To run the application:
    echo   %PYTHON_CMD% Main_GUI.py
)

echo.
echo If you encounter any dependency issues, please create a virtual environment:
echo   %PYTHON_CMD% -m venv venv
echo   venv\Scripts\activate
echo   pip install -r requirements.txt
echo.

pause 