woodblock = {
    'input': {
        'x_lim': (0., 0.6),
        'y_lim': (0, 17000),
        'name': 'input'
    },
    'reconstruction_erosion': {
        'x_lim': (0.2, 0.4),
        'y_lim': (1500, 2500),
        'name': 'reconstruction_erosion'
    },
    'erosion': {
        'x_lim': (0.08, 0.16),
        'y_lim': (500, 1000),
        'name': 'erosion'
    },
    'opening': {
        'x_lim': (0.075, 0.4),
        'y_lim': (0, 4000),
        'name': 'opening'
    },
    'white_noise': {
        'x_lim': (0., 0.6),
        'y_lim': (0, 20000),
        'name': 'white_noise'
    },
    'white_noise_zoom': {
        'x_lim': (0.1, 0.4),
        'y_lim': (1000, 2000),
        'name': 'white_noise_zoom'
    },
    'erosion_noise_zoom': {
        'x_lim': (0.08, 0.16),
        'y_lim': (500, 1000),
        'name': 'erosion_noise_zoom'
    },
    'input_noise': {
        'x_lim': (0., 0.6),
        'y_lim': (0, 17000),
        'name': 'input_noise'
    },
    'vertical_thin': {
        'x_lim': (0.1, 0.25),
        'y_lim': (250, 2000),
        'name': 'vertical_thin'
    },
    'vertical_top_hat': {
        'x_lim': (0.1, 0.25),
        'y_lim': (250, 2000),
        'name': 'vertical_top_hat'
    },
    'vertical_threshold': {
        'x_lim': (0.1, 0.25),
        'y_lim': (250, 2000),
        'name': 'vertical_threshold'
    },
    'horizontal_filtered': {
        'x_lim': (0.1, 0.25),
        'y_lim': (250, 2000),
        'name': 'horizontal_filtered'
    },
    'lines_sinusoids': {
        'x_lim': (0.1, 0.5),
        'y_lim': (250, 2000),
        'name': 'lines_sinusoids'
    },
    'horizontal_thin': {
        'x_lim': (0.08, 0.17),
        'y_lim': (0, 20000),
        'name': 'horizontal_thin',
        'fig_size': (5., 4.)
    },
    'horizontal_top_hat': {
        'x_lim': (0.08, 0.17),
        'y_lim': (0, 20000),
        'name': 'horizontal_top_hat',
        'fig_size': (5., 4.)
    },
    'horizontal_threshold': {
        'x_lim': (0.08, 0.17),
        'y_lim': (0, 20000),
        'name': 'horizontal_threshold',
        'fig_size': (5., 4.)
    },
    'vertical_filtered': {
        'x_lim': (0.08, 0.17),
        'y_lim': (0, 20000),
        'name': 'vertical_filtered',
        'fig_size': (5., 4.)
    },
    'lines_transient': {
        'x_lim': (0.05, 0.25),
        'y_lim': (0, 20000),
        'name': 'lines_transient',
        'fig_size': (4., 4.)
    },
    'input_transient': {
        'x_lim': (0., 0.6),
        'y_lim': (0, 20000),
        'name': 'input_transient'
    }
}


