from . import *
from .music import PianoRoll, ActivationsStack, Texture, Rhythm, TimePoint, FrequencyPoint


class ActivationNode:
    def __init__(self, t_s: TimePoint, t_a: TimePoint, xi: FrequencyPoint, i: int):
        self.t_s = t_s
        self.t_a = t_a
        self.xi = xi
        self.i = i

    def __str__(self):
        return r't_a=%s, f=%s, t_s=%s, i=%s' % (self.t_a, self.xi, self.t_s, self.i)

    @property
    def label(self):
        return r'$(%s, %d)$' % (self.t_a, self.i)


class GraphActivations(nx.DiGraph):
    def __init__(self, piano_roll: PianoRoll, activations_stack: ActivationsStack, texture: Texture):
        super().__init__()
        self.array = np.empty(piano_roll.array.shape, dtype=object)
        self.piano_roll = piano_roll

        # Create stack of activations
        activations_stack_array = activations_stack.to_array()

        # Loop
        for n_s in range(piano_roll.array.shape[-1]):
            t_s = n_s * piano_roll.tatum + piano_roll.origin.time
            for m in range(piano_roll.array.shape[-2]):
                xi = m * piano_roll.step + piano_roll.origin.frequency

                # Add empty list to the graph
                self.array[m, n_s] = []

                # Add activations
                if piano_roll.array[m, n_s] > 0:
                    for i in range(activations_stack_array.shape[0]):
                        rhythm: Rhythm = texture[i]
                        for u in range(rhythm.array.shape[-1]):
                            t_a = t_s - rhythm.tatum * u
                            n_a = (t_a - piano_roll.origin.time) // piano_roll.tatum

                            inside = 0 <= n_a < activations_stack_array.shape[2]
                            covers = rhythm.array[0, u] >= piano_roll.array[m, n_s]
                            exists = inside and activations_stack_array[i, m, n_a]

                            if inside and covers and exists:
                                node = ActivationNode(t_s, t_a, xi, i)

                                self.add_node(node, label=node.label)

                                # Compute number of elements
                                self.array[m, n_s].append(node)
