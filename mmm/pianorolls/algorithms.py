from mmm.pianorolls import *
from mmm.pianorolls.music import PianoRoll, PianoRollStack, Activations, Texture, ActivationsStack
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


def synchronize_activations_stack(activations_stack: ActivationsStack):
    activations_stack_array = activations_stack.to_array()
    contraction_frequency = np.any(activations_stack_array, axis=-2, keepdims=True)
    contraction_indexes = np.all(contraction_frequency, axis=0, keepdims=True)
    activations_stack_array *= contraction_indexes
    return activations_stack_array


def compute_size_graph(clusters: List[List], order_derivation: int):
    k = order_derivation
    N = len(clusters) - 1

    sizes = []
    for cluster in clusters:
        sizes.append(len(cluster))

    size_v = 0
    for i in range(k, N + 1):
        prod = 1
        for m in range(0, k + 1):
            prod *= sizes[i - m]
        size_v += prod

    size_e = 0
    for i in range(k + 1, N + 1):
        prod = 1
        for m in range(0, k + 2):
            prod *= sizes[i - m]
        size_e += prod

    return size_v, size_e
