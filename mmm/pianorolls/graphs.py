import networkx as nx
from multimethod import multimethod
from .music import PianoRoll, Texture, Rhythm, TimePoint, FrequencyPoint, ActivationsStack, Activations, Harmony, \
    RomanNumeral
from .dictionaries import chord_to_roman_numeral_dict


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

    @property
    def activation(self):
        return self.t_a, self.xi, self.i


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
            # Position
            x = self.nodes[edge[0]]['pos']
            y = self.nodes[edge[1]]['pos']
            pos = x[0] * placement + y[0] * (1 - placement), x[1] * placement + y[1] * (1 - placement)

            # Label
            try:
                list_1 = ['%s' % a for a in edge[0]]
            except TypeError:
                list_1 = ['%s' % edge[0]]
            try:
                list_2 = ['%s' % edge[1][-1]]
            except TypeError:
                list_2 = ['%s' % edge[1]]
            label = '$(' + ', '.join(list_1 + list_2) + ')$'

            # Add node
            derived_graph.add_node(edge, pos=pos, label=label)

            # Add edges
            for outgoing_edge in self.edges(edge[1]):
                # Add edge
                derived_graph.add_edge(edge, outgoing_edge)

        return derived_graph


class ActivationsGraph(Graph):
    def __init__(self, piano_roll: PianoRoll, activations_stack: ActivationsStack, texture: Texture,
                 lexicographic_priority: str = 'frequency'):
        super().__init__()
        self.piano_roll = piano_roll
        self.activations_stack = activations_stack
        self.texture = texture

        self.clusters: List[List[ActivationNode]] = []

        self.array = np.empty(piano_roll.array.shape, dtype=object)

        self.fill_graph(lexicographic_priority)

    def fill_graph(self, lexicographic_priority: str):
        if lexicographic_priority == 'frequency':
            self.fill_graph_frequency()
        elif lexicographic_priority == 'time':
            self.fill_graph_time()
        else:
            raise ValueError('Lexicographic priority must be either "frequency" or "time".')

    def fill_graph_frequency(self):
        # Loop
        previous_nodes = []
        for n_s in range(self.piano_roll.array.shape[-1]):
            t_p = n_s * self.piano_roll.tatum + self.piano_roll.origin.time
            for m in range(self.piano_roll.array.shape[-2]):
                self.clusters.append([])

                xi = m * self.piano_roll.step + self.piano_roll.origin.frequency

                # Add empty list to the graph
                self.array[m, n_s] = []

                # Add activations
                if self.piano_roll.array[m, n_s] > 0:
                    for i in range(len(self.activations_stack)):
                        rhythm: Rhythm = self.texture[i]
                        activations: Activations = self.activations_stack[i]
                        for u in range(rhythm.array.shape[-1]):
                            t_a = t_p - rhythm.origin.time - rhythm.tatum * u
                            n_a = (t_a - self.piano_roll.origin.time) // self.piano_roll.tatum

                            inside = 0 <= n_a < activations.array.shape[-1] and 0 <= m < activations.array.shape[-2]
                            covers = rhythm.array[0, u] >= self.piano_roll.array[m, n_s]
                            exists = inside and activations.array[m, n_a]

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

    def fill_graph_time(self):
        # Loop
        previous_nodes = []
        for m in range(self.piano_roll.array.shape[-2]):
            xi = m * self.piano_roll.step + self.piano_roll.origin.frequency
            for n_s in range(self.piano_roll.array.shape[-1]):
                t_p = n_s * self.piano_roll.tatum + self.piano_roll.origin.time

                self.clusters.append([])

                # Add empty list to the graph
                self.array[m, n_s] = []

                # Add activations
                if self.piano_roll.array[m, n_s] > 0:
                    for i in range(len(self.activations_stack)):
                        rhythm: Rhythm = self.texture[i]
                        activations: Activations = self.activations_stack[i]
                        for u in range(rhythm.array.shape[-1]):
                            t_a = t_p - rhythm.origin.time - rhythm.tatum * u
                            n_a = (t_a - self.piano_roll.origin.time) // self.piano_roll.tatum

                            inside = 0 <= n_a < activations.array.shape[-1] and 0 <= m < activations.array.shape[-2]
                            covers = rhythm.array[0, u] >= self.piano_roll.array[m, n_s]
                            exists = inside and activations.array[m, n_a]

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

        self.start = None
        self.end = None

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

                # Set scope
                self.nodes[u]['t_scope'] = node.t_p - self.texture.extension.duration

            # Add edges
            for u in previous_cluster:
                for v in self.clusters[-1]:
                    self.add_edge(u, v)

            previous_cluster = self.clusters[-1]

    def add_start_end_nodes(self):
        # Add start node
        self.start = 'S'
        self.add_node(self.start)
        for node in self.clusters[0]:
            self.add_edge(self.start, node)

        # Add end node
        self.end = 'E'
        self.add_node(self.end)
        for node in self.clusters[-1]:
            self.add_edge(node, self.end)

    def derive(self, make_clusters=True, placement=0.5):
        derived_graph = DerivedActivationsGraph(self.piano_roll, self.texture)

        if make_clusters:
            for _ in range(len(self.clusters) - 1):
                derived_graph.clusters.append([])

        # Add nodes
        for edge in self.edges:
            u = *edge[0], edge[1][-1]
            derived_graph.add_node(u)
            derived_graph.nodes[u]['t_scope'] = self.nodes[edge[1]]['t_scope']

            if make_clusters:
                derived_graph.clusters[u[0].cluster].append(u)

            # Add edges
            for outgoing_edge in self.edges(edge[1]):
                v = *outgoing_edge[0], outgoing_edge[1][-1]
                derived_graph.add_edge(u, v)

        return derived_graph

    def remove_inconsistent_nodes(self):
        nodes_to_remove = []
        for node in self.nodes:
            t_scope = self.nodes[node]['t_scope']
            indexes = set()
            for activation in node:
                if activation.t_a == t_scope:
                    indexes.add(activation.i)
            if len(indexes) != len(self.texture) and len(indexes) != 0:
                nodes_to_remove.append(node)

        self.remove_nodes_from(nodes_to_remove)
        for node in nodes_to_remove:
            self.clusters[node[0].cluster].remove(node)

    def weight_graph(self):
        for edge in self.edges:
            u = edge[0]
            v = edge[1]

            if v == 'E':
                new_activations = {}
                new_time_a = {}
            elif u == 'S':
                new_activations = set([a.activation for a in v])
                new_time_a = set([a.t_a for a in v])
            else:
                new_activations = set([a.activation for a in v]) - set([a.activation for a in u])
                new_time_a = set([a.t_a for a in v]) - set([a.t_a for a in u])

            weight = len(new_activations) + len(new_time_a)

            self.edges[edge]['weight'] = weight


