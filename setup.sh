#!/bin/bash
# MIDI Music Generation Project Setup Script
# This script installs all required dependencies for the project

echo "====================================================="
echo "  MIDI Music Generation - Dependency Installer"
echo "====================================================="
echo ""

# Function to check if a command exists
command_exists() {
  command -v "$1" &> /dev/null
}

# Check for Python
if command_exists python3; then
  PYTHON_CMD="python3"
  echo "✅ Python3 found"
else
  echo "❌ Python3 not found. Please install Python 3.x"
  exit 1
fi

# Check for pip
if command_exists pip3; then
  PIP_CMD="pip3"
  echo "✅ pip3 found"
elif command_exists pip; then
  PIP_CMD="pip"
  echo "✅ pip found"
else
  echo "❌ pip not found. Installing pip..."
  $PYTHON_CMD -m ensurepip --default-pip
  PIP_CMD="pip3"
fi

# Create virtual environment (optional)
echo ""
echo "Would you like to create a virtual environment? (y/n)"
read -r create_venv

if [ "$create_venv" = "y" ] || [ "$create_venv" = "Y" ]; then
  echo "Creating virtual environment..."
  $PYTHON_CMD -m venv venv
  
  # Activate the virtual environment
  if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment created and activated"
  else
    echo "❌ Failed to create virtual environment"
  fi
fi

echo ""
echo "Installing required Python packages..."
$PIP_CMD install --upgrade pip
$PIP_CMD install tensorflow keras numpy opencv-python Pillow mido pygame midi2audio openpyxl prettytable music21

echo ""
echo "Checking for system dependencies..."

# Check for FluidSynth (required for MIDI to audio conversion)
if command_exists fluidsynth; then
  echo "✅ FluidSynth found"
else
  echo "⚠️ FluidSynth not found. Audio conversion may not work properly."
  echo "To install FluidSynth:"
  echo "  - On Ubuntu/Debian: sudo apt-get install fluidsynth"
  echo "  - On macOS: brew install fluidsynth"
  echo "  - On Windows: Download from https://www.fluidsynth.org/"
fi

# Create required directories
echo ""
echo "Creating required directories..."
mkdir -p MIDI/Models MIDI/Output/MIDI MIDI/Output/MP3 MIDI/Result

echo ""
echo "====================================================="
echo "  Setup Complete!"
echo "====================================================="
echo ""
echo "To run the application:"
echo "  $PYTHON_CMD Main_GUI.py"
echo ""
echo "If you created a virtual environment, remember to activate it:"
echo "  source venv/bin/activate  # On Linux/macOS"
echo "  venv\\Scripts\\activate     # On Windows"
echo "" 