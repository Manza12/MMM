from .. import *

from ..plot import plot_stft, plot_lines, plot_two_spectrogram
from ..processing import apply_reconstruction_by_erosion, apply_opening
from ..parameters import MIN_DB
from ..utils import get_duration


def plot_single(spectrogram, name, title, images_folder, v_min=MIN_DB, v_max=0, c_map='afmhot', phd=None):
    fig = plot_stft(spectrogram.cpu().numpy(), v_min=v_min, v_max=v_max, c_map=c_map, title=title)

    fig.savefig(images_folder / (name + '.png'), dpi=300)

    if phd is not None:
        from mmm.spectrograms.parameters import TIME_RESOLUTION, FREQUENCY_PRECISION
        fig.axes[0].set_xlim(phd['x_lim'][0] / TIME_RESOLUTION, phd['x_lim'][1] / TIME_RESOLUTION)
        fig.axes[0].set_ylim(phd['y_lim'][0] / FREQUENCY_PRECISION, phd['y_lim'][1] / FREQUENCY_PRECISION)
        phd_folder = images_folder / 'phd'
        phd_folder.mkdir(parents=True, exist_ok=True)
        fig.savefig(phd_folder / (phd['name'] + '.eps'), dpi=300)

    return fig


def plot_compare(spectrogram_1, spectrogram_2, name, title, images_folder,
                 v_min_1=MIN_DB, v_max_1: Optional[int] = 0, v_min_2=MIN_DB, v_max_2: Optional[int] = 0,
                 c_map_1='afmhot', c_map_2='afmhot', phd=None):
    fig = plot_two_spectrogram(spectrogram_1.cpu().numpy(), spectrogram_2.cpu().numpy(),
                               v_min_1=v_min_1, v_max_1=v_max_1, v_min_2=v_min_2, v_max_2=v_max_2,
                               c_map_1=c_map_1, c_map_2=c_map_2, title=title,
                               fig_size=phd.get('fig_size', (8., 4.)),
                               sharexy=phd.get('sharexy', False) if phd is not None else False,
                               cb_1=phd.get('cb_1', True) if phd is not None else True,
                               cb_2=phd.get('cb_2', True) if phd is not None else True,
                               full_screen=False)
    fig.savefig(images_folder / (name + '.png'), dpi=300)

    if phd is not None:
        from ..parameters import TIME_RESOLUTION, FREQUENCY_PRECISION

        fig.axes[0].set_xlim(phd['x_lim'][0] / TIME_RESOLUTION, phd['x_lim'][1] / TIME_RESOLUTION)
        fig.axes[0].set_ylim(phd['y_lim'][0] / FREQUENCY_PRECISION, phd['y_lim'][1] / FREQUENCY_PRECISION)

        fig.axes[1].set_xlim(phd['x_lim'][0] / TIME_RESOLUTION, phd['x_lim'][1] / TIME_RESOLUTION)
        fig.axes[1].set_ylim(phd['y_lim'][0] / FREQUENCY_PRECISION, phd['y_lim'][1] / FREQUENCY_PRECISION)

        phd_folder = images_folder / 'phd'
        phd_folder.mkdir(parents=True, exist_ok=True)

        dpi = 300

        x_border = 4.
        bbox_0 = mpl.transforms.Bbox([[0., 0.], [x_border, 4.]])
        bbox_1 = mpl.transforms.Bbox([[x_border, 0.], [8., 4.]])

        fig.savefig(phd_folder / (phd['name'] + '_0.eps'), dpi=dpi, bbox_inches=bbox_0)
        fig.savefig(phd_folder / (phd['name'] + '_1.eps'), dpi=dpi, bbox_inches=bbox_1)

    return fig