class TonalGraph(nx.DiGraph):
    def __init__(self, activations_harmony: ActivationsStack, harmony: Harmony, activations: Activations,
                 terminal_nodes=False, bonus_seventh=0.1, weight_type=int, weight_fn=None, complete=True
                 ):
        super().__init__()

        self.harmony = harmony
        self.activations = activations
        self.activations_harmony = activations_harmony

        activations_stack = activations_harmony.to_array()
        shape = activations_stack.shape

        self.array = np.empty(shape[1:], dtype=object)
        self.offsets = np.zeros(shape[1], dtype=int)

        if terminal_nodes:
            self.add_node('S', label='$S$')
            previous_nodes = ['S']
        else:
            previous_nodes = []

        for t in range(shape[-1]):
            current_nodes = []
            for f in range(shape[-2]):
                self.array[f, t] = []
                off = 0
                for i in range(shape[0]):
                    if activations_harmony[i].array[f, t]:
                        roman_numeral: RomanNumeral = harmony[i]

                        node = (t, f, i)

                        frequencies = frozenset([int(f) % 12 for f in roman_numeral.frequencies])
                        label = chord_to_roman_numeral_dict[frequencies]

                        off += 1

                        self.add_node(node, label=label)
                        self.array[f, t].append(node)
                        current_nodes.append(node)

                        for p_node in previous_nodes:
                            if weight_fn is None:
                                try:
                                    weight = p_node[1] != node[1]
                                except IndexError:
                                    weight = 0
                                if len(harmony[node[2]]) == 4:
                                    weight -= bonus_seventh
                            else:
                                weight = weight_fn(p_node, node, bonus_seventh)

                            if complete:
                                self.add_edge(p_node, node, weight=weight_type(weight))
                            else:
                                if p_node[1] == node[1]:
                                    self.add_edge(p_node, node, weight=weight_type(weight))
            if len(current_nodes) != 0:
                previous_nodes = current_nodes

        if terminal_nodes:
            self.add_node('E', label='$E$')
            for node in previous_nodes:
                self.add_edge(node, 'E', weight=0)

        # Assign positions
        offset = 0
        for xi in range(shape[1]):
            max_n = 0
            for t in range(shape[2]):
                nodes = self.array[xi, t]
                max_n = max(max_n, len(nodes))
                for n, node in enumerate(nodes):
                    self.nodes[node]['pos'] = (t, n + offset - max_n / 2 + 0.5)

            self.offsets[xi] = max_n
            offset += max_n

        if terminal_nodes:
            self.nodes['S']['pos'] = (-1, np.sum(offset) / 2)
            self.nodes['E']['pos'] = (shape[2], np.sum(offset) / 2)
