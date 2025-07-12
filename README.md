# MIDI Music Generation

## Project Overview

This project implements an **Automatic Music Generation System** using bio-inspired algorithms combined with deep learning models. The system can analyze existing MIDI files and generate new musical compositions by learning patterns from the training data.

## Key Features

- MIDI file processing and analysis
- Dataset management (splitting into training/testing sets)
- Implementation of multiple deep learning architectures:
  - Recurrent Neural Network (RNN)
  - Gated Recurrent Unit (GRU)
  - Long Short-Term Memory (LSTM)
  - Optimized Long Short-Term Memory (O-LSTM) - proposed approach
- Bio-inspired optimization algorithms
- Performance comparison and evaluation
- Music generation from trained models
- Graphical user interface for easy interaction

## Technical Components

### Deep Learning Models

The project implements and compares four different recurrent neural network architectures:

1. **Basic RNN** - Standard recurrent neural network model
2. **GRU** - Gated Recurrent Unit, which solves some vanishing gradient issues in RNNs
3. **LSTM** - Long Short-Term Memory, which is better at capturing long-term dependencies
4. **O-LSTM** - Optimized LSTM, a novel approach that enhances standard LSTM by combining multiple input branches (notes, offsets, durations) and optimizing the network using bio-inspired algorithms

### Bio-Inspired Optimization

The project uses the African Vultures Optimization Algorithm (AVOA) implemented in AVOA.py to optimize neural network parameters, improving the quality of generated music. This bio-inspired algorithm mimics the foraging behavior of vultures, including elimination-dispersal, reproduction, and chemotaxis steps to find optimal configurations for the neural network parameters.

### Dataset

The project includes a collection of MIDI files organized as:
- Training dataset (80%)
- Testing dataset (20%)

These files are used to train the models and evaluate their performance.

### GUI Application

The system provides a graphical user interface (Main_GUI.py) that allows users to:

- Load and view MIDI files
- Split datasets
- Train different models
- Test model performance
- Generate music
- View performance metrics and comparisons
- Export results (tables, graphs)

## Project Structure

```
MIDIMusicGeneration/
├── Dataset/               # Main MIDI file collection
├── MIDI/
│   ├── Code/              # Core code modules
│   ├── config.py          # Configuration settings
│   ├── Dataset/           # Working dataset copy
│   ├── MIDIFiles/         # Processed MIDI files
│   ├── Models/            # Trained model weights
│   │   ├── EGRUweights.hdf5
│   │   ├── ELSTMweights.hdf5
│   │   ├── ERNNweights.hdf5
│   │   └── ...
│   ├── MusicGeneration/   # Deep learning implementations
│   │   ├── AVOA.py        # Bio-inspired optimization algorithm
│   │   ├── ExistingGRU.py # GRU implementation
│   │   ├── ExistingRNN.py # RNN implementation
│   │   ├── ExistingLSTM.py # LSTM implementation
│   │   └── ProposedOLSTM.py # Optimized LSTM implementation
│   ├── Output/            # Generated music output
│   │   ├── MIDI/          # Generated MIDI files
│   │   └── MP3/           # Converted MP3 files
│   └── Result/            # Performance evaluation results
├── Main_GUI.py            # Main graphical user interface
└── Scripts/               # Helper scripts
```

## How It Works

1. **Data Preparation**:
   - MIDI files are loaded and processed
   - The dataset is split into training (80%) and testing (20%) sets

2. **Model Training**:
   - Different neural network architectures (RNN, GRU, LSTM, O-LSTM) are trained on the dataset
   - Bio-inspired algorithms optimize model parameters
   - Model weights are saved for later use

3. **Music Generation**:
   - Trained models generate new musical compositions
   - The system converts generated data into MIDI files
   - MIDI files can be converted to MP3 format for easier listening

4. **Performance Evaluation**:
   - Models are evaluated using metrics like accuracy, precision, recall, F-score
   - Comparative analysis identifies the best-performing approach
   - Results are presented as tables and graphs

## Requirements

