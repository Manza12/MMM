import time
import torch
import nnAudio.features.cqt as cqt
import nnAudio.features.stft as stft
from .utils import to_db
from .parameters import *


def create_cqt_layer(fs=FS,
                     hop_length=HOP_LENGTH,
                     f_min=F_MIN,
                     n_bins=N_BINS,
                     bins_per_octave=BINS_PER_OCTAVE,
                     filter_scale=FILTER_SCALE,
                     norm=NORM,
                     window=WINDOW,
                     device=DEVICE,
                     verbose=False):
    if verbose:
        print('Creating STFT layer...')
    start = time.time()
    cqt_layer = cqt.CQT(sr=fs,
                        hop_length=hop_length,
                        fmin=f_min,
                        n_bins=n_bins,
                        bins_per_octave=bins_per_octave,
                        filter_scale=filter_scale,
                        norm=norm,
                        window=window,
                        center=True,
                        pad_mode='constant',
                        trainable=False,
                        output_format='Magnitude',
                        verbose=verbose).to(device)
    cqt_layer.fs = fs

    if verbose:
        torch.cuda.synchronize(device)
        print('Time to create CQT layer: %.3f seconds' % (time.time() - start))

    return cqt_layer


def create_stft_layer(n_fft=N_FFT,
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
                      device=DEVICE,
                      verbose=False):
    if verbose:
        print('Creating STFT layer...')
    start = time.time()
    stft_layer = stft.STFT(n_fft=n_fft,
                           win_length=win_length,
                           hop_length=hop_length,
                           window=window,
                           freq_scale=freq_scale,
                           center=center,
                           pad_mode=pad_mode,
                           iSTFT=iSTFT,
                           sr=sr,
                           trainable=trainable,
                           output_format=output_format,
                           verbose=verbose).to(device)
    stft_layer.fs = FS
    if verbose:
        torch.cuda.synchronize(device)
        print('Time to create STFT layer: %.3f seconds' % (time.time() - start))

    return stft_layer


def apply_cqt_layer(signal, cqt_layer, verbose=True, input_name='signal', device=DEVICE):
    # Apply to signal
    signal_tensor = torch.tensor(signal, device=device, dtype=torch.float32)

    start = time.time()
    spectrogram = cqt_layer(signal_tensor, normalization_type='convolutional')
    spectrogram = to_db(spectrogram)
    if verbose:
        torch.cuda.synchronize(device)
        print('Time to apply CQT to %s: %.3f seconds' % (input_name, time.time() - start))

    return spectrogram


def apply_stft_layer(signal, stft_layer, verbose=True, output_format='Magnitude', input_name='signal', device=DEVICE):
    # Apply to signal
    signal_tensor = torch.tensor(signal, device=device, dtype=torch.float32)

    start = time.time()
    spectrogram_complex = stft_layer(signal_tensor)
    if output_format == 'Magnitude':
        spectrogram = torch.sqrt(spectrogram_complex[0, :, :, 0]**2 + spectrogram_complex[0, :, :, 1]**2)
        spectrogram = to_db(spectrogram)
    else:
        spectrogram = spectrogram_complex[0, :, :, :]

    if verbose:
        torch.cuda.synchronize(device)
        print('Time to apply STFT to %s: %.3f seconds' % (input_name, time.time() - start))

    return spectrogram
