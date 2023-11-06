anastasia = {
    'start': 3.2,
    'end': 4.,  # 4.67
    'parameters': {
        'closing_time_width': 0.025,
        'closing_frequency_width': 75,
    },
    'plot': {
        # Input
        'input': {
            'x_lim': (0.1, 0.55),
            'y_lim': (0, 1000),
            'name': 'input',
            'fig_size': (6, 4)
        },
        'closing': {
            'x_lim': (0.1, 0.55),
            'y_lim': (0, 1000),
            'sharexy': False,
            'name': 'closing'
        },
        'reconstruction_erosion': {
            'x_lim': (0.1, 0.55),
            'y_lim': (000, 1000),
            'sharexy': False,
            'name': 'reconstruction_erosion'
        },

        # Noise
        'opening': {
            'x_lim': (1.2, 2.2),
            'y_lim': (4800, 7200),
            'sharexy': False,
            'name': 'opening'
        },
        'input_noise': {
            'x_lim': (1.2, 2.2),
            'y_lim': (4800, 7200),
            'sharexy': False,
            'name': 'input_noise'
        },

        # Sinusoids
        'vertical_thin': {
            'x_lim': (1.6, 1.9),
            'y_lim': (850, 2200),
            'sharexy': False,
            'name': 'vertical_thin'
        },
        'vertical_top_hat': {
            'x_lim': (1.6, 1.9),
            'y_lim': (850, 1600),
            'fig_size': (8., 2.),
            'sharexy': False,
            'name': 'vertical_top_hat'
        },
        'vertical_threshold': {
            'x_lim': (1.6, 1.9),
            'y_lim': (850, 1600),
            'fig_size': (8., 2.),
            'sharexy': False,
            'name': 'vertical_threshold'
        },
        'horizontal_filtered': {
            'x_lim': (0.25, 0.75),
            'y_lim': (500, 1500),
            'fig_size': (6., 3.),
            'sharexy': False,
            'name': 'horizontal_filtered'
        },

        'lines_sinusoids': {
            'y_lim': (0, 12000),
            'name': 'lines_sinusoids'
        },
        'input_sinusoids': {
            'y_lim': (0, 12000),
            'name': 'input_sinusoids'
        },

        # Transients
        'horizontal_thin': {
            'x_lim': (1.6, 1.9),
            'y_lim': (850, 2200),
            'sharexy': False,
            'name': 'horizontal_thin',
        },
        'horizontal_top_hat': {
            'x_lim': (1.65, 1.75),
            'y_lim': (850, 2200),
            'fig_size': (5., 4.),
            'sharexy': False,
            'name': 'horizontal_top_hat',
        },
        'horizontal_threshold': {
            'x_lim': (1.65, 1.75),
            'y_lim': (850, 2200),
            'fig_size': (5., 4.),
            'sharexy': False,
            'name': 'horizontal_threshold',
        },
        'vertical_filtered': {
            'x_lim': (0.9, 1.3),
            'y_lim': (1000, 4000),
            'fig_size': (6., 3.),
            'sharexy': False,
            'name': 'vertical_filtered',
        },

        'lines_transient': {
            'x_lim': (0.5, 1.2),
            'y_lim': (200, 2200),
            'name': 'lines_transient',
        },
        'input_transient': {
            'y_lim': (0, 12000),
            'name': 'input_transient'
        },

        # Output
        'input_lines': {
            'x_lim': (1.2, 1.9),
            'y_lim': (250, 2500),
            'fig_size': (4., 4.),
            'name': 'input_lines',
        },
        'input_output': {
            'x_lim': (1.2, 1.9),
            'y_lim': (250, 2500),
            'sharexy': False,
            'name': 'input_output'
        },
        'input_denoised': {
            'y_lim': (0, 12000),
            'name': 'input_denoised'
        },
    }
}

anastasia_bis = {
    'name': 'anastasia',
    'start': 8.8,
    'end': 11.8,
    'parameters': {
        'closing_time_width': 0.025,
        'closing_frequency_width': 75,
    },
    'plot': {
        'input_lines': {
            'x_lim': (0., 1.6),
            'y_lim': (0, 4000),
            'fig_size': (4., 4.),
            'name': 'input_lines',
            'extension': 'svg',
            'horizontal': False,
        },
    }
}

