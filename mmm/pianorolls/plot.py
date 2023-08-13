import matplotlib.pyplot as plt

from . import *
from .music import Time, TimePoint, TimeShift, FrequencyShift, PianoRoll, ChromaRoll
from .utils import midi_numbers_to_chromas, midi_numbers_to_pitches, round_half_up


def format_freq(x, pos, freq_names):
    if pos:
        pass
    n = int(round(x))
    if 0 <= n < len(freq_names):
        return freq_names[n]
    else:
        return ""


def format_time(x, pos, time_names):
    if pos:
        pass
    n = int(round_half_up(x))
    if n < len(time_names):
        if n >= 0:
            return time_names[n]
    else:
        return ""


def plot_activations(a, t, f, fig_title=None, full_screen=False, fig_size=(640, 480),
                     freq_label='Frequency (Hz)', time_label='Time (s)', dpi=120,
                     grid_t=False, grid_f=False, marker_color='r',
                     ax=None):

    if ax is None:
        fig = plt.figure(figsize=(fig_size[0] / dpi, fig_size[1] / dpi), dpi=dpi)

        if fig_title:
            fig.suptitle(fig_title)

        ax = fig.add_subplot(111)
    else:
        fig = ax.get_figure()

    activations = np.where(a)
    ax.scatter(activations[1] - 0.5, activations[0], c=marker_color, marker='x')

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

    return fig


def plot_time_frequency(a, t, f, v_min=None, v_max=None, c_map='Greys',
                        fig_title=None, full_screen=False, fig_size=(640, 480),
                        freq_label='Frequency (Hz)', time_label='Time (s)', dpi=120,
                        grid_t=False, grid_f=False,
                        colorbar=False, colorbar_ticks=None, colorbar_labels=None, colorbar_title='', cb_discrete=False,
                        interpolation='nearest', return_image=False):
    if v_min is None:
        v_min = np.min(a)
    if v_max is None:
        v_max = np.max(a)

    fig = plt.figure(figsize=(fig_size[0]/dpi, fig_size[1]/dpi), dpi=dpi)

    if fig_title:
        fig.suptitle(fig_title)

    ax = fig.add_subplot(111)

    # Create cmap
    if cb_discrete or (v_min == 0 and (v_max == 1 or v_max == 2)):
        if cb_discrete:
            cmap = mpl.cm.get_cmap(c_map, v_max - v_min)
        else:
            cmap = mpl.cm.get_cmap(c_map, v_max - v_min + 1)
    else:
        cmap = mpl.cm.get_cmap(c_map)

    im = ax.imshow(a, cmap=cmap, aspect='auto', origin='lower', interpolation=interpolation, vmin=v_min, vmax=v_max)

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

    if colorbar:
        if colorbar_ticks is not None:
            cbar = fig.colorbar(im, ax=ax, orientation='vertical', ticks=colorbar_ticks)
            if colorbar_labels is not None:
                cbar.ax.set_yticklabels(colorbar_labels)
        else:
            cbar = fig.colorbar(im, ax=ax, orientation='vertical')

        # Place colorbar ticks correctly in case they are discrete
        if v_min == 0 and v_max == 1:
            ticks = np.array([0, 1])
            cbar.set_ticks((0.5 + ticks) * np.max(ticks) / ticks.size)
            cbar.set_ticklabels([0, 1])
        elif v_min == 0 and v_max == 2:
            ticks = np.array([0, 1, 2])
            cbar.set_ticks((0.5 + ticks) * np.max(ticks) / ticks.size)
            cbar.set_ticklabels(['$\\bot$', '$\\cdot$', '$\\times$'])

        # Colorbar title
        cbar.ax.set_title(colorbar_title)

    if return_image:
        return fig, im
    else:
        return fig


