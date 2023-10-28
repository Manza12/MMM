from . import *
from .graphs import ActivationsGraph, TonalGraph
from .music import TimePoint, PianoRoll, ChromaRoll, ActivationsStack, TimeSeconds
from .utils import round_half_up


def format_freq(x, pos, freq_names):
    if pos:
        pass
    n = int(round(x))
    return freq_names[n]


def format_time(x, pos, time_names):
    if pos:
        pass
    n = int(round_half_up(x))
    return time_names[n]


def plot_activations(a, t, f, fig_title=None, full_screen=False, fig_size=(640, 480),
                     freq_label='Frequency (Hz)', time_label='Time (s)', dpi=120,
                     grid_t=False, grid_f=False,
                     marker_color: Optional[str] = 'r', marker_size=None,
                     ax=None):

    if ax is None:
        fig = plt.figure(figsize=(fig_size[0] / dpi, fig_size[1] / dpi), dpi=dpi)

        if fig_title:
            fig.suptitle(fig_title)

        ax = fig.add_subplot(111)
    else:
        fig = ax.get_figure()

    activations = np.where(a)
    ax.scatter(activations[1] - 0.5, activations[0], c=marker_color, s=marker_size, marker='x')

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
        v_min = min(v_min, 0)
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


def plot_piano_roll(piano_roll: PianoRoll,
                    freq_label: Optional[str] = None, time_label: Optional[str] = None,
                    colorbar=True, colorbar_ticks=None, colorbar_labels=None,
                    x_tick_start=None, x_tick_step=None,
                    y_tick_start=None, y_tick_step=None,
                    marker_color='r', marker_size=None,
                    tight_frame=True,
                    **kwargs):
    if time_label is None:
        if isinstance(piano_roll.origin.time, TimeSeconds):
            time_label = 'Time (s)'
        else:
            time_label = 'Time (wholes)'
    elif time_label in ['Time (m, b)', 'Temps (mesure, temps)']:
        TimePoint.__str__ = lambda self: f'({self.measure}, {self.beat})'
    elif time_label in ['Time (m)', 'Temps (mesure)']:
        TimePoint.__str__ = lambda self: f'{self.measure}'

    if freq_label is None:
        if piano_roll.frequency_nature == 'point':
            if isinstance(piano_roll, ChromaRoll):
                freq_label = 'Chroma'
            else:
                freq_label = 'Pitch'
        else:
            freq_label = 'Shift (semitones)'

    if piano_roll.array.dtype == bool:
        fig = plot_activations(piano_roll.array, piano_roll.time_vector, piano_roll.frequency_vector,
                               freq_label=freq_label, time_label=time_label,
                               marker_color=marker_color, marker_size=marker_size,
                               **kwargs)
    else:
        if piano_roll.dynamics is None:
            fig = plot_time_frequency(piano_roll.array, piano_roll.time_vector, piano_roll.frequency_vector,
                                      freq_label=freq_label, time_label=time_label,
                                      colorbar=colorbar, colorbar_ticks=colorbar_ticks, colorbar_labels=colorbar_labels,
                                      **kwargs)
        else:
            fig = plot_time_frequency(piano_roll.array[1, :, :], piano_roll.time_vector, piano_roll.frequency_vector,
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
        # For Activations with zero tatum
        if x_tick_step / piano_roll.tatum == 0:
            ticks = np.array([0.])
        else:
            ticks = np.arange((x_tick_start - piano_roll.extension.time.start) / piano_roll.tatum,
                              (piano_roll.extension.time.end - piano_roll.extension.time.start) / piano_roll.tatum + 1,
                              x_tick_step / piano_roll.tatum)
        ticks -= 0.5
        plt.xticks(ticks)
    else:
        # Update the ticks
        x_ticks = plt.xticks()[0]
        plt.xticks(x_ticks - 0.5)

    if y_tick_step is not None:
        if y_tick_start is None:
            y_tick_start = piano_roll.extension.frequency.lower

        start = (y_tick_start - piano_roll.extension.frequency.lower) / piano_roll.step
        end = (piano_roll.extension.frequency.higher - piano_roll.extension.frequency.lower) / piano_roll.step
        step = y_tick_step / piano_roll.step
        ticks = np.arange(start, end + 1, step)
        plt.yticks(ticks)

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


def plot_activations_stack(activations_stack: ActivationsStack,
                           freq_label: Optional[str] = None, time_label: Optional[str] = None,
                           fig_size=(640, 480), fig_title=None, dpi=120,
                           x_tick_start=None, x_tick_step=None,
                           y_tick_start=None, y_tick_step=None,
                           marker_size=None,
                           tight_frame=True,
                           legend=False, legend_params=None,
                           **kwargs):
    if legend_params is None:
        legend_params = {}
    assert len(activations_stack) >= 1
    assert len({a.tatum for a in activations_stack if len(a) != 0}) == 1
    assert len({a.extension for a in activations_stack if len(a) != 0}) == 1
    assert len({a.frequency_nature for a in activations_stack if len(a) != 0}) == 1
    a_master = activations_stack[0]

    if time_label is None:
        time_label = 'Time (wholes)'
    elif time_label == 'Time (m, b)':
        TimePoint.__str__ = lambda self: f'({self.measure}, {self.beat})'
    elif time_label in ['Time (measure)', 'Temps (mesure)']:
        TimePoint.__str__ = lambda self: f'{self.measure}'

    if freq_label is None:
        if a_master.frequency_nature == 'point':
            if isinstance(a_master, ChromaRoll):
                freq_label = 'Chroma'
            else:
                freq_label = 'Pitch'
        else:
            freq_label = 'Shift (semitones)'

    assert a_master.array.dtype == bool
    fig = plt.figure(figsize=(fig_size[0] / dpi, fig_size[1] / dpi), dpi=dpi)

    if fig_title:
        fig.suptitle(fig_title)

    ax = fig.add_subplot(111)
    cm = plt.get_cmap('gist_rainbow')
    n_colors = len(activations_stack)
    ax.set_prop_cycle(color=[cm(1. * i / n_colors) for i in range(n_colors)])

    for activations in activations_stack:
        if len(activations) == 0:
            continue
        plot_activations(activations.array, activations.time_vector, activations.frequency_vector,
                         freq_label=freq_label, time_label=time_label,
                         marker_color=None, marker_size=marker_size,
                         ax=ax, **kwargs)

    if x_tick_step is not None:
        if x_tick_start is None:
            x_tick_start = TimePoint(0, 1)
        # For Activations with zero tatum
        if x_tick_step / activations_stack[0].tatum == 0:
            ticks = np.array([0.])
        else:
            ticks = np.arange((x_tick_start - a_master.extension.time.start) / a_master.tatum,
                              (a_master.extension.time.end - a_master.extension.time.start) / a_master.tatum + 1,
                              x_tick_step / a_master.tatum)
        ticks -= 0.5
        plt.xticks(ticks)
    else:
        # Update the ticks
        x_ticks = plt.xticks()[0]
        plt.xticks(x_ticks - 0.5)

    if y_tick_step is not None:
        if y_tick_start is None:
            y_tick_start = a_master.extension.frequency.lower

        start = (y_tick_start - a_master.extension.frequency.lower) / a_master.step
        end = (a_master.extension.frequency.higher - a_master.extension.frequency.lower) / a_master.step
        step = y_tick_step / a_master.step
        ticks = np.arange(start, end + 1, step)
        plt.yticks(ticks)

    if legend:
        if legend_params is None:
            legend_params = {}
        labels = legend_params.pop('labels', [r'$A_{%d}$' % (j + 1) for j in range(len(activations_stack))])

        if legend_params.pop('outside', False):
            # Put a legend to the right of the current axis
            box = ax.get_position()
            ax.set_position([box.x0, box.y0 + 0.08, box.width * 0.85, box.height])
            plt.legend(fig.axes[0].collections, labels, **legend_params,
                       loc='center left', bbox_to_anchor=(1, 0.5))
        else:
            plt.legend(fig.axes[0].collections, labels, **legend_params)

    # Update the limits
    if tight_frame:
        plt.xlim([-0.5, a_master.array.shape[1] - 0.5])
        plt.ylim([-0.5, a_master.array.shape[0] - 0.5])
    else:
        plt.xlim([-1.5, a_master.array.shape[1] + 0.5])
        plt.ylim([-1.5, a_master.array.shape[0] + 0.5])

    # Tight layout
    if legend_params.pop('outside', False):
        plt.tight_layout()

    return fig


def plot_activations_graph(graph: ActivationsGraph, fig_size=(9., 6.), pad_f=0.5, plot_edges=False,
                           node_font_size=12, grid_font_size=13, node_size=2500):
    fig = plt.figure(figsize=fig_size)

    # Compute number of elements
    n_elements = np.zeros_like(graph.array, dtype=int)
    for m in range(graph.array.shape[-2]):
        for n_s in range(graph.array.shape[-1]):
            n_elements[m, n_s] = len(graph.array[m, n_s])

    max_f = np.max(n_elements, axis=-1)
    offset = np.cumsum(max_f + pad_f * max_f.astype(bool))
    offset = np.concatenate(([0], offset))

    # Assign positions
    for m in range(graph.piano_roll.array.shape[-2]):
        for n_s in range(graph.piano_roll.array.shape[-1]):
            nodes = graph.array[m, n_s]
            for n, node in enumerate(nodes):
                y = n + offset[m] + (max_f[m] - n_elements[m, n_s]) / 2 + pad_f / 2
                graph.nodes[node]['pos'] = (n_s, y)

    # Plot graph
    pos = nx.get_node_attributes(graph, 'pos')
    labels = nx.get_node_attributes(graph, 'label')

    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=node_font_size)
    if plot_edges:
        nx.draw_networkx_edges(graph, pos, edge_color='k', arrows=True, node_size=node_size)

    # Grid
    plt.text(-0.75, -1.5, r'$t_P$', fontdict={'fontsize': grid_font_size}, ha='center', va='center')
    plt.text(-1., -1.5, r'/', fontdict={'fontsize': int(grid_font_size * 4 / 3)}, ha='center', va='center')
    plt.text(-1.25, -1.5, r'$\xi$', fontdict={'fontsize': grid_font_size}, ha='center', va='center')

    # Grid frequency
    for m in range(graph.piano_roll.array.shape[-2]):
        if max_f[m] == 0:
            continue
        xi = graph.piano_roll.origin.frequency + m * graph.piano_roll.step
        y = offset[m] + (max_f[m] - 1) / 2 + pad_f / 2
        plt.text(-1., y, str(xi), ha='center', va='center', fontdict={'fontsize': grid_font_size})

        # Plot horizontal lines
        y = offset[m] - 0.5
        plt.plot([-1.5, graph.piano_roll.array.shape[-1] - 0.5], [y, y], 'k--', linewidth=0.5)

    # Plot last horizontal line
    y = offset[-1] - 0.5
    plt.plot([-1.5, graph.piano_roll.array.shape[-1] - 0.5], [y, y], 'k--', linewidth=0.5)

    # Grid time
    for n in range(graph.piano_roll.array.shape[-1]):
        t = graph.piano_roll.origin.time + n * graph.piano_roll.tatum
        plt.text(n, -1.5, r'$%s$' % t, ha='center', va='center',
                 fontdict={'fontsize': grid_font_size})

        # Plot vertical lines
        x = n - 0.5
        plt.plot([x, x], [-2, offset[-1] - 0.5], 'k--', linewidth=0.5)

    # Plot last vertical line
    x = graph.piano_roll.array.shape[-1] - 0.5
    plt.plot([x, x], [-2, offset[-1] - 0.5], 'k--', linewidth=0.5)

    # Adjust limits
    x_lim = [-1.5, graph.piano_roll.array.shape[-1] - 0.4]
    y_lim = [-2, offset[-1] - 0.5]

    plt.xlim(x_lim)
    plt.ylim(y_lim)

    plt.tight_layout()
    plt.axis('off')

    return fig


