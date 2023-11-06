from .morphology import *
from .parameters import *
from .utils import from_db, to_db


# Input
def apply_closing(spectrogram, parameters, verbose=True):
    start = time.time()

    time_width = parameters.get('closing_time_width', WINDOW_SPREAD[0])
    frequency_width = parameters.get('closing_frequency_width', WINDOW_SPREAD[1])

    shape = (int(np.ceil(frequency_width / FREQUENCY_PRECISION)),
             int(np.ceil(time_width / TIME_RESOLUTION)))

    str_el = torch.ones(shape).to(DEVICE)

    spectrogram_closed = greyscale.closing(spectrogram, str_el, border='g')

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply closing: %.3f seconds' % (time.time() - start))

    return spectrogram_closed


def apply_reconstruction_by_erosion(marker, spectrogram, verbose=True):
    start = time.time()

    spectrogram_filled = reconstruction_erosion(marker, spectrogram, verbose=verbose,
                                                iterations=RECONSTRUCTION_EROSION_ITERATIONS)

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply reconstruction by erosion: %.3f seconds' % (time.time() - start))

    return spectrogram_filled


def apply_erosion(spectrogram):
    start = time.time()

    window = win.get_window(WINDOW, int(np.ceil(WIN_LENGTH / FS / TIME_RESOLUTION)))
    window_db = to_db(window, 'numpy')
    str_el = torch.from_numpy(window_db).to(torch.float32).to(DEVICE)
    str_el = str_el.view(1, -1)

    spectrogram_eroded = greyscale.erosion(spectrogram, str_el, border='g')

    torch.cuda.synchronize(DEVICE)
    print('Time to apply erosion: %.3f seconds' % (time.time() - start))

    return spectrogram_eroded


# Noise
def apply_opening(spectrogram, parameters, verbose=True):
    start = time.time()

    time_width = parameters.get('opening_time_width', WINDOW_SPREAD[0])
    frequency_width = parameters.get('opening_frequency_width', WINDOW_SPREAD[1])

    shape = (int(np.ceil(frequency_width / FREQUENCY_PRECISION)),
             int(np.ceil(time_width / TIME_RESOLUTION)))

    str_el = torch.zeros(shape).to(DEVICE)

    spectrogram_opened = greyscale.opening(spectrogram, str_el, border='g')

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply opening: %.3f seconds' % (time.time() - start))

    return spectrogram_opened


# Sinusoids
def apply_vertical_thinning(spectrogram, verbose=True):
    print('Applying vertical thinning...')

    start = time.time()

    spectrogram_thinned = greyscale_thinning(spectrogram, direction='v', verbose=verbose,
                                             iterations=VERTICAL_THINNING_ITERATIONS)

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply vertical thinning: %.3f seconds' % (time.time() - start))

    return spectrogram_thinned


def apply_vertical_top_hat(spectrogram, verbose=True):
    start = time.time()

    shape = (3, 1)

    str_el = torch.zeros(shape).to(DEVICE)

    spectrogram_top_hat = spectrogram - greyscale.opening(spectrogram, str_el)

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply vertical top-hat: %.3f seconds' % (time.time() - start))

    return spectrogram_top_hat


def apply_top_hat_threshold(spectrogram, spectrogram_top_hat, threshold=TOP_HAT_DIFF_THRESHOLD, min_db=MIN_DB,
                            verbose=True):
    start = time.time()

    spectrogram_threshold = torch.clone(spectrogram)
    spectrogram_threshold[spectrogram_top_hat <= threshold] = min_db

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply top-hat threshold: %.3f seconds' % (time.time() - start))

    return spectrogram_threshold


def remove_small_horizontal_lines(spectrogram, verbose=True):
    print('Removing small horizontal lines...')

    start = time.time()

    min_length_bins = int(MIN_LENGTH_SINUSOIDS / TIME_RESOLUTION)
    iterations = min_length_bins // 2

    spectrogram_trimming = greyscale_trimming(spectrogram, iterations, 'h', verbose=verbose)
    spectrogram_reconstruction = reconstruction_dilation(spectrogram_trimming, spectrogram)

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to remove small horizontal lines: %.3f seconds' % (time.time() - start))

    return spectrogram_reconstruction


# Transients
def apply_horizontal_thinning(spectrogram, verbose=True):
    print('Applying horizontal thinning...')
    start = time.time()

    spectrogram_thinned = greyscale_thinning(spectrogram, direction='h', verbose=verbose,
                                             iterations=HORIZONTAL_THINNING_ITERATIONS)

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply horizontal thinning: %.3f seconds' % (time.time() - start))

    return spectrogram_thinned


