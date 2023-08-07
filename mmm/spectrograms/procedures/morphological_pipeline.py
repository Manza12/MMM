from ..processing import *
from ..procedures.io import load_or_compute


def apply_morphology_input(spectrograms, arrays_folder, load):
    spectrogram = spectrograms['input']

    print('\nMorphology - Input')

    # Reconstruction by erosion
    spectrogram_reconstruction_erosion = load_or_compute('reconstruction_erosion', arrays_folder, load,
                                                         lambda: apply_reconstruction_by_erosion(spectrogram))

    # Erosion
    spectrogram_erosion = load_or_compute('erosion', arrays_folder, load,
                                          lambda: apply_erosion(spectrogram_reconstruction_erosion))

    spectrograms['reconstruction_erosion'] = spectrogram_reconstruction_erosion
    spectrograms['erosion'] = spectrogram_erosion


def apply_morphology_noise(spectrograms, arrays_folder, load):
    print('\nMorphology - Noise')

    # Opening for get noise component
    spectrogram_opening = load_or_compute('opening', arrays_folder, load,
                                          lambda: apply_opening(spectrograms['erosion']))

    spectrograms['opening'] = spectrogram_opening


def apply_morphology_sinusoids(spectrograms, arrays_folder, load):
    # Sinusoids
    print('\nMorphology - Sinusoids')

    # Vertical Thinning
    spectrogram_vertical_thin = load_or_compute('vertical_thin', arrays_folder, load,
                                                lambda: apply_vertical_thinning(spectrograms['erosion']))

    # Vertical top-hat
    spectrogram_vertical_top_hat = load_or_compute('vertical_top_hat', arrays_folder, load,
                                                   lambda: apply_vertical_top_hat(spectrogram_vertical_thin))

    # Vertical threshold
    spectrogram_vertical_threshold = load_or_compute('vertical_threshold', arrays_folder, load,
                                                     lambda: apply_top_hat_threshold(
                                                         spectrograms['reconstruction_erosion'],
                                                         spectrogram_vertical_top_hat))

    # Remove small horizontal lines
    spectrogram_horizontal_filtered = load_or_compute('horizontal_filtered', arrays_folder, load,
                                                      lambda: remove_small_horizontal_lines(
                                                          spectrogram_vertical_threshold))

    spectrograms['vertical_thin'] = spectrogram_vertical_thin
    spectrograms['vertical_top_hat'] = spectrogram_vertical_top_hat
    spectrograms['vertical_threshold'] = spectrogram_vertical_threshold
    spectrograms['horizontal_filtered'] = spectrogram_horizontal_filtered


def apply_morphology_transient(spectrograms, arrays_folder, load):
    spectrogram_reconstruction_erosion = spectrograms['reconstruction_erosion']

    # Transient
    print('\nMorphology - Transient')

    # Horizontal Thinning
    spectrogram_horizontal_thin = load_or_compute('horizontal_thin', arrays_folder, load,
                                                  lambda: apply_horizontal_thinning(spectrogram_reconstruction_erosion))

    # Horizontal top-hat
    spectrogram_horizontal_top_hat = load_or_compute('horizontal_top_hat', arrays_folder, load,
                                                     lambda: apply_horizontal_top_hat(spectrogram_horizontal_thin))

    # Horizontal threshold
    spectrogram_horizontal_threshold = load_or_compute('horizontal_threshold', arrays_folder, load,
                                                       lambda: apply_top_hat_threshold(
                                                           spectrogram_reconstruction_erosion,
                                                           spectrogram_horizontal_top_hat))

    # Remove small vertical lines
    spectrogram_vertical_filtered = load_or_compute('vertical_filtered', arrays_folder, load,
                                                    lambda: remove_small_vertical_lines(
                                                        spectrogram_horizontal_threshold))

    spectrograms['horizontal_thin'] = spectrogram_horizontal_thin
    spectrograms['horizontal_top_hat'] = spectrogram_horizontal_top_hat
    spectrograms['horizontal_threshold'] = spectrogram_horizontal_threshold
    spectrograms['vertical_filtered'] = spectrogram_vertical_filtered


def apply_morphology(spectrograms, paths, load, components):
    if components['input']:
        apply_morphology_input(spectrograms, paths['arrays_folder'], load)
    if components['noise']:
        apply_morphology_noise(spectrograms, paths['arrays_folder'], load)
    if components['sinusoids']:
        apply_morphology_sinusoids(spectrograms, paths['arrays_folder'], load)
    if components['transient']:
        apply_morphology_transient(spectrograms, paths['arrays_folder'], load)
