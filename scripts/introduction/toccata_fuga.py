from mmm import *
from mmm.pianorolls.music import TimeShift
from mmm.pianorolls.plot import plot_piano_roll
from mmm.spectrograms.layers import create_stft_layer, apply_stft_layer
from mmm.spectrograms.procedures.io import read_wav
from mmm.spectrograms.plot import plot_stft
from mmm.pianorolls.midi import read_midi_seconds

# Parameters
phd = True
name = 'toccata_fuga'

# Paths
project_folder = Path('..') / Path('..')

data_folder = project_folder / Path('data')

audio_folder = data_folder / Path('audio')
midi_folder = data_folder / Path('midi')

output_folder = project_folder / Path('phd') / Path('introduction')
output_folder.mkdir(parents=True, exist_ok=True)

# Read wav file
print('Getting input...')

file_path = audio_folder / (name + '.wav')

x = read_wav(file_path)

# Create STFT layer
stft_layer = create_stft_layer()

# Apply STFT layer
spectrogram = apply_stft_layer(x, stft_layer)
spectrogram_numpy = spectrogram.cpu().numpy()
spectrogram_numpy = spectrogram_numpy[:500, :]

# Read MIDI file
piano_rolls = read_midi_seconds(midi_folder / (name + '.mid'))
piano_roll = piano_rolls[0]
for pr in piano_rolls[1:]:
    piano_roll += pr
piano_roll.change_tatum(TimeShift(1, 10), inplace=True)

# Plot STFT
plot_stft(spectrogram_numpy, -120, 0, fig_size=(8., 4.))
plt.savefig(output_folder / (name + '_spectrogram.pdf'))

# Plot piano roll
plot_piano_roll(piano_roll, fig_size=(8. * 100, 4. * 100))
plt.savefig(output_folder / (name + '_piano_roll.pdf'))

plt.show()
