from mmm import *
from mmm.spectrograms.layers import create_cqt_layer, apply_cqt_layer
from mmm.spectrograms.procedures.io import read_wav, load_or_compute, take_excerpt
from mmm.spectrograms.plot import plot_cqt
from mmm.pianorolls.music import TimeShift
from mmm.pianorolls.plot import plot_piano_roll
from mmm.pianorolls.midi import read_midi

# Parameters
phd = True
name = 'anastasia'

# Paths
project_folder = Path('..') / Path('..')

data_folder = project_folder / Path('data')

audio_folder = data_folder / Path('audio')
midi_folder = data_folder / Path('midi')

output_folder = project_folder / Path('phd') / Path('defence')
output_folder.mkdir(parents=True, exist_ok=True)

# Read wav file
print('Getting input...')

file_path = audio_folder / (name + '.wav')

x = take_excerpt(file_path, 3., 20.)

# Load STFT layer
objects_folder = data_folder / Path('objects')
cqt_layer = load_or_compute('cqt_layer', objects_folder, {'cqt_layer': True}, create_cqt_layer)

# Apply STFT layer
spectrogram_cqt = apply_cqt_layer(x, cqt_layer)
spectrogram_cqt_numpy = spectrogram_cqt.cpu().numpy()

# Read MIDI file
piano_roll = read_midi(midi_folder / (name + '.mid'))
piano_roll.change_tatum(TimeShift(1, 8), inplace=True)

# Plot STFT
plot_cqt(spectrogram_cqt_numpy, cqt_layer, -120, 0, fig_size=(8., 4.))
plt.savefig(output_folder / (name + '_spectrogram.jpeg'))

# Plot piano roll
plot_piano_roll(piano_roll, fig_size=(8. * 100, 4. * 100))
plt.savefig(output_folder / (name + '_pianoroll.jpeg'))

plt.show()
