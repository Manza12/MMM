from . import *
from .morphology import greyscale_thinning, reconstruction_erosion, binary_thinning, reconstruction_dilation, \
    greyscale_trimming
from .parameters import DEVICE, TIME_RESOLUTION, FREQUENCY_PRECISION, TOP_HAT_DIFF_THRESHOLD, \
    TOP_HAT_ABS_THRESHOLD, MIN_AMPLI_DB, \
    TOP_HAT_TRANSIENT_DIFF_THRESHOLD, TOP_HAT_TRANSIENT_ABS_THRESHOLD, CLOSING_TRANSIENT_FREQUENCY_FACTOR, \
    CLOSING_TRANSIENT_TIME_FACTOR, FS, WINDOW, WIN_LENGTH, N_FFT, DROP, MIN_LENGTH_TRANSIENT, MIN_LENGTH_SINUSOIDS, \
    FILTER_SINUSOIDS, MIN_DB
from .utils import from_db, to_db


def apply_reconstruction_by_erosion(spectrogram, verbose=True):
    start = time.time()

    spectrogram_filled = reconstruction_erosion(None, spectrogram, verbose_it_step=100, verbose=verbose)

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply reconstruction by erosion: %.3f seconds' % (time.time() - start))

    return spectrogram_filled


def apply_opening(spectrogram, verbose=True):
    start = time.time()

    time_width, frequency_width = WINDOW_SPREAD

    shape = (int(np.ceil(frequency_width / FREQUENCY_PRECISION)),
             int(np.ceil(time_width / TIME_RESOLUTION)))

    str_el = torch.zeros(shape).to(DEVICE)

    spectrogram_opened = greyscale.opening(spectrogram, str_el, border='g')

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply opening: %.3f seconds' % (time.time() - start))

    return spectrogram_opened


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


def apply_vertical_top_hat_v0(spectrogram, verbose=True):
    start = time.time()

    _, frequency_width = WINDOW_SPREAD

    shape = (int(np.ceil(frequency_width / FREQUENCY_PRECISION)), 1)

    str_el = torch.zeros(shape).to(DEVICE)

    spectrogram_top_hat = spectrogram - greyscale.opening(spectrogram, str_el)

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply vertical top-hat: %.3f seconds' % (time.time() - start))

    return spectrogram_top_hat


def apply_vertical_top_hat(spectrogram, verbose=True):
    start = time.time()

    shape = (3, 1)

    str_el = torch.zeros(shape).to(DEVICE)

    spectrogram_top_hat = spectrogram - greyscale.opening(spectrogram, str_el)

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply vertical top-hat: %.3f seconds' % (time.time() - start))

    return spectrogram_top_hat


def apply_horizontal_top_hat(spectrogram, verbose=True):
    start = time.time()

    shape = (1, 3)

    str_el = torch.zeros(shape).to(DEVICE)

    spectrogram_top_hat = spectrogram - greyscale.opening(spectrogram, str_el)

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply horizontal top-hat: %.3f seconds' % (time.time() - start))

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
    start = time.time()

    min_length_bins = int(MIN_LENGTH_SINUSOIDS / TIME_RESOLUTION)
    iterations = min_length_bins // 2

    spectrogram_trimming = greyscale_trimming(spectrogram, iterations, 'h')
    spectrogram_reconstruction = reconstruction_dilation(spectrogram_trimming, spectrogram)

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to remove small horizontal lines: %.3f seconds' % (time.time() - start))

    return spectrogram_reconstruction


def remove_small_vertical_lines(spectrogram, verbose=True):
    start = time.time()

    min_length_bins = int(MIN_LENGTH_TRANSIENT / FREQUENCY_PRECISION)
    iterations = min_length_bins // 2

    spectrogram_trimming = greyscale_trimming(spectrogram, iterations, 'v')
    spectrogram_reconstruction = reconstruction_dilation(spectrogram_trimming, spectrogram)

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to remove small vertical lines: %.3f seconds' % (time.time() - start))

    return spectrogram_reconstruction


def link_lines(spectrogram_marker, spectrogram_condition, verbose=True):
    start = time.time()

    spectrogram_linked = reconstruction_dilation(spectrogram_marker, spectrogram_condition, verbose=True,
                                                 verbose_it_step=100)

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to link lines: %.3f seconds' % (time.time() - start))

    return spectrogram_linked


def apply_horizontal_closing(spectrogram, verbose=True):
    start = time.time()

    shape = (1, int(np.ceil(WINDOW_SPREAD[0] / TIME_RESOLUTION)))

    str_el_closing = torch.zeros(shape).to(DEVICE)
    spectrogram_closed = greyscale.closing(spectrogram, str_el_closing, border='g')

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply closing: %.3f seconds' % (time.time() - start))

    return spectrogram_closed


def apply_vertical_thinning(spectrogram, verbose=True):
    print('Applying vertical thinning...')

    start = time.time()

    spectrogram_thinned = greyscale_thinning(spectrogram, direction='v', verbose=verbose, verbose_it_step=100)

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply vertical thinning: %.3f seconds' % (time.time() - start))

    return spectrogram_thinned


