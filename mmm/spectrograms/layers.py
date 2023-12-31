from . import *
from .utils import to_db
from .parameters import *


def create_stft_layer(verbose=False):
    if verbose:
        print('Creating STFT layer...')
    start = time.time()
    stft_layer = stft.STFT(n_fft=N_FFT,
                           win_length=WIN_LENGTH,
                           hop_length=HOP_LENGTH,
                           window=WINDOW,
                           freq_scale=FREQ_SCALE,
                           center=CENTER,
                           pad_mode=PAD_MODE,
                           iSTFT=True,
                           sr=FS,
                           trainable=False,
                           output_format=OUTPUT_FORMAT,
                           verbose=False).to(DEVICE)
    stft_layer.fs = FS
    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to create STFT layer: %.3f seconds' % (time.time() - start))

    return stft_layer


def apply_stft_layer(signal, stft_layer, verbose=True, output_format='Magnitude', input_name='signal'):
    # Apply to signal
    signal_tensor = torch.tensor(signal, device=DEVICE, dtype=torch.float32)

    start = time.time()
    spectrogram_complex = stft_layer(signal_tensor)
    if output_format == 'Magnitude':
        spectrogram = torch.sqrt(spectrogram_complex[0, :, :, 0]**2 + spectrogram_complex[0, :, :, 1]**2)
        spectrogram = to_db(spectrogram)
    else:
        spectrogram = spectrogram_complex[0, :, :, :]

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply STFT to %s: %.3f seconds' % (input_name, time.time() - start))

    return spectrogram
