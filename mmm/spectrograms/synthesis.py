import time
import numpy as np
import scipy.signal.windows as win
import scipy.fft as fft
from .parameters import TIME_RESOLUTION, FS, NOISE_SIGMA, FREQUENCY_PRECISION, FADE_OUT, FADE_OUT_FREQ, FADE_IN_FREQ, \
    FADE_IN
from .utils import from_db


def synthesize_white_noise(n):
    white_noise = np.random.randn(n) * NOISE_SIGMA
    return white_noise


def synthesize_noise_mask(white_noise_stft, mask, stft_layer, verbose=False):
    start = time.time()

    # Filter spectrogram
    mask_amplitude = from_db(mask).unsqueeze(-1)
    filtered_noise_stft = mask_amplitude * white_noise_stft[:, :mask_amplitude.shape[1], :]

    # Synthesize
    filtered_noise = stft_layer.inverse(filtered_noise_stft.unsqueeze(0))[0].cpu().numpy()

    if verbose:
        print('Time to synthesize noise: %.3f s' % (time.time() - start))

    return filtered_noise


def modulated_sinusoid(times, freqs, ampli, fs=FS, fade_out=None, fade_in=None):
    ts = 1 / fs

    fade_out = int(fade_out * FS) if fade_out is not None else 0
    fade_in = int(fade_in * FS) if fade_in is not None else 0

    t = np.arange(times.min(), times.max(), ts)
    freqs_interp = np.interp(t, times, freqs)
    ampli_interp = np.interp(t, times, ampli)

    fade_in = min(fade_in, freqs_interp.size // 2)
    fade_out = min(fade_out, freqs_interp.size // 2)

    sinusoid = 2 * ampli_interp * np.sin(2 * np.pi * np.cumsum(freqs_interp) * ts)

    sinusoid[:fade_in] *= np.cos(np.pi * np.flip(np.arange(fade_in)) / (2 * fade_in)) ** 2
    sinusoid[sinusoid.size-fade_out:] *= np.cos(np.pi * np.arange(fade_out) / (2 * fade_out)) ** 2

    return sinusoid


def synthesize_sinusoids(lines_h, fs=FS, verbose=True):
    start = time.time()
    if verbose:
        print('Synthesizing sinusoids...')
    durations = [np.max(line[:, 0]) for line in lines_h]
    if len(durations) == 0:
        duration = 0
    elif len(durations) == 1:
        duration = durations[0]
    else:
        duration = max(*durations)

    signal_sinusoids = np.zeros(int(np.ceil(duration * fs)))

    for line in lines_h:
        times = line[:, 0]
        freqs = line[:, 1]
        ampli = line[:, 2]

        s = modulated_sinusoid(times, freqs, ampli, fade_out=FADE_OUT, fade_in=FADE_IN)

        idx_0 = int(times.min() * fs)
        idx_1 = idx_0 + s.size
        signal_sinusoids[idx_0:idx_1] += s

    if verbose:
        print('Time to synthesize sinusoids: %.3f s' % (time.time() - start))

    return signal_sinusoids


def generate_transient(times, freqs, ampli, duration, fs=FS):
    taus = duration * freqs / (fs / 2)
    omegas = (fs / 2) * times / duration

    fade_out = int(FADE_OUT_FREQ / FREQUENCY_PRECISION) * TIME_RESOLUTION
    fade_in = int(FADE_IN_FREQ / FREQUENCY_PRECISION) * TIME_RESOLUTION

    sinusoid = modulated_sinusoid(taus, omegas, ampli, fade_out=fade_out, fade_in=fade_in)
    sinusoid = np.pad(sinusoid, (int(taus.min() * fs), 0), mode='constant')

    n = int(duration * fs)
    transient = 8 * fft.fft(sinusoid, 2 * n, norm='ortho').real[:n]

    return transient


def cut_transient(s, times):
    idx_0 = int(times.min() * FS)
    idx_1 = int(times.max() * FS)
    w = np.zeros_like(s)
    w[idx_0:idx_1] = 1
    h = win.get_window('hann', int(FADE_IN * FS))
    h = h / h.sum()
    w = np.convolve(w, h, mode='same')
    s *= w
    return s


def synthesize_transient(lines_v, duration, fs=FS, verbose=True):
    start = time.time()
    if verbose:
        print('Synthesizing transient...')

    signal_transient = np.zeros(int(duration * fs))

    for line in lines_v:
        times = line[:, 0]
        freqs = line[:, 1]
        ampli = line[:, 2]

        s = generate_transient(times, freqs, ampli, duration)

        s = cut_transient(s, times)

        signal_transient += s

    if verbose:
        print('Time to synthesize transient: %.3f s' % (time.time() - start))

    return signal_transient
