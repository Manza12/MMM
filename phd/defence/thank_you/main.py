import numpy as np
from scipy.io.wavfile import write
import scipy.signal.windows as windows


def sinusoid(t_0, t_1, f_0, duration=1., fs=44100, volume=0.1, t_smooth=0.01):
    t = np.arange(0, duration, 1 / fs)
    s = volume * np.sin(2 * np.pi * f_0 * t)

    n_0 = int(t_0 * fs)
    n_1 = int(t_1 * fs)
    a = np.ones(len(t))
    a[:n_0] = 0
    a[n_1:] = 0

    n_smooth = int(t_smooth * fs)
    g = windows.hann(n_smooth)
    g = g / np.sum(g)
    a_smooth = np.convolve(a, g, mode='same')

    x_smooth = s * a_smooth

    return x_smooth.astype(np.float32)


def transient(t_0, f_0, f_1, duration=1., fs=44100, volume=0.1, t_smooth=0.01, gain=128):
    t = np.arange(0, duration, 1 / fs)
    f = t_0 * (fs / 2) / duration
    s = volume * np.sin(2 * np.pi * f * t)

    t_0 = f_0 * duration / (fs / 2)
    n_0 = int(t_0 * fs)
    t_1 = f_1 * duration / (fs / 2)
    n_1 = int(t_1 * fs)
    a = np.ones(len(t))
    a[:n_0] = 0
    a[n_1:] = 0

    n_smooth = int(t_smooth * fs)
    g = windows.hann(n_smooth)
    g = g / np.sum(g)
    a_smooth = np.convolve(a, g, mode='same')

    x_smooth = s * a_smooth

    x_transient = np.fft.fft(x_smooth, n=int(2*duration*fs)).real[:int(duration*fs)] / fs * gain
    x_transient = x_transient.astype(np.float32)

    return x_transient


def line(t_0, t_1, f_0, f_1, duration=1., fs=44100, volume=0.1, t_smooth=0.01):
    t = np.arange(0, duration, 1 / fs)

    n_0 = int(t_0 * fs)
    n_1 = int(t_1 * fs)

    f = np.zeros(len(t))
    f[:n_0] = f_0
    f[n_1:] = f_1
    f[n_0:n_1] = np.linspace(f_0, f_1, n_1 - n_0)
    s = volume * np.sin(2 * np.pi * np.cumsum(f) / fs)

    a = np.ones(len(t))
    a[:n_0] = 0
    a[n_1:] = 0

    n_smooth = int(t_smooth * fs)
    g = windows.hann(n_smooth)
    g = g / np.sum(g)
    a_smooth = np.convolve(a, g, mode='same')
    a_smooth = a_smooth.astype(np.float32)

    x_smooth = s * a_smooth
    x_smooth = x_smooth.astype(np.float32)

    return x_smooth


def circle(t_0, t_1, f_c, f_r, orientation='both', duration=1., fs=44100, volume=0.1, t_smooth=0.01):
    t = np.arange(0, duration, 1 / fs)

    t_c = (t_0 + t_1) / 2
    t_r = (t_1 - t_0) / 2

    n_0 = int(t_0 * fs)
    n_1 = int(t_1 * fs)

    if orientation == 'both' or orientation == 'plus':
        f_plus = np.zeros(len(t))
        f_plus[:n_0] = f_c
        f_plus[n_1:] = f_c
        f_plus[n_0:n_1] = f_c + f_r * np.sqrt(1 - 0.99*((t[n_0:n_1] - t_c) / t_r)**2)
        s_plus = volume * np.sin(2 * np.pi * np.cumsum(f_plus) / fs)
    else:
        s_plus = np.zeros(len(t))

    if orientation == 'both' or orientation == 'minus':
        f_minus = np.zeros(len(t))
        f_minus[:n_0] = f_c
        f_minus[n_1:] = f_c
        f_minus[n_0:n_1] = f_c - f_r * np.sqrt(1 - 0.99*((t[n_0:n_1] - t_c) / t_r)**2)
        s_minus = volume * np.sin(2 * np.pi * np.cumsum(f_minus) / fs)
    else:
        s_minus = np.zeros(len(t))

    a = np.ones(len(t))
    a[:n_0] = 0
    a[n_1:] = 0

    n_smooth = int(t_smooth * fs)
    g = windows.hann(n_smooth)
    g = g / np.sum(g)
    a_smooth = np.convolve(a, g, mode='same')
    a_smooth = a_smooth.astype(np.float32)

    x_smooth = s_minus * a_smooth + s_plus * a_smooth
    x_smooth = x_smooth.astype(np.float32)

    return x_smooth


if __name__ == '__main__':
    _duration = 3.
    _fs = 44100

    x = np.zeros(int(_duration * _fs), dtype=np.float32)

    x += sinusoid(t_0=0.2, t_1=0.4, f_0=12000, duration=_duration, fs=_fs)
    x += transient(t_0=0.3, f_0=6000, f_1=12000, duration=_duration, fs=_fs)
    x += sinusoid(t_0=0.5, t_1=0.6, f_0=9000, duration=_duration, fs=_fs)
    x += transient(t_0=0.5, f_0=6000, f_1=12000, duration=_duration, fs=_fs)
    x += transient(t_0=0.6, f_0=6000, f_1=12000, duration=_duration, fs=_fs)
    x += line(t_0=0.7, t_1=0.8, f_0=6000, f_1=12000, duration=_duration, fs=_fs)
    x += line(t_0=0.8, t_1=0.9, f_0=12000, f_1=6000, duration=_duration, fs=_fs)
    x += sinusoid(t_0=0.75, t_1=0.85, f_0=9000, duration=_duration, fs=_fs)
    x += transient(t_0=1., f_0=6000, f_1=12000, duration=_duration, fs=_fs)
    x += transient(t_0=1.2, f_0=6000, f_1=12000, duration=_duration, fs=_fs)
    x += line(t_0=1., t_1=1.2, f_0=12000, f_1=6000, duration=_duration, fs=_fs)
    x += transient(t_0=1.3, f_0=6000, f_1=12000, duration=_duration, fs=_fs)
    x += line(t_0=1.3, t_1=1.5, f_0=9000, f_1=6000, duration=_duration, fs=_fs)
    x += line(t_0=1.3, t_1=1.5, f_0=9000, f_1=12000, duration=_duration, fs=_fs)
    x += line(t_0=2., t_1=2.2, f_0=6000, f_1=12000, duration=_duration, fs=_fs)
    x += line(t_0=2., t_1=2.1, f_0=12000, f_1=9000, duration=_duration, fs=_fs)
    x += circle(t_0=2.3, t_1=2.5, f_c=9000, f_r=3000, duration=_duration, fs=_fs)

    # x += circle(t_0=2.6, t_1=2.8, f_c=12000, f_r=6000, orientation='minus', duration=_duration, fs=_fs)

    x += circle(t_0=2.6, t_1=2.8, f_c=9000, f_r=3000, orientation='minus', duration=_duration, fs=_fs)
    x += transient(t_0=2.6, f_0=9000, f_1=12000, duration=_duration, fs=_fs)
    x += transient(t_0=2.8, f_0=9000, f_1=12000, duration=_duration, fs=_fs)

    # x += np.random.normal(0, 0.01, len(x))

    write('thank_you.wav', _fs, x)
