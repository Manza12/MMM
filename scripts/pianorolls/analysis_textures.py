from mmm.pianorolls.music import *
from mmm.pianorolls.midi import create_midi
from mmm.pianorolls.morphology import erosion, dilation
from mmm.pianorolls.plot import plot_piano_roll  # , plot_activations_stack

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

# Activations
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
piano_roll = dilation(activations_harmonic_textures, harmonic_textures)

midi_file = create_midi(piano_roll, tempo=120)
midi_path = folder / Path('moonlight_3rd_53-56.mid')
midi_file.save(midi_path)

# Erosion texture
activations_texture: ActivationsStack = erosion(piano_roll, texture)

# Figures
# Piano roll
plot_piano_roll(piano_roll, time_label='Time (m, b)',
                x_tick_start=TimePoint(0), x_tick_step=TimeShift('1'),
                fig_size=(460, 280), tight_frame=False)

file_path = folder / Path('piano_roll.pdf')
plt.savefig(file_path)

# Erosion texture
for j, activations in enumerate(activations_texture):
    plot_piano_roll(activations, time_label='Time (m, b)', tight_frame=False,
                    x_tick_start=TimePoint(0), x_tick_step=TimeShift('1'),
                    fig_size=(400, 260), marker_size=10)
    file_path = folder / Path('erosion_texture-%d.pdf' % (j + 1))
    plt.savefig(file_path)

# Dilation texture
for j, pair in enumerate(zip(activations_texture, texture)):
    activations, rhythm = pair
    d: PianoRoll = dilation(activations, rhythm)
    d.change_tatum(piano_roll.tatum, inplace=True)
    d.change_extension(piano_roll.extension)
    plot_piano_roll(d, time_label='Time (m, b)', tight_frame=False,
                    x_tick_start=TimePoint(0), x_tick_step=TimeShift('1'),
                    fig_size=(460, 260))
    file_path = folder / Path('dilation_texture-%d.pdf' % (j + 1))
    plt.savefig(file_path)

# # Harmonic textures
# fig_sizes = [(216, 216), (324, 216), (324, 216), (324, 216), (216, 216)]
# for h, harmonic_texture in enumerate(harmonic_textures):
#     plot_piano_roll(harmonic_texture, fig_size=fig_sizes[h], tight_frame=False,
#                     x_tick_start=TimeShift(0), x_tick_step=TimeShift('1/8'))
#     file_path = folder / Path('harmonic_texture-%d.pdf' % (h + 1))
#     plt.savefig(file_path)
#
# # Erosion optimal
# activations_harmonic_textures.change_tatum(inplace=True)
# activations_harmonic_textures.change_extension(piano_roll.extension)
# plot_activations_stack(activations_harmonic_textures,
#                        time_label='Time (m, b)', tight_frame=False,
#                        x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/2'),
#                        fig_size=(500, 300), marker_size=20, legend=True,
#                        legend_params={'loc': 'upper left', 'ncol': 2, 'columnspacing': 0.2,
#                                       'labelspacing': 0., 'fontsize': 'large'})
# file_path = folder / Path('erosion_harmonic_textures.pdf')
# plt.savefig(file_path)
#
# # Dilation optimal
# for j, pair in enumerate(zip(activations_harmonic_textures, harmonic_textures)):
#     activations, note_value = pair
#     d: PianoRoll = dilation(activations, note_value)
#     d.change_tatum(piano_roll.tatum, inplace=True)
#     d.reduce(inplace=True)
#     d.change_extension(piano_roll.extension)
#     plot_piano_roll(d, time_label='Time (m, b)', tight_frame=False,
#                     x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/2'),
#                     fig_size=(360, 300))
#     file_path = folder / Path('dilation_harmonic_textures-%d.pdf' % (j + 1))
#     plt.savefig(file_path)
#
# # Dilation optimal (reduced)
# d = dilation(activations_harmonic_textures, harmonic_textures)
#
# plot_piano_roll(d, time_label='Time (m, b)',
#                 x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/2'),
#                 fig_size=(800, 400), tight_frame=False)
#
# file_path = folder / Path('dilation_harmonic_textures.pdf')
# plt.savefig(file_path)

plt.show()
