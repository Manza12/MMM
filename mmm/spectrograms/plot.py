from . import *
from .parameters import TIME_RESOLUTION, FREQUENCY_PRECISION
from .tfst import TFST
from .parameters import N_FFT, FS


def create_time_vector(n):
    return np.arange(n) * TIME_RESOLUTION


def create_frequency_vector():
    return np.arange(N_FFT // 2 + 1) * FS / N_FFT


def format_freq(x, pos, freq_names):
    if pos:
        pass
    n = int(round(x))
    if 0 <= n < len(freq_names):
        return str(round(freq_names[n]))
    else:
        return ""


def format_time(x, pos, time_names):
    if pos:
        pass
    n = int(np.ceil(x))
    if 0 <= n < len(time_names):
        return str(round(time_names[n], 3))
    else:
        return ""


def update_slider(val, fig, im, array):
    im.set_data(array[val, :, :])
    fig.canvas.draw()


def plot_time_frequency(a, t, f, v_min=0, v_max=1, c_map='Greys',
                        fig_title=None, full_screen=False, fig_size=(640, 480),
                        freq_label='Frequency (Hz)', time_label='Time (s)', dpi=120,
                        grid_t=False, grid_f=False,
                        colorbar=False, colorbar_ticks=None, colorbar_labels=None,
                        interpolation='none', return_image=False):
    fig = plt.figure(figsize=(fig_size[0]/dpi, fig_size[1]/dpi), dpi=dpi)

    if fig_title:
        fig.suptitle(fig_title)

    ax = fig.add_subplot(111)

    im = ax.imshow(a, cmap=c_map, aspect='auto', vmin=v_min, vmax=v_max, origin='lower', interpolation=interpolation)

    # Freq axis
    ax.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: format_freq(x, pos, f)))

    # Time axis
    ax.xaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: format_time(x, pos, t)))

    # Grid
    if grid_t:
        plt.grid(axis='x')
    if grid_f:
        plt.grid(axis='y')

    # Labels
    ax.set_xlabel(time_label)
    ax.set_ylabel(freq_label)

    if full_screen:
        backend = mpl.get_backend()
        manager = plt.get_current_fig_manager()
        if backend == 'WXAgg':
            manager.frame.Maximize(True)
        elif backend == 'TkAgg':
            manager.resize(*manager.window.maxsize())
        elif backend == 'Qt5Agg':
            manager.window.showMaximized()
        else:
            raise Exception("Backend not supported.")

    # Colorbar
    if colorbar:
        if colorbar_ticks is not None:
            cbar = fig.colorbar(im, ax=ax, orientation='vertical', ticks=colorbar_ticks, format="%2.0f dB")
            if colorbar_labels is not None:
                cbar.ax.set_yticklabels(colorbar_labels)
        else:
            fig.colorbar(im, ax=ax, orientation='vertical', format="%2.0f dB")

    if return_image:
        return fig, im
    else:
        return fig


def plot_stft(spectrogram: np.ndarray, v_min: float, v_max: float, title: str = '',
              c_map: str = 'afmhot', fig_size: (float, float) = (6., 4.),
              full_screen: bool = False, cb: bool = True):
    frequency_vector = create_frequency_vector()
    time_vector = create_time_vector(spectrogram.shape[-1])

    fig = plt.figure(figsize=fig_size)
    fig.canvas.manager.set_window_title(title)

    ax = fig.subplots()

    if len(spectrogram.shape) == 3:
        spectrogram = spectrogram[0, :, :]
    im = ax.imshow(spectrogram, cmap=c_map, aspect='auto', vmin=v_min, vmax=v_max, origin='lower')

    # Freq axis
    ax.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: format_freq(x, pos, frequency_vector)))

    # Time axis
    ax.xaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: format_time(x, pos, time_vector)))

    # Labels
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')

    # Colorbar
    if cb:
        fig.colorbar(im, ax=ax, format="%2.0f dB")

    plt.tight_layout()

    # Full screen
    if full_screen:
        if mpl.get_backend() == 'QtAgg':
            fig.canvas.manager.window.showMaximized()

    return fig


