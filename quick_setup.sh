#!/bin/bash
# Quick setup script for Ubuntu/Debian systems
# This script automatically creates a virtual environment and installs all dependencies

echo "====================================================="
echo "  MIDI Music Generation - Quick Setup"
echo "====================================================="
echo ""

# Check for Python
if command -v python3 &> /dev/null; then
  PYTHON_CMD="python3"
  echo "✅ Python3 found"
else
  echo "❌ Python3 not found. Please install Python 3.x"
  exit 1
fi

# Get Python version
PYTHON_VERSION=$($PYTHON_CMD --version | cut -d' ' -f2 | cut -d'.' -f1-2)

# Install python3-venv if needed
if ! $PYTHON_CMD -m venv --help > /dev/null 2>&1; then
  echo "Installing python3-venv package (may require password)..."
  sudo apt-get update
  if sudo apt-get install -y python3-venv; then
    echo "✅ python3-venv installed"
  elif sudo apt-get install -y python$PYTHON_VERSION-venv; then
    echo "✅ python$PYTHON_VERSION-venv installed"
  else
    echo "❌ Failed to install python3-venv. Please install manually with:"
    echo "   sudo apt-get install python3-venv or python$PYTHON_VERSION-venv"
    exit 1
  fi
fi

# Check for pip
if ! command -v pip3 &> /dev/null; then
  echo "Installing pip (may require password)..."
  sudo apt-get install -y python3-pip
fi

# Create and activate virtual environment
echo "Creating virtual environment..."
$PYTHON_CMD -m venv venv

if [ ! -f "venv/bin/activate" ]; then
  echo "❌ Failed to create virtual environment"
  exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python packages..."
pip install --upgrade pip
pip install wheel  # Ensure wheel is installed
pip install -r requirements.txt

# Check if FluidSynth is installed
echo "Checking for FluidSynth..."
if ! command -v fluidsynth &> /dev/null; then
  echo "FluidSynth not found. Would you like to install it? (y/n)"
  read -r install_fluidsynth
  
  if [ "$install_fluidsynth" = "y" ] || [ "$install_fluidsynth" = "Y" ]; then
    echo "Installing FluidSynth (may require password)..."
    sudo apt-get install -y fluidsynth
  else
    echo "⚠️ FluidSynth not installed. Audio conversion may not work properly."
  fi
else
  echo "✅ FluidSynth already installed"
fi

# Create required directories
echo "Creating required directories..."
mkdir -p MIDI/Models MIDI/Output/MIDI MIDI/Output/MP3 MIDI/Result

# Create run script
echo "Creating run script..."
cat > run_app.sh << EOF
#!/bin/bash
# Run the MIDI Music Generation application
source venv/bin/activate
python3 Main_GUI.py
EOF
chmod +x run_app.sh

echo ""
echo "====================================================="
echo "  Setup Complete!"
echo "====================================================="
echo ""
echo "To run the application:"
echo "  ./run_app.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  python3 Main_GUI.py"
echo "" 