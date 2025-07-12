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
echo Would you like to create a virtual environment? (y/n)
set /p create_venv=

if /i "%create_venv%" EQU "y" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv venv
    
    REM Activate the virtual environment
    if exist venv\Scripts\activate.bat (
        call venv\Scripts\activate.bat
        echo Virtual environment created and activated
    ) else (
        echo Failed to create virtual environment
    )
)

echo.
echo Installing required Python packages...
%PIP_CMD% install --upgrade pip
%PIP_CMD% install tensorflow keras numpy opencv-python Pillow mido pygame midi2audio openpyxl prettytable music21

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
echo To run the application:
echo   %PYTHON_CMD% Main_GUI.py
echo.
echo If you created a virtual environment, remember to activate it:
echo   venv\Scripts\activate
echo.

pause 