- Python 3.6+
- TensorFlow/Keras
- NumPy
- OpenCV
- PIL (Python Imaging Library)
- Mido (MIDI Objects)
- Pygame (Audio playback)
- FluidSynth (MIDI to audio conversion)
- Tkinter (GUI)
- OpenPyXL (Excel file handling)
- PrettyTable (formatted console output)
- Pandas (data manipulation)
- Music21 (music analysis)

## Installation

### Quick Setup (Recommended)

We provide convenient setup scripts that will install all required dependencies:

#### For Linux/macOS:

```bash
# Option 1: Quick automated setup (recommended for Ubuntu/Debian)
chmod +x quick_setup.sh
./quick_setup.sh

# Option 2: Interactive setup
chmod +x setup.sh
./setup.sh
```

#### For Windows:

```
# Option 1: Quick automated setup (recommended)
quick_setup.bat

# Option 2: Interactive setup
setup.bat
```

### Manual Setup

If you prefer to install dependencies manually:

1. Create a virtual environment:
   ```
   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Install FluidSynth (required for MIDI to audio conversion):
   - **Ubuntu/Debian**: `sudo apt-get install fluidsynth`
   - **macOS**: `brew install fluidsynth`
   - **Windows**: Download from [FluidSynth website](https://www.fluidsynth.org/)

## Usage

1. Launch the application:
   ```
   python3 Main_GUI.py
   ```

2. Use the GUI to:
   - Read MIDI files from the dataset
   - Split data into training and testing sets
   - Train the models
   - Test model performance
   - Generate new music
   - Play the generated music directly from the interface
   - View comparative results

### Audio Playback

The application includes an integrated audio player that allows you to:

- Select and play generated MIDI files
- Control playback with play/stop buttons
- Automatically converts MIDI to audio format for playback

Note: Full audio functionality requires FluidSynth to be installed.

## Troubleshooting

### Common Issues

#### Missing Python Packages

If you encounter errors like `ModuleNotFoundError: No module named 'pandas'` or `ModuleNotFoundError: No module named 'openpyxl'`:

1. **Verify virtual environment activation**: Make sure you've activated the virtual environment before running the application
   ```bash
   # Linux/macOS
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

2. **Install missing packages directly**:
   ```bash
   pip install pandas openpyxl
   ```

3. **On Debian/Ubuntu systems with externally-managed-environment error**:
   ```bash
   # Option 1: Use the --break-system-packages flag
   pip install --break-system-packages -r requirements.txt
   
   # Option 2: Install to user directory
   pip install --user -r requirements.txt
   
   # Option 3: Use the setup scripts which handle this properly
   ./quick_setup.sh
   ```

#### Virtual Environment Issues

If you have trouble creating a virtual environment:

1. **Install venv package**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-venv
   
   # Or for specific Python version:
   sudo apt-get install python3.10-venv  # Replace 3.10 with your version
   ```

2. **Use system packages directly** (if you can't create a virtual environment):
   ```bash
   pip install --user -r requirements.txt
   ```

#### FluidSynth Not Found

If audio conversion doesn't work:

1. **Install FluidSynth**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install fluidsynth
   
   # macOS
   brew install fluidsynth
   ```

2. **Verify soundfont installation**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install fluid-soundfont-gm
   ```

## Potential Applications

- Assisting composers in creating new musical ideas
- Generating background music for games, videos, and other media
- Creating variations of existing musical pieces
- Educational tools for understanding music theory and composition

## Technical Innovations

The main technical innovation of this project is the Optimized Long Short-Term Memory (O-LSTM) architecture, which enhances standard LSTM networks in two key ways:

1. **Multi-branch Input Processing**: The O-LSTM model processes musical data through three separate input branches (notes, offsets, and durations), which are then merged and processed together before splitting again for output prediction. This architecture captures the complexity of musical structures better than traditional single-branch approaches.

2. **Bio-inspired Optimization**: The African Vultures Optimization Algorithm (AVOA) is used to fine-tune the network parameters, mimicking natural foraging behaviors to find optimal configurations. This optimization approach improves the quality, coherence, and creativity of the generated music beyond what standard gradient-based optimization can achieve. 