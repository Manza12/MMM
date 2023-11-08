from mmm import *
from mmm.spectrograms.layers import create_cqt_layer, apply_cqt_layer
from mmm.spectrograms.procedures.io import load_or_compute, take_excerpt
from mmm.spectrograms.plot import plot_cqt

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

x = take_excerpt(file_path, 2., 14.)

# Load STFT layer
objects_folder = data_folder / Path('objects')
cqt_layer = load_or_compute('cqt_layer', objects_folder, {'cqt_layer': True}, create_cqt_layer)

# Apply STFT layer
spectrogram_cqt = apply_cqt_layer(x, cqt_layer)
spectrogram_cqt_numpy = spectrogram_cqt.cpu().numpy()
np.save(str(output_folder / (name + '_spectrogram_cqt.npy')), spectrogram_cqt_numpy)

# Plot STFT
plot_cqt(spectrogram_cqt_numpy, cqt_layer, -120, 0, fig_size=(8., 4.))
plt.savefig(output_folder / (name + '_spectrogram_cqt.jpeg'))

plt.show()