def apply_vertical_linking(spectrogram, min_db=MIN_DB, verbose=True):
    print('Applying vertical linking...')
    start = time.time()

    spectrogram_link = torch.clone(spectrogram)
    str_el = torch.zeros((2, 1)).to(DEVICE)
    spectrogram_top_hat = spectrogram - greyscale.opening(spectrogram, str_el)
    spectrogram_link[spectrogram_top_hat == 0] = min_db

    str_el = torch.zeros((3, 3)).to(DEVICE)
    spectrogram_dilation = greyscale.dilation(spectrogram_top_hat, str_el)
    spectrogram_thinning = binary_thinning(torch.gt(spectrogram_dilation, 0), direction='v', verbose=verbose,
                                           verbose_it_step=100)
    spectrogram_link = greyscale.dilation(spectrogram, str_el)
    spectrogram_link[torch.logical_not(spectrogram_thinning)] = min_db

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply vertical linking: %.3f seconds' % (time.time() - start))

    return spectrogram_link


def apply_horizontal_thinning(spectrogram, verbose=True):
    print('Applying horizontal thinning...')
    start = time.time()

    spectrogram_thinned = greyscale_thinning(spectrogram, direction='h', verbose=verbose, verbose_it_step=100)

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply horizontal thinning: %.3f seconds' % (time.time() - start))

    return spectrogram_thinned


def apply_horizontal_linking(spectrogram, min_db=MIN_DB, verbose=True):
    print('Applying horizontal linking...')
    start = time.time()

    spectrogram_link = torch.clone(spectrogram)
    str_el = torch.zeros((1, 2)).to(DEVICE)
    spectrogram_top_hat = spectrogram - greyscale.opening(spectrogram, str_el)
    spectrogram_link[spectrogram_top_hat == 0] = min_db

    str_el = torch.zeros((7, 7)).to(DEVICE)
    spectrogram_dilation = greyscale.dilation(spectrogram_top_hat, str_el)
    spectrogram_thinning = binary_thinning(torch.gt(spectrogram_dilation, 0), direction='h', verbose=verbose,
                                           verbose_it_step=100)
    spectrogram_link = greyscale.dilation(spectrogram, str_el)
    spectrogram_link[torch.logical_not(spectrogram_thinning)] = min_db

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply horizontal linking: %.3f seconds' % (time.time() - start))

    return spectrogram_link


def apply_top_hat_transient(spectrogram, min_db=MIN_DB, verbose=True):
    start = time.time()

    time_width, _ = WINDOW_SPREAD

    shape = (1, int(np.ceil(time_width / TIME_RESOLUTION)))

    str_el = torch.zeros(shape).to(DEVICE)

    spectrogram_top_hat = spectrogram - greyscale.opening(spectrogram, str_el)

    spectrogram_top_hat[spectrogram_top_hat < TOP_HAT_TRANSIENT_DIFF_THRESHOLD] = 0
    spectrogram_top_hat[spectrogram < TOP_HAT_TRANSIENT_ABS_THRESHOLD] = 0

    spectrogram_residual = torch.clone(spectrogram)
    spectrogram_residual[spectrogram_top_hat == 0] = min_db

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply top-hat transient: %.3f seconds' % (time.time() - start))

    return spectrogram_residual


def get_residual(spectrogram, spectrogram_opening, verbose=True, min_db=-100, return_top_hat=False):
    start = time.time()

    spectrogram_top_hat = spectrogram - spectrogram_opening
    spectrogram_top_hat[spectrogram_top_hat < TOP_HAT_DIFF_THRESHOLD] = 0
    if return_top_hat:
        if verbose:
            torch.cuda.synchronize(DEVICE)
            print('Time to compute top-hat: %.3f seconds' % (time.time() - start))
        return spectrogram_top_hat

    spectrogram_residual = torch.clone(spectrogram)
    spectrogram_residual[spectrogram_top_hat == 0] = min_db
    spectrogram_residual[spectrogram < TOP_HAT_ABS_THRESHOLD] = min_db

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to get residual: %.3f seconds' % (time.time() - start))

    return spectrogram_residual


def apply_closing_transient(spectrogram, verbose=True):
    start = time.time()

    CLOSING_TRANSIENT_FREQUENCY_WIDTH = WINDOW_SPREAD[1] / CLOSING_TRANSIENT_FREQUENCY_FACTOR
    CLOSING_TRANSIENT_TIME_WIDTH = WINDOW_SPREAD[0] / CLOSING_TRANSIENT_TIME_FACTOR

    shape = (int(np.ceil(CLOSING_TRANSIENT_FREQUENCY_WIDTH / FREQUENCY_PRECISION)),
             int(np.ceil(CLOSING_TRANSIENT_TIME_WIDTH / TIME_RESOLUTION)))

    str_el_closing = torch.zeros(shape).to(DEVICE)
    spectrogram_closed = greyscale.closing(spectrogram, str_el_closing, border='g')

    if verbose:
        torch.cuda.synchronize(DEVICE)
        print('Time to apply closing: %.3f seconds' % (time.time() - start))

    return spectrogram_closed


def get_lines(spectrogram: torch.Tensor, sort_by, min_db=MIN_DB, verbose=True, verbose_it_step=100):
    start = time.time()

    if verbose:
        print('Finding %s lines...' % sort_by)

    structure = np.ones((3, 3))

    labels, n_labels = image.label((spectrogram > min_db).cpu().numpy(), structure=structure)
    labels_tensor = torch.tensor(labels, device=DEVICE)

    if sort_by == 'time':
        min_length_bins = int(MIN_LENGTH_SINUSOIDS / TIME_RESOLUTION)
    elif sort_by == 'frequency':
        min_length_bins = MIN_LENGTH_TRANSIENT // FREQUENCY_PRECISION
    else:
        raise ValueError('Parameter sort_by must be either "time" or "frequency"')

    lines = []
    for i in range(1, n_labels + 1):
        values = labels_tensor == i
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
