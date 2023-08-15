import torch
import numpy as np
from nnMorpho.binary_operators import erosion
from .music import Activations, PianoRoll


def dilate_activations(activations: Activations, piano_roll: PianoRoll):
    result = PianoRoll()
    for activation in activations:
        shifted_piano_roll = piano_roll.copy()
        shifted_piano_roll.shift(activation)
        result += shifted_piano_roll
    return result


def erosion_piano_roll(piano_roll: PianoRoll, structuring_element: PianoRoll):
    # Origin
    if structuring_element.frequency_nature == 'shift':
        origin_frequency = - structuring_element.origin.frequency // structuring_element.step
    else:
        raise NotImplementedError

    if structuring_element.time_nature == 'shift':
        origin_time = - structuring_element.origin.time // structuring_element.tatum
    else:
        raise NotImplementedError

    # To PyTorch tensors
    piano_roll_tensor = torch.from_numpy(piano_roll.array)
    str_el_tensor = torch.from_numpy(structuring_element.array)

    # Erosion
    eroded_tensor = erosion(piano_roll_tensor, str_el_tensor, origin=(origin_time, origin_frequency))

    # To numpy array
    eroded_array = eroded_tensor.numpy()

    # To PianoRoll
    activations = PianoRoll.empty_like(piano_roll)
    activations.array = eroded_array.astype(np.bool)

    return activations
