from mmm import *
from mmm.spectrograms.layers import create_stft_layer, apply_stft_layer
from mmm.spectrograms.procedures.io import take_excerpt, load_or_compute
from mmm.spectrograms.plot import plot_stft
from mmm.spectrograms.parameters import TIME_RESOLUTION, FREQUENCY_PRECISION, WINDOW, MIN_DB

# Parameters
name = 'thank_you'

# Paths
project_folder = Path('..') / Path('..') / Path('..')

data_folder = project_folder / Path('data')

audio_folder = Path('.')

# Read wav file
print('Getting input...')

file_path = audio_folder / (name + '.wav')

x = take_excerpt(file_path, 0., None)

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
plot_stft(spectrogram_stft_numpy, MIN_DB, 0, fig_size=(16., 9.), c_map='afmhot', cb=False)
# plt.xlim(0 / TIME_RESOLUTION, 3 / TIME_RESOLUTION)
plt.ylim(0 / FREQUENCY_PRECISION, 18000 / FREQUENCY_PRECISION)
plt.axis('off')
plt.savefig(audio_folder / (name + '_stft.svg'), bbox_inches='tight', pad_inches=0)

plt.show()