def plot_input_lines(lines, filtered_lines, spectrogram, images_folder, phd=None):
    fig = plot_stft(spectrogram.cpu().numpy(), v_min=MIN_DB, v_max=0, c_map='afmhot', title='Input + lines',
                    full_screen=False, fig_size=phd.get('fig_size', (6., 4.)),
                    cb=phd.get('cb', True) if phd is not None else True)

    plot_lines(lines, fig, 'b', phd=phd, label='Lines')
    plot_lines(filtered_lines, fig, 'c', phd=phd, label='Filtered lines')

    plt.legend()

    if phd is not None:
        from ..parameters import TIME_RESOLUTION, FREQUENCY_PRECISION

        fig.axes[0].set_xlim(phd['x_lim'][0] / TIME_RESOLUTION, phd['x_lim'][1] / TIME_RESOLUTION)
        fig.axes[0].set_ylim(phd['y_lim'][0] / FREQUENCY_PRECISION, phd['y_lim'][1] / FREQUENCY_PRECISION)

        phd_folder = images_folder / 'phd'
        phd_folder.mkdir(parents=True, exist_ok=True)

        dpi = 300

        plt.tight_layout()

        fig.savefig(phd_folder / (phd['name'] + '.svg'), dpi=dpi)


def plot_input(spectrograms, plot, images_folder):
    spectrogram = spectrograms['input']
    spectrogram_reconstruction_erosion = spectrograms['reconstruction_erosion']

    # Input spectrogram
    if plot['input']:
        plot_single(spectrogram, 'input', 'Input', images_folder)

    # Filled spectrogram
    if plot['reconstruction_erosion']:
        plot_compare(spectrogram, spectrogram_reconstruction_erosion, 'reconstruction_erosion',
                     'Reconstruction by erosion', images_folder)


def plot_noise(spectrograms, plot, images_folder):
    spectrogram = spectrograms['input']
    spectrogram_reconstruction_erosion = spectrograms['reconstruction_erosion']
    spectrogram_opening = spectrograms['opening']
    spectrogram_erosion = spectrograms['erosion']
    spectrogram_filtered_noise = spectrograms['filtered_noise']

    # Opening spectrogram
    if plot['opening']:
        plot_compare(spectrogram_reconstruction_erosion, spectrogram_opening, 'opening', 'Opening', images_folder)

    # Erosion spectrogram
    if plot['erosion']:
        plot_compare(spectrogram_opening, spectrogram_erosion, 'erosion', 'Erosion', images_folder)
        plot_compare(spectrogram, spectrogram_filtered_noise, 'input_noise', 'Input - Noise', images_folder)

    # Filtered noise spectrogram
    if plot['filtered_noise']:
        plot_compare(spectrogram_opening, spectrogram_filtered_noise, 'filtered_noise', 'Filtered noise', images_folder)

    # Input - Noise spectrogram
    if plot['input_noise']:
        plot_compare(spectrogram, spectrogram_filtered_noise, 'input_noise', 'Input - Noise', images_folder)


def plot_sinusoids(lines, spectrograms, plot, images_folder):
    # Erosion spectrogram
    if plot['erosion_reconstruction']:
        plot_compare(spectrograms['reconstruction_erosion'], spectrograms['erosion_reconstruction'],
                     'erosion_reconstruction', 'Reconstruction - Erosion', images_folder)

    # Vertical thinning spectrogram
    if plot['vertical_thin']:
        plot_compare(spectrograms['erosion_reconstruction'], spectrograms['vertical_thin'], 'vertical_thin',
                     'Vertical thinning', images_folder)

    # Vertical top-hat spectrogram
    if plot['vertical_top_hat']:
        plot_compare(spectrograms['vertical_thin'], spectrograms['vertical_top_hat'], 'vertical_top_hat',
                     'Vertical top-hat', images_folder, v_min_2=0, v_max_2=None, c_map_2='Greys')

    # Vertical threshold spectrogram
    if plot['vertical_threshold']:
        plot_compare(spectrograms['vertical_top_hat'], spectrograms['vertical_threshold'], 'vertical_threshold',
                     'Vertical threshold', images_folder, v_min_1=0, v_max_1=None, c_map_1='Greys')

    # Horizontal filtering spectrogram
    if plot['horizontal_filtered']:
        plot_compare(spectrograms['vertical_threshold'], spectrograms['horizontal_filtered'], 'horizontal_filtered',
                     'Horizontal filtered', images_folder)

    # Lines - Sinusoids
    if plot['lines_sinusoids']:
        lines_sinusoids = lines['sinusoids']
        filtered_lines_sinusoids = lines['filtered_sinusoids']
        spectrogram = spectrograms['input']

        fig = plot_stft(spectrogram.cpu().numpy(), v_min=MIN_DB, v_max=0, c_map='afmhot',
                        title='Input + lines sinusoids')

        plot_lines(lines_sinusoids, fig=fig, color='b')
        plot_lines(filtered_lines_sinusoids, fig=fig, color='w')

    # Input - Sinusoids spectrogram
    if plot['input_sinusoids']:
        plot_compare(spectrograms['input'], spectrograms['sinusoids'], 'input_sinusoids', 'Input - Sinusoids',
                     images_folder)


