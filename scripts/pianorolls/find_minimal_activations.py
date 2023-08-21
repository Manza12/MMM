import time
import logging

from mmm.pianorolls.algorithms import find_minimal_activations
from mmm.pianorolls.music import *
from mmm.pianorolls.midi import create_midi
from mmm.pianorolls.morphology import erosion, dilation
from mmm.pianorolls.plot import plot_piano_roll, plot_activations_graph, plot_activations_stack
from mmm.pianorolls.graphs import ActivationsGraph, DerivedActivationsGraph

# Parameters
full = False
sync = True
sparse = True

load = True
log = False
TimePoint.__str__ = lambda self: '(%s, %s)' % (self.beat, self.offset)

# Path
piece = 'moonlight_3rd' + ('_53-56' if full else '_54') + ('_sync' if sync else '') + ('_sparse' if sparse else '')
folder = Path('..') / Path('..') / Path('phd') / Path('chapter_5') / Path('minimal_activations') / Path(piece)
folder.mkdir(parents=True, exist_ok=True)

# Log
if log:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(folder / 'log.txt'),
            logging.StreamHandler()
        ]
    )

# Textures
texture = Texture(
    Rhythm(
        Hit('0/8', '1/8'),
    ),
    Rhythm(
        Hit('1/8', '1/8'),
        Hit('2/8', '1/8'),
    ),
    Rhythm(
        Hit('3/8', '1/8'),
    ),
)

texture_homogeneous = Texture(
    Rhythm(
        Hit('0', '1/2'),
    ),
    Rhythm(
        Hit('0', '1/2'),
    ),
    Rhythm(
        Hit('0', '1/2'),
    ),
)

# Harmonies
i = Harmony(
    Chord(-12, 0, 12+3, 24, 24+3),
    Chord(3, 7, 24, 24+3),
    Chord(0, 3, 24+3, 24+7),
)
iv = Harmony(
    Chord(-7),
    Chord(5, 8, 24, 24+5),
    Chord(0, 5, 24+5, 24+8),
)
i46 = Harmony(
    Chord(-5),
    Chord(3, 7, 24, 24+3),
    Chord(0, 3, 24+3, 24+7),
)
V24 = Harmony(
    Chord(-7),
    Chord(2, 7, 24-1, 24+2),
    Chord(-1, 2, 24+2, 24+7),
)
i6 = Harmony(
    Chord(-9),
    Chord(7, 12, 12+7, 24+3),
    Chord(0, 3, 24+3, 24+7),
)
Np = Harmony(
    Chord(-7),
    Chord(8, 13, 12+5, 24+1),
    Chord(5, 8, 12+8, 24+5),
)
i46_2 = Harmony(
    Chord(-5),
    Chord(7, 12, 12+3, 24),
    Chord(3, 7, 12+7, 24+3),
)
V = Harmony(
    Chord(-5),
    Chord(5, 11, 12+2, 24-1),
    Chord(-1, 5, 12+5, 24+2),
)

# Harmonic textures
if full:
    harmonic_textures = PianoRollStack(
        texture * i,
        texture * iv,
        texture * i46,
        texture * V24,
        texture * i6,
        texture * Np,
        texture * i46_2,
        texture * V,
    )
else:
    harmonic_textures = PianoRollStack(
        texture * i46,
        texture * V24,
    )

# Activations
if full:
    start = TimePoint(53, 1, 0)
    Gs3 = FrequencyPoint(56)
    activations_harmonic_textures = ActivationsStack(
        Activations(TimeFrequency(start, Gs3)),
        Activations(TimeFrequency(start + TimeShift(1, 2), Gs3)),
        Activations(TimeFrequency(start + TimeShift(2, 2), Gs3)),
        Activations(TimeFrequency(start + TimeShift(3, 2), Gs3)),
        Activations(TimeFrequency(start + TimeShift(4, 2), Gs3)),
        Activations(TimeFrequency(start + TimeShift(5, 2), Gs3)),
        Activations(TimeFrequency(start + TimeShift(6, 2), Gs3)),
        Activations(TimeFrequency(start + TimeShift(7, 2), Gs3)),
    )
