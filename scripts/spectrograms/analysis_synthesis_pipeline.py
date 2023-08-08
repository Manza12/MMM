import sys

from mmm import *
from mmm.spectrograms.layers import create_stft_layer, apply_stft_layer

from mmm.spectrograms.procedures.io import load_or_compute, write_signals, read_wav
from mmm.spectrograms.procedures.morphological_pipeline import apply_morphology
from mmm.spectrograms.procedures.plot_pipeline import plot_phd, plot_all
from mmm.spectrograms.procedures.synthesis import synthesize_signals


# Parameters
phd = True
name = 'piano'

components = {
    'input': True,
    'noise': True,
    'sinusoids': True,
    'transient': True,
    'output': True,
}

operations = {
    'processing': True,
    'synthesis': True,
    'signals': True,
    'plots': True,
}

load = {
    # STFT Layer
    'stft_layer': True,

    # Input
    'spectrogram': True,
    'reconstruction_erosion': True,
    'erosion': True,

    # Noise
    'white_noise': True,
    'opening': True,
    'filtered_noise': True,

    # Sinusoids
    'erosion_reconstruction': True,
    'vertical_thin': True,
    'vertical_top_hat': True,
    'vertical_threshold': True,
    'horizontal_filtered': True,
    'lines_sinusoids': True,
    'sinusoids': True,

    # Transient
    'horizontal_thin': True,
    'horizontal_top_hat': True,
    'horizontal_threshold': True,
    'vertical_filtered': True,
    'lines_transient': True,
    'transient': True,
}

plot = {
    # Input
    'input': True,
    'reconstruction_erosion': False,
    'erosion': False,

    # Noise
    'opening': False,
    'white_noise': False,
    'filtered_noise': False,
    'input_noise': True,

    # Sinusoids
    'erosion_reconstruction': False,
    'vertical_thin': False,
    'vertical_top_hat': False,
    'vertical_threshold': False,
    'horizontal_filtered': False,
    'horizontal_link': False,
    'lines_sinusoids': True,
    'input_sinusoids': True,

    # Transient
    'horizontal_thin': False,
    'horizontal_top_hat': False,
    'horizontal_threshold': False,
    'vertical_filtered': False,
    'lines_transient': True,
    'input_transient': True,

    # Output
    'input_output': True,
}

# Paths
project_folder = Path('..') / Path('..')

data_folder = project_folder / Path('data')

audio_folder = data_folder / Path('audio')
objects_folder = data_folder / Path('objects')

results_folder = project_folder / Path('phd') / Path('chapter_3') / Path('music_instruments')

output_folder = results_folder / Path(name)

arrays_folder = output_folder / Path('arrays')
images_folder = output_folder / Path('images')

paths = {
    'project_folder': project_folder,
    'results_folder': results_folder,
    'output_folder': output_folder,
    'arrays_folder': arrays_folder,
    'images_folder': images_folder,
    'audio_folder': audio_folder,
    'objects_folder': objects_folder,
}

paths['output_folder'].mkdir(parents=True, exist_ok=True)
paths['arrays_folder'].mkdir(parents=True, exist_ok=True)
paths['images_folder'].mkdir(parents=True, exist_ok=True)

# Log
log = False
if log:
    log_path = paths['output_folder'] / 'log.txt'
    sys.stdout = open(log_path, 'w')

# Start
start_full = time.time()
print('Analyzing ' + name + '...\n')

# Read wav file
print('Getting input...')

paths['file_path'] = paths['audio_folder'] / (name + '.wav')

x = read_wav(paths['file_path'])

# Create STFT layer
stft_layer = load_or_compute('stft_layer', paths['objects_folder'], load, create_stft_layer)

# Apply STFT layer
spectrogram = load_or_compute('spectrogram', paths['arrays_folder'], load, lambda: apply_stft_layer(x, stft_layer))

# Morphology
spectrograms = {'input': spectrogram}
if operations['processing']:
    print('\nProcessing...')
    apply_morphology(spectrograms, paths, load, components)

# Synthesis
signals = {'input': x}
lines = {}
if operations['synthesis']:
    print('\nSynthesis...')
    synthesize_signals(lines, signals, spectrograms, paths, load, components, stft_layer)

    # Write signals
    write_signals(signals, paths, components)

# End
end_full = time.time()
print('Total time: %.3f s' % (end_full - start_full))
sys.stdout.close()

# Plots
if operations['plots']:
    if phd:
        from mmm.spectrograms.phd_settings import settings
        plot_phd(lines, spectrograms, plot, components, paths, settings[name])
    else:
        plot_all(lines, signals, spectrograms, plot, components, paths)
