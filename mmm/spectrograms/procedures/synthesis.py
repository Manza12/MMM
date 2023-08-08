from .. import *

from ..layers import apply_stft_layer
from ..synthesis import synthesize_noise_mask, synthesize_white_noise, synthesize_sinusoids, synthesize_transient
from ..processing import get_lines, filter_lines
from ..utils import get_duration, to_db

from .io import load_or_compute


def synthesize_noise_signal(signals, spectrograms, paths, load, stft_layer):
    print('\nSynthesis - Noise')

    n = signals['input'].size

    # White noise
    white_noise = load_or_compute('white_noise', paths['arrays_folder'], load, lambda: synthesize_white_noise(n))

    white_noise_stft = apply_stft_layer(white_noise, stft_layer, verbose=True, output_format='Complex',
                                        input_name='white noise')

    # Noise
    filtered_noise = load_or_compute('filtered_noise', paths['audio_folder'], load,
                                     lambda: synthesize_noise_mask(white_noise_stft, spectrograms['opening'],
                                                                   stft_layer, verbose=True),
                                     extension='.wav')

    signals['white_noise'] = white_noise
    signals['filtered_noise'] = filtered_noise

    spectrogram_white_noise = to_db(torch.sqrt(white_noise_stft[:, :, 0]**2 + white_noise_stft[:, :, 1]**2))
    spectrogram_filtered_noise = apply_stft_layer(filtered_noise, stft_layer, verbose=True, input_name='filtered noise')

    spectrograms['white_noise'] = spectrogram_white_noise
    spectrograms['filtered_noise'] = spectrogram_filtered_noise


def synthesize_sinusoids_signal(lines, signals, spectrograms, paths, load, stft_layer):
    print('\nSynthesis - Sinusoids')

    lines_sinusoids = load_or_compute('lines_sinusoids', paths['arrays_folder'], load,
                                      lambda: get_lines(spectrograms['horizontal_filtered'], 'time'))
    filtered_lines = filter_lines(lines_sinusoids, 1)
    lines['sinusoids'] = lines_sinusoids
    lines['filtered_sinusoids'] = filtered_lines

    sinusoids = load_or_compute('sinusoids', paths['audio_folder'], load,
                                lambda: synthesize_sinusoids(filtered_lines), extension='.wav')

    signals['sinusoids'] = sinusoids

    spectrogram_sinusoids = apply_stft_layer(sinusoids, stft_layer, verbose=True, input_name='sinusoids')

    spectrograms['sinusoids'] = spectrogram_sinusoids


def synthesize_transient_signal(lines, signals, spectrograms, paths, load, stft_layer):
    print('\nSynthesis - Transient')

    lines_transient = load_or_compute('lines_transient', paths['arrays_folder'], load,
                                      lambda: get_lines(spectrograms['vertical_filtered'], 'frequency'))
    filtered_lines = filter_lines(lines_transient, 0)
    lines['transient'] = lines_transient
    lines['filtered_transient'] = filtered_lines

    duration = get_duration(signals['input'])
    transient = load_or_compute('transient', paths['audio_folder'], load,
                                lambda: synthesize_transient(filtered_lines, duration), extension='.wav')

    signals['transient'] = transient

    spectrogram_transient = apply_stft_layer(transient, stft_layer, verbose=True, input_name='transient')

    spectrograms['transient'] = spectrogram_transient


def synthesize_output_signal(signals, spectrograms, stft_layer):
    filtered_noise = signals['filtered_noise']
    sinusoids = signals['sinusoids']
    transient = signals['transient']

    print('\nSynthesis - Output')
    output_size = max(len(filtered_noise), len(sinusoids), len(transient))

    output = np.zeros(output_size, dtype=np.float32)
    output[:filtered_noise.size] += filtered_noise
    output[:sinusoids.size] += sinusoids
    output[:transient.size] += transient

    signals['output'] = output

    spectrogram_output = apply_stft_layer(output, stft_layer, verbose=True, input_name='output')

    spectrograms['output'] = spectrogram_output


def synthesize_signals(lines, signals, spectrograms, paths, load, components, stft_layer):
    if components['noise']:
        synthesize_noise_signal(signals, spectrograms, paths, load, stft_layer)
    if components['sinusoids']:
        synthesize_sinusoids_signal(lines, signals, spectrograms, paths, load, stft_layer)
    if components['transient']:
        synthesize_transient_signal(lines, signals, spectrograms, paths, load, stft_layer)
    if components['output']:
        synthesize_output_signal(signals, spectrograms, stft_layer)
