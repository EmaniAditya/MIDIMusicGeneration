#!/usr/bin/env python3
"""
Test script to verify MIDI file processing functionality
"""

import os
import sys
from mido import MidiFile

def list_midi_files(directory):
    """List all MIDI files in the given directory"""
    print(f"Searching for MIDI files in: {directory}")
    if not os.path.exists(directory):
        print(f"ERROR: Directory '{directory}' does not exist.")
        return []
        
    midi_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.mid', '.midi')):
                midi_files.append(os.path.join(root, file))
    
    print(f"Found {len(midi_files)} MIDI files")
    return midi_files

def analyze_midi_file(midi_file):
    """Analyze a MIDI file and print its details"""
    try:
        print(f"\nAnalyzing: {midi_file}")
        midi = MidiFile(midi_file, clip=True)
        
        print(f"Type: {midi.type}")
        print(f"Length: {midi.length:.2f} seconds")
        print(f"Ticks per beat: {midi.ticks_per_beat}")
        print(f"Number of tracks: {len(midi.tracks)}")
        
        for i, track in enumerate(midi.tracks):
            print(f"\nTrack {i}: {track.name}")
            message_count = len(track)
            note_on_count = sum(1 for msg in track if msg.type == 'note_on' and msg.velocity > 0)
            note_off_count = sum(1 for msg in track if msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0))
            print(f"  Messages: {message_count}")
            print(f"  Notes: {note_on_count}")
            
        return True
    except Exception as e:
        print(f"Error processing {midi_file}: {str(e)}")
        return False

def main():
    """Main function"""
    # Check for dataset directory
    dataset_dir = "MIDI/Dataset"
    if not os.path.exists(dataset_dir):
        alternative_dirs = ["Dataset", "MIDI/MIDIFiles"]
        for alt_dir in alternative_dirs:
            if os.path.exists(alt_dir):
                dataset_dir = alt_dir
                print(f"Using alternative directory: {alt_dir}")
                break
    
    # List and analyze MIDI files
    midi_files = list_midi_files(dataset_dir)
    
    if not midi_files:
        print("No MIDI files found. Exiting.")
        return 1
    
    # Analyze up to 3 MIDI files for demonstration
    successful = 0
    for midi_file in midi_files[:3]:
        if analyze_midi_file(midi_file):
            successful += 1
    
    print(f"\nSuccessfully analyzed {successful} out of {min(3, len(midi_files))} MIDI files")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 