def plot_piano_roll(piano_roll: PianoRoll, note_names: bool = True, time_shift: Optional[Time] = None,
                    time_vector: Iterable = None, freq_vector: Iterable = None,
                    measure_width: Optional[Time] = None, measure_offset: Optional[Time] = None,
                    measure_number_offset: int = 0,
                    freq_label: Optional[str] = None, time_label: Optional[str] = None,
                    colorbar=False, colorbar_ticks=None, colorbar_labels=None,
                    x_tick_start=None, x_tick_step=None,
                    marker_color='r',
                    tight_frame=True,
                    **kwargs):
    if time_label == 'Time (m, b)':
        TimePoint.__str__ = lambda self: f'({self.measure}, {self.beat})'
    if time_vector is None:
        time_vector = np.arange(piano_roll.extension.time.start,
                                piano_roll.extension.time.end + piano_roll.tatum,
                                piano_roll.tatum)

    if time_label is None:
        time_label = 'Time (wholes)'

    if time_shift is not None:
        time_vector += time_shift

    if freq_vector is None:
        freq_vector = np.arange(piano_roll.extension.frequency.lower.value,
                                (piano_roll.extension.frequency.higher + FrequencyShift(1)).value,
                                piano_roll.step.value)
        if note_names:
            if isinstance(piano_roll, ChromaRoll) or note_names == 'chroma':
                freq_vector = midi_numbers_to_chromas(freq_vector)
                if freq_label is None:
                    freq_label = 'Chroma'
            else:
                freq_vector = midi_numbers_to_pitches(freq_vector)
                if freq_label is None:
                    freq_label = 'Pitch'
        else:
            freq_vector = freq_vector
            if freq_label is None:
                freq_label = 'MIDI numbers'

    if piano_roll.array.dtype == np.bool:
        fig = plot_activations(piano_roll.array, time_vector, freq_vector, freq_label=freq_label, time_label=time_label,
                               marker_color=marker_color, **kwargs)
    else:
        if piano_roll.dynamics is None:
            fig = plot_time_frequency(piano_roll.array, time_vector, freq_vector,
                                      freq_label=freq_label, time_label=time_label,
                                      colorbar=colorbar, colorbar_ticks=colorbar_ticks, colorbar_labels=colorbar_labels,
                                      **kwargs)
        else:
            fig = plot_time_frequency(piano_roll.array[1, :, :], time_vector, freq_vector,
                                      freq_label=freq_label, time_label=time_label,
                                      colorbar=colorbar, colorbar_ticks=colorbar_ticks,
                                      colorbar_labels=colorbar_labels,
                                      **kwargs)
            y, x = np.where(piano_roll.array[0, :, :] == 2)
            onsets = plt.scatter(x-0.5, y, s=30, c='r', marker="|")
            fig.__dict__['onsets'] = onsets

    if x_tick_step is not None:
        if x_tick_start is None:
            x_tick_start = TimePoint(0, 1)
        ticks = np.arange((x_tick_start - piano_roll.extension.time.start) / piano_roll.tatum,
                          (piano_roll.extension.time.end / piano_roll.tatum) + 1,
                          x_tick_step / piano_roll.tatum)
        ticks -= 0.5
        plt.xticks(ticks)
    else:
        # Update the ticks
        x_ticks = plt.xticks()[0]
        plt.xticks(x_ticks - 0.5)

    if measure_width is not None:
        if measure_offset is None:
            measure_offset = TimeShift(0, 1)

        for i in np.arange(measure_offset // piano_roll.tatum, piano_roll.extension.time.end // piano_roll.tatum,
                           measure_width // piano_roll.tatum):
            plt.vlines(i-0.5, ymin=-1, ymax=len(freq_vector))
            plt.text(i - 0.5, len(freq_vector) + 1,
                     str(measure_number_offset + 1 + i // (measure_width // piano_roll.tatum)))

    # Update the limits
    if tight_frame:
        plt.xlim([-0.5, piano_roll.array.shape[1] - 0.5])
        plt.ylim([-0.5, piano_roll.array.shape[0] - 0.5])
    else:
        plt.xlim([-1.5, piano_roll.array.shape[1] + 0.5])
        plt.ylim([-1.5, piano_roll.array.shape[0] + 0.5])

    # Tight layout
    plt.tight_layout()

    return fig
