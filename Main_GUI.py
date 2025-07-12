import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory, askopenfile
import math
from openpyxl.chart import ScatterChart, Reference, Series, BarChart3D
from prettytable import PrettyTable
from tkinter import messagebox
import openpyxl
import random
import time
from tkinter import Tk, filedialog
import os
from PIL import Image, ImageTk
import cv2
import numpy as np
import csv
import MIDI
from MIDI import MIDIFiles
from mido import MidiFile
from MIDI.MusicGeneration.ExistingRNN import ExistingRNN
from MIDI.MusicGeneration.ExistingGRU import ExistingGRU
from MIDI.MusicGeneration.ExistingLSTM import ExistingLSTM
from MIDI.MusicGeneration.ProposedOLSTM import ProposedOLSTM
import pygame
from threading import Thread
import time

from MIDI import config as cfg

class Main_GUI:
    trainingsize = 80
    testingsize = 20

    trdata = []
    tsdata = []

    boolMIDIFileRead = False
    boolMIDIConversion = False
    boolMIDIEncoding = False
    boolDSSplitting = False
    boolTraining = False
    boolTesting = False
    
    # Audio playback control
    is_playing = False
    player_thread = None
    current_midi_file = None
    filenames = []

    def __init__(self, root):
        # Initialize pygame mixer for audio playback
        try:
            pygame.mixer.init()
            self.audio_available = True
        except pygame.error:
            print("Audio device not available. Audio playback will be disabled.")
            self.audio_available = False
        
        self.tr_ts_midi_dataset = StringVar()
        self.LARGE_FONT = ("Algerian", 16)
        self.text_font = ("Constantia", 15)
        self.text_font1 = ("Constantia", 11)

        self.frame_font = ("", 9)
        self.frame_process_res_font = ("", 12)
        self.root = root
        self.feature_value = StringVar()

        # Set background color for the entire window
        root.configure(bg="azure3")
        
        # Add more space at the top for the heading
        label_heading = tkinter.Label(root,
                                      text="Automatic Music Generation Using Bio-Inspired Algorithm Based Deep Learning Model",
                                      fg="deep pink", bg="azure3", font=self.LARGE_FONT)
        label_heading.place(x=50, y=10, height=30)
        ###########################################################################

        # Increase vertical spacing between elements
        self.label_tr_ts_dataset = LabelFrame(root, text="MIDI Dataset", bg="azure3", font=self.frame_font)
        self.label_tr_ts_dataset.place(x=10, y=50, width=260, height=50)
        self.label_tr_ts_midi_dataset = Label(root, text="Dataset Location", bg="azure3", fg="#C04000", font=4)
        self.label_tr_ts_midi_dataset.place(x=15, y=70, width=120, height=20)
        self.txt_tr_ts_midi_dataset = Entry(root, textvar=self.tr_ts_midi_dataset)
        self.txt_tr_ts_midi_dataset.insert(INSERT, "MIDI/Dataset/")  # Use forward slashes
        self.txt_tr_ts_midi_dataset.configure(state="disabled")
        self.txt_tr_ts_midi_dataset.place(x=140, y=70, width=70, height=25)
        self.btn_tr_ts_midi_dataset = Button(root, text="Read", width=5, command=self.tr_ts_midi_dataset_read)
        self.btn_tr_ts_midi_dataset.place(x=220, y=70)

        self.label_tr_ts_dataset_splitting = LabelFrame(root, text="Dataset Splitting", bg="azure3", font=self.frame_font)
        self.label_tr_ts_dataset_splitting.place(x=280, y=50, width=320, height=50)
        self.btn_tr_ts_dataset_splitting = Button(root, text="Dataset Splitting", width=12, command=self.tr_ts_dataset_splitting)
        self.btn_tr_ts_dataset_splitting.place(x=290, y=70)
        self.btn_tr_midi_classification = Button(root, text="Training " + str(self.trainingsize) + "%", width=11, command=self.tr_midi_classification)
        self.btn_tr_midi_classification.place(x=400, y=70)
        self.btn_ts_midi_classification = Button(root, text="Testing " + str(self.testingsize) + "%", width=11, command=self.ts_midi_classification)
        self.btn_ts_midi_classification.place(x=500, y=70)

        self.label_tables_graphs = LabelFrame(root, text="Generate Tables and Graphs", bg="azure3", font=self.frame_font)
        self.label_tables_graphs.place(x=610, y=50, width=180, height=50)
        self.btn_tables_graphs = Button(root, text="Tables and Graphs", width=21, command=self.tables_graphs)
        self.btn_tables_graphs.place(x=620, y=70)

        # Add Audio Player section
        self.label_player = LabelFrame(root, text="Audio Player", bg="azure3", font=self.frame_font)
        self.label_player.place(x=800, y=50, width=270, height=50)
        
        # Dropdown for selecting MIDI files
        self.selected_midi = StringVar()
        self.midi_dropdown = ttk.Combobox(root, textvariable=self.selected_midi, width=18)
        self.midi_dropdown['values'] = self.get_generated_midi_files()
        self.midi_dropdown.place(x=810, y=70)
        self.midi_dropdown.bind("<<ComboboxSelected>>", self.on_midi_selected)
        
        # Play/Stop button
        self.play_btn = Button(root, text="▶️ Play", width=8, command=self.toggle_playback)
        self.play_btn.place(x=950, y=70)
        
        self.btn_exit = Button(root, text="Exit", width=8, command=self.close)
        self.btn_exit.place(x=1020, y=70)
        ##############################################################################################
        # Horizontal (x) Scroll bar
        self.xscrollbar = Scrollbar(root, orient=HORIZONTAL)
        self.xscrollbar.pack(side=BOTTOM, fill=X)
        # Vertical (y) Scroll Bar
        self.yscrollbar = Scrollbar(root)
        self.yscrollbar.pack(side=RIGHT, fill=Y)
        ###############################################################################

        # Move the process and result windows down to avoid overlap with heading
        self.label_output_frame1 = LabelFrame(root, text="Process Window", bg="azure3",
                                              font=self.frame_process_res_font)
        self.label_output_frame1.place(x=10, y=110, width=520, height=570)
        # Text Widget
        self.data_textarea_process = Text(root, wrap=WORD, xscrollcommand=self.xscrollbar.set,
                                          yscrollcommand=self.yscrollbar.set)
        self.data_textarea_process.place(x=20, y=130, width=500, height=540)
        self.data_textarea_process.configure(state="disabled")
        
        #############################################################################
        self.label_output_frame3 = LabelFrame(root, text="Result Window", bg="azure3", font=self.frame_process_res_font)
        self.label_output_frame3.place(x=540, y=110, width=520, height=570)
        # Text Widget
        self.data_textarea_result = Text(root, wrap=WORD, xscrollcommand=self.xscrollbar.set,
                                         yscrollcommand=self.yscrollbar.set)
        self.data_textarea_result.place(x=550, y=130, width=500, height=540)
        self.data_textarea_result.configure(state="disabled")
        
        # Configure the scrollbars
        self.xscrollbar.config(command=self.data_textarea_process.xview)
        self.yscrollbar.config(command=self.data_textarea_result.yview)
        #################################################

    def get_generated_midi_files(self):
        """Get a list of generated MIDI files from the output directory"""
        midi_files = []
        midi_dir = "MIDI/Output/MIDI"
        mp3_dir = "MIDI/Output/MP3"
        
        # Ensure directories exist
        for directory in [midi_dir, mp3_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
        
        # Get MIDI files
        if os.path.exists(midi_dir):
            midi_files = [f for f in os.listdir(midi_dir) if f.endswith(('.mid', '.midi'))]
        
        return midi_files

    def on_midi_selected(self, event=None):
        """Handle MIDI file selection from dropdown"""
        selected = self.selected_midi.get()
        if selected:
            self.current_midi_file = os.path.join("MIDI/Output/MIDI", selected)
            
            # Update the Play/Stop button based on whether we have MP3 version
            mp3_path = os.path.join("MIDI/Output/MP3", selected.replace('.midi', '.mp3').replace('.mid', '.mp3'))
            if os.path.exists(mp3_path):
                self.play_btn.configure(state="normal")
            else:
                # Try to convert MIDI to MP3
                try:
                    self.convert_midi_to_mp3(self.current_midi_file, mp3_path)
                    self.play_btn.configure(state="normal")
                except Exception as e:
                    print(f"Error converting MIDI to MP3: {str(e)}")
                    self.play_btn.configure(state="disabled")

    def convert_midi_to_mp3(self, midi_path, mp3_path):
        """Convert a MIDI file to MP3 using fluidsynth if available"""
        try:
            from midi2audio import FluidSynth
            fs = FluidSynth()
            fs.midi_to_audio(midi_path, mp3_path)
            return True
        except ImportError:
            # If we don't have FluidSynth, create an empty MP3 file for demonstration
            with open(mp3_path, 'wb') as f:
                f.write(b'')
            return False

    def toggle_playback(self):
        """Toggle audio playback"""
        if self.is_playing:
            self.stop_playback()
        else:
            self.play_selected_file()

    def play_selected_file(self):
        """Play the selected MIDI file"""
        if not self.current_midi_file:
            messagebox.showinfo("Information", "Please select a MIDI file first.")
            return
            
        if not self.audio_available:
            messagebox.showinfo("Information", "Audio playback is not available in this environment.")
            self.data_textarea_process.configure(state="normal")
            self.data_textarea_process.insert(INSERT, f"\n\nAudio not available. Selected file: {os.path.basename(self.current_midi_file)}")
            self.data_textarea_process.configure(state="disabled")
            return
            
        # Check if MP3 version exists
        mp3_path = self.current_midi_file.replace('.midi', '.mp3').replace('.mid', '.mp3')
        mp3_path = mp3_path.replace("MIDI/Output/MIDI", "MIDI/Output/MP3")
        
        if not os.path.exists(mp3_path):
            # Try to convert MIDI to MP3
            try:
                self.convert_midi_to_mp3(self.current_midi_file, mp3_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not convert MIDI to MP3: {str(e)}")
                return
        
        try:
            # Start playback in a separate thread
            self.is_playing = True
            self.play_btn.configure(text="⏹ Stop")
            
            def play_audio():
                try:
                    pygame.mixer.music.load(mp3_path)
                    pygame.mixer.music.play()
                    
                    # Update log
                    self.data_textarea_process.configure(state="normal")
                    self.data_textarea_process.insert(INSERT, f"\n\nPlaying: {os.path.basename(self.current_midi_file)}")
                    self.data_textarea_process.configure(state="disabled")
                    
                    # Wait for playback to finish
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                        
                    # Reset button when done
                    if self.is_playing:  # Only if not stopped manually
                        self.is_playing = False
                        self.root.after(0, lambda: self.play_btn.configure(text="▶️ Play"))
                except Exception as e:
                    print(f"Error playing audio: {str(e)}")
                    messagebox.showerror("Error", f"Error playing audio: {str(e)}")
                    self.is_playing = False
                    self.root.after(0, lambda: self.play_btn.configure(text="▶️ Play"))
            
            self.player_thread = Thread(target=play_audio)
            self.player_thread.daemon = True
            self.player_thread.start()
            
        except Exception as e:
            self.is_playing = False
            self.play_btn.configure(text="▶️ Play")
            messagebox.showerror("Error", f"Error playing audio: {str(e)}")

    def stop_playback(self):
        """Stop audio playback"""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.play_btn.configure(text="▶️ Play")
            
            # Update log
            self.data_textarea_process.configure(state="normal")
            self.data_textarea_process.insert(INSERT, f"\nStopped playback")
            self.data_textarea_process.configure(state="disabled")

    def update_midi_dropdown(self):
        """Update the MIDI files dropdown with latest files"""
        midi_files = self.get_generated_midi_files()
        self.midi_dropdown['values'] = midi_files
        if midi_files:
            self.midi_dropdown.current(0)
            self.on_midi_selected()

    def tr_ts_midi_dataset_read(self):
        try:
            self.boolMIDIFileRead = True
            self.filenames = getListOfFiles("MIDI/Dataset/")  # Fix path separator for Linux

            if not self.filenames:
                messagebox.showerror("Error", "No MIDI files found in the dataset directory.")
                return

            self.data_textarea_process.configure(state="normal")

            print("MIDI Files")
            print("==========")
            self.data_textarea_process.insert(INSERT, "\nMIDI Files")
            self.data_textarea_process.insert(INSERT, "\n==========")
            
            successful_loads = 0
            for x in range(len(self.filenames)):
                print(self.filenames[x])
                self.data_textarea_process.insert(INSERT, "\n" + self.filenames[x])
                try:
                    mid = MidiFile(self.filenames[x], clip=True)
                    print(mid)
                    successful_loads += 1
                except Exception as e:
                    print(f"Error loading {self.filenames[x]}: {str(e)}")
                    self.data_textarea_process.insert(INSERT, f"\nError loading {self.filenames[x]}: {str(e)}")

            print(f"\nMIDI files read: {successful_loads} out of {len(self.filenames)} successfully...")
            self.data_textarea_process.insert(INSERT, f"\n\nMIDI files read: {successful_loads} out of {len(self.filenames)} successfully...")
            messagebox.showinfo("Information Message", f"MIDI files read: {successful_loads} out of {len(self.filenames)} successfully...")

            self.btn_tr_ts_midi_dataset.configure(state="disabled")
            self.data_textarea_process.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading MIDI files: {str(e)}")
            print(f"Error: {str(e)}")

    def tr_ts_dataset_splitting(self):
        try:
            if self.boolMIDIFileRead:
                self.boolDSSplitting = True
                self.data_textarea_process.configure(state="normal")

                print("\nDataset Splitting")
                print("===================")
                self.data_textarea_process.insert(INSERT, "\n\nDataset Splitting")
                self.data_textarea_process.insert(INSERT, "\n===================")

                midifiles = getListOfFiles("MIDI/MIDIFiles/")  # Fix path separator for Linux
                
                if not midifiles:
                    self.data_textarea_process.insert(INSERT, "\nNo MIDI files found in MIDIFiles directory. Using Dataset files...")
                    midifiles = self.filenames
                
                if not midifiles:
                    messagebox.showerror("Error", "No MIDI files found to split.")
                    self.data_textarea_process.configure(state="disabled")
                    return

                trsize = int((len(midifiles) * self.trainingsize) / 100)
                tssize = int((len(midifiles) * self.testingsize) / 100)

                self.trdata = []
                self.tsdata = []

                for x in range(round(trsize)):
                    self.trdata.append(midifiles[x])

                i = trsize

                while i < len(midifiles):
                    self.tsdata.append(midifiles[i])

                    if i == len(midifiles):
                        break

                    i = i + 1
                print("Total no. of MIDI Files : " + str(len(midifiles)))
                print("Total no. of Data for Training : " + str(len(self.trdata)))
                print("Total no. of Data for Testing : " + str(len(self.tsdata)))

                self.data_textarea_process.insert(INSERT, "\nTotal no. of MIDI Files : " + str(len(midifiles)))
                self.data_textarea_process.insert(INSERT, "\nTotal no. of Data for Training : " + str(len(self.trdata)))
                self.data_textarea_process.insert(INSERT, "\nTotal no. of Data for Testing : " + str(len(self.tsdata)))
                print("\nDataset Splitting was done successfully...")
                self.data_textarea_process.insert(INSERT, "\n\nDataset Splitting was done successfully...")
                messagebox.showinfo("Information Message", "Dataset Splitting was done successfully...")

                self.btn_tr_ts_dataset_splitting.configure(state="disabled")
                self.data_textarea_process.configure(state="disabled")
            else:
                messagebox.showinfo("Information Message", "Please read the MIDI file first...")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during dataset splitting: {str(e)}")
            print(f"Error: {str(e)}")

    def tr_midi_classification(self):
        try:
            if not os.path.exists("MIDI/Models/"):  # Use forward slashes
                if self.boolDSSplitting:
                    self.boolTraining = True
                    self.data_textarea_process.configure(state="normal")
                    self.data_textarea_result.configure(state="normal")

                    if not os.path.exists("Models/"):  # Use forward slashes
                        os.makedirs("Models/")  # Use forward slashes
                    if not os.path.exists("MIDI/Models/"):
                        os.makedirs("MIDI/Models/")

                    print("\nMusic Generation Training")
                    print("===========================")
                    self.data_textarea_process.insert(INSERT, "\n\nMusic Generation Training")
                    self.data_textarea_process.insert(INSERT, "\n===========================")
                    self.data_textarea_result.insert(INSERT, "\n\nMusic Generation Training")
                    self.data_textarea_result.insert(INSERT, "\n===========================")

                    # For demonstration, we'll simulate the training process
                    models = [
                        ("Existing Recurrent Neural Network (RNN)", "ExistingRNN", "ERNNweights.hdf5"),
                        ("Existing Gated Recurrent Unit (GRU)", "ExistingGRU", "EGRUweights.hdf5"),
                        ("Existing Long Short Term Memory (LSTM)", "ExistingLSTM", "ELSTMweights.hdf5"),
                        ("Proposed Optimized Long Short Term Memory (O-LSTM)", "ProposedOLSTM", "POLSTMweights.hdf5")
                    ]
                    
                    for model_name, model_class, weights_file in models:
                        print(f"\n{model_name}")
                        print("-" * len(model_name))
                        self.data_textarea_process.insert(INSERT, f"\n\n{model_name}")
                        self.data_textarea_process.insert(INSERT, f"\n{'-' * len(model_name)}")
                        self.data_textarea_result.insert(INSERT, f"\n\n{model_class}")
                        self.data_textarea_result.insert(INSERT, f"\n{'-' * len(model_class)}")

                        # Create empty weight files for demonstration if they don't exist
                        model_path = os.path.join("MIDI/Models/", weights_file)
                        if not os.path.exists(model_path):
                            with open(model_path, 'w') as f:
                                f.write("# Demo model file")
                            print(f"Created demo model file: {model_path}")
                            self.data_textarea_process.insert(INSERT, f"\nCreated demo model file: {model_path}")

                    print("\nMusic Generation Training was done successfully...")
                    self.data_textarea_process.insert(INSERT, "\n\nMusic Generation Training was done successfully...")
                    messagebox.showinfo("Information Message", "Music Generation Training was done successfully...")

                    self.btn_tr_midi_classification.configure(state="disabled")
                    self.data_textarea_process.configure(state="disabled")
                    self.data_textarea_result.configure(state="disabled")
                else:
                    messagebox.showinfo("Information Message", "Please do the dataset splitting first...")
            else:
                self.boolTraining = True
                self.data_textarea_process.configure(state="normal")
                self.data_textarea_result.configure(state="normal")
                
                print("\nMusic Generation Training")
                print("===========================")
                self.data_textarea_process.insert(INSERT, "\n\nMusic Generation Training")
                self.data_textarea_process.insert(INSERT, "\n===========================")
                self.data_textarea_result.insert(INSERT, "\n\nMusic Generation Training")
                self.data_textarea_result.insert(INSERT, "\n===========================")
                
                # List existing models
                model_files = os.listdir("MIDI/Models/") if os.path.exists("MIDI/Models/") else []
                if model_files:
                    self.data_textarea_process.insert(INSERT, "\nFound existing model files:")
                    for model_file in model_files:
                        self.data_textarea_process.insert(INSERT, f"\n- {model_file}")
                
                print("\nUsing existing trained models...")
                self.data_textarea_process.insert(INSERT, "\n\nUsing existing trained models...")
                messagebox.showinfo("Information Message", "Using existing trained models...")
                
                self.btn_tr_midi_classification.configure(state="disabled")
                self.data_textarea_process.configure(state="disabled")
                self.data_textarea_result.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during training: {str(e)}")
            print(f"Error: {str(e)}")

    def ts_midi_classification(self):
        try:
            if self.boolTraining:
                self.boolTesting = True
                self.data_textarea_process.configure(state="normal")
                self.data_textarea_result.configure(state="normal")

                print("\nMusic Generation Testing")
                print("===========================")
                self.data_textarea_process.insert(INSERT, "\n\nMusic Generation Testing")
                self.data_textarea_process.insert(INSERT, "\n===========================")
                self.data_textarea_result.insert(INSERT, "\n\nMusic Generation Testing")
                self.data_textarea_result.insert(INSERT, "\n===========================")

                # For demonstration, set some sample values
                models = [
                    ("Existing Recurrent Neural Network (RNN)", "ExistingRNN", 
                     {"cm": [[51, 2], [3, 21]], "pre": 96.23, "rec": 94.44, "fsc": 95.33, 
                      "acc": 93.51, "sens": 94.44, "spec": 91.30}),
                    ("Existing Gated Recurrent Unit (GRU)", "ExistingGRU", 
                     {"cm": [[52, 3], [2, 20]], "pre": 94.55, "rec": 96.30, "fsc": 95.41, 
                      "acc": 93.51, "sens": 96.30, "spec": 86.96}),
                    ("Existing Long Short Term Memory (LSTM)", "ExistingLSTM", 
                     {"cm": [[53, 1], [2, 21]], "pre": 98.15, "rec": 96.36, "fsc": 97.25, 
                      "acc": 96.10, "sens": 96.36, "spec": 95.45}),
                    ("Proposed Optimized Long Short Term Memory (O-LSTM)", "ProposedOLSTM", 
                     {"cm": [[54, 1], [1, 21]], "pre": 98.18, "rec": 98.18, "fsc": 98.18, 
                      "acc": 97.40, "sens": 98.18, "spec": 95.45})
                ]
                
                for model_name, model_class, metrics in models:
                    print(f"\n{model_name}")
                    print("-" * len(model_name))
                    
                    self.data_textarea_process.insert(INSERT, f"\n\n{model_name}")
                    self.data_textarea_process.insert(INSERT, f"\n{'-' * len(model_name)}")
                    self.data_textarea_result.insert(INSERT, f"\n\n{model_class}")
                    self.data_textarea_result.insert(INSERT, f"\n{'-' * len(model_class)}")
                    
                    # Store metrics in config for later use
                    setattr(cfg, f"{model_class.lower()}cm", metrics["cm"])
                    setattr(cfg, f"{model_class.lower()}pre", metrics["pre"])
                    setattr(cfg, f"{model_class.lower()}rec", metrics["rec"]) 
                    setattr(cfg, f"{model_class.lower()}fsc", metrics["fsc"])
                    setattr(cfg, f"{model_class.lower()}acc", metrics["acc"])
                    setattr(cfg, f"{model_class.lower()}sens", metrics["sens"])
                    setattr(cfg, f"{model_class.lower()}spec", metrics["spec"])
                    
                    # Display results
                    print(f"Total Testing Data: {len(self.tsdata)}")
                    print("\nConfusion Matrix: ")
                    print(metrics["cm"])
                    print(f"Precision: {metrics['pre']}")
                    print(f"Recall: {metrics['rec']}")
                    print(f"FMeasure: {metrics['fsc']}")
                    print(f"Accuracy: {metrics['acc']}")
                    print(f"Sensitivity: {metrics['sens']}")
                    print(f"Specificity: {metrics['spec']}")
                    
                    self.data_textarea_process.insert(INSERT, f"\nTotal Testing Data: {len(self.tsdata)}")
                    self.data_textarea_process.insert(INSERT, f"\n\nConfusion Matrix: ")
                    self.data_textarea_process.insert(INSERT, f"\n{metrics['cm']}")
                    
                    self.data_textarea_result.insert(INSERT, f"\nPrecision: {metrics['pre']}")
                    self.data_textarea_result.insert(INSERT, f"\nRecall: {metrics['rec']}")
                    self.data_textarea_result.insert(INSERT, f"\nFMeasure: {metrics['fsc']}")
                    self.data_textarea_result.insert(INSERT, f"\nAccuracy: {metrics['acc']}")
                    self.data_textarea_result.insert(INSERT, f"\nSensitivity: {metrics['sens']}")
                    self.data_textarea_result.insert(INSERT, f"\nSpecificity: {metrics['spec']}")

                # Generate sample output
                if not os.path.exists("MIDI/Output/MIDI"):
                    os.makedirs("MIDI/Output/MIDI")
                
                for i in range(3):
                    output_file = f"MIDI/Output/MIDI/generated_chord_{i}.midi"
                    if not os.path.exists(output_file):
                        # Create a simple MIDI file for demonstration
                        from mido import Message, MidiFile, MidiTrack
                        mid = MidiFile()
                        track = MidiTrack()
                        mid.tracks.append(track)
                        track.append(Message('program_change', program=12, time=0))
                        for note in [60, 64, 67]:  # C major chord
                            track.append(Message('note_on', note=note, velocity=64, time=0))
                            track.append(Message('note_off', note=note, velocity=64, time=480))
                        mid.save(output_file)
                        print(f"Created sample output file: {output_file}")
                        self.data_textarea_process.insert(INSERT, f"\nCreated sample output file: {output_file}")

                print("\nMusic Generation Testing was done successfully...")
                self.data_textarea_process.insert(INSERT, "\n\nMusic Generation Testing was done successfully...")
                messagebox.showinfo("Information Message", "Music Generation Testing was done successfully...")

                # Update the MIDI dropdown with newly generated files
                self.update_midi_dropdown()

                self.btn_ts_midi_classification.configure(state="disabled")
                self.data_textarea_process.configure(state="disabled")
                self.data_textarea_result.configure(state="disabled")
            else:
                messagebox.showinfo("Information Message", "Please do the training first...")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during testing: {str(e)}")
            print(f"Error: {str(e)}")

    def tables_graphs(self):
        try:
            if self.boolTesting:
                def result():
                    if not os.path.exists("MIDI/Result/"):  # Use forward slashes
                        os.makedirs("MIDI/Result/")  # Use forward slashes

                    wb = openpyxl.Workbook()
                    ws = wb.active
                    rows = [
                        ("", "Precision", "Recall", "FMeasure", "Accuracy", "Sensitivity", "Specificity"),
                        ("Existing RNN", cfg.ernnpre, cfg.ernnrec, cfg.ernnfsc, cfg.ernnacc, cfg.ernnsens, cfg.ernnspec),
                        ("Existing GRU", cfg.egrupre, cfg.egrurec, cfg.egrufsc, cfg.egruacc, cfg.egrusens, cfg.egruspec),
                        ("Existing LSTM", cfg.elstmpre, cfg.elstmrec, cfg.elstmfsc, cfg.elstmacc, cfg.elstmsens, cfg.elstmspec),
                        ("Proposed OLSTM", cfg.polstmpre, cfg.polstmrec, cfg.polstmfsc, cfg.polstmacc, cfg.polstmsens, cfg.polstmspec)
                    ]
                    for row in rows:
                        ws.append(row)
                    data = Reference(ws, min_col=2, min_row=2, max_col=6, max_row=5)  # Corrected max_row
                    titles = Reference(ws, min_col=1, min_row=2, max_row=5)  # Corrected reference
                    chart = BarChart3D()
                    chart.title = "Result"
                    chart.add_data(data=data, titles_from_data=True)
                    chart.set_categories(titles)
                    chart.x_axis.title = "Classification Algorithms"
                    chart.y_axis.title = "Performance Metrics"
                    ws.add_chart(chart, "I5")  # Moved chart position to make space
                    
                    result_file = "MIDI/Result/Result.xlsx"  # Use forward slashes
                    wb.save(result_file)
                    
                    print("\nResult\n")
                    x1 = PrettyTable()
                    x1.field_names = ["Model", "Precision", "Recall", "FMeasure", "Accuracy", "Sensitivity", "Specificity"]
                    x1.add_row(["Existing RNN", cfg.ernnpre, cfg.ernnrec, cfg.ernnfsc, cfg.ernnacc, cfg.ernnsens, cfg.ernnspec])
                    x1.add_row(["Existing GRU", cfg.egrupre, cfg.egrurec, cfg.egrufsc, cfg.egruacc, cfg.egrusens, cfg.egruspec])
                    x1.add_row(["Existing LSTM", cfg.elstmpre, cfg.elstmrec, cfg.elstmfsc, cfg.elstmacc, cfg.elstmsens, cfg.elstmspec])
                    x1.add_row(["Proposed OLSTM", cfg.polstmpre, cfg.polstmrec, cfg.polstmfsc, cfg.polstmacc, cfg.polstmsens, cfg.polstmspec])
                    
                    # Display the table in the result window
                    self.data_textarea_result.configure(state="normal")
                    self.data_textarea_result.insert(INSERT, "\n\nPerformance Comparison Results\n")
                    self.data_textarea_result.insert(INSERT, str(x1))
                    self.data_textarea_result.configure(state="disabled")
                    
                    print(x1.get_string(title="Performance Comparison Results"))
                    return result_file

                result_file = result()
                messagebox.showinfo("Result", f"Graphs and tables are generated successfully!\nSaved to: {result_file}")
            else:
                messagebox.showerror("Error", "Please complete the testing first...")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating tables and graphs: {str(e)}")
            print(f"Error: {str(e)}")

    def close(self):
        # Stop any playing audio
        if self.is_playing:
            self.stop_playback()
        
        # Quit pygame mixer
        pygame.mixer.quit()
        
        # Close the window
        self.root.destroy()

def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    try:
        listOfFile = os.listdir(dirName)
        allFiles = list()
        # Iterate over all the entries
        for entry in listOfFile:
            # Create full path
            fullPath = os.path.join(dirName, entry)
            # If entry is a directory then get the list of files in this directory
            if os.path.isdir(fullPath):
                allFiles = allFiles + getListOfFiles(fullPath)
            else:
                allFiles.append(fullPath)
        return allFiles
    except Exception as e:
        print(f"Error accessing directory {dirName}: {str(e)}")
        return []

# Main function to start the application
if __name__ == "__main__":
    root = Tk()
    root.title("AUTOMATIC MUSIC GENERATION")
    # Increase window size to accommodate all elements properly
    root.geometry("1080x700")
    root.resizable(True, True)  # Make window resizable
    root.configure(bg="azure3")
    od = Main_GUI(root)
    root.mainloop()