def plot_tonal_graph(graph: TonalGraph, fig_size=(8., 4.), pad_f=0., shortest_path=None, weighted=False):
    fig = plt.figure(figsize=fig_size)

    # Compute number of elements
    n_elements = np.zeros_like(graph.array, dtype=np.int16)
    for m in range(graph.array.shape[-2]):
        for n_s in range(graph.array.shape[-1]):
            n_elements[m, n_s] = len(graph.array[m, n_s])

    max_f = np.max(n_elements, axis=-1)
    offset = np.cumsum(max_f + pad_f * max_f.astype(bool))
    offset = np.concatenate(([0], offset))

    # Assign positions
    for m in range(graph.activations.array.shape[-2]):
        for n_s in range(graph.activations.array.shape[-1]):
            nodes = graph.array[m, n_s]
            for n, node in enumerate(nodes):
                y = n + offset[m] + (max_f[m] - n_elements[m, n_s]) / 2 + pad_f / 2
                graph.nodes[node]['pos'] = (n_s, y)

    if shortest_path is not None:
        graph.nodes['S']['pos'] = (-0.5, offset[-1] / 2 + pad_f / 2)
        graph.nodes['E']['pos'] = (graph.activations.array.shape[-1], offset[-1] / 2 + pad_f / 2)

    # Plot graph
    pos = nx.get_node_attributes(graph, 'pos')
    labels = nx.get_node_attributes(graph, 'label')

    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=12)

    if weighted:
        modulation_list = []
        continuation_list = []
        artificial_list = []
        for edge in graph.edges:
            if edge[0] == 'S' or edge[1] == 'E':
                artificial_list.append(edge)
            elif edge[0][1] == edge[1][1]:
                continuation_list.append(edge)
            else:
                modulation_list.append(edge)

        artificial_artist = nx.draw_networkx_edges(graph, pos, edgelist=artificial_list,
                                                   width=0.8, style='dashed', node_size=750)
        modulation_artist = nx.draw_networkx_edges(graph, pos, edgelist=modulation_list,
                                                   width=0.2, node_size=750)
        continuation_artist = nx.draw_networkx_edges(graph, pos, edgelist=continuation_list,
                                                     width=2, node_size=750)
    else:
        nx.draw_networkx_edges(graph, pos, node_size=750)
        artificial_artist = None
        modulation_artist = None
        continuation_artist = None

    if shortest_path is not None:
        edge_list = [(shortest_path[i], shortest_path[i+1]) for i in range(len(shortest_path)-1)]
        shortest_artist = nx.draw_networkx_edges(graph, pos, edgelist=edge_list,
                                                 edge_color='r', width=3, node_size=750)
    else:
        shortest_artist = None

    # Limits
    x_lim = (-1, graph.array.shape[1]-0.5)
    plt.xlim(x_lim)
    y_lim = (-1, np.sum(graph.offsets)-0.5)
    plt.ylim(y_lim)

    # Grid time
    for n in range(graph.activations.array.shape[-1]):
        t = graph.activations.origin.time + n * graph.activations.tatum
        plt.text(n, -1, '%s' % t, ha='center', va='center')

    # Plot vertical line
    x = 0 - 0.75
    plt.plot([x, x], [-2, offset[-1] - 0.5], 'k--', linewidth=0.5)

    # Grid frequency
    for m in range(graph.activations.array.shape[-2]):
        if max_f[m] == 0:
            continue
        xi = graph.activations.origin.frequency + m * graph.activations.step
        y = offset[m] + (max_f[m] - 1) / 2 + pad_f / 2
        plt.text(-1., y, str(xi), ha='center', va='center')

        # Plot horizontal lines
        y = offset[m] - 0.5
        plt.plot([-1.5, graph.activations.array.shape[-1] - 0.5], [y, y], 'k--', linewidth=0.5)

    plt.text(-1, -1, r'$t/\xi$', ha='center', va='center', fontdict={'fontsize': 15})

    if shortest_path is not None:
        import matplotlib.patches as patches
        from matplotlib.legend_handler import HandlerPatch

        class ArrowHandler(HandlerPatch):
            def create_artists(self, legend, orig_handle, x_descent, y_descent, width, height, font_size, trans):
                p = patches.Arrow(0, 3, 15, 0, color='r', width=5)
                self.update_prop(p, orig_handle, legend)
                p.set_transform(trans)
                return [p]

        class DashedArrowHandler(HandlerPatch):
            def create_artists(self, legend, orig_handle, x_descent, y_descent, width, height, font_size, trans):
                p = patches.Arrow(0, 3, 15, 0, width=5)
                self.update_prop(p, orig_handle, legend)
                p.set_transform(trans)
                return [p]

        if weighted:
            plt.legend([artificial_artist[0], modulation_artist[0], continuation_artist[0], shortest_artist[0]],
                       ['Artificiel', 'Modulation', 'Même tonique', 'Plus court chemin'], loc='upper center',
                       handler_map={artificial_artist[0]: DashedArrowHandler(),
                                    modulation_artist[0]: ArrowHandler(),
                                    continuation_artist[0]: ArrowHandler(),
                                    shortest_artist[0]: ArrowHandler()},
                       ncol=4)
        else:
            plt.legend(shortest_artist, ['Shortest path'], loc='upper right',
                       handler_map={shortest_artist[0]: ArrowHandler()})

    # Adjust limits
    x_lim = [-1.5, graph.activations.array.shape[-1] - 0.4 + 1]
    y_lim = [-2, offset[-1] - 0.5 + 1.5]

    plt.xlim(x_lim)
    plt.ylim(y_lim)

    plt.tight_layout()
    plt.axis('off')

    return fig
