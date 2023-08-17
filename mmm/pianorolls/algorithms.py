from mmm.pianorolls import *
from mmm.pianorolls.music import PianoRoll, PianoRollStack, Activations, Texture
from mmm.pianorolls.morphology import erosion


@multimethod
def redundancy(piano_roll: PianoRoll, structuring_elements: PianoRollStack, c: dict, percentage=True):
    activations_stack = erosion(piano_roll, structuring_elements)

    rho = 0
    for activations, structuring_element in zip(activations_stack, structuring_elements):
        activations: Activations
        structuring_element: PianoRoll
        rho += activations.measure() * structuring_element.measure(c)

    rho -= piano_roll.measure(c)
    rho /= piano_roll.measure(c)

    if percentage:
        rho *= 100

    return rho


@multimethod
def redundancy(piano_roll: PianoRoll, texture: Texture, c: dict, percentage=True):
    activations_stack = erosion(piano_roll, texture)

    rho = 0
    for activations, rhythm in zip(activations_stack, texture):
        activations: Activations
        rhythm: PianoRoll
        rho += activations.measure() * rhythm.measure(c)

    rho -= piano_roll.measure(c)
    rho /= piano_roll.measure(c)

    if percentage:
        rho *= 100

    return rho
