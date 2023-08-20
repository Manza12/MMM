import time

from mmm.pianorolls.algorithms import find_minimal_activations
from mmm.pianorolls.music import *
from mmm.pianorolls.morphology import erosion, dilation
from mmm.pianorolls.plot import plot_piano_roll, plot_activations_graph
from mmm.pianorolls.graphs import ActivationsGraph, DerivedActivationsGraph

# Parameters
plot = False

# Textures
texture = Texture(
    Rhythm(
        Hit('0/4', '1/2'),
    ),
    Rhythm(
        Hit('1/4', '1/4'),
    ),
)

# Harmonies
i_1 = Harmony(
    Chord(0),
    Chord(3),
)

i_2 = Harmony(
    Chord(0, 3),
    Chord(0),
)

# Harmonic textures
harmonic_textures = PianoRollStack(
    texture * i_1,
    texture * i_2,
    texture * i_1,
)

# Activations
start = TimePoint(1, 1, 0)
C4 = FrequencyPoint(60)
activations_harmonic_textures = ActivationsStack(
    Activations(TimeFrequency(start, C4)),
    Activations(TimeFrequency(start + TimeShift(1, 2), C4)),
    Activations(TimeFrequency(start + TimeShift(1, 1), C4)),
)

# Piano roll
piano_roll = dilation(activations_harmonic_textures, harmonic_textures)

# Erosion texture
activations_texture: ActivationsStack = erosion(piano_roll, texture)
activations_texture.change_extension(piano_roll.extension)

# Create graph
graph = ActivationsGraph(piano_roll, activations_texture.to_array(), texture)
print(graph)

# Synchronize textures
graph_synchronized = ActivationsGraph(piano_roll, activations_texture.synchronize(), texture)
print(graph_synchronized)

# Create derived graph of order 0
derived_graph = DerivedActivationsGraph(graph_synchronized)
print(derived_graph)

# Figures
if plot:
    # Erosion texture
    for j, activations in enumerate(activations_texture):
        plot_piano_roll(activations, time_label='Time (m, b)', tight_frame=False,
                        x_tick_start=TimePoint(0), x_tick_step=TimeShift('1'),
                        fig_size=(400, 260), marker_size=10)

    # Plot graph
    fig = plot_activations_graph(graph, fig_size=(8.5, 8.))

# Find minimal activations
start = time.time()
shortest_paths, min_activation_stacks, derived_graph = \
    find_minimal_activations(derived_graph, verbose=True, load=True)
print('Time to find minimal activations: %.3f s' % (time.time() - start))
print()

# Pick a single path
assert len(shortest_paths) == 1
shortest_path = shortest_paths[0]
min_activation_stack = min_activation_stacks[0]

# Minimal activations
for j, activations in enumerate(min_activation_stack):
    activations.change_extension(piano_roll.extension)
    plot_piano_roll(activations, time_label='Time (m, b)', tight_frame=False,
                    x_tick_start=TimePoint(0), x_tick_step=TimeShift('1'),
                    fig_size=(400, 260), marker_size=10)

plt.show()
