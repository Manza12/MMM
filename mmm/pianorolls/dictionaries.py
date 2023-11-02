from .parameters import SHARP, FLAT

note_value_to_denominator_dict = {
    'whole': 1,
    'half': 2,
    'quarter': 4,
    'eighth': 8,
    '16th': 16,
    '32nd': 32,
    '64th': 64,
    '128th': 128,
}

number_to_chroma_spanish_dict = {
    0: 'Do',
    1: 'Do' + SHARP,
    2: 'Re',
    3: 'Mi' + FLAT,
    4: 'Mi',
    5: 'Fa',
    6: 'Fa' + SHARP,
    7: 'Sol',
    8: 'La' + FLAT,
    9: 'La',
    10: 'Si' + FLAT,
    11: 'Si'
}

number_to_chroma_english_dict = {
    0: 'C',
    1: 'C' + SHARP,
    2: 'D',
    3: 'E' + FLAT,
    4: 'E',
    5: 'F',
    6: 'F' + SHARP,
    7: 'G',
    8: 'A' + FLAT,
    9: 'A',
    10: 'B' + FLAT,
    11: 'B'
}

number_to_chroma_french_dict = {
    0: 'do',
    1: 'do' + SHARP,
    2: 'ré',
    3: 'mi' + FLAT,
    4: 'mi',
    5: 'fa',
    6: 'fa' + SHARP,
    7: 'sol',
    8: 'la' + FLAT,
    9: 'la',
    10: 'si' + FLAT,
    11: 'si'
}

# number_to_chroma_french_dict = {
#     0: '\x1B[3mdo\x1B[0m',
#     1: '\x1B[3mdo' + SHARP + '\x1B[0m',
#     2: '\x1B[3mré\x1B[0m',
#     3: '\x1B[0mmi\x1B[0m' + FLAT,
#     4: '\x1B[0mmi\x1B[0m',
#     5: '\x1B[0mfa\x1B[0m',
#     6: '\x1B[0mfa' + SHARP + '\x1B[0m',
#     7: '\x1B[0msol\x1B[0m',
#     8: '\x1B[0mla' + FLAT + '\x1B[0m',
#     9: '\x1B[0mla\x1B[0m',
#     10: '\x1B[0msi' + FLAT + '\x1B[0m',
#     11: '\x1B[0msi\x1B[0m'
# }

pitch_to_note_number_dict = {
    'C': 0,
    'D': 2,
    'E': 4,
    'F': 5,
    'G': 7,
    'A': 9,
    'B': 11
}

roman_numeral_to_factors_dict = {
    'I': {
        '1': 0,
        '2': 2,
        '3': 4,
        '4': 5,
        '5': 7,
        '6': 9,
        '7': 11
    },
    'ii': {
        '1': 2,
        '3': 5,
        '5': 9,
        '7': 0
    },
    'III': {
        '1': 4,
        '3': 7,
        '5': 10
    },
    'V': {
        '1': 7,
        '3': 11,
        '4': 0,
        '5': 2,
        '6': 4,
        '7': 5
    },
    'IV': {
        '1': 5,
        '2': 7,
        '2+': 8,
        '3': 9,
        '4': 11,
        '5': 0,
        '6': 2,
        '7': 4
    },
    'vi': {
        '1': 9,
        '3': 0,
        '5': 4,
        '7': 7
    },
    'i': {
        '1': 0,
        '2': 2,
        '3': 3,
        '4': 5,
        '5': 7,
        '6': 8,
        '7': 10
    },
    'iiº': {
        '1': 2,
        '3': 5,
        '5': 8,
        '7': 0,
    },
    'iv': {
        '1': 5,
        '2': 7,
        '3': 8,
        '5': 0,
        '6': 2,
        '7': 3
    },
    'VI': {
        '1': 8,
        '3': 0,
        '5': 3,
        '7': 7
    },
    'V/V': {
        '1': 2,
        '3': 6,
        '5': 9,
        '7': 0
    },
    'Maj': {
        '1': 0,
        '2': 2,
        '3': 4,
        '4': 5,
        '4+': 6,
        '5': 7,
        '6': 9,
        '7': 11
    },
    'MinN': {
        '1': 0,
        '2': 2,
        '3': 3,
        '4': 5,
        '4+': 6,
        '5': 7,
        '6': 8,
        '7': 10
    },
    'Min': {
        '1': 0,
        '2': 2,
        '3': 3,
        '4': 5,
        '4+': 6,
        '5': 7,
        '6': 8,
        '7': 10
    },
    'MinH': {
        '1': 0,
        '2': 2,
        '3': 3,
        '4': 5,
        '4+': 6,
        '5': 7,
        '6': 8,
        '7': 11
    },
    'MinC': {
        '1': 0,
        '2': 2,
        '3': 3,
        '4': 5,
        '4+': 6,
        '5': 7,
        '6': 9,
        '7': 10
    },
    'MinM': {
        '1': 0,
        '2': 2,
        '3': 3,
        '4': 5,
        '4+': 6,
        '5': 7,
        '6': 9,
        '7': 11
    },
    'Np': {
        '1': 1,
        '3': 5,
        '5': 8
    },
    'viiº': {
        '1': 11,
        '3': 2,
        '5': 5,
        '7': 8
    },
    'viiº/V': {
        '1': 6,
        '3': 9,
        '5': 0,
        '7': 3
    },
    'vii7': {
        '1': 11,
        '3': 2,
        '5': 5,
        '7': 9
    },
}

chord_to_roman_numeral_dict = {
    # Triads
    frozenset({0, 4, 7}): 'I',
    frozenset({0, 3, 7}): 'i',
    frozenset({2, 5, 9}): 'ii',
    frozenset({4, 7, 11}): 'iii',
    frozenset({2, 5, 8}): 'iiº',
    frozenset({5, 9, 0}): 'IV',
    frozenset({5, 8, 0}): 'iv',
    frozenset({7, 11, 2}): 'V',
    frozenset({7, 0, 2}): 'V45',
    frozenset({9, 0, 4}): 'vi',
    frozenset({8, 0, 3}): 'VI',
    frozenset({2, 5, 11}): 'viiº',
    frozenset({1, 5, 8}): 'N',

    # Seventh chords
    frozenset({0, 4, 7, 11}): 'I7',
    frozenset({0, 3, 7, 10}): 'i7',
    frozenset({2, 5, 9, 0}): 'ii7',
    frozenset({2, 5, 8, 0}): 'iiº7',
    frozenset({4, 7, 11, 2}): 'iii7',
    frozenset({5, 9, 0, 4}): 'IV7',
    frozenset({5, 8, 0, 3}): 'iv7',
    frozenset({7, 11, 2, 5}): 'V7',
    frozenset({7, 0, 2, 5}): 'V457',
    frozenset({9, 0, 4, 7}): 'vi7',
    frozenset({8, 0, 3, 7}): 'VI7',
    frozenset({2, 5, 11, 9}): 'viiº7',
    frozenset({2, 5, 11, 8}): '7º',
}
