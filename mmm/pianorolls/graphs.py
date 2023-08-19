from __future__ import annotations
import time
from . import *
from .music import PianoRoll, Texture, Rhythm, TimePoint, FrequencyPoint


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


class DerivedActivationNode:
    def __init__(self, t_p: TimePoint, t_a: TimePoint, xi: FrequencyPoint, i: int, cluster: int):
        self.t_p = t_p
        self.t_a = t_a
        self.xi = xi
        self.i = i

        self.cluster = cluster

    def __eq__(self, other):
        if isinstance(other, DerivedActivationNode):
            return self.t_p == other.t_a and self.t_p == other.t_a and self.xi == other.xi and self.i == other.i
        else:
            return False

    def __str__(self):
        return r'(%s, %s, %s, %d) #%d' % (self.t_p, self.t_a, self.xi, self.i, self.cluster)

    def __hash__(self):
        return hash((self.t_p, self.t_a, self.xi, self.i))

    def same_activation(self, other):
        if isinstance(other, DerivedActivationNode):
            return self.t_a == other.t_a and self.xi == other.xi and self.i == other.i
        else:
            return False


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


class ActivationsGraph(Graph):
    def __init__(self, piano_roll: PianoRoll, activations_stack_array: np.ndarray, texture: Texture):
        super().__init__()
        self.piano_roll = piano_roll
        self.activations_stack_array = activations_stack_array
        self.texture = texture

        self.clusters: List[List[ActivationNode]] = []

        self.array = np.empty(piano_roll.array.shape, dtype=object)

        # Loop
        previous_nodes = []
        for n_s in range(piano_roll.array.shape[-1]):
            t_p = n_s * piano_roll.tatum + piano_roll.origin.time
            for m in range(piano_roll.array.shape[-2]):
                self.clusters.append([])

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
                                self.clusters[-1].append(node)

                                # Add edges
                                for previous_node in previous_nodes:
                                    self.add_edge(previous_node, node)

                                # Compute number of elements
                                self.array[m, n_s].append(node)

                if len(self.clusters[-1]) != 0:
                    previous_nodes = self.clusters[-1]
                else:
                    self.clusters.pop(-1)


class DerivedActivationsGraph(Graph):
    @multimethod
    def __init__(self, piano_roll: PianoRoll, texture: Texture):
        super().__init__()

        self.texture = texture
        self.piano_roll = piano_roll

        self.clusters = []

    @multimethod
    def __init__(self, graph: ActivationsGraph):
        super().__init__()
        self.__init__(graph.piano_roll, graph.texture)

        previous_cluster = []
        for cluster in graph.clusters:
            self.clusters.append([])

            # Add nodes
            for node in cluster:
                u = (DerivedActivationNode(node.t_p, node.t_a, node.xi, node.i, len(self.clusters) - 1), )
                self.add_node(u)
                self.clusters[-1].append(u)

            # Add edges
            for u in previous_cluster:
                for v in self.clusters[-1]:
                    self.add_edge(u, v)

            previous_cluster = self.clusters[-1]

    def derive(self, make_clusters=True, placement=0.5):
        derived_graph = DerivedActivationsGraph(self.piano_roll, self.texture)

        if make_clusters:
            for _ in range(len(self.clusters) - 1):
                derived_graph.clusters.append([])

        # Add nodes
        for edge in self.edges:
            u = *edge[0], edge[1][-1]
            derived_graph.add_node(u)

            if make_clusters:
                derived_graph.clusters[u[0].cluster].append(u)

            # Add edges
            for outgoing_edge in self.edges(edge[1]):
                v = *outgoing_edge[0], outgoing_edge[1][-1]
                derived_graph.add_edge(u, v)

        return derived_graph

    def find_minimal_activations(self, derivation_order=None, verbose=False, folder_save=None):
        # Differentiate the graph
        if derivation_order is None:
            order_texture = (self.texture.extension.end - self.texture.extension.start) // self.texture.tatum
            order_frequency = np.max(np.sum((self.piano_roll.array.astype(bool)).astype(np.int8), axis=0))
            order = order_frequency * order_texture
            derivation_order = order - 2

        if verbose:
            print('Number of derivatives: %d' % derivation_order)

        derived_graph = self

        start_all = time.time()
        for k in range(derivation_order):
            print('Computing derivative %d...' % (k + 1))

            # Differentiate graph
            start = time.time()
            derived_graph = derived_graph.derive()
            print('Time to differentiate graph: %.3f' % (time.time() - start))

            # Save graph
            if folder_save is not None:
                file_name = 'derivative_graph-%d.gpickle' % (k + 1)
                nx.write_gpickle(derived_graph, folder_save / file_name)

        if verbose:
            print('Time to differentiate graph: %.3f s' % (time.time() - start_all))
            print('Derivative of %d order graph: %s' % (derivation_order, derived_graph))

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
