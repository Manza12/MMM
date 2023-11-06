from mmm import *
from mmm.spectrograms.layers import create_stft_layer, apply_stft_layer
from mmm.spectrograms.procedures.io import take_excerpt, load_or_compute
from mmm.spectrograms.plot import plot_stft
from mmm.spectrograms.parameters import TIME_RESOLUTION, FREQUENCY_PRECISION, WINDOW

# Parameters
name = 'anastasia'

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

x = take_excerpt(file_path, 3., 9.)

# Load STFT layer
objects_folder = data_folder / Path('objects')
layer_name = 'stft_layer_' + \
             str(int(TIME_RESOLUTION * 1000)) + '_ms_' + \
             str(int(FREQUENCY_PRECISION)) + '_Hz_' + \
             str(WINDOW)
stft_layer = load_or_compute(layer_name, objects_folder, {'stft_layer': True}, create_stft_layer)

# Apply STFT layer
spectrogram_stft = apply_stft_layer(x, stft_layer)
spectrogram_stft_numpy = spectrogram_stft.cpu().numpy()

# Plot STFT
plot_stft(spectrogram_stft_numpy, -120, 0, fig_size=(6., 4.))

plt.show()
