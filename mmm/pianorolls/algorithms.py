import time
import os
import logging
from mmm.pianorolls import *
from mmm.pianorolls.graphs import DerivedActivationsGraph
from mmm.pianorolls.music import PianoRoll, PianoRollStack, Activations, Texture, ActivationsStack, TimeFrequency
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


def compute_size_graph(clusters: List[List], order_derivation: int):
    k = order_derivation
    L = len(clusters) - 1

    sizes = []
    for cluster in clusters:
        sizes.append(len(cluster))

    size_v = 0
    for i in range(k, L + 1):
        prod = 1
        for m in range(0, k + 1):
            prod *= sizes[i - m]
        size_v += prod

    size_e = 0
    for i in range(k + 1, L + 1):
        prod = 1
        for m in range(0, k + 2):
            prod *= sizes[i - m]
        size_e += prod

    return size_v, size_e


def concatenate_path(path: list):
    concatenated_path = []
    for n, node in enumerate(path):
        if node == 'S':
            continue
        elif node == 'E':
            new_node = path[n - 1]
            for a, act in enumerate(new_node):
                if a == 0:
                    continue
                concatenated_path.append(act)
        else:
            concatenated_path.append(node[0])
    return concatenated_path


def find_minimal_activations(activations_graph: DerivedActivationsGraph,
                             derivation_order=None, verbose=False, folder_save=None,
                             load=False, sparse=True, max_shortest_paths=10):
    # Compute order of derivation
    if derivation_order is None:
        texture_length = (activations_graph.texture.extension.end - activations_graph.texture.extension.start)
        order_texture = texture_length // activations_graph.texture.tatum
        if sparse:
            order_frequency = np.max(np.sum((activations_graph.piano_roll.array.astype(bool)).astype(np.int8), axis=0))
            order = order_frequency * order_texture
        else:
            order = order_texture
        derivation_order = order - 1

    if verbose:
        logging.info('Number of derivatives: %d' % derivation_order)

    derived_graph = activations_graph

    # Save graph
    if folder_save is not None:
        file_name = 'derivative_graph-0.gpickle'
        nx.write_gpickle(derived_graph, folder_save / file_name)

    # Try to load last derived graph
    last_loaded = False
    if load and folder_save is not None:
        start_load = time.time()
        file_name = 'derivative_graph-%d.gpickle' % derivation_order
        if os.path.isfile(folder_save / file_name):
            derived_graph = nx.read_gpickle(folder_save / file_name)
            last_loaded = True
        if last_loaded and verbose:
            logging.info('Time to load graph: %.3f s' % (time.time() - start_load))

    if not last_loaded:
        start_all = time.time()
        for k in range(derivation_order):
            if verbose:
                logging.info('Computing derivative %d...' % (k + 1))
            file_name = 'derivative_graph-%d.gpickle' % (k + 1)

            # Try to load graph
            if load and folder_save is not None:
                start_load = time.time()
                try:
                    derived_graph = nx.read_gpickle(folder_save / file_name)
                    logging.info('Time to load graph: %.3f' % (time.time() - start_load))
                    continue
                except FileNotFoundError:
                    pass

            # Differentiate graph
            start = time.time()
            derived_graph = derived_graph.derive()
            logging.info('Time to derive graph: %.3f' % (time.time() - start))

            # Save graph
            if folder_save is not None:
                nx.write_gpickle(derived_graph, folder_save / file_name)

        if verbose:
            logging.info('Time to derive graph: %.3f s' % (time.time() - start_all))
            logging.info('Derivative of %d order graph: %s' % (derivation_order, derived_graph))

    # Remove inconsistent nodes
    if sparse:
        start = time.time()
        derived_graph.remove_inconsistent_nodes()
        if verbose:
            logging.info('Time to remove inconsistent nodes: %.3f s' % (time.time() - start))
            logging.info('Pruned graph: %s' % derived_graph)

    # Add start and end nodes
    start = time.time()
    derived_graph.add_start_end_nodes()
    if verbose:
        logging.info('Time to add start and end nodes: %.3f s' % (time.time() - start))

    # Weight graph
    start = time.time()
    derived_graph.weight_graph()
    if verbose:
        logging.info('Time to weight graph: %.3f s' % (time.time() - start))
        logging.info('Weighted graph: %s' % derived_graph)

    # Save graph
    if folder_save is not None:
        file_name = 'pruned_weighted_graph-%d.gpickle' % derivation_order
        nx.write_gpickle(derived_graph, folder_save / file_name)

    # Find the shortest paths
    start = time.time()
    try:
        # All shortest paths
        shortest_paths = []
        shortest_paths_generator = nx.all_shortest_paths(derived_graph, derived_graph.start, derived_graph.end,
                                                         weight='weight')
        n = 0
        for shortest_path in shortest_paths_generator:
            shortest_paths.append(shortest_path)
            n += 1
            if n == max_shortest_paths:
                logging.info('Maximum number of shortest paths reached.')
                break
        logging.info('Time to find shortest paths: %.3f' % (time.time() - start))
        logging.info('Number of shortest paths: %d' % len(shortest_paths))
    except nx.NetworkXNoPath:
        shortest_paths = []
        logging.info('No path found')

    # Concatenate paths
    concatenated_paths = []
    for shortest_path in shortest_paths:
        concatenated_paths.append(concatenate_path(shortest_path))

    # Create activations stack
    activation_stacks = []
    for path in concatenated_paths:
        activations_list = []
        for i in range(len(derived_graph.texture)):
            activations = [TimeFrequency(activation.t_a, activation.xi) for activation in path if activation.i == i]
            activations_list.append(Activations(*activations))
        activation_stack = ActivationsStack(*activations_list)
        activation_stacks.append(activation_stack)

    return shortest_paths, activation_stacks, derived_graph
