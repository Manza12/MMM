from .music import Activations, PianoRoll


def dilate_activations(activations: Activations, piano_roll: PianoRoll):
    result = PianoRoll()
    for activation in activations:
        shifted_piano_roll = piano_roll.copy()
        shifted_piano_roll.shift(activation)
        result += shifted_piano_roll
    return result
