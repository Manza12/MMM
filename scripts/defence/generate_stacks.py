import time

from mmm import *
from mmm.spectrograms.morphology import reconstruction_erosion_stack, greyscale_thinning_stack, \
    reconstruction_dilation, greyscale_trimming_stack
from mmm.spectrograms.parameters import TIME_RESOLUTION, FREQUENCY_PRECISION, MIN_LENGTH_SINUSOIDS

from mmm.spectrograms.procedures.io import save_pickle, load_or_compute
from mmm.spectrograms.procedures.morphological_pipeline import apply_morphology

# Parameters
start_full = time.time()
name = 'anastasia_excerpt'

generate = {
    'reconstruction_erosion': False,
    'vertical_thinning': False,
    'horizontal_thinning': False,
    'horizontal_trimming': True,
    'reconstruction_dilation': False,
}

components = {
    'input': True,
    'noise': True,
    'sinusoids': True,
    'transient': True,
    'output': True,
    'denoised': False,
}

load = {
    # Input
    'spectrogram': True,
    'closing': True,
    'reconstruction_erosion': True,
    'reconstruction_stack': True,

    # Noise
    'white_noise': True,
    'opening': True,
    'filtered_noise': True,

    # Sinusoids
    'vertical_thin': True,
    'vertical_top_hat': True,
    'vertical_threshold': True,

    'horizontal_filtered': False,
    'lines_sinusoids': False,
    'sinusoids': False,

    # Transient
    'horizontal_thin': True,
    'horizontal_top_hat': True,
    'horizontal_threshold': True,

    'vertical_filtered': False,
    'lines_transient': False,
    'transient': False,
}

# Paths
project_folder = Path('..') / Path('..')

data_folder = project_folder / Path('data')

audio_folder = data_folder / Path('audio')
objects_folder = data_folder / Path('objects')

results_folder = project_folder / Path('phd') / Path('defence') / Path('results')

output_folder = results_folder / Path(name + '_%dms_%dHz' % (TIME_RESOLUTION * 1000, FREQUENCY_PRECISION))

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

paths['objects_folder'].mkdir(parents=True, exist_ok=True)
paths['output_folder'].mkdir(parents=True, exist_ok=True)
paths['arrays_folder'].mkdir(parents=True, exist_ok=True)
paths['images_folder'].mkdir(parents=True, exist_ok=True)

# Load data
spectrogram = load_or_compute('spectrogram', paths['arrays_folder'], load, None)
spectrograms = {'input': spectrogram}
apply_morphology(spectrograms, paths, load, components, {})

# Create stacks

# Reconstruction erosion
if generate['reconstruction_erosion']:
    spectrogram_closing = spectrograms['closing']
    spectrogram_stack_reconstruction = reconstruction_erosion_stack(spectrogram_closing, spectrogram,
                                                                    max_iterations=100, verbose=True)
    file_path = arrays_folder / ('spectrogram_reconstruction_stack' + '.pickle')
    save_pickle(file_path, spectrogram_stack_reconstruction)

# Thinning
spectrogram_reconstruction = spectrograms['reconstruction_erosion']

# Vertical thinning
if generate['vertical_thinning']:
    spectrogram_stack_thinning = greyscale_thinning_stack(spectrogram_reconstruction, direction='v',
                                                          max_iterations=100, verbose=True)
    file_path = arrays_folder / ('spectrogram_vertical_thinning_stack' + '.pickle')
    save_pickle(file_path, spectrogram_stack_thinning)

# Horizontal thinning
if generate['horizontal_thinning']:
    spectrogram_stack_thinning = greyscale_thinning_stack(spectrogram_reconstruction, direction='h',
                                                          max_iterations=100, verbose=True)
    file_path = arrays_folder / ('spectrogram_horizontal_thinning_stack' + '.pickle')
    save_pickle(file_path, spectrogram_stack_thinning)

# Horizontal trimming
if generate['horizontal_trimming']:
    min_length_bins = int(MIN_LENGTH_SINUSOIDS / TIME_RESOLUTION)
    iterations = min_length_bins // 2

    spectrogram_vertical_threshold = spectrograms['vertical_threshold']
    spectrogram_trimming = greyscale_trimming_stack(spectrogram_vertical_threshold, iterations, 'h')

    file_path = arrays_folder / ('spectrogram_horizontal_trimming_stack' + '.pickle')
    save_pickle(file_path, spectrogram_trimming)

# Reconstruction by dilation
if generate['reconstruction_dilation']:
    spectrogram_trimming = spectrograms['trimming']
    spectrogram_reconstruction = reconstruction_dilation(spectrogram_trimming, spectrogram)

    file_path = arrays_folder / ('spectrogram_reconstruction_dilation_stack' + '.pickle')
    save_pickle(file_path, spectrogram_reconstruction)

# End
end_full = time.time()
print('Total time: %.3f s' % (end_full - start_full))
