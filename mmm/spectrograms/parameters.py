from . import *

# STFT parameters
FS = 44100  # Hz
DEVICE = 'cuda:0'  # 'cpu' or 'cuda:0'
WIN_LENGTH = 2048  # samples
OVERSAMPLING = 2  # no unit
N_FFT = WIN_LENGTH * OVERSAMPLING  # samples
FREQUENCY_PRECISION = FS / N_FFT  # Hz
TIME_RESOLUTION = 0.001  # s
HOP_LENGTH = int(FS * TIME_RESOLUTION)  # samples
WINDOW = 'blackman'  # ('gaussian', 1/100) or 'hann'
PAD_MODE = 'constant'  # 'constant' or 'reflect'
OUTPUT_FORMAT = 'Complex'  # 'Magnitude' or 'Complex'
FREQ_SCALE = 'no'  # 'no', 'linear', 'log', 'mel', 'cqt_hz', 'cqt_note'
CENTER = True  # True or False

# Spectrogram parameters
EPS = np.finfo(np.float32).eps
MIN_DB = 20 * np.log10(EPS)

# Synthesis parameters
NOISE_SIGMA = 30.  # no unit

# Morphology parameters
DROP = 60  # dB
TOP_HAT_DIFF_THRESHOLD = 5  # dB
TOP_HAT_ABS_THRESHOLD = -100  # dB

# Sinusoids parameters
MIN_AMPLI_DB = -100  # dB
FADE_IN = 0.005  # s
FADE_OUT = 0.01  # s
MIN_LENGTH_SINUSOIDS = 0.1  # s
FILTER_SINUSOIDS = (3, 0.05)  # (order, cutoff) or None

# Transient parameters
MIN_LENGTH_TRANSIENT = 100  # Hz
TOP_HAT_TRANSIENT_DIFF_THRESHOLD = 10  # dB
TOP_HAT_TRANSIENT_ABS_THRESHOLD = -100  # dB
CLOSING_TRANSIENT_FREQUENCY_FACTOR = 1.5  # no unit
CLOSING_TRANSIENT_TIME_FACTOR = 2  # no unit
FADE_OUT_FREQ = 50  # Hz
FADE_IN_FREQ = 50  # Hz
CONNECTION_SIZE_TRANSIENT = (7, 7)  # no unit
