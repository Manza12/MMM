from mmm.pianorolls.music import *
from mmm.pianorolls.midi import create_midi
from mmm.pianorolls.morphology import erosion, dilation
from mmm.pianorolls.plot import plot_piano_roll, plot_activations_stack, plot_activations_graph
from mmm.pianorolls.graphs import ActivationsGraph


# Parameters
plot = False
TimePoint.__str__ = lambda self: '(%s, %s)' % (self.beat, self.offset)

# Path
folder = Path('..') / Path('..') / Path('phd') / Path('chapter_5') / Path('textures')
folder.mkdir(parents=True, exist_ok=True)

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

# Harmonies
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

# Harmonic textures
harmonic_textures = PianoRollStack(
    texture * i46,
    texture * V24,
)

# Activations
start = TimePoint(54, 1, 0)
Gs3 = FrequencyPoint(56)
activations_harmonic_textures = ActivationsStack(
    Activations(TimeFrequency(start, Gs3)),
    Activations(TimeFrequency(start + TimeShift(1, 2), Gs3)),
)

# Piano roll
piano_roll = dilation(activations_harmonic_textures, harmonic_textures)

midi_file = create_midi(piano_roll, tempo=120)
midi_path = folder / Path('moonlight_3rd_54.mid')
midi_file.save(midi_path)

# Erosion texture
activations_texture: ActivationsStack = erosion(piano_roll, texture)
activations_texture.change_extension(piano_roll.extension)

# Create graph
graph = ActivationsGraph(piano_roll, activations_texture.to_array(), texture)

# Figures
if plot:
    # Piano roll
    plot_piano_roll(piano_roll, time_label='Time (m, b)',
                    x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/2'),
                    fig_size=(460, 280), tight_frame=False)

    file_path = folder / Path('piano_roll-54.pdf')
    plt.savefig(file_path)

    # Erosion texture
    plot_activations_stack(activations_texture, time_label='Time (m, b)',
                           tight_frame=False,
                           x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/2'),
                           fig_size=(400, 260), marker_size=10,
                           legend=True,
                           legend_params={
                               'columnspacing': 0.2,
                               'labelspacing': 0.,
                               'handletextpad': 0.1
                           })
    file_path = folder / Path('erosion_texture-54.pdf')
    plt.savefig(file_path)

# Plot graph - vertices
fig = plot_activations_graph(graph, fig_size=(8.5, 8.))
file_path = folder / Path('graph-54.pdf')
fig.savefig(file_path)

# Plot graph - edges
fig = plot_activations_graph(graph, fig_size=(8.5, 4.), plot_edges=True,
                             node_font_size=8, grid_font_size=10, node_size=1000)
file_path = folder / Path('graph-54_edges.pdf')
fig.savefig(file_path)

plt.show()
