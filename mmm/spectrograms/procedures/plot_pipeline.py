from mmm.spectrograms import *
from mmm.spectrograms.plot import plot_stft, plot_lines, plot_two_spectrogram
from mmm.spectrograms.parameters import MIN_DB


def plot_single(spectrogram, name, title, images_folder, v_min: Optional[float] = MIN_DB, v_max: Optional[float] = 0,
                c_map='afmhot', paper=None):
    if v_min is None:
        v_min = spectrogram.min()
    if v_max is None:
        v_max = spectrogram.max()
    fig = plot_stft(spectrogram.cpu().numpy(), v_min=v_min, v_max=v_max, c_map=c_map, title=title,
                    fig_size=paper.get('fig_size', (6., 4.)) if paper is not None else (6., 4.))

    if paper is not None:
        from mmm.spectrograms.parameters import TIME_RESOLUTION, FREQUENCY_PRECISION
        if paper.get('x_lim', None) is not None:
            fig.axes[0].set_xlim(paper['x_lim'][0] / TIME_RESOLUTION, paper['x_lim'][1] / TIME_RESOLUTION)
        if paper.get('y_lim', None) is not None:
            fig.axes[0].set_ylim(paper['y_lim'][0] / FREQUENCY_PRECISION, paper['y_lim'][1] / FREQUENCY_PRECISION)
        extension = paper.get('extension', 'pdf')
        fig.savefig(images_folder / (paper['name'] + '.' + extension), dpi=300)
    else:
        fig.savefig(images_folder / (name + '.pdf'), dpi=300)

    return fig


def plot_compare(spectrogram_1, spectrogram_2, name, title, images_folder,
                 v_min_1=MIN_DB, v_max_1: Optional[int] = 0, v_min_2=MIN_DB, v_max_2: Optional[int] = 0,
                 c_map_1='afmhot', c_map_2='afmhot', paper=None):
    fig_size = (8., 4.) if paper is None else paper.get('fig_size', (8., 4.))
    fig = plot_two_spectrogram(spectrogram_1.cpu().numpy(), spectrogram_2.cpu().numpy(),
                               v_min_1=v_min_1, v_max_1=v_max_1, v_min_2=v_min_2, v_max_2=v_max_2,
                               c_map_1=c_map_1, c_map_2=c_map_2, title=title,
                               fig_size=fig_size,
                               sharexy=paper.get('sharexy', True) if paper is not None else True,
                               cb_1=paper.get('cb_1', True) if paper is not None else True,
                               cb_2=paper.get('cb_2', True) if paper is not None else True,
                               full_screen=False)
    fig.savefig(images_folder / (name + '.pdf'), dpi=300)

    if paper is not None:
        from mmm.spectrograms.parameters import TIME_RESOLUTION, FREQUENCY_PRECISION

        if paper.get('x_lim', None) is not None:
            fig.axes[0].set_xlim(paper['x_lim'][0] / TIME_RESOLUTION, paper['x_lim'][1] / TIME_RESOLUTION)
            fig.axes[1].set_xlim(paper['x_lim'][0] / TIME_RESOLUTION, paper['x_lim'][1] / TIME_RESOLUTION)
        if paper.get('y_lim', None) is not None:
            fig.axes[0].set_ylim(paper['y_lim'][0] / FREQUENCY_PRECISION, paper['y_lim'][1] / FREQUENCY_PRECISION)
            fig.axes[1].set_ylim(paper['y_lim'][0] / FREQUENCY_PRECISION, paper['y_lim'][1] / FREQUENCY_PRECISION)

        dpi = 300

        x_border = fig_size[0] / 2
        bbox_0 = mpl.transforms.Bbox([[0., 0.], [x_border, fig_size[1]]])
        bbox_1 = mpl.transforms.Bbox([[x_border, 0.], fig_size])

        split_folder = images_folder / 'split'
        split_folder.mkdir(parents=True, exist_ok=True)

        extension = paper.get('extension', 'pdf')
        fig.savefig(split_folder / (paper['name'] + '_0.' + extension), dpi=dpi, bbox_inches=bbox_0)
        fig.savefig(split_folder / (paper['name'] + '_1.' + extension), dpi=dpi, bbox_inches=bbox_1)

    return fig


