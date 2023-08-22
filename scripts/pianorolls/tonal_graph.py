import matplotlib.pyplot as plt
from pathlib import Path
import networkx as nx

from mmm.pianorolls.graphs import TonalGraph
from mmm.pianorolls.midi import create_midi
from mmm.pianorolls.music import Rhythm, Hit, Texture, Harmony, Chord, PianoRoll, PianoRollStack, ActivationsStack, \
    Activations, TimeFrequency, TimePoint, TimeShift, FrequencyPoint, RomanNumeral
from mmm.pianorolls.morphology import dilation, erosion
from mmm.pianorolls.plot import plot_piano_roll, plot_activations_stack, plot_tonal_graph_vertices

# Path
piece = 'moonlight_3rd_53-56'
folder = Path('..') / Path('..') / Path('phd') / Path('chapter_5') / Path('harmony') / Path(piece)
folder.mkdir(parents=True, exist_ok=True)

# Textures
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

harmonic_textures = PianoRollStack(
    texture_homogeneous * i,
    texture_homogeneous * iv,
    texture_homogeneous * i46,
    texture_homogeneous * V24,
    texture_homogeneous * i6,
    texture_homogeneous * Np,
    texture_homogeneous * i46_2,
    texture_homogeneous * V,
)

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

# Piano roll
piano_roll: PianoRoll = dilation(activations_harmonic_textures, harmonic_textures)

piano_roll.change_tatum(TimeShift(1, 4), inplace=True)
midi_file = create_midi(piano_roll, tempo=120)
midi_path = folder / Path(piece + '.mid')
midi_file.save(midi_path)

piano_roll.change_tatum(TimeShift(1, 2), inplace=True)

# Get activations
activations_stack = erosion(piano_roll, Texture(Rhythm(Hit('0', '1/2'))))
activations = activations_stack[0]

# To chroma roll
activations_chroma = activations.to_chroma_roll()

# Erode harmony
harmony = Harmony(
    RomanNumeral(0, 4, 7, label='I'),
    RomanNumeral(0, 3, 7, label='i'),
    RomanNumeral(2, 5, 9, label='ii'),
    RomanNumeral(2, 5, 8, label='ii°'),
    RomanNumeral(0, 5, 9, label='IV'),
    RomanNumeral(0, 5, 8, label='iv'),
    RomanNumeral(2, 7, 11, label='V'),
    RomanNumeral(0, 2, 7, label='V$^{45}$'),
    RomanNumeral(0, 4, 9, label='vi'),
    RomanNumeral(0, 3, 8, label='VI'),
    RomanNumeral(2, 5, 11, label='vii°'),
    RomanNumeral(1, 5, 8, label='N'),
)

activations_harmony: ActivationsStack = erosion(activations_chroma, harmony)
activations_harmony.change_tatum(piano_roll.tatum, inplace=True)
activations_harmony.change_extension(activations_chroma.extension)

# Remove empty activations
for activations, chord in zip(activations_harmony, harmony):
    if len(activations) == 0:
        activations_harmony.remove(activations)
        harmony.remove(chord)

# Tonal graph
tonal_graph = TonalGraph(activations_harmony, harmony, activations)

# Tonal graph - path
tonal_graph_path = TonalGraph(activations_harmony, harmony, activations, terminal_nodes=True)

# Shortest path
shortest_path = nx.shortest_path(tonal_graph_path, 'S', 'E', weight='weight')

# Plot activations input
plot_piano_roll(activations, time_label='Time (m, b)', tight_frame=False,
                x_tick_start=TimePoint(0), x_tick_step=TimeShift('1'),
                fig_size=(460, 260), marker_size=10)
plt.savefig(folder / Path('activations.pdf'))

plot_piano_roll(activations_chroma, time_label='Time (m, b)', tight_frame=False,
                x_tick_start=TimePoint(0), x_tick_step=TimeShift('1'),
                fig_size=(460, 260), marker_size=10)
plt.savefig(folder / Path('activations_chroma.pdf'))

# Plot activations harmony
plot_activations_stack(activations_harmony, time_label='Time (m, b)',
                       tight_frame=False,
                       x_tick_start=TimePoint(0), x_tick_step=TimeShift('1'),
                       fig_size=(600, 300), marker_size=10,
                       legend=True,
                       legend_params={
                           'columnspacing': 0.2,
                           'labelspacing': 0.,
                           'handletextpad': 0.1,
                           'labels': [rn.label for i, rn in enumerate(harmony) if len(activations_harmony[i]) != 0],
                           'outside': True,
                       })
plt.savefig(folder / Path('activations_harmony.pdf'))

# Plot graph
plot_tonal_graph_vertices(tonal_graph)
plt.savefig(folder / Path('tonal_graph.pdf'))

plot_tonal_graph_vertices(tonal_graph_path, shortest_path=shortest_path)
plt.savefig(folder / Path('tonal_graph-shortest_path.pdf'))

plt.show()