def plot_transient(lines, signals, spectrograms, plot, images_folder):
    spectrogram = spectrograms['input']
    spectrogram_reconstruction_erosion = spectrograms['reconstruction_erosion']
    spectrogram_horizontal_link = spectrograms['horizontal_link']
    spectrogram_transient = spectrograms['transient']
    spectrogram_top_hat_transient = spectrograms['top_hat_transient']
    spectrogram_closing_transient = spectrograms['closing_transient']
    spectrogram_horizontal_thin = spectrograms['horizontal_thin']

    # Top hat transient spectrogram
    if plot['top_hat_transient']:
        plot_compare(spectrogram_reconstruction_erosion, spectrogram_top_hat_transient, 'top_hat_transient',
                     'Top hat transient', images_folder)

    # Closing transient spectrogram
    if plot['closing_transient']:
        plot_compare(spectrogram_top_hat_transient, spectrogram_closing_transient, 'closing_transient',
                     'Closing transient',
                     images_folder)

    # Horizontal thinning spectrogram
    if plot['horizontal_thin']:
        plot_compare(spectrogram_closing_transient, spectrogram_horizontal_thin, 'horizontal_thin',
                     'Horizontal thinning',
                     images_folder)

    # Horizontal link spectrogram
    if plot['horizontal_link']:
        plot_compare(spectrogram_horizontal_thin, spectrogram_horizontal_link, 'horizontal_link', 'Horizontal link',
                     images_folder)

    # Lines - Transient
    if plot['lines_transient']:
        lines_transient = lines['transient']
        sinusoids = signals['sinusoids']
        plot_lines(lines_transient, x_lim=[0., get_duration(sinusoids)])

    # Link - Transient spectrogram
    if plot['horizontal_link']:
        plot_compare(spectrogram_horizontal_link, spectrogram_transient, 'link_transient', 'Link - Transient',
                     images_folder)

    # Input - Transient spectrogram
    if plot['input_transient']:
        plot_compare(spectrogram, spectrogram_transient, 'input_transient', 'Input - Transient', images_folder)


def plot_output(spectrograms, plot, images_folder):
    spectrogram = spectrograms['input']
    spectrogram_output = spectrograms['output']

    # Input - Output spectrogram
    if plot['input_output']:
        plot_compare(spectrogram, spectrogram_output, 'input_output', 'Input - Output', images_folder)


def plot_all(lines, signals, spectrograms, plot, components, paths):
    if components['input']:
        plot_input(spectrograms, plot, paths['images_folder'])
    if components['noise']:
        plot_noise(spectrograms, plot, paths['images_folder'])
    if components['sinusoids']:
        plot_sinusoids(lines, spectrograms, plot, paths['images_folder'])
    if components['transient']:
        plot_transient(lines, signals, spectrograms, plot, paths['images_folder'])
    if components['output']:
        plot_output(spectrograms, plot, paths['images_folder'])

    plt.show()


