import numpy as np
from multimethod import multimethod
from .music import Activations, PianoRoll, PianoRollStack, TimeFrequency, ActivationsStack, Texture, Harmony, \
    TimeShift, ChromaRoll, ChromaChord, ActivationsChroma, EntangledTexture


@multimethod
def dilation(activations: Activations, structuring_element: PianoRoll):
    result = PianoRoll()
    for activation in activations:
        shifted_piano_roll = structuring_element.copy()
        shifted_piano_roll.shift(activation)
        result += shifted_piano_roll
    return result


@multimethod
def dilation(activations_list: ActivationsStack, structuring_elements: PianoRollStack):
    result = PianoRoll()
    for activations, structuring_element in zip(activations_list.activations_list, structuring_elements.piano_rolls):
        result += dilation(activations, structuring_element)
    return result


@multimethod
def dilation(activations_list: ActivationsStack, texture: Texture):
    result = PianoRoll()
    for activations, structuring_element in zip(activations_list.activations_list, texture):
        result += dilation(activations, structuring_element)
    return result


@multimethod
def erosion(piano_roll: PianoRoll, structuring_element: PianoRoll):
    import torch
    from nnMorpho.binary_operators import erosion as binary_erosion

    # Tatum
    if structuring_element.tatum != piano_roll.tatum and structuring_element.tatum != TimeShift(0):
        new_tatum = piano_roll.tatum.gcd(structuring_element.tatum,
                                         piano_roll.origin.time - structuring_element.origin.time)
        piano_roll = piano_roll.change_tatum(new_tatum)
        structuring_element = structuring_element.change_tatum(new_tatum)

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
    eroded_tensor = binary_erosion(piano_roll_tensor, str_el_tensor, origin=(origin_frequency, origin_time))

    # To numpy array
    eroded_array = eroded_tensor.numpy()

    # To Activations
    f, t = np.where(eroded_array)
    activations = Activations(*[TimeFrequency(
        piano_roll.origin.time + t[i] * piano_roll.tatum,
        piano_roll.origin.frequency + f[i] * piano_roll.step) for i in range(len(f))])

    return activations


@multimethod
def erosion(piano_roll: PianoRoll, structuring_elements: PianoRollStack):
    e_list = []
    for structuring_element in structuring_elements.piano_rolls:
        e_list.append(erosion(piano_roll, structuring_element))
    result = ActivationsStack(*e_list)
    return result


@multimethod
def erosion(piano_roll: PianoRoll, texture: Texture):
    e_list = []
    for rhythm in texture:
        e_list.append(erosion(piano_roll, rhythm))
    result = ActivationsStack(*e_list)
    return result


@multimethod
def erosion(piano_roll: PianoRoll, texture: EntangledTexture):
    e_list = []
    for rhythm in texture:
        e_list.append(erosion(piano_roll, rhythm))
    result = ActivationsStack(*e_list)
    return result


@multimethod
def erosion(chroma_roll: ChromaRoll, harmony: Harmony):
    e_list = []
    for chord in harmony:
        if isinstance(chord, ChromaChord):
            e_list.append(erosion_cylindrical(chroma_roll, chord))
        else:
            raise ValueError('Chord should be a ChromaChord')
    result = ActivationsStack(*e_list)
    return result


def erosion_cylindrical(chroma_roll: ChromaRoll, chord: ChromaChord):
    # Erosion
    eroded_array = np.zeros_like(chroma_roll.array)
    for n in range(chroma_roll.array.shape[-1]):
        for m in range(chroma_roll.array.shape[-2]):
            value = True
            for i in range(chord.array.shape[-2]):
                chord_on = chord.array[i, 0]
                chroma_roll_on = chroma_roll.array[(m + i) % 12, n]
                if chord_on and not chroma_roll_on:
                    value = False
                    break
            eroded_array[m, n] = value

    # ActivationsChroma
    f, t = np.where(eroded_array)
    values = [TimeFrequency(
        chroma_roll.origin.time + t[i] * chroma_roll.tatum,
        chroma_roll.origin.frequency + f[i] * chroma_roll.step) for i in range(len(f))]
    activations = ActivationsChroma(*values)

    return activations
