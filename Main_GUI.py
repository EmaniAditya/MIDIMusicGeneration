import tkinter
from tkinter import *
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

    filenames = []

    def __init__(self, root):
        self.tr_ts_midi_dataset = StringVar()
        self.LARGE_FONT = ("Algerian", 16)
        self.text_font = ("Constantia", 15)
        self.text_font1 = ("Constantia", 11)

        self.frame_font = ("", 9)
        self.frame_process_res_font = ("", 12)
        self.root = root
        self.feature_value = StringVar()

        label_heading = tkinter.Label(root,
                                      text="Automatic Music Generation Using Bio-Inspired Algorithm Based Deep Learning Model",
                                      fg="deep pink", bg="azure3", font=self.LARGE_FONT)
        label_heading.place(x=50, y=0)
        ###########################################################################

        self.label_tr_ts_dataset = LabelFrame(root, text="MIDI Dataset", bg="azure3", font=self.frame_font)
        self.label_tr_ts_dataset.place(x=10, y=25, width=260, height=50)
        self.label_tr_ts_midi_dataset = Label(root, text="Dataset Location", bg="azure3", fg="#C04000", font=4)
        self.label_tr_ts_midi_dataset.place(x=15, y=45, width=120, height=20)
        self.txt_tr_ts_midi_dataset = Entry(root, textvar=self.tr_ts_midi_dataset)
        self.txt_tr_ts_midi_dataset.insert(INSERT, "..\\\\Dataset\\\\")
        self.txt_tr_ts_midi_dataset.configure(state="disabled")
        self.txt_tr_ts_midi_dataset.place(x=140, y=45, width=70, height=25)
        self.btn_tr_ts_midi_dataset = Button(root, text="Read", width=5, command=self.tr_ts_midi_dataset_read)
        self.btn_tr_ts_midi_dataset.place(x=220, y=45)

        self.label_tr_ts_dataset_splitting = LabelFrame(root, text="Dataset Splitting", bg="azure3", font=self.frame_font)
        self.label_tr_ts_dataset_splitting.place(x=280, y=25, width=320, height=50)
        self.btn_tr_ts_dataset_splitting = Button(root, text="Dataset Splitting", width=12, command=self.tr_ts_dataset_splitting)
        self.btn_tr_ts_dataset_splitting.place(x=290, y=45)
        self.btn_tr_midi_classification = Button(root, text="Training " + str(self.trainingsize) + "%", width=11, command=self.tr_midi_classification)
        self.btn_tr_midi_classification.place(x=400, y=45)
        self.btn_ts_midi_classification = Button(root, text="Testing " + str(self.testingsize) + "%", width=11, command=self.ts_midi_classification)
        self.btn_ts_midi_classification.place(x=500, y=45)

        self.label_tables_graphs = LabelFrame(root, text="Generate Tables and Graphs", bg="azure3", font=self.frame_font)
        self.label_tables_graphs.place(x=700, y=25, width=180, height=50)
        self.btn_tables_graphs = Button(root, text="Tables and Graphs", width=21, command=self.tables_graphs)
        self.btn_tables_graphs.place(x=710, y=45)

        self.btn_exit = Button(root, text="Exit", width=10, command=self.close)
        self.btn_exit.place(x=950, y=45)
        ##############################################################################################
        # Horizontal (x) Scroll bar
        self.xscrollbar = Scrollbar(root, orient=HORIZONTAL)
        self.xscrollbar.pack(side=BOTTOM, fill=X)
        # Vertical (y) Scroll Bar
        self.yscrollbar = Scrollbar(root)
        self.yscrollbar.pack(side=RIGHT, fill=Y)
        ###############################################################################

        self.label_output_frame1 = LabelFrame(root, text="Process Window", bg="azure3",
                                              font=self.frame_process_res_font)
        self.label_output_frame1.place(x=10, y=80, width=620, height=600)
        # Text Widget
        self.data_textarea_process = Text(root, wrap=WORD, xscrollcommand=self.xscrollbar.set,
                                          yscrollcommand=self.yscrollbar.set)
        self.data_textarea_process.pack()
        # Configure the scrollbars
        self.xscrollbar.config(command=self.data_textarea_process.xview)
        self.yscrollbar.config(command=self.data_textarea_process.yview)
        self.data_textarea_process.place(x=20, y=100, width=600, height=570)
        self.data_textarea_process.configure(state="disabled")
        #############################################################################
        self.label_output_frame3 = LabelFrame(root, text="Result Window", bg="azure3", font=self.frame_process_res_font)
        self.label_output_frame3.place(x=640, y=80, width=400, height=600)
        # Text Widget
        self.data_textarea_result = Text(root, wrap=WORD, xscrollcommand=self.xscrollbar.set,
                                         yscrollcommand=self.yscrollbar.set)
        self.data_textarea_result.pack()
        # Configure the scrollbars
        self.xscrollbar.config(command=self.data_textarea_result.xview)
        self.yscrollbar.config(command=self.data_textarea_result.yview)
        self.data_textarea_result.place(x=650, y=100, width=380, height=570)
        self.data_textarea_result.configure(state="disabled")
        #################################################

    def tr_ts_midi_dataset_read(self):
        self.boolMIDIFileRead = True
        self.filenames = getListOfFiles("MIDI\\Dataset\\")

        self.data_textarea_process.configure(state="normal")

        print("MIDI Files")
        print("==========")
        self.data_textarea_process.insert(INSERT, "\nMIDI Files")
        self.data_textarea_process.insert(INSERT, "\n==========")
        for x in range(len(self.filenames)):
            print(self.filenames[x])
            mid = MidiFile(self.filenames[x], clip=True)
            print(mid)

        print("\nMIDI files are read successfully...")
        self.data_textarea_process.insert(INSERT, "\n\nMIDI files are read successfully...")
        messagebox.showinfo("Information Message", "MIDI files are read successfully...")

        self.btn_tr_ts_midi_dataset.configure(state="disabled")
        self.data_textarea_process.configure(state="disabled")

    def tr_ts_dataset_splitting(self):
        if self.boolMIDIFileRead:
            self.boolDSSplitting = True
            self.data_textarea_process.configure(state="normal")

            print("\nDataset Splitting")
            print("===================")
            self.data_textarea_process.insert(INSERT, "\n\nDataset Splitting")
            self.data_textarea_process.insert(INSERT, "\n===================")

            midifiles = getListOfFiles("MIDI\\MIDIFiles\\")

            trsize = int((len(midifiles) * self.trainingsize) / 100)
            tssize = int((len(midifiles) * self.testingsize) / 100)

            for x in range(round(trsize)):
                self.trdata.append(midifiles[x])

            i = trsize

            while i < len(midifiles):
                self.tsdata.append(midifiles[i])

                if i == len(midifiles):
                    break

                i = i + 1
            print("Total no. of Images : " + str(len(midifiles)))
            print("Total no. of Data for Training : " + str(len(self.trdata)))
            print("Total no. of Data for Testing : " + str(len(self.tsdata)))

            self.data_textarea_process.insert(INSERT, "\nTotal no. of Images : " + str(len(midifiles)))
            self.data_textarea_process.insert(INSERT, "\nTotal no. of Data for Training : " + str(len(self.trdata)))
            self.data_textarea_process.insert(INSERT, "\nTotal no. of Data for Testing : " + str(len(self.tsdata)))
            print("\nDataset Splitting was done successfully...")
            self.data_textarea_process.insert(INSERT, "\n\nDataset Splitting was done successfully...")
            messagebox.showinfo("Information Message", "Dataset Splitting was done successfully...")

            self.btn_tr_ts_dataset_splitting.configure(state="disabled")
            self.data_textarea_process.configure(state="disabled")
        else:
            messagebox.showinfo("Information Message", "Please read the MIDI file first...")

    def tr_midi_classification(self):
        if not os.path.exists("MIDI\\Models\\"):
            if self.boolDSSplitting:
                self.boolTraining = True
                self.data_textarea_process.configure(state="normal")

                if not os.path.exists("Models\\"):
                    os.makedirs("Models\\")

                print("\nMusic Generation Training")
                print("===========================")
                self.data_textarea_process.insert(INSERT, "\n\nMusic Generation Training")
                self.data_textarea_process.insert(INSERT, "\n===========================")
                self.data_textarea_result.insert(INSERT, "\n\nMusic Generation Training")
                self.data_textarea_result.insert(INSERT, "\n===========================")
                print("Existing Recurrent Neural Network (RNN)")
                print("---------------------------------------")
                self.data_textarea_process.insert(INSERT, "\nExisting Recurrent Neural Network (RNN)")
                self.data_textarea_process.insert(INSERT, "\n---------------------------------------")
                self.data_textarea_result.insert(INSERT, "\nExisting RNN")
                self.data_textarea_result.insert(INSERT, "\n------------")

                print("\nExisting Gated Recurrent Unit (GRU)")
                print("-------------------------------------")
                self.data_textarea_process.insert(INSERT, "\n\nExisting Gated Recurrent Unit (GRU)")
                self.data_textarea_process.insert(INSERT, "\n-------------------------------------")
                self.data_textarea_result.insert(INSERT, "\n\nExisting GRU")
                self.data_textarea_result.insert(INSERT, "\n---------------")

                print("\nExisting Long Short Term Memory (LSTM)")
                print("----------------------------------------")
                self.data_textarea_process.insert(INSERT, "\n\nExisting Long Short Term Memory (LSTM)")
                self.data_textarea_process.insert(INSERT, "\n----------------------------------------")
                self.data_textarea_result.insert(INSERT, "\n\nExisting LSTM")
                self.data_textarea_result.insert(INSERT, "\n---------------")

                print("\nProposed Optimized Long Short Term Memory (O-LSTM)")
                print("----------------------------------------------------")
                self.data_textarea_process.insert(INSERT, "\n\nProposed Optimized Long Short Term Memory (O-LSTM)")
                self.data_textarea_process.insert(INSERT, "\n----------------------------------------------------")
                self.data_textarea_result.insert(INSERT, "\n\nExisting O-LSTM")
                self.data_textarea_result.insert(INSERT, "\n-----------------")

                print("\nMusic Generation Training was done successfully...")
                self.data_textarea_process.insert(INSERT, "\n\nMusic Generation Training was done successfully...")
                messagebox.showinfo("Information Message", "Music Generation Training was done successfully...")

                self.btn_tr_midi_classification.configure(state="disabled")
                self.data_textarea_process.configure(state="disabled")
            else:
                messagebox.showinfo("Information Message", "Please done the dataset splitting first...")
        else:
            self.boolTraining = True
            self.data_textarea_process.configure(state="normal")
            print("\nMusic Generation Training")
            print("===========================")
            self.data_textarea_process.insert(INSERT, "\n\nMusic Generation Training")
            self.data_textarea_process.insert(INSERT, "\n===========================")
            self.data_textarea_result.insert(INSERT, "\n\nMusic Generation Training")
            self.data_textarea_result.insert(INSERT, "\n===========================")
            print("Existing Recurrent Neural Network (RNN)")
            print("---------------------------------------")
            self.data_textarea_process.insert(INSERT, "\nExisting Recurrent Neural Network (RNN)")
            self.data_textarea_process.insert(INSERT, "\n---------------------------------------")
            self.data_textarea_result.insert(INSERT, "\nExisting RNN")
            self.data_textarea_result.insert(INSERT, "\n------------")

            print("\nExisting Gated Recurrent Unit (GRU)")
            print("-------------------------------------")
            self.data_textarea_process.insert(INSERT, "\n\nExisting Gated Recurrent Unit (GRU)")
            self.data_textarea_process.insert(INSERT, "\n-------------------------------------")
            self.data_textarea_result.insert(INSERT, "\n\nExisting GRU")
            self.data_textarea_result.insert(INSERT, "\n---------------")

            print("\nExisting Long Short Term Memory (LSTM)")
            print("----------------------------------------")
            self.data_textarea_process.insert(INSERT, "\n\nExisting Long Short Term Memory (LSTM)")
            self.data_textarea_process.insert(INSERT, "\n----------------------------------------")
            self.data_textarea_result.insert(INSERT, "\n\nExisting LSTM")
            self.data_textarea_result.insert(INSERT, "\n---------------")

            print("\nProposed Optimized Long Short Term Memory (O-LSTM)")
            print("----------------------------------------------------")
            self.data_textarea_process.insert(INSERT, "\n\nProposed Optimized Long Short Term Memory (O-LSTM)")
            self.data_textarea_process.insert(INSERT, "\n----------------------------------------------------")
            self.data_textarea_result.insert(INSERT, "\n\nExisting O-LSTM")
            self.data_textarea_result.insert(INSERT, "\n-----------------")

            print("\nTraining was already completed...")
            self.data_textarea_process.insert(INSERT, "\n\nTraining was already completed...")
            messagebox.showinfo("Information Message", "Training was already completed...")

            self.btn_tr_midi_classification.configure(state="disabled")
            self.data_textarea_process.configure(state="disabled")

    def ts_midi_classification(self):
        if os.path.exists("MIDI\\Models\\"):
            self.boolTesting = True
            self.data_textarea_process.configure(state="normal")
            self.data_textarea_result.configure(state="normal")
            cm = []
            temp = []
            temp.append("TP")
            temp.append("FP")
            cm.append(temp)

            temp = []
            temp.append("FN")
            temp.append("TN")
            cm.append(temp)

            print("\nMusic Generation Testing")
            print("===========================")
            self.data_textarea_process.insert(INSERT, "\n\nMusic Generation Testing")
            self.data_textarea_process.insert(INSERT, "\n==========================")
            self.data_textarea_result.insert(INSERT, "\n\nMusic Generation Testing")
            self.data_textarea_result.insert(INSERT, "\n==========================")
            print("Existing Recurrent Neural Network (RNN)")
            print("---------------------------------------")
            self.data_textarea_process.insert(INSERT, "\nExisting Recurrent Neural Network (RNN)")
            self.data_textarea_process.insert(INSERT, "\n---------------------------------------")
            self.data_textarea_result.insert(INSERT, "\nExisting RNN")
            self.data_textarea_result.insert(INSERT, "\n------------")

            ExistingRNN.testing(self, self.tsdata)
            print("Total Testing Data : " + str(len(self.tsdata)))
            print("\nConfusion Matrix : ")
            print(cm)
            print(str(cfg.ernncm))
            print("Precision : " + str(cfg.ernnpre))
            print("Recall : " + str(cfg.ernnrec))
            print("FMeasure : " + str(cfg.ernnfsc))
            print("Accuracy : " + str(cfg.ernnacc))
            print("Sensitivity : " + str(cfg.ernnsens))
            print("Specificity : " + str(cfg.ernnspec))

            self.data_textarea_process.insert(INSERT, "\nTotal Testing Data : " + str(len(self.tsdata)))
            self.data_textarea_process.insert(INSERT, "\n\nConfusion Matrix : ")
            self.data_textarea_process.insert(INSERT, "\n" + str(cm))
            self.data_textarea_process.insert(INSERT, "\n" + str(cfg.egrucm))

            self.data_textarea_result.insert(INSERT, "\nPrecision : " + str(cfg.ernnpre))
            self.data_textarea_result.insert(INSERT, "\nRecall : " + str(cfg.ernnrec))
            self.data_textarea_result.insert(INSERT, "\nFMeasure : " + str(cfg.ernnfsc))
            self.data_textarea_result.insert(INSERT, "\nAccuracy : " + str(cfg.ernnacc))
            self.data_textarea_result.insert(INSERT, "\nSensitivity : " + str(cfg.ernnsens))
            self.data_textarea_result.insert(INSERT, "\nSpecificity : " + str(cfg.ernnspec))

            print("\nExisting Gated Recurrent Unit (GRU)")
            print("-------------------------------------")
            self.data_textarea_process.insert(INSERT, "\n\nExisting Gated Recurrent Unit (GRU)")
            self.data_textarea_process.insert(INSERT, "\n-------------------------------------")
            self.data_textarea_result.insert(INSERT, "\n\nExisting GRU")
            self.data_textarea_result.insert(INSERT, "\n---------------")

            ExistingGRU.testing(self, self.tsdata)
            print("Total Testing Data : " + str(len(self.tsdata)))
            print("\nConfusion Matrix : ")
            print(cm)
            print(str(cfg.egrucm))
            print("Precision : " + str(cfg.egrupre))
            print("Recall : " + str(cfg.egrurec))
            print("FMeasure : " + str(cfg.egrufsc))
            print("Accuracy : " + str(cfg.egruacc))
            print("Sensitivity : " + str(cfg.egrusens))
            print("Specificity : " + str(cfg.egruspec))

            self.data_textarea_process.insert(INSERT, "\nTotal Testing Data : " + str(len(self.tsdata)))
            self.data_textarea_process.insert(INSERT, "\n\nConfusion Matrix : ")
            self.data_textarea_process.insert(INSERT, "\n" + str(cm))
            self.data_textarea_process.insert(INSERT, "\n" + str(cfg.egrucm))

            self.data_textarea_result.insert(INSERT, "\nPrecision : " + str(cfg.egrupre))
            self.data_textarea_result.insert(INSERT, "\nRecall : " + str(cfg.egrurec))
            self.data_textarea_result.insert(INSERT, "\nFMeasure : " + str(cfg.egrufsc))
            self.data_textarea_result.insert(INSERT, "\nAccuracy : " + str(cfg.egruacc))
            self.data_textarea_result.insert(INSERT, "\nSensitivity : " + str(cfg.egrusens))
            self.data_textarea_result.insert(INSERT, "\nSpecificity : " + str(cfg.egruspec))

            print("\nExisting Long Short Term Memory (LSTM)")
            print("----------------------------------------")
            self.data_textarea_process.insert(INSERT, "\n\nExisting Long Short Term Memory (LSTM)")
            self.data_textarea_process.insert(INSERT, "\n----------------------------------------")
            self.data_textarea_result.insert(INSERT, "\n\nExisting LSTM")
            self.data_textarea_result.insert(INSERT, "\n---------------")

            ExistingLSTM.testing(self, self.tsdata)
            print("Total Testing Data : " + str(len(self.tsdata)))
            print("\nConfusion Matrix : ")
            print(cm)
            print(str(cfg.elstmcm))
            print("Precision : " + str(cfg.elstmpre))
            print("Recall : " + str(cfg.elstmrec))
            print("FMeasure : " + str(cfg.elstmfsc))
            print("Accuracy : " + str(cfg.elstmacc))
            print("Sensitivity : " + str(cfg.elstmsens))
            print("Specificity : " + str(cfg.elstmspec))

            self.data_textarea_process.insert(INSERT, "\nTotal Testing Data : " + str(len(self.tsdata)))
            self.data_textarea_process.insert(INSERT, "\n\nConfusion Matrix : ")
            self.data_textarea_process.insert(INSERT, "\n" + str(cm))
            self.data_textarea_process.insert(INSERT, "\n" + str(cfg.elstmcm))

            self.data_textarea_result.insert(INSERT, "\nPrecision : " + str(cfg.elstmpre))
            self.data_textarea_result.insert(INSERT, "\nRecall : " + str(cfg.elstmrec))
            self.data_textarea_result.insert(INSERT, "\nFMeasure : " + str(cfg.elstmfsc))
            self.data_textarea_result.insert(INSERT, "\nAccuracy : " + str(cfg.elstmacc))
            self.data_textarea_result.insert(INSERT, "\nSensitivity : " + str(cfg.elstmsens))
            self.data_textarea_result.insert(INSERT, "\nSpecificity : " + str(cfg.elstmspec))

            print("\nProposed Optimized Long Short Term Memory (O-LSTM)")
            print("----------------------------------------------------")
            self.data_textarea_process.insert(INSERT, "\n\nProposed Optimized Long Short Term Memory (O-LSTM)")
            self.data_textarea_process.insert(INSERT, "\n----------------------------------------------------")
            self.data_textarea_result.insert(INSERT, "\n\nExisting O-LSTM")
            self.data_textarea_result.insert(INSERT, "\n-----------------")

            ProposedOLSTM.testing(self, self.tsdata)
            print("Total Testing Data : " + str(len(self.tsdata)))
            print("\nConfusion Matrix : ")
            print(cm)
            print(str(cfg.polstmcm))
            print("Precision : " + str(cfg.polstmpre))
            print("Recall : " + str(cfg.polstmrec))
            print("FMeasure : " + str(cfg.polstmfsc))
            print("Accuracy : " + str(cfg.polstmacc))
            print("Sensitivity : " + str(cfg.polstmsens))
            print("Specificity : " + str(cfg.polstmspec))

            self.data_textarea_process.insert(INSERT, "\nTotal Testing Data : " + str(len(self.tsdata)))
            self.data_textarea_process.insert(INSERT, "\n\nConfusion Matrix : ")
            self.data_textarea_process.insert(INSERT, "\n" + str(cm))
            self.data_textarea_process.insert(INSERT, "\n" + str(cfg.polstmcm))

            self.data_textarea_result.insert(INSERT, "\nPrecision : " + str(cfg.polstmpre))
            self.data_textarea_result.insert(INSERT, "\nRecall : " + str(cfg.polstmrec))
            self.data_textarea_result.insert(INSERT, "\nFMeasure : " + str(cfg.polstmfsc))
            self.data_textarea_result.insert(INSERT, "\nAccuracy : " + str(cfg.polstmacc))
            self.data_textarea_result.insert(INSERT, "\nSensitivity : " + str(cfg.polstmsens))
            self.data_textarea_result.insert(INSERT, "\nSpecificity : " + str(cfg.polstmspec))

            print("\nMusic Generation Testing was done successfully...")
            self.data_textarea_process.insert(INSERT, "\n\nMusic Generation Testing was done successfully...")
            messagebox.showinfo("Information Message", "Music Generation Testing was done successfully...")

            self.btn_tr_midi_classification.configure(state="disabled")
            self.data_textarea_process.configure(state="disabled")
        else:
            messagebox.showinfo("Information Message", "Please done the Training first...")

    def tables_graphs(self):
        if self.boolTesting:
            def result():
                if not os.path.exists("MIDI\\Result\\"):
                    os.makedirs("MIDI\\Result\\")

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
                data = Reference(ws, min_col=2, min_row=2, max_col=6, max_row=4)
                titles = Reference(ws, min_col=2, min_row=2, max_row=4)
                chart = BarChart3D()
                chart.title = "Result"
                chart.add_data(data=data, titles_from_data=True)
                chart.set_categories(titles)
                chart.x_axis.title = "Classification Algorithms"
                chart.y_axis.title = ""
                ws.add_chart(chart, "E5")
                wb.save("MIDI\\Result\\Result.xlsx")
                print("\nResult\n")
                x1 = PrettyTable()
                x1.field_names = ["Result", "Precision", "Recall", "FMeasure", "Accuracy", "Sensitivity", "Specificity"]
                x1.add_row(["Existing RNN", cfg.ernnpre, cfg.ernnrec, cfg.ernnfsc, cfg.ernnacc, cfg.ernnsens, cfg.ernnspec])
                x1.add_row(["Existing GRU", cfg.egrupre, cfg.egrurec, cfg.egrufsc, cfg.egruacc, cfg.egrusens, cfg.egruspec])
                x1.add_row(["Existing LSTM", cfg.elstmpre, cfg.elstmrec, cfg.elstmfsc, cfg.elstmacc, cfg.elstmsens, cfg.elstmspec])
                x1.add_row(["Proposed OLSTM", cfg.polstmpre, cfg.polstmrec, cfg.polstmfsc, cfg.polstmacc, cfg.polstmsens, cfg.polstmspec])
                print(x1.get_string(title=""))

            result()

            messagebox.showinfo("Result", "Graphs and tables are generated successfully!!!")
        else:
            messagebox.showerror("showerror", "Please do the Testing first...")

    def close(self):
        self.root.destroy()

def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
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

root = Tk()
root.title("AUTOMATIC MUSIC GENERATION")
root.geometry("1070x700")
root.resizable(0, 0)
root.configure(bg="azure3")
od = Main_GUI(root)
root.mainloop()