def plot_input_phd(spectrograms, plot, images_folder, settings):
    # Input spectrogram
    if plot['input']:
        plot_single(spectrograms['input'], 'input', 'Input', images_folder,
                    phd=settings['input'])

    # Reconstruction by erosion spectrogram
    if plot['reconstruction_erosion']:
        plot_compare(spectrograms['input'], spectrograms['reconstruction_erosion'], 'reconstruction_erosion',
                     'Reconstruction by erosion', images_folder,
                     phd=settings['reconstruction_erosion'])

    # Erosion spectrogram
    if plot['erosion']:
        plot_compare(spectrograms['reconstruction_erosion'], spectrograms['erosion'],
                     'erosion', 'Erosion', images_folder,
                     phd={'x_lim': (0.08, 0.16), 'y_lim': (500, 1000), 'name': 'erosion'})


def plot_noise_phd(spectrograms, plot, images_folder, settings):
    # Opening spectrogram
    if plot['opening']:
        plot_compare(spectrograms['erosion'], spectrograms['opening'],
                     'opening', 'Opening', images_folder,
                     phd=settings['opening'])

    # White noise spectrogram
    if plot['white_noise']:
        plot_single(spectrograms['white_noise'],
                    'white_noise', 'White Noise', images_folder,
                    v_min=-60, v_max=10,
                    phd=settings['white_noise'])
        plot_single(spectrograms['white_noise'], 'white_noise_zoom', 'White Noise Zoom', images_folder,
                    v_min=-60, v_max=10,
                    phd=settings['white_noise_zoom'])
        spectrogram_white_noise_reconstruction_erosion = \
            apply_reconstruction_by_erosion(spectrograms['white_noise'], verbose=False)
        plot_single(spectrogram_white_noise_reconstruction_erosion, 'white_noise_reconstruction_erosion',
                    'White Noise Filled', images_folder, v_min=-60, v_max=10,
                    phd=settings['white_noise_zoom'])
        spectrogram_white_noise_opening = apply_opening(spectrogram_white_noise_reconstruction_erosion, verbose=False)
        plot_single(spectrogram_white_noise_opening,
                    'white_noise_opening', 'White Noise Opening', images_folder,
                    v_min=-60, v_max=10,
                    phd=settings['white_noise_zoom'])
        spectrogram_white_noise_raw_opening = apply_opening(spectrograms['white_noise'], verbose=False)
        plot_single(spectrogram_white_noise_raw_opening,
                    'white_noise_opening_raw', 'White Noise Opening raw', images_folder,
                    v_min=-60, v_max=10,
                    phd=settings['white_noise_zoom'])

    # Filtered noise spectrogram
    if plot['filtered_noise']:
        plot_compare(spectrograms['opening'], spectrograms['filtered_noise'],
                     'filtered_noise', 'Filtered noise', images_folder)

        plot_compare(spectrograms['opening'], spectrograms['filtered_noise'],
                     'input_noise', 'Input - Noise', images_folder,
                     phd=settings['erosion_noise_zoom'])

    # Input - Noise spectrogram
    if plot['input_noise']:
        plot_compare(spectrograms['input'], spectrograms['filtered_noise'],
                     'input_noise', 'Input - Noise', images_folder,
                     phd=settings['input_noise'])