# toccata_fuga = {
#     'start': 0.,
#     'end': 3.5,
#     'parameters': {
#         'closing_time_width': 0.025,
#         'closing_frequency_width': 75,
#     },
#     'plot': {},
# }
#
# luis_alonso = {
#     'start': 70.,
#     'end': 74.0,
#     'parameters': {
#         'closing_time_width': 0.025,
#         'closing_frequency_width': 75,
#     },
#     'plot': {
#         'input': {
#             'name': 'input',
#         },
#         'input_noise': {
#             'name': 'input_noise'
#         },
#         'input_sinusoids': {
#             'name': 'input_sinusoids'
#         },
#         'input_transient': {
#             'name': 'input_transient'
#         },
#         'input_lines': {
#             'name': 'input_lines',
#             'x_lim': (1., 2.),
#             'y_lim': (0, 5000),
#             'fig_size': (4., 4.),
#         },
#     },
# }
#
# flute_bach = {
#     'start': 0.,
#     'end': 4.2,
#     'parameters': {
#         'closing_time_width': 0.025,
#         'closing_frequency_width': 75,
#     },
#     'plot': {},
# }
#
# partita_b_minor = {
#     'start': 813.8,
#     'end': 818.2,
#     'parameters': {
#         'closing_time_width': 0.025,
#         'closing_frequency_width': 75,
#     },
#     'plot': {},
# }
#
# violin_vibrato = {
#     'start': 0.,
#     'end': 2.,
#     'parameters': {
#         'closing_time_width': 0.025,
#         'closing_frequency_width': 75,
#     },
#     'plot': {
#         'input_lines': {
#             'x_lim': (1.2, 1.9),
#             'y_lim': (700, 3000),
#             'fig_size': (4., 4.),
#             'vertical': False,
#             'name': 'input_lines',
#             'extension': 'svg',
#         },
#     },
# }
#
# marimba = {
#     'start': 0.,
#     'end': 4.,
#     'parameters': {
#         'closing_time_width': 0.025,
#         'closing_frequency_width': 75,
#     },
#     'plot': {},
# }
#
# piano = {
#     'start': 0.,
#     'end': 4.,
#     'parameters': {
#         'closing_time_width': 0.025,
#         'closing_frequency_width': 75,
#     },
#     'plot': {
#         'input_noise': {
#             'x_lim': (0.35, 1.5),
#             'y_lim': (0, 2500),
#             'fig_size': (8., 2.),
#             # 'vertical': False,
#             'name': 'input_noise',
#             'extension': 'svg',
#             'sharexy': False,
#         },
#     },
# }
#
# woodblock = {
#     'start': 0.,
#     'end': 4.,
#     'parameters': {
#         'closing_time_width': 0.025,
#         'closing_frequency_width': 75,
#     },
#     'plot': {},
# }
#
# flute = {
#     'start': 0.,
#     'end': 4.,
#     'parameters': {
#         'closing_time_width': 0.025,
#         'closing_frequency_width': 75,
#     },
#     'plot': {
#         'input_lines': {
#             'x_lim': (0., 1.5),
#             'y_lim': (0, 4000),
#             'fig_size': (4., 4.),
#             # 'vertical': False,
#             'name': 'input_lines',
#         },
#         'input_noise': {
#             'name': 'input_noise'
#         },
#     },
# }
#
# trombone = {
#     'start': 0.,
#     'end': 4.,
#     'parameters': {
#         'closing_time_width': 0.025,
#         'closing_frequency_width': 75,
#     },
#     'plot': {
#         'input_lines': {
#             # 'x_lim': (0., 1.5),
#             # 'y_lim': (0, 4000),
#             'fig_size': (4., 4.),
#             'vertical': False,
#             'name': 'input_lines',
#         },
#     },
# }
#
# snap = {
#     'start': 0.,
#     'end': 0.5,
#     'parameters': {
#         'closing_time_width': 0.025,
#         'closing_frequency_width': 75,
#     },
#     'plot': {
#         'input_lines': {
#             # 'x_lim': (0., 1.5),
#             # 'y_lim': (0, 4000),
#             'fig_size': (4., 4.),
#             # 'vertical': False,
#             'name': 'input_lines',
#         },
#
#     },
# }
#
# triangle = {
#     'start': 0.,
#     'end': 1.,
#     'parameters': {
#         'closing_time_width': 0.025,
#         'closing_frequency_width': 75,
#     },
#     'plot': {
#         'input_lines': {
#             # 'x_lim': (0., 1.5),
#             # 'y_lim': (0, 4000),
#             'fig_size': (4., 4.),
#             # 'vertical': False,
#             'name': 'input_lines',
#         },
#
#     },
# }
#
# guiro = {
#     'start': 0.,
#     'end': 1.,
#     'parameters': {
#         'closing_time_width': 0.025,
#         'closing_frequency_width': 75,
#     },
#     'plot': {
#         'input_lines': {
#             'x_lim': (0.3, 1.),
#             'y_lim': (0, 4000),
#             'fig_size': (4., 4.),
#             # 'vertical': False,
#             'name': 'input_lines',
#         },
#         'input_noise': {
#             'name': 'input_noise'
#         },
#         'input_output': {
#             'name': 'input_output'
#         },
#     },
# }
