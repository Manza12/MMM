from __future__ import annotations
import time
from . import *
from .music import PianoRoll, ActivationsStack, Texture, Rhythm, TimePoint, FrequencyPoint


class ActivationNode:
    def __init__(self, t_p: TimePoint, t_a: TimePoint, xi: FrequencyPoint, i: int):
        self.t_p = t_p
        self.t_a = t_a
        self.xi = xi
        self.i = i

    def __str__(self):
        return r't_a=%s, f=%s, t_p=%s, i=%s' % (self.t_a, self.xi, self.t_p, self.i)

    @property
    def label(self):
        return r'$(%s, %d)$' % (self.t_a, self.i)


class Graph(nx.DiGraph):
    def derive_label_weight(self, placement=0.5):
        derivative_graph = Graph()

        # Add nodes
        for edge in self.edges:
            x = self.nodes[edge[0]]['pos']
            y = self.nodes[edge[1]]['pos']
            pos = x[0] * placement + y[0] * (1 - placement), x[1] * placement + y[1] * (1 - placement)

            label = ''.join([self.nodes[node]['label'] for node in edge])
            derivative_graph.add_node(edge, pos=pos, label=label)

            # Add edges
            for outgoing_edge in self.edges(edge[1]):
                old_labels = [self.nodes[node]['label'] for node in edge]
                weight = 0 if self.nodes[outgoing_edge[1]]['label'] in old_labels else 1

                # Add edge
                derivative_graph.add_edge(edge, outgoing_edge, weight=weight)

        return derivative_graph

    def derive(self, placement=0.5):
        derived_graph = Graph()

        # Add nodes
        for edge in self.edges:
            x = self.nodes[edge[0]]['pos']
            y = self.nodes[edge[1]]['pos']
            pos = x[0] * placement + y[0] * (1 - placement), x[1] * placement + y[1] * (1 - placement)

            derived_graph.add_node(edge, pos=pos, label='$(%s, %s)$' % edge)

            # Add edges
            for outgoing_edge in self.edges(edge[1]):
                # Add edge
                derived_graph.add_edge(edge, outgoing_edge)

        return derived_graph


class DerivedActivationsGraph(Graph):
    def __init__(self, graph: Union[ActivationsGraph, DerivedActivationsGraph]):
        super().__init__()

        # Add nodes
        for edge in graph.edges:
            if isinstance(edge[0], tuple):
                u = *edge[0], edge[1][-1]
            else:
                u = edge
            self.add_node(u)

            # Add edges
            for outgoing_edge in graph.edges(edge[1]):
                if isinstance(outgoing_edge[0], tuple):
                    v = *outgoing_edge[0], outgoing_edge[1][-1]
                else:
                    v = outgoing_edge
                self.add_edge(u, v)

    def derive(self, placement=0.5):
        return DerivedActivationsGraph(self)


class ActivationsGraph(Graph):
    def __init__(self, piano_roll: PianoRoll, activations_stack_array: np.ndarray, texture: Texture):
        super().__init__()
        self.piano_roll = piano_roll
        self.activations_stack_array = activations_stack_array
        self.texture = texture

        self.array = np.empty(piano_roll.array.shape, dtype=object)

        # Loop
        previous_nodes = []
        for n_s in range(piano_roll.array.shape[-1]):
            t_p = n_s * piano_roll.tatum + piano_roll.origin.time
            for m in range(piano_roll.array.shape[-2]):
                current_nodes = []

                xi = m * piano_roll.step + piano_roll.origin.frequency

                # Add empty list to the graph
                self.array[m, n_s] = []

                # Add activations
                if piano_roll.array[m, n_s] > 0:
                    for i in range(activations_stack_array.shape[0]):
                        rhythm: Rhythm = texture[i]
                        for u in range(rhythm.array.shape[-1]):
                            t_a = t_p - rhythm.origin.time - rhythm.tatum * u
                            n_a = (t_a - piano_roll.origin.time) // piano_roll.tatum

                            inside = 0 <= n_a < activations_stack_array.shape[2]
                            covers = rhythm.array[0, u] >= piano_roll.array[m, n_s]
                            exists = inside and activations_stack_array[i, m, n_a]

                            if inside and covers and exists:
                                node = ActivationNode(t_p, t_a, xi, i)

                                self.add_node(node, label=node.label)
                                current_nodes.append(node)

                                # Add edges
                                for previous_node in previous_nodes:
                                    self.add_edge(previous_node, node)

                                # Compute number of elements
                                self.array[m, n_s].append(node)

                if len(current_nodes) != 0:
                    previous_nodes = current_nodes

    def derive(self, placement=0.5):
        return DerivedActivationsGraph(self)

    def find_minimal_activations(self, derivation_order=None, verbose=False, folder_save=None):
        # Differentiate the graph
        if derivation_order is None:
            order_texture = (self.texture.extension.end - self.texture.extension.start) // self.texture.tatum
            order_frequency = np.max(np.sum((self.piano_roll.array.astype(bool)).astype(np.int8), axis=0))
            order = order_frequency * order_texture
            n_diff = order - 1
        else:
            n_diff = derivation_order

        if verbose:
            print('Number of derivatives: %d' % n_diff)

        derived_graph = self

        start_all = time.time()
        for k in range(n_diff):
            print('Computing derivative %d...' % (k + 1))

            # Differentiate graph
            start = time.time()
            derived_graph = derived_graph.derive()
            # derivative_graph = differentiate_graph_overlap(derivative_graph,
            #                                                label_fn=concatenate_labels,
            #                                                weight_fn=weight_indexes)
            print('Time to differentiate graph: %.3f' % (time.time() - start))

            # Save graph
            if folder_save is not None:
                file_name = 'derivative_graph-%d.gpickle' % (k + 1)
                nx.write_gpickle(derived_graph, folder_save / file_name)

        if verbose:
            print('Time to differentiate graph: %.3f s' % (time.time() - start_all))
            print('Derivative of %d order graph: %s' % (n_diff, derived_graph))

        # # Remove inconsistent nodes
        # start = time.time()
        # remove_inconsistent_nodes(derivative_graph, len(texture))
        # print('Time to remove inconsistent nodes: %.3f s' % (time.time() - start))
        # if verbose:
        #     print('Pruned graph: %s' % derivative_graph)

        # # Find the shortest path
        # start = time.time()
        # shortest_path = nx.shortest_path(derivative_graph, derivative_graph.graph['start'],
        #                                  derivative_graph.graph['end'])
        # length = nx.shortest_path_length(derivative_graph, derivative_graph.graph['start'],
        #                                  derivative_graph.graph['end'])
        # print('Time to find shortest path: %.3f' % (time.time() - start))
        # concatenated_path = concatenate_path(shortest_path)
        #
        # # Create minimal activations
        # minimal_result = np.zeros_like(activation_stack)

        # for node in concatenated_path:
        #     if isinstance(node, ActivationNode):
        #         minimal_result[node.i, node.xi, node.t_a] = True

        return derived_graph
