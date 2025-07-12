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

# Check if we're in an externally managed environment (Debian/Ubuntu PEP 668)
is_externally_managed=false
if $PIP_CMD install --dry-run pytest 2>&1 | grep -q "externally-managed-environment"; then
  is_externally_managed=true
  echo "⚠️  Detected externally managed Python environment (PEP 668)"
  echo "    Creating a virtual environment is HIGHLY RECOMMENDED"
  echo ""
fi

# Create virtual environment
create_venv="n"
if [ "$is_externally_managed" = true ]; then
  echo "This system requires using a virtual environment to install packages."
  echo "Would you like to create a virtual environment? (y/n) [RECOMMENDED: y]"
else
  echo "Would you like to create a virtual environment? (y/n) [Recommended for isolation]"
fi
read -r create_venv

if [ "$create_venv" = "y" ] || [ "$create_venv" = "Y" ]; then
  # Check if python3-venv is installed (required on Debian/Ubuntu)
  if ! $PYTHON_CMD -m venv --help > /dev/null 2>&1; then
    echo "❌ python3-venv is not installed. Installing now..."
    echo "This may require your password."
    sudo apt-get update && sudo apt-get install -y python3-venv python3-full
  fi
  
  echo "Creating virtual environment..."
  $PYTHON_CMD -m venv venv
  
  # Activate the virtual environment
  if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment created and activated"
    # Update PIP_CMD and PYTHON_CMD to use the virtualenv versions
    PIP_CMD="pip"
    PYTHON_CMD="python"
  else
    echo "❌ Failed to create virtual environment"
    exit 1
  fi
else
  if [ "$is_externally_managed" = true ]; then
    echo "❌ Cannot proceed without a virtual environment on this system."
    echo "   Please create a virtual environment manually:"
    echo "   $ python3 -m venv venv"
    echo "   $ source venv/bin/activate"
    echo "   Then run this script again."
    exit 1
  else
    echo "⚠️ Proceeding without a virtual environment (not recommended)."
    echo "   Some dependencies may not install correctly."
  fi
fi

echo ""
echo "Installing required Python packages..."
$PIP_CMD install --upgrade pip

# Install packages
echo "Installing Python dependencies..."
if [ "$is_externally_managed" = true ] && [ "$create_venv" != "y" ] && [ "$create_venv" != "Y" ]; then
  # This should never happen due to the exit above, but just in case
  $PIP_CMD install --break-system-packages tensorflow keras numpy opencv-python Pillow mido pygame midi2audio openpyxl prettytable music21
else
  $PIP_CMD install tensorflow keras numpy opencv-python Pillow mido pygame midi2audio openpyxl prettytable music21
fi

# Check installation status
if [ $? -ne 0 ]; then
  echo "❌ Some packages failed to install. Please check the error messages above."
  echo "   You might need to install them manually."
else
  echo "✅ Python packages installed successfully"
fi

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

if [ "$create_venv" = "y" ] || [ "$create_venv" = "Y" ]; then
  echo "  1. Activate the virtual environment (if not already active):"
  echo "     source venv/bin/activate"
  echo "  2. Run the application:"
  echo "     python Main_GUI.py"
  
  # Create a convenience script
  cat > run_app.sh << EOF
#!/bin/bash
# Convenience script to run the MIDI Music Generation app
source venv/bin/activate
python Main_GUI.py
EOF
  chmod +x run_app.sh
  echo ""
  echo "A convenience script has been created. You can run the app with:"
  echo "  ./run_app.sh"
else
  echo "  $PYTHON_CMD Main_GUI.py"
fi

echo ""
echo "If you encounter any dependency issues, please create a virtual environment:"
echo "  $PYTHON_CMD -m venv venv"
echo "  source venv/bin/activate  # On Linux/macOS"
echo "  venv\\Scripts\\activate     # On Windows"
echo "  pip install -r requirements.txt"
echo "" 