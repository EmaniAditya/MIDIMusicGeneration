# Configuration settings for the MIDI Music Generation project

# Models
models = ["ernn", "egru", "elstm", "polstm"]

# Metrics for each model
# These will be updated during testing

# RNN
ernncm = [[0, 0], [0, 0]]  # Confusion matrix
ernnpre = 0.0  # Precision
ernnrec = 0.0  # Recall
ernnfsc = 0.0  # F-score
ernnacc = 0.0  # Accuracy
ernnsens = 0.0  # Sensitivity
ernnspec = 0.0  # Specificity

# GRU
egrucm = [[0, 0], [0, 0]]  # Confusion matrix
egrupre = 0.0  # Precision
egrurec = 0.0  # Recall
egrufsc = 0.0  # F-score
egruacc = 0.0  # Accuracy
egrusens = 0.0  # Sensitivity
egruspec = 0.0  # Specificity

# LSTM
elstmcm = [[0, 0], [0, 0]]  # Confusion matrix
elstmpre = 0.0  # Precision
elstmrec = 0.0  # Recall
elstmfsc = 0.0  # F-score
elstmacc = 0.0  # Accuracy
elstmsens = 0.0  # Sensitivity
elstmspec = 0.0  # Specificity

# Proposed O-LSTM
polstmcm = [[0, 0], [0, 0]]  # Confusion matrix
polstmpre = 0.0  # Precision
polstmrec = 0.0  # Recall
polstmfsc = 0.0  # F-score
polstmacc = 0.0  # Accuracy
polstmsens = 0.0  # Sensitivity
polstmspec = 0.0  # Specificity

# Paths
midi_dataset_path = "MIDI/Dataset/"
midi_files_path = "MIDI/MIDIFiles/"
models_path = "MIDI/Models/"
output_midi_path = "MIDI/Output/MIDI/"
output_mp3_path = "MIDI/Output/MP3/"
result_path = "MIDI/Result/"

# Training parameters
batch_size = 64
epochs = 100
validation_split = 0.2