def plot_cqt(spectrogram: np.ndarray, cqt_layer: cqt.CQT, v_min: float, v_max: float, title: str = '',
             c_map: str = 'afmhot', fig_size: (float, float) = (6., 4.)):
    fig = plt.figure(figsize=fig_size)
    fig.suptitle(title)

    ax = fig.subplots()

    im = ax.imshow(spectrogram[0, :, :], cmap=c_map, aspect='auto', vmin=v_min, vmax=v_max, origin='lower')

    # Freq axis
    frequency_vector = cqt_layer.frequencies
    ax.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: format_freq(x, pos, frequency_vector)))

    # Time axis
    time_vector = np.arange(spectrogram.shape[-1]) * cqt_layer.hop_length / cqt_layer.fs
    ax.xaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: format_time(x, pos, time_vector)))

    # Labels
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')

    # Colorbar
    fig.colorbar(im, ax=ax, format="%2.0f dB")

    plt.tight_layout()

    return fig


def plot_tfst(spectrogram: np.ndarray, tfst_layer: TFST, v_min: float, v_max: float, title: str = '',
              fig_size: (float, float) = (6., 4.)):
    fig = plt.figure(figsize=fig_size)
    fig.suptitle(title)

    plt.subplots_adjust(bottom=0.25)
    ax = fig.subplots()

    im = ax.imshow(spectrogram[0, :, :], cmap='afmhot', aspect='auto', vmin=v_min, vmax=v_max, origin='lower')
    ax_slider = plt.axes([0.25, 0.1, 0.45, 0.03])

    # Freq axis
    frequency_vector = tfst_layer.frequencies.cpu().numpy()
    ax.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: format_freq(x, pos, frequency_vector)))

    # Time axis
    time_vector = np.arange(spectrogram.shape[-1]) * tfst_layer.hop_length / tfst_layer.fs
    ax.xaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: format_time(x, pos, time_vector)))

    # Labels
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')

    # Colorbar
    fig.colorbar(im, ax=ax, format="%2.0f dB")

    # Slider
    slider = wid.Slider(
        ax=ax_slider,
        label='Window size',
        valmin=0,
        valmax=spectrogram.shape[0] - 1,
        valinit=0,
        valstep=1,
    )
    slider.valtext.set_text(tfst_layer.sizes[0])

    def update(val):
        im.set_data(spectrogram[val, :, :])
        slider.valtext.set_text(tfst_layer.sizes[val])
        fig.canvas.draw()

    return fig, slider, update


def plot_two_spectrogram(spectrogram_1: np.ndarray, spectrogram_2: np.ndarray,
                         v_min_1=None, v_max_1=None, v_min_2=None, v_max_2=None, c_map_1='afmhot', c_map_2='afmhot',
                         fig_size: (float, float) = (12, 8), title: str = '',
                         sharexy=False, full_screen=False,
                         cb_1=True, cb_2=True):
    time_vector = create_time_vector(spectrogram_1.shape[1])
    frequency_vector = create_frequency_vector()

    if sharexy:
        fig, axs = plt.subplots(1, 2, sharex='all', sharey='all', figsize=fig_size)
    else:
        fig, axs = plt.subplots(1, 2, figsize=fig_size)

    fig.canvas.manager.set_window_title(title)

    if len(spectrogram_1.shape) == 3:
        spectrogram_1 = spectrogram_1[0, :, :]
    if len(spectrogram_2.shape) == 3:
        spectrogram_2 = spectrogram_2[0, :, :]

    if v_min_1 is None:
        v_min_1 = np.min(spectrogram_1)
    if v_max_1 is None:
        v_max_1 = np.max(spectrogram_1)
    if v_min_2 is None:
        v_min_2 = np.min(spectrogram_2)
    if v_max_2 is None:
        v_max_2 = np.max(spectrogram_2)

    image_1 = axs[0].imshow(spectrogram_1, cmap=c_map_1, vmin=v_min_1, vmax=v_max_1, aspect='auto', origin='lower')
    image_2 = axs[1].imshow(spectrogram_2, cmap=c_map_2, vmin=v_min_2, vmax=v_max_2, aspect='auto', origin='lower')

    # Freq axis
    axs[0].yaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: format_freq(x, pos, frequency_vector)))
    axs[1].yaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: format_freq(x, pos, frequency_vector)))

    # Time axis
    axs[0].xaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: format_time(x, pos, time_vector)))
    axs[1].xaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: format_time(x, pos, time_vector)))

    # Labels
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Frequency (Hz)')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Frequency (Hz)')

    # Colorbar
    if cb_1:
        fig.colorbar(image_1, ax=axs[0], format="%2.0f dB")
    if cb_2:
        fig.colorbar(image_2, ax=axs[1], format="%2.0f dB")

    plt.tight_layout()

    # Full screen
    if full_screen:
        if mpl.get_backend() == 'QtAgg':
            fig.canvas.manager.window.showMaximized()
        elif mpl.get_backend() == 'TkAgg':
            manager = fig.canvas.manager
            manager.resize(*manager.window.maxsize())

    return fig