def plot_input_lines(horizontal_lines, vertical_lines, spectrogram, images_folder, paper=None):
    fig = plot_stft(spectrogram.cpu().numpy(), v_min=MIN_DB, v_max=0, c_map='afmhot', title='Input + lines',
                    full_screen=False, fig_size=paper.get('fig_size', (6., 4.)),
                    cb=paper.get('cb', True) if paper is not None else True)

    if paper is not None:
        if paper.get('horizontal', True):
            plot_lines(horizontal_lines, fig, 'b', paper=paper, label='Horizontal lines')
        if paper.get('vertical', True):
            plot_lines(vertical_lines, fig, 'c', paper=paper, label='Vertical lines')
    else:
        plot_lines(horizontal_lines, fig, 'b', label='Horizontal lines')
        plot_lines(vertical_lines, fig, 'c', label='Vertical lines')

    plt.legend(loc='upper right')

    if paper is not None:
        from mmm.spectrograms.parameters import TIME_RESOLUTION, FREQUENCY_PRECISION

        if paper.get('x_lim', None) is not None:
            fig.axes[0].set_xlim(paper['x_lim'][0] / TIME_RESOLUTION, paper['x_lim'][1] / TIME_RESOLUTION)
        if paper.get('y_lim', None) is not None:
            fig.axes[0].set_ylim(paper['y_lim'][0] / FREQUENCY_PRECISION, paper['y_lim'][1] / FREQUENCY_PRECISION)

        dpi = 300

        plt.tight_layout()

        if paper.get('extension', None) is not None:
            fig.savefig(images_folder / (paper['name'] + '.' + paper['extension']), dpi=dpi)
        else:
            fig.savefig(images_folder / (paper['name'] + '.pdf'), dpi=dpi)


def plot_input_lines_filtered(lines, filtered_lines, spectrogram, images_folder, paper=None):
    fig = plot_stft(spectrogram.cpu().numpy(), v_min=MIN_DB, v_max=0, c_map='afmhot', title='Input + lines',
                    full_screen=False, fig_size=paper.get('fig_size', (6., 4.)),
                    cb=paper.get('cb', True) if paper is not None else True)

    plot_lines(lines, fig, 'b', paper=paper, label='Lines')
    plot_lines(filtered_lines, fig, 'c', paper=paper, label='Filtered lines')

    plt.legend()

    if paper is not None:
        from mmm.spectrograms.parameters import TIME_RESOLUTION, FREQUENCY_PRECISION

        if paper.get('x_lim', None) is not None:
            fig.axes[0].set_xlim(paper['x_lim'][0] / TIME_RESOLUTION, paper['x_lim'][1] / TIME_RESOLUTION)
        if paper.get('y_lim', None) is not None:
            fig.axes[0].set_ylim(paper['y_lim'][0] / FREQUENCY_PRECISION, paper['y_lim'][1] / FREQUENCY_PRECISION)

        dpi = 300

        plt.tight_layout()

        fig.savefig(images_folder / (paper['name'] + '.pdf'), dpi=dpi)


def plot_input(spectrograms, images_folder, settings):
    # Input spectrogram
    if settings.get('input', None) is not None:
        plot_single(spectrograms['input'],
                    'input', 'Input', images_folder,
                    paper=settings['input'])

    # Noise zoom
    if settings.get('noise_zoom', None) is not None:
        plot_single(spectrograms['input'],
                    'noise_zoom', 'Noise zoom', images_folder,
                    paper=settings['noise_zoom'])

    # Closing spectrogram
    if settings.get('closing', None) is not None:
        if settings['closing'].get('single', False):
            plot_single(spectrograms['closing'], 'closing', 'Closing',
                        images_folder, paper=settings['closing'])
        else:
            plot_compare(spectrograms['input'], spectrograms['closing'],
                         'closing', 'Closing', images_folder,
                         paper=settings['closing'])

    # Reconstruction by erosion spectrogram
    if settings.get('reconstruction_erosion', None) is not None:
        if settings['reconstruction_erosion'].get('single', False):
            plot_single(spectrograms['reconstruction_erosion'],
                        'reconstruction_erosion', 'Reconstruction by erosion',
                        images_folder, paper=settings['reconstruction_erosion'])
        else:
            plot_compare(spectrograms['input'], spectrograms['reconstruction_erosion'],
                         'reconstruction_erosion', 'Reconstruction by erosion',
                         images_folder, paper=settings['reconstruction_erosion'])


def plot_input_defence(spectrograms, images_folder, settings):
    # Input spectrogram
    if settings.get('input', None) is not None:
        plot_single(spectrograms['input'],
                    'input', 'Input', images_folder,
                    paper=settings['input'])

    # Closing spectrogram
    if settings.get('closing', None) is not None:
        plot_single(spectrograms['closing'], 'closing', 'Closing',
                    images_folder, paper=settings['closing'])

    # Reconstruction by erosion spectrogram
    if settings.get('reconstruction_erosion', None) is not None:
        plot_single(spectrograms['reconstruction_erosion'],
                    'reconstruction_erosion', 'Reconstruction by erosion',
                    images_folder, paper=settings['closing'])