def apply_horizontal_top_hat(spectrogram, verbose=True):
    start = time.time()

    shape = (1, 3)

    str_el = torch.zeros(shape).to(DEVICE)

    spectrogram_top_hat = spectrogram - greyscale.opening(spectrogram, str_el)

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply horizontal top-hat: %.3f seconds' % (time.time() - start))

    return spectrogram_top_hat


def remove_small_vertical_lines(spectrogram, verbose=True):
    print('Removing small vertical lines...')

    start = time.time()

    min_length_bins = int(MIN_LENGTH_TRANSIENT / FREQUENCY_PRECISION)
    iterations = min_length_bins // 2

    spectrogram_trimming = greyscale_trimming(spectrogram, iterations, 'v', verbose=verbose)
    spectrogram_reconstruction = reconstruction_dilation(spectrogram_trimming, spectrogram)

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to remove small vertical lines: %.3f seconds' % (time.time() - start))

    return spectrogram_reconstruction


def get_lines(spectrogram: torch.Tensor, sort_by, min_db=MIN_DB, verbose=True, verbose_it_step=100):
    start = time.time()

    if verbose:
        print('Finding %s lines...' % sort_by)

    structure = np.ones((3, 3))

    labels, n_labels = image.label(torch.greater(spectrogram, min_db).cpu().numpy(), structure=structure)
    labels_tensor = torch.tensor(labels, device=DEVICE)

    if sort_by == 'time':
        min_length_bins = int(MIN_LENGTH_SINUSOIDS / TIME_RESOLUTION)
    elif sort_by == 'frequency':
        min_length_bins = MIN_LENGTH_TRANSIENT // FREQUENCY_PRECISION
    else:
        raise ValueError('Parameter sort_by must be either "time" or "frequency"')

    lines = []
    for i in range(1, n_labels + 1):
        values = torch.eq(labels_tensor, i)
        idxs = torch.argwhere(values)

        if idxs.shape[0] < min_length_bins:
            continue

        # Sort
        if sort_by == 'time':
            idxs_sort = idxs[idxs[:, 1].argsort()]
        elif sort_by == 'frequency':
            idxs_sort = idxs[idxs[:, 0].argsort()]
        else:
            raise ValueError('Parameter sort_by must be either "time" or "frequency"')

        ampli_db = spectrogram[idxs_sort[:, 0], idxs_sort[:, 1]]
        if torch.max(ampli_db) < MIN_AMPLI_DB:
            continue

        times = idxs_sort[:, 1] * TIME_RESOLUTION
        freqs = idxs_sort[:, 0] * FREQUENCY_PRECISION
        ampli = from_db(ampli_db)

        line = torch.stack((times, freqs, ampli), dim=1)

        lines.append(line.cpu().numpy())

        if verbose and i % verbose_it_step == 0:
            print('Iteration %d / %d' % (i, n_labels))

    if verbose:
        print('Number of lines found: %d' % len(lines))
        print('Time to find horizontal lines: %.3f seconds' % (time.time() - start))

    return lines


def filter_lines(lines, axis):
    if FILTER_SINUSOIDS is None:
        return lines

    ba = sig.butter(*FILTER_SINUSOIDS)

    filtered_lines = []
    for line in lines:
        y = line[:, axis]
        new_line = np.copy(line)
        new_line[:, axis] = sig.filtfilt(*ba, y, method="gust")

        filtered_lines.append(new_line)

    return filtered_lines


def get_window_spread(w, drop, nfft, fs=1):
    w_db = to_db(w / w.max(), library='numpy')
    t = (np.arange(w.size) - w.size // 2) / fs
    t_max = 2 * np.max(np.abs(t[w_db >= w_db.max() - drop]))

    W = np.fft.fft(w, nfft)
    W_db = to_db(W, library='numpy')
    f = np.fft.fftfreq(nfft, 1 / fs)
    f_max = 2 * np.max(np.abs(f[W_db >= W_db.max() - drop]))

    return t_max, f_max


if isinstance(WINDOW, Tuple):
    NEW_WINDOW = (WINDOW[0], FS * WINDOW[1] / np.sqrt(2 * np.pi))
else:
    NEW_WINDOW = WINDOW
WINDOW_SPREAD = get_window_spread(win.get_window(NEW_WINDOW, WIN_LENGTH), DROP, N_FFT, FS)
# print('Window spread for a %d dB drop:'
#       '\nTime: %d ms'
#       '\nFrequency: %d Hz' % (DROP, WINDOW_SPREAD[0] * 1e3, WINDOW_SPREAD[1]))
# print()