anastasia_excerpt = {
    'start': None,
    'end': None,
    'parameters': {},
    'plot': {
        # 'input': {
        #     'name': 'input',
        #     'x_lim': (0., 3.),
        #     'y_lim': (0, 2000),
        #     'fig_size': (10., 4.),
        #     'extension': 'svg',
        # },
        # 'closing': {
        #     'name': 'closing',
        #     'x_lim': (0., 3.),
        #     'y_lim': (0, 2000),
        #     'fig_size': (10., 4.),
        #     'single': True,
        #     'extension': 'svg',
        # },
        # 'reconstruction_erosion': {
        #     'name': 'reconstruction_erosion',
        #     'x_lim': (0., 3.),
        #     'y_lim': (0, 2000),
        #     'fig_size': (10., 4.),
        #     'single': True,
        #     'extension': 'svg',
        # },
        # 'vertical_thinning': {
        #     'name': 'vertical_thinning',
        #     'x_lim': (0., 3.),
        #     'y_lim': (0, 2000),
        #     'fig_size': (10., 4.),
        #     'single': True,
        #     'extension': 'svg',
        # },
        # 'vertical_top_hat': {
        #     'name': 'vertical_top_hat',
        #     'x_lim': (0., 3.),
        #     'y_lim': (0, 2000),
        #     'fig_size': (10., 4.),
        #     'single': True,
        #     'extension': 'svg',
        # },
        # 'vertical_threshold': {
        #     'name': 'vertical_threshold',
        #     'x_lim': (0., 3.),
        #     'y_lim': (0, 2000),
        #     'fig_size': (10., 4.),
        #     'single': True,
        #     'extension': 'svg',
        # },
        # 'horizontal_top_hat': {
        #     'name': 'horizontal_top_hat',
        #     'x_lim': (0., 3.),
        #     'y_lim': (0, 2000),
        #     'fig_size': (10., 4.),
        #     'single': True,
        #     'extension': 'svg',
        # },
        # 'horizontal_threshold': {
        #     'name': 'horizontal_threshold',
        #     'x_lim': (0., 3.),
        #     'y_lim': (0, 2000),
        #     'fig_size': (10., 4.),
        #     'single': True,
        #     'extension': 'svg',
        # },
        # 'vertical_filtered': {
        #     'name': 'vertical_filtered',
        #     'x_lim': (0., 3.),
        #     'y_lim': (0, 2000),
        #     'fig_size': (10., 4.),
        #     'single': True,
        #     'extension': 'svg',
        # },
        'opening': {
            'name': 'opening',
            'x_lim': (0., 3.),
            'y_lim': (0, 2000),
            'fig_size': (10., 4.),
            'single': True,
            'extension': 'svg',
        },
    }
}

marimba = {
    'lines_sinusoids': {
        'x_lim': (0.05, 0.6),
        'y_lim': (0, 4500),
        # 'sharexy': 'all',
        'fig_size': (4, 3),
        'full_screen': False,
        'name': 'lines_sinusoids'
    },
    'input_sinusoids': {
        'x_lim': (0.05, 0.6),
        'y_lim': (0, 3200),
        # 'sharexy': 'all',
        'fig_size': (6, 3),
        'name': 'input_sinusoids'
    },
    'lines_transient': {
        'x_lim': (0.05, 0.35),
        'y_lim': (0, 22050),
        # 'sharexy': 'all',
        'cb': False,
        'fig_size': (3., 4.),
        'full_screen': False,
        'name': 'lines_transient'
    },
    'input_transient': {
        'x_lim': (0., 0.2),
        'y_lim': (0, 22050),
        'fig_size': (4., 4.),
        'cb_1': False,
        'cb_2': True,
        # 'sharexy': 'all',
        'name': 'input_transient'
    },
}

gong = {
    'input_noise': {
        'x_lim': (0., 1.7),
        'y_lim': (0, 22050),
        # 'sharexy': 'all',
        'cb_1': False,
        'fig_size': (6., 3.),
        'full_screen': False,
        'name': 'input_noise'
    },
    'input_sinusoids': {
        'x_lim': (0., 1.7),
        'y_lim': (0, 22050),
        # 'sharexy': 'all',
        'fig_size': (6., 3.),
        'cb_1': False,
        'name': 'input_sinusoids'
    },
    'input_transient': {
        'x_lim': (0., 1.7),
        'y_lim': (0, 22050),
        # 'sharexy': 'all',
        'fig_size': (6., 3.),
        'cb_1': False,
        'name': 'input_transient'
    },
    'input_output': {
        'x_lim': (0., 1.75),
        'y_lim': (0, 22050),
        # 'sharexy': 'all',
        'full_screen': False,
        'name': 'input_output'
    },
}