else:
    start = TimePoint(54, 1, 0)
    Gs3 = FrequencyPoint(56)
    activations_harmonic_textures = ActivationsStack(
        Activations(TimeFrequency(start, Gs3)),
        Activations(TimeFrequency(start + TimeShift(1, 2), Gs3)),
    )

# Piano roll
piano_roll = dilation(activations_harmonic_textures, harmonic_textures)

midi_file = create_midi(piano_roll, tempo=120)
midi_path = folder / Path(piece + '.mid')
midi_file.save(midi_path)

# Erosion texture
activations_texture: ActivationsStack = erosion(piano_roll, texture)
activations_texture.change_extension(piano_roll.extension)

# Create graph
if sparse:
    graph = ActivationsGraph(piano_roll, activations_texture, texture, lexicographic_priority='frequency')
else:
    graph = ActivationsGraph(piano_roll, activations_texture, texture, lexicographic_priority='time')
if log:
    logging.info(graph)
    logging.info('Clusters size: %s' % [len(cluster) for cluster in graph.clusters])

# Synchronize textures
if sync:
    graph = ActivationsGraph(piano_roll, activations_texture.synchronize(), texture)
if log:
    logging.info(graph)
    logging.info('Clusters size: %s' % [len(cluster) for cluster in graph.clusters])

# Plot graph
fig = plot_activations_graph(graph, fig_size=(8.5, 4.), plot_edges=True,
                             node_font_size=8, grid_font_size=10, node_size=1000)

# Create derived graph of order 0
derived_graph = DerivedActivationsGraph(graph)
if log:
    logging.info(derived_graph)

# Find minimal activations
start = time.time()
shortest_paths, min_activation_stacks, derived_graph = \
    find_minimal_activations(derived_graph, folder_save=folder, verbose=log, load=load, sparse=sparse)
if log:
    logging.info('Time to find minimal activations: %.3f s' % (time.time() - start))

# Pick a single path
if len(shortest_paths) == 0:
    if log:
        logging.info('No shortest path found')
else:
    if len(shortest_paths) > 1:
        if log:
            logging.info('Found %d shortest paths' % len(shortest_paths))
            logging.info('Picking the first path')
        shortest_path = shortest_paths[0]
        min_activation_stack = min_activation_stacks[0]
    else:
        if log:
            logging.info('Found 1 shortest path')
        shortest_path = shortest_paths[0]
        min_activation_stack = min_activation_stacks[0]

    collpased_piano_roll = dilation(min_activation_stack, texture_homogeneous)

    midi_file = create_midi(collpased_piano_roll, tempo=120, ticks_per_beat=1)
    midi_path = folder / Path('moonlight_3rd_53-56_collapsed.mid')
    midi_file.save(midi_path)

    # Minimal activations
    for j, activations in enumerate(min_activation_stack):
        activations.change_tatum(piano_roll.tatum)
        activations.change_extension(piano_roll.extension)
        plot_piano_roll(activations, time_label='Time (m, b)', tight_frame=False,
                        x_tick_start=TimePoint(0), x_tick_step=TimeShift('1'),
                        fig_size=(400, 260), marker_size=10)
        plt.savefig(folder / Path('minimal_activations_%d.pdf' % j))

    # Plot together
    plot_activations_stack(min_activation_stack, time_label='Time (m, b)',
                           tight_frame=False,
                           x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/2'),
                           fig_size=(400, 260), marker_size=10,
                           legend=True,
                           legend_params={
                               'columnspacing': 0.2,
                               'labelspacing': 0.,
                               'handletextpad': 0.1
                           })
    plt.savefig(folder / Path('minimal_activations.pdf'))

plt.show()