def plot_two_spectrogram_one_colorbar(spectrogram_1: np.ndarray, spectrogram_2: np.ndarray,
                                      v_min_1=None, v_max_1=None, v_min_2=None, v_max_2=None,
                                      c_map_1='afmhot', c_map_2='afmhot',
                                      fig_size: (float, float) = (12, 8), title: str = '',
                                      sharexy=False, full_screen=False):
    time_vector = create_time_vector(spectrogram_1.shape[1])
    frequency_vector = create_frequency_vector()

    if sharexy:
        fig, axs = plt.subplots(1, 2, sharex='all', sharey='all', figsize=fig_size)
    else:
        fig, axs = plt.subplots(1, 2, figsize=fig_size)

    fig.canvas.manager.set_window_title(title)

    if len(spectrogram_1.shape) == 3:
        spectrogram_1 = spectrogram_1[0, :, :]
    if len(spectrogram_2.shape) == 3:
        spectrogram_2 = spectrogram_2[0, :, :]

    if v_min_1 is None:
        v_min_1 = np.min(spectrogram_1)
    if v_max_1 is None:
        v_max_1 = np.max(spectrogram_1)
    if v_min_2 is None:
        v_min_2 = np.min(spectrogram_2)
    if v_max_2 is None:
        v_max_2 = np.max(spectrogram_2)

    axs[0].imshow(spectrogram_1, cmap=c_map_1, vmin=v_min_1, vmax=v_max_1, aspect='auto', origin='lower')
    image_2 = axs[1].imshow(spectrogram_2, cmap=c_map_2, vmin=v_min_2, vmax=v_max_2, aspect='auto', origin='lower')

    # Freq axis
    axs[0].yaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: format_freq(x, pos, frequency_vector)))
    axs[1].yaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: format_freq(x, pos, frequency_vector)))

    # Time axis
    axs[0].xaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: format_time(x, pos, time_vector)))
    axs[1].xaxis.set_major_formatter(tick.FuncFormatter(lambda x, pos: format_time(x, pos, time_vector)))

    # Labels
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Frequency (Hz)')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Frequency (Hz)')

    # Colorbar
    # fig.colorbar(image_1, ax=axs[0], format="%2.0f dB")
    fig.colorbar(image_2, ax=axs[1], format="%2.0f dB")

    plt.tight_layout()

    # Full screen
    if full_screen:
        if mpl.get_backend() == 'QtAgg':
            fig.canvas.manager.window.showMaximized()
        elif mpl.get_backend() == 'TkAgg':
            manager = fig.canvas.manager
            manager.resize(*manager.window.maxsize())

    return fig


def plot_pixels(x_list, label_list, m, n, show=True, v_min=None, v_max=None):
    if v_min is None:
        v_min = min([x.min() for x in x_list])
    if v_max is None:
        v_max = max([x.max() for x in x_list])

    assert len(x_list) == len(label_list)
    fig, axs = plt.subplots(m, n, figsize=(10, 5))

    if axs.ndim == 1:
        axs = axs.reshape(1, -1)

    for i in range(m):
        for j in range(n):
            idx = i * n + j
            x = x_list[idx]
            label = label_list[idx]

            axs[i, j].set_xticks(np.arange(x.shape[1] + 1) - 0.5, minor=True)
            axs[i, j].set_yticks(np.arange(x.shape[0] + 1) - 0.5, minor=True)
            axs[i, j].set_xticks([])
            axs[i, j].set_yticks([])
            axs[i, j].grid(which='minor')

            axs[i, j].imshow(x.numpy(), cmap='Greys', vmin=v_min, vmax=v_max)
            axs[i, j].set_title(label)

    if show:
        plt.show()


def plot_lines(lines, fig=None, *args, phd=None, **kwargs):
    if fig is None:
        fig, ax = plt.subplots(1, 1, figsize=phd.get('fig_size', (8., 4.)))
    else:
        ax = fig.axes[0]

    for line in lines:
        if fig is None:
            ax.plot(line[:, 0], line[:, 1], *args, **kwargs)
        else:
            ax.plot(line[:, 0] / TIME_RESOLUTION, line[:, 1] / FREQUENCY_PRECISION, *args, **kwargs)

        kwargs.pop('label', None)

    # Full screen
    if phd.get('full_screen', True):
        if mpl.get_backend() == 'QtAgg':
            fig.canvas.manager.window.showMaximized()
        elif mpl.get_backend() == 'TkAgg':
            manager = fig.canvas.manager
            manager.resize(*manager.window.maxsize())

    return fig