violin = {
    'input_noise': {
        'x_lim': (0., 1.75),
        'y_lim': (0, 10000),
        # 'sharexy': 'all',
        'full_screen': False,
        'name': 'input_noise'
    },
    'input_sinusoids': {
        'x_lim': (0., 1.75),
        'y_lim': (0, 10000),
        # 'sharexy': 'all',
        'name': 'input_sinusoids'
    },
    'input_output': {
        'x_lim': (0., 1.75),
        'y_lim': (0, 10000),
        # 'sharexy': 'all',
        'full_screen': False,
        'name': 'input_output'
    },
}

violin_vibrato = {
    'lines_sinusoids': {
        'x_lim': (0.4, 1.2),
        'y_lim': (1000, 5500),
        # 'sharexy': 'all',
        'fig_size': (4., 4.),
        'full_screen': False,
        'name': 'lines_sinusoids'
    },
    'input_sinusoids': {
        'x_lim': (0.4, 1.2),
        'y_lim': (1000, 5500),
        # 'sharexy': 'all',
        'name': 'input_sinusoids'
    },
}


piano = {
    'input_sinusoids': {
        'x_lim': (0.3, 1.3),
        'y_lim': (0, 5000),
        'cb_1': False,
        # 'sharexy': 'all',
        'fig_size': (6, 3),
        'name': 'input_sinusoids'
    },
    'input_noise': {
        'x_lim': (0.3, 1.3),
        'y_lim': (0, 5000),
        'cb_1': False,
        # 'sharexy': 'all',
        'fig_size': (6, 3),
        'name': 'input_noise'
    },
    'input_transient': {
        'x_lim': (0.3, 1.3),
        'y_lim': (0, 5000),
        'cb_1': False,
        'fig_size': (6, 3),
        # 'sharexy': 'all',
        'name': 'input_transient'
    },
    'input_output': {
        'x_lim': (0.3, 1.3),
        'y_lim': (0, 5000),
        'cb_1': False,
        # 'sharexy': 'all',
        'name': 'input_output'
    },
}

interferences = {
    # 'input_sinusoids': {
    #     'x_lim': (0., 0.5),
    #     'y_lim': (0, 5000),
    #     'cb_1': False,
    #     'sharexy': 'all',
    #     'fig_size': (6, 3),
    #     'name': 'input_sinusoids'
    # },
    'vertical_thin': {
        'x_lim': (0., 0.5),
        'y_lim': (0, 2000),
        'name': 'vertical_thin'
    },
    'vertical_top_hat': {
        'x_lim': (0., 0.5),
        'y_lim': (0, 2000),
        'name': 'vertical_top_hat'
    },
    'vertical_threshold': {
        'x_lim': (0., 0.5),
        'y_lim': (0, 2000),
        'name': 'vertical_threshold'
    },
    'horizontal_filtered': {
        'x_lim': (0., 0.5),
        'y_lim': (0, 2000),
        'name': 'horizontal_filtered'
    },
    'lines_sinusoids': {
        'x_lim': (0., 0.5),
        'y_lim': (0, 2000),
        'name': 'lines_sinusoids'
    },
    # 'input_noise': {
    #     'x_lim': (0., 0.5),
    #     'y_lim': (0, 5000),
    #     'cb_1': False,
    #     'sharexy': 'all',
    #     'fig_size': (6, 3),
    #     'name': 'input_noise'
    # },
    # 'input_transient': {
    #     'x_lim': (0., 0.5),
    #     'y_lim': (0, 5000),
    #     'cb_1': False,
    #     'fig_size': (6, 3),
    #     'sharexy': 'all',
    #     'name': 'input_transient'
    # },
    # 'input_output': {
    #     'x_lim': (0., 0.5),
    #     'y_lim': (0, 5000),
    #     'cb_1': False,
    #     'sharexy': 'all',
    #     'name': 'input_output'
    # },
}

settings = {
    'woodblock': woodblock,
    'marimba': marimba,
    'gong': gong,
    'violin': violin,
    'violin_vibrato': violin_vibrato,
    'piano': piano,
    'interferences': interferences
}