def plot_sinusoids_phd(lines, spectrograms, plot, images_folder, settings):
    # Vertical thinning spectrogram
    if plot['vertical_thin']:
        plot_compare(spectrograms['reconstruction_erosion'], spectrograms['vertical_thin'],
                     'vertical_thin', 'Vertical thinning', images_folder,
                     phd=settings['vertical_thin'])

    # Vertical top-hat spectrogram
    if plot['vertical_top_hat']:
        plot_compare(spectrograms['vertical_thin'], spectrograms['vertical_top_hat'],
                     'vertical_top_hat', 'Vertical top-hat', images_folder,
                     v_min_2=0, v_max_2=None, c_map_2='Greys',
                     phd=settings['vertical_top_hat'])

    # Vertical threshold spectrogram
    if plot['vertical_threshold']:
        plot_compare(spectrograms['vertical_top_hat'], spectrograms['vertical_threshold'], 'vertical_threshold',
                     'Vertical threshold', images_folder, v_min_1=0, v_max_1=None, c_map_1='Greys',
                     phd=settings['vertical_threshold'])

    # Horizontal filtered
    if plot['horizontal_filtered']:
        plot_compare(spectrograms['vertical_threshold'], spectrograms['horizontal_filtered'], 'horizontal_filtered',
                     'Horizontal filtered', images_folder,
                     phd=settings['horizontal_filtered'])

    # Lines - Sinusoids
    if plot['lines_sinusoids']:
        plot_input_lines(lines['sinusoids'], lines['filtered_sinusoids'], spectrograms['input'], images_folder,
                         phd=settings['lines_sinusoids'])

    # Input - Sinusoids spectrogram
    if plot['input_sinusoids']:
        plot_compare(spectrograms['input'], spectrograms['sinusoids'],
                     'input_sinusoids', 'Input - Sinusoids', images_folder,
                     phd=settings['input_sinusoids'])


def plot_transient_phd(lines, spectrograms, plot, images_folder, settings):
    # Horizontal thinning spectrogram
    if plot['horizontal_thin']:
        plot_compare(spectrograms['reconstruction_erosion'], spectrograms['horizontal_thin'],
                     'horizontal_thin', 'Horizontal thinning', images_folder,
                     phd=settings['horizontal_thin'])

    # Horizontal top-hat spectrogram
    if plot['horizontal_top_hat']:
        plot_compare(spectrograms['horizontal_thin'], spectrograms['horizontal_top_hat'],
                     'horizontal_top_hat', 'Horizontal top-hat', images_folder,
                     v_min_2=0, v_max_2=None, c_map_2='Greys',
                     phd=settings['horizontal_top_hat'])

    # Horizontal threshold spectrogram
    if plot['horizontal_threshold']:
        plot_compare(spectrograms['horizontal_top_hat'], spectrograms['horizontal_threshold'], 'horizontal_threshold',
                     'Horizontal threshold', images_folder, v_min_1=0, v_max_1=None, c_map_1='Greys',
                     phd=settings['horizontal_threshold'])

    # Vertical filtered
    if plot['vertical_filtered']:
        plot_compare(spectrograms['horizontal_threshold'], spectrograms['vertical_filtered'], 'vertical_filtered',
                     'Vertical filtered', images_folder,
                     phd=settings['vertical_filtered'])

    # Lines - Transient
    if plot['lines_transient']:
        plot_input_lines(lines['transient'], lines['filtered_transient'], spectrograms['input'], images_folder,
                         phd=settings['lines_transient'])

    # Input - Transient spectrogram
    if plot['input_transient']:
        plot_compare(spectrograms['input'], spectrograms['transient'],
                     'input_transient', 'Input - Transient', images_folder,
                     phd=settings['input_transient'])


def plot_output_phd(spectrograms, plot, images_folder):
    # Input - Output spectrogram
    if plot['input_output']:
        plot_compare(spectrograms['input'], spectrograms['output'], 'input_output', 'Input - Output', images_folder)


def plot_phd(lines, spectrograms, plot, components, paths, settings):
    if components['input']:
        plot_input_phd(spectrograms, plot, paths['images_folder'], settings)
    if components['noise']:
        plot_noise_phd(spectrograms, plot, paths['images_folder'], settings)
    if components['sinusoids']:
        plot_sinusoids_phd(lines, spectrograms, plot, paths['images_folder'], settings)
    if components['transient']:
        plot_transient_phd(lines, spectrograms, plot, paths['images_folder'], settings)
    if components['output']:
        plot_output_phd(spectrograms, plot, paths['images_folder'])

    plt.show()
