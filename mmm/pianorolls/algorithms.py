import time
import os
from mmm.pianorolls import *
from mmm.pianorolls.graphs import DerivedActivationsGraph
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


def find_minimal_activations(activations_graph: DerivedActivationsGraph,
                             derivation_order=None, verbose=False, folder_save=None,
                             load=False):
    # Differentiate the graph
    if derivation_order is None:
        texture_length = (activations_graph.texture.extension.end - activations_graph.texture.extension.start)
        order_texture = texture_length // activations_graph.texture.tatum

        order_frequency = np.max(np.sum((activations_graph.piano_roll.array.astype(bool)).astype(np.int8), axis=0))

        order = order_frequency * order_texture
        derivation_order = order - 2

    if verbose:
        print('Number of derivatives: %d' % derivation_order)

    derived_graph = activations_graph

    # Save graph
    if folder_save is not None:
        file_name = 'derivative_graph-0.gpickle'
        nx.write_gpickle(derived_graph, folder_save / file_name)

    # Try to load last derived graph
    last_loaded = False
    if load and folder_save is not None:
        start = time.time()
        file_name = 'derivative_graph-%d.gpickle' % derivation_order
        if os.path.isfile(folder_save / file_name):
            derived_graph = nx.read_gpickle(folder_save / file_name)
            last_loaded = True
        if verbose:
            print('Time to load graph: %.3f s' % (time.time() - start))
            print('Derivative of %d order graph: %s' % (derivation_order, derived_graph))

    if not last_loaded:
        start_all = time.time()
        for k in range(derivation_order):
            if verbose:
                print('Computing derivative %d...' % (k + 1))
            file_name = 'derivative_graph-%d.gpickle' % (k + 1)

            # Try to load graph
            if load and folder_save is not None:
                if os.path.isfile(folder_save / file_name):
                    derived_graph = nx.read_gpickle(folder_save / file_name)
                    continue

            # Differentiate graph
            start = time.time()
            derived_graph = derived_graph.derive()
            print('Time to differentiate graph: %.3f' % (time.time() - start))

            # Save graph
            if folder_save is not None:
                nx.write_gpickle(derived_graph, folder_save / file_name)

        if verbose:
            print('Time to differentiate graph: %.3f s' % (time.time() - start_all))
            print('Derivative of %d order graph: %s' % (derivation_order, derived_graph))

    # Remove inconsistent nodes
    start = time.time()
    derived_graph.remove_inconsistent_nodes()
    if verbose:
        print('Time to remove inconsistent nodes: %.3f s' % (time.time() - start))
        print('Pruned graph: %s' % derived_graph)

    # Save graph
    if folder_save is not None:
        file_name = 'pruned_derivative_graph-%d.gpickle' % derivation_order
        nx.write_gpickle(derived_graph, folder_save / file_name)

    # Add start and end nodes
    start = time.time()
    derived_graph.add_start_end_nodes()
    if verbose:
        print('Time to add start and end nodes: %.3f s' % (time.time() - start))

    # Find the shortest path
    start = time.time()
    shortest_path = nx.shortest_path(derived_graph, derived_graph.start, derived_graph.end)
    print('Time to find shortest path: %.3f' % (time.time() - start))
    # concatenated_path = concatenate_path(shortest_path)
    #
    # # Create minimal activations
    # minimal_result = np.zeros_like(activation_stack)

    # for node in concatenated_path:
    #     if isinstance(node, ActivationNode):
    #         minimal_result[node.i, node.xi, node.t_a] = True

    return shortest_path
