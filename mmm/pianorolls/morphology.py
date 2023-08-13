from . import *

from .music import PianoRoll, TimeFrequency, FrequencyShift
from .generation import Activations


def dilate_sparse(activation_table, block):
    activation_table: Activations
    block: PianoRoll

    step = activation_table.step

    # Change tatum
    tatum = activation_table.tatum.gcd(block.tatum)
    ratio = int(activation_table.tatum / tatum)
    new_shape = (activation_table.array.shape[0], activation_table.array.shape[1] * (activation_table.tatum // tatum))
    array = np.zeros(new_shape, dtype=block.array.dtype)
    block = block.change_tatum(tatum)

    # Pad result
    array = np.pad(array, ((0, block.array.shape[0] - 1), (0, block.array.shape[1] - 1)))

    # Compute
    str_el = block.array
    for tf in activation_table:
        tf: TimeFrequency

        f_0 = (tf.frequency - activation_table.extension.frequency.lower) // step
        f_1 = f_0 + str_el.shape[0]

        t_0 = (tf.time - activation_table.extension.time.start) // tatum
        t_1 = t_0 + str_el.shape[1]

        array[f_0: f_1, t_0: t_1] = np.maximum(array[f_0: f_1, t_0: t_1], str_el)

    # Create piano_roll
    origin = (activation_table.origin[0] + block.origin[0],
              activation_table.origin[1] * ratio + block.origin[1])
    if activation_table.time_nature == 'point':
        if block.time_nature == 'shift':
            time_nature = 'point'
        else:
            raise ValueError('Cannot add two points.')
    else:
        time_nature = block.time_nature
    if activation_table.frequency_nature == 'point':
        if block.frequency_nature == 'shift':
            frequency_nature = 'point'
        else:
            raise ValueError('Cannot add two points.')
    else:
        frequency_nature = block.frequency_nature
    assert activation_table.step == block.step == FrequencyShift(1)
    result = PianoRoll(array, origin, tatum, FrequencyShift(1), time_nature, frequency_nature)

    return result
