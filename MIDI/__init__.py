# MIDI Music Generation Package
# This file makes the MIDI directory a Python package

# Import necessary submodules
import os

# Define package structure
__all__ = ["MusicGeneration", "Run", "config"]

# Make sure directories exist
required_dirs = [
    "Models", 
    "Output/MIDI",
    "Output/MP3",
    "Result"
]

# Create required directories if they don't exist
for directory in required_dirs:
    dir_path = os.path.join(os.path.dirname(__file__), directory)
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
            print(f"Created directory: {dir_path}")
        except Exception as e:
            print(f"Error creating directory {dir_path}: {e}")
