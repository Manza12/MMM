from . import *

from .dictionaries import number_to_chroma_spanish_dict, number_to_chroma_french_dict, number_to_chroma_english_dict, \
    pitch_to_note_number_dict, note_value_to_denominator_dict


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
        elif isinstance(number, int):
            assert isinstance(result, int), 'Cannot combine integers with other types'
            result = math.gcd(result, number)
        else:
            raise ValueError('Invalid type')
    return result


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier


def round_half_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n*multiplier - 0.5) / multiplier


def midi_number_to_pitch(number: Optional[int], language: str = 'english') -> Optional[str]:
    if number is None:
        return None
    chroma = midi_number_to_chroma(number % 12, language=language)
    octave = number // 12 - 1

    return chroma + str(octave)


def midi_number_to_chroma(number: int, language: str = 'english') -> str:
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


def midi_numbers_to_pitches(midi_numbers):
    pitches_vector = []

    for midi_number in midi_numbers:
        pitches_vector.append(midi_number_to_pitch(midi_number))

    return pitches_vector


def midi_numbers_to_chromas(midi_numbers):
    chromas_vector = []

    for midi_number in midi_numbers:
        if midi_number is None:
            chromas_vector.append(None)
        else:
            chromas_vector.append(midi_number_to_chroma(midi_number % 12))

    return chromas_vector


def pitch_to_note_number(step: str, octave: int, alter: int) -> int:
    result = (octave + 1) * 12

    result += pitch_to_note_number_dict[step]

    if alter:
        result += alter

    return result


def duration_whole_to_unicode(duration: Union[float, frac]) -> str:
    duration = frac(duration)
    if int(duration * 64) == duration * 64:
        pass
    else:
        raise NotImplementedError('duration %f not implemented.' % duration)

    if duration < 0:
        result = '-'
        duration = -duration
    else:
        result = ''

    while duration >= 1.:
        if not result == '':
            result += '+ '
        result += u'𝅝 '
        duration -= 1

    while duration >= 1/2:
        if not result == '':
            result += '+ '
        result += u'𝅗𝅥 '
        duration -= 1/2

    while duration >= 1/4:
        if not result == '':
            result += '+ '
        result += u'𝅘𝅥 '
        duration -= 1/4

    while duration >= 1/8:
        if not result == '':
            result += '+ '
        result += u'𝅘𝅥𝅮 '
        duration -= 1/8

    while duration >= 1/16:
        if not result == '':
            result += '+ '
        result += u'𝅘𝅥𝅯 '
        duration -= 1/16

    while duration >= 1/32:
        if not result == '':
            result += '+ '
        result += u'𝅘𝅥𝅰 '
        duration -= 1/32

    while duration >= 1/64:
        if not result == '':
            result += '+ '
        result += u'𝅘𝅥𝅱 '
        duration -= 1/64

    if not duration == 0:
        raise NotImplementedError('duration not implemented.')
    else:
        return result


def beat_unit_to_tuple(beat_unit, beat_unit_dot) -> tuple:
    numerator = 1
    if beat_unit is None:
        return 0, 1
    else:
        try:
            denominator = note_value_to_denominator_dict[beat_unit]
        except KeyError:
            raise ValueError('Unimplemented beat_unit %s' % beat_unit)

    if beat_unit_dot:
        denominator *= 2
        numerator = 2 * numerator + 1

    return numerator, denominator


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