def plot_noise(spectrograms, images_folder, settings):
    # Opening spectrogram
    if settings.get('opening', None) is not None:
        plot_compare(spectrograms['reconstruction_erosion'], spectrograms['opening'],
                     'opening', 'Opening', images_folder,
                     paper=settings['opening'])

    # Filtered noise spectrogram
    if settings.get('filtered_noise', None) is not None:
        plot_compare(spectrograms['opening'], spectrograms['filtered_noise'],
                     'filtered_noise', 'Filtered noise', images_folder)

        plot_compare(spectrograms['opening'], spectrograms['filtered_noise'],
                     'input_noise', 'Input - Noise', images_folder,
                     paper=settings['erosion_noise_zoom'])

    # Input - Noise spectrogram
    if settings.get('input_noise', None) is not None:
        plot_compare(spectrograms['input'], spectrograms['filtered_noise'],
                     'input_noise', 'Input - Noise', images_folder,
                     paper=settings['input_noise'])


def plot_sinusoids(lines, spectrograms, images_folder, settings):
    # Vertical thinning spectrogram
    if settings.get('vertical_thin', None) is not None:
        if settings['vertical_thin'].get('single', False):
            plot_single(spectrograms['vertical_thin'],
                        'vertical_thin', 'Vertical thinning', images_folder,
                        paper=settings['vertical_thin'])
        else:
            plot_compare(spectrograms['reconstruction_erosion'], spectrograms['vertical_thin'],
                         'vertical_thin', 'Vertical thinning', images_folder,
                         paper=settings['vertical_thin'])

    # Vertical top-hat spectrogram
    if settings.get('vertical_top_hat', None) is not None:
        if settings['vertical_top_hat'].get('single', False):
            plot_single(spectrograms['vertical_top_hat'],
                        'vertical_top_hat', 'Vertical top-hat', images_folder,
                        v_min=0, v_max=None, c_map='Greys',
                        paper=settings['vertical_top_hat'])
        else:
            plot_compare(spectrograms['vertical_thin'], spectrograms['vertical_top_hat'],
                         'vertical_top_hat', 'Vertical top-hat', images_folder,
                         v_min_2=0, v_max_2=None, c_map_2='Greys',
                         paper=settings['vertical_top_hat'])

    # Vertical threshold spectrogram
    if settings.get('vertical_threshold', None) is not None:
        if settings['vertical_threshold'].get('single', False):
            plot_single(spectrograms['vertical_threshold'],
                        'vertical_threshold', 'Vertical threshold', images_folder,
                        paper=settings['vertical_threshold'])
        else:
            plot_compare(spectrograms['vertical_top_hat'], spectrograms['vertical_threshold'],
                         'vertical_threshold', 'Vertical threshold', images_folder,
                         v_min_1=0, v_max_1=None, c_map_1='Greys',
                         paper=settings['vertical_threshold'])

    # Horizontal filtered
    if settings.get('horizontal_filtered', None) is not None:
        plot_compare(spectrograms['vertical_threshold'], spectrograms['horizontal_filtered'],
                     'horizontal_filtered', 'Horizontal filtered', images_folder,
                     paper=settings['horizontal_filtered'])

    # Lines - Sinusoids
    if settings.get('lines_sinusoids', None) is not None:
        plot_input_lines_filtered(lines['sinusoids'], lines['filtered_sinusoids'], spectrograms['input'],
                                  images_folder,
                                  paper=settings['lines_sinusoids'])

    # Input - Sinusoids spectrogram
    if settings.get('input_sinusoids', None) is not None:
        plot_compare(spectrograms['input'], spectrograms['sinusoids'],
                     'input_sinusoids', 'Input - Sinusoids',
                     images_folder,
                     paper=settings['input_sinusoids'])


