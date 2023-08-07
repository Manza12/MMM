from .. import *

from ..parameters import FS


def read_wav(file_path: Path):
    warnings.filterwarnings("ignore", category=wav.WavFileWarning)
    fs, data = wav.read(file_path)

    assert fs == FS, f"Sampling frequency must be {FS} Hz"

    if issubclass(data.dtype.type, numbers.Integral):
        data = data / np.iinfo(data.dtype).max

    return data


def write_wav(file_path: Path, data: np.ndarray):
    wav.write(file_path, FS, data.astype(np.float32))


def save_pickle(file_path, data):
    with open(file_path, 'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(file_path, verbose=False, name=''):
    start = time.time()
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    if verbose:
        print('Time to load %s: %.3f seconds' % (name, time.time() - start))
    return data


def try_to_load_pickle(file_path, verbose=False, name=''):
    try:
        data = load_pickle(file_path, verbose=verbose, name=name)
    except FileNotFoundError:
        data = None
    except ValueError:
        data = None
    return data


def try_to_read_wav(file_path):
    try:
        data = read_wav(file_path)
    except FileNotFoundError:
        data = None
    except ValueError:
        data = None
    return data


def load_or_compute(name, folder, load, function, extension='.pickle', verbose=True) -> np.ndarray:
    path = folder / (name + extension)

    if load[name]:
        if extension == '.pickle':
            result = try_to_load_pickle(path, verbose=verbose, name=name)
        elif extension == '.wav':
            result = try_to_read_wav(path)
        else:
            raise ValueError('Extension not supported')
    else:
        result = None

    if not load[name] or result is None:
        result = function()
        save_pickle(path, result)

    return result


def write_signals(signals, paths, components):
    if components['input']:
        x = signals['input']
        input_path = paths['output_folder'] / 'input.wav'
        write_wav(input_path, x)

    if components['noise']:
        filtered_noise = signals['filtered_noise']
        filtered_noise_path = paths['output_folder'] / 'filtered_noise.wav'
        write_wav(filtered_noise_path, filtered_noise)

    if components['sinusoids']:
        sinusoids = signals['sinusoids']
        sinusoids_path = paths['output_folder'] / 'sinusoids.wav'
        write_wav(sinusoids_path, sinusoids)

    if components['transient']:
        transient = signals['transient']
        transient_path = paths['output_folder'] / 'transient.wav'
        write_wav(transient_path, transient)

    if components['output']:
        output = signals['output']
        output_path = paths['output_folder'] / 'output.wav'
        write_wav(output_path, output)
