from . import *

from .dictionaries import number_to_chroma_spanish_dict, number_to_chroma_french_dict, number_to_chroma_english_dict


def lcm(x, y):
    if x > y:
        greater = x
    else:
        greater = y

    while True:
        if (greater % x == 0) and (greater % y == 0):
            result = greater
            break
        greater += 1

    return result


def gcd(*list_numbers):
    if len(list_numbers) == 0:
        return 1
    result = list_numbers[0]
    for number in list_numbers:
        if isinstance(number, frac):
            assert isinstance(result, frac), 'Cannot combine rationals with other types'
            common_denominator = lcm(result.denominator, number.denominator)
            number_numerator = number.numerator * common_denominator // number.denominator
            result_numerator = result.numerator * common_denominator // result.denominator
            result = frac(math.gcd(result_numerator, number_numerator), common_denominator)
        else:
            result = math.gcd(result, number)
    return result


def midi_number_to_pitch(number: Optional[int], language: str = 'english') -> Optional[str]:
    if number is None:
        return None
    chroma = number_to_chroma(number % 12, language=language)
    octave = number // 12 - 1

    return chroma + str(octave)


def number_to_chroma(number: int, language: str = 'english') -> str:
    if number is None:
        return 'Rest'

    if language == 'spanish':
        return number_to_chroma_spanish_dict[number]
    elif language == 'english':
        return number_to_chroma_english_dict[number]
    elif language == 'french':
        return number_to_chroma_french_dict[number]
    else:
        raise ValueError("Variable language should be one of\n- spanish\n- french\n- english")


def midi_numbers_to_chromas(midi_numbers):
    chromas_vector = []

    for midi_number in midi_numbers:
        if midi_number is None:
            chromas_vector.append(None)
        else:
            chromas_vector.append(number_to_chroma(midi_number % 12))

    return chromas_vector


def nature_of_list(x: List[str]) -> Optional[str]:
    nature = None
    for e in x:
        if nature is None:
            nature = e
        else:
            if e is not None:
                assert nature == e, 'List should be of same nature.'
    else:
        return nature


def nature_of_sum(a: Optional[str], b: Optional[str]) -> Optional[str]:
    if a is None:
        assert b is None
    if a == 'point':
        if b == 'shift':
            return 'point'
        else:
            raise ValueError('Cannot sum two points.')
    else:
        return b