def plot_transient(lines, spectrograms, images_folder, settings):
    # Horizontal thinning spectrogram
    if settings.get('horizontal_thin', None) is not None:
        if settings['horizontal_thin'].get('single', False):
            plot_single(spectrograms['horizontal_thin'],
                        'horizontal_thin', 'Horizontal thinning', images_folder,
                        paper=settings['horizontal_thin'])
        else:
            plot_compare(spectrograms['reconstruction_erosion'], spectrograms['horizontal_thin'],
                         'horizontal_thin', 'Horizontal thinning',
                         images_folder,
                         paper=settings['horizontal_thin'])

    # Horizontal top-hat spectrogram
    if settings.get('horizontal_top_hat', None) is not None:
        if settings['horizontal_top_hat'].get('single', False):
            plot_single(spectrograms['horizontal_top_hat'],
                        'horizontal_top_hat', 'Horizontal top-hat', images_folder,
                        v_min=0, v_max=None, c_map='Greys',
                        paper=settings['horizontal_top_hat'])
        else:
            plot_compare(spectrograms['horizontal_thin'], spectrograms['horizontal_top_hat'],
                         'horizontal_top_hat', 'Horizontal top-hat',
                         images_folder,
                         v_min_2=0, v_max_2=None, c_map_2='Greys',
                         paper=settings['horizontal_top_hat'])

    # Horizontal threshold spectrogram
    if settings.get('horizontal_threshold', None) is not None:
        if settings['horizontal_threshold'].get('single', False):
            plot_single(spectrograms['horizontal_threshold'],
                        'horizontal_threshold', 'Horizontal threshold', images_folder,
                        paper=settings['horizontal_threshold'])
        else:
            plot_compare(spectrograms['horizontal_top_hat'], spectrograms['horizontal_threshold'],
                         'horizontal_threshold', 'Horizontal threshold',
                         images_folder,
                         v_min_1=0, v_max_1=None, c_map_1='Greys',
                         paper=settings['horizontal_threshold'])

    # Vertical filtered
    if settings.get('vertical_filtered', None) is not None:
        if settings['vertical_filtered'].get('single', False):
            plot_single(spectrograms['vertical_filtered'],
                        'vertical_filtered', 'Vertical filtered', images_folder,
                        paper=settings['vertical_filtered'])
        else:
            plot_compare(spectrograms['horizontal_threshold'], spectrograms['vertical_filtered'],
                         'vertical_filtered', 'Vertical filtered',
                         images_folder,
                         paper=settings['vertical_filtered'])

    # Lines - Transient
    if settings.get('lines_transient', None) is not None:
        plot_input_lines_filtered(lines['transient'], lines['filtered_transient'], spectrograms['input'],
                                  images_folder,
                                  paper=settings['lines_transient'])

    # Input - Transient spectrogram
    if settings.get('input_transient', None) is not None:
        plot_compare(spectrograms['input'], spectrograms['transient'],
                     'input_transient', 'Input - Transient',
                     images_folder,
                     paper=settings['input_transient'])


def plot_output(spectrograms, lines, images_folder, settings):
    # Input - lines
    if settings.get('input_lines', None) is not None:
        plot_input_lines(lines['sinusoids'], lines['transient'], spectrograms['input'],
                         images_folder,
                         paper=settings['input_lines'])

    # Input - Output spectrogram
    if settings.get('input_output', None) is not None:
        plot_compare(spectrograms['input'], spectrograms['output'],
                     'input_output', 'Input - Output',
                     images_folder,
                     paper=settings['input_output'])

    # Input - Denoised spectrogram
    if settings.get('input_denoised', None) is not None:
        plot_compare(spectrograms['input'], spectrograms['denoised'],
                     'input_denoised', 'Input - Denoised',
                     images_folder,
                     paper=settings['input_denoised'])


def plot_all(lines, spectrograms, components, paths, settings):
    if components['input']:
        plot_input(spectrograms, paths['images_folder'], settings['plot'])
    if components['noise']:
        plot_noise(spectrograms, paths['images_folder'], settings['plot'])
    if components['sinusoids']:
        plot_sinusoids(lines, spectrograms, paths['images_folder'], settings['plot'])
    if components['transient']:
        plot_transient(lines, spectrograms, paths['images_folder'], settings['plot'])
    if components['output']:
        plot_output(spectrograms, lines, paths['images_folder'], settings['plot'])

    plt.show()


def plot_defence(lines, spectrograms, components, paths, settings):
    if components['input']:
        plot_input_defence(spectrograms, paths['images_folder'], settings['plot'])
    if components['noise']:
        plot_noise(spectrograms, paths['images_folder'], settings['plot'])
    if components['sinusoids']:
        plot_sinusoids(lines, spectrograms, paths['images_folder'], settings['plot'])
    if components['transient']:
        plot_transient(lines, spectrograms, paths['images_folder'], settings['plot'])
    if components['output']:
        plot_output(spectrograms, lines, paths['images_folder'], settings['plot'])

    plt.show()
