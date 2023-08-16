from mmm.pianorolls.algorithms import redundancy
from mmm.pianorolls.midi import create_midi
from mmm.pianorolls.music import *
from mmm.pianorolls.morphology import erosion, dilation
from mmm.pianorolls.plot import plot_piano_roll

# Parameters
c = {'attack': 0, 'sustain': 1}

# Path
folder = Path('..') / Path('..') / Path('phd') / Path('chapter_5') / Path('harmonic_textures')
folder.mkdir(parents=True, exist_ok=True)

# Textures
t_1 = Texture(
    Rhythm(
        Hit('0/8', '1/8'),
    ),
    Rhythm(
        Hit('1/8', '1/8'),
    )
)

t_2 = Texture(
    Rhythm(Hit('1/16', '1/16')),
    Rhythm(Hit('2/16', '1/16')),
    Rhythm(Hit('3/16', '1/16')),
    Rhythm(Hit('4/16', '1/16'))
)

# Chords
IP = Chord(0, 7)
I64 = Chord(7, 12, 15, 19)
I5 = Chord(0, 3, 7, 12)
I6 = Chord(3, 7, 12, 15)
I_full = Chord(0, 12, 24+7, 36, 36+3, 36+7)
I_full64 = Chord(7, 24+7, 36, 36+3, 36+7)

# Harmonic textures
harmonic_textures = [
    t_1 * IP,
    t_2 * I64,
    t_2 * I5,
    t_2 * I6,
    t_1 * Harmony(I_full, I_full64),
]

# Activations
start = TimePoint('0/4')
CS2 = FrequencyPoint(61-12-12)
activations_chords = [
    Activations(*[TimeFrequency(start + TimeShift(k, 4), CS2) for k in range(7)]),

    Activations(*[TimeFrequency(start + TimeShift(3 * k, 4), CS2 + FrequencyShift(12 * k)) for k in range(3)]),
    Activations(*[TimeFrequency(start + TimeShift(1 + 3 * k, 4), CS2 + FrequencyShift(12 * (k + 1))) for k in range(2)]),
    Activations(*[TimeFrequency(start + TimeShift(2 + 3 * k, 4), CS2 + FrequencyShift(12 * (k + 1))) for k in range(2)]),

    Activations(TimeFrequency(start + TimeShift(7, 4), CS2))
]

# Piano roll
piano_roll = PianoRoll()
for harmonic_texture, activations in zip(harmonic_textures, activations_chords):
    shifted_harmonic_texture = activations + harmonic_texture
    piano_roll = piano_roll + shifted_harmonic_texture

print('Measure of the piano roll:', piano_roll.measure(c))

midi_file = create_midi(piano_roll, tempo=120)
midi_path = folder / Path('moonlight_3rd.mid')
midi_file.save(midi_path)

# Trivial erosion
hit_8 = Hit('0', '1/8')
hit_16 = Hit('0', '1/16')
note_values = PianoRollStack(hit_8, hit_16)
activations_note_values: ActivationsStack = erosion(piano_roll, note_values)

print('Redundancy of hit_8: %.1f%%' % redundancy(piano_roll, note_values, c))

# # Packing two by two
# B_2_by_2 = PianoRollStack(
#     piano_roll[TimePoint('1/16'): TimePoint('3/16'), FrequencyPoint(69): FrequencyPoint(73)],
#     piano_roll[TimePoint('3/16'): TimePoint('5/16'), FrequencyPoint(69): FrequencyPoint(78)],
#     piano_roll[TimePoint('7/16'): TimePoint('9/16'), FrequencyPoint(69): FrequencyPoint(79)],
#     piano_roll[TimePoint('13/16'): TimePoint('15/16'), FrequencyPoint(67): FrequencyPoint(72)],
#     piano_roll[TimePoint('15/16'): TimePoint('17/16'), FrequencyPoint(67): FrequencyPoint(77)],
# )
#
# for j, b in enumerate(B_2_by_2):
#     B_2_by_2[j] = b - TimeFrequency(b.origin.time, b.origin.frequency)
#
# A_2_by_2 = erosion(piano_roll, B_2_by_2)
# piano_roll_two_by_two = dilation(A_2_by_2, B_2_by_2)

# Figures
# Eighth note
plot_piano_roll(hit_8.change_tatum(TimeShift(1, 16)),
                tight_frame=False, fig_size=(360, 240),
                x_tick_start=TimeShift(0), x_tick_step=TimeShift('1/8'))
file_path = folder / Path('eighth_note.pdf')
plt.savefig(file_path)

# Sixteenth note
plot_piano_roll(hit_16, tight_frame=False, fig_size=(360, 240),
                x_tick_start=TimeShift(0), x_tick_step=TimeShift('1/16'))
file_path = folder / Path('sixteenth_note.pdf')
plt.savefig(file_path)

# Erosion trivial
for j, activations in enumerate(activations_note_values):
    plot_piano_roll(activations, time_label='Time (m, b)', tight_frame=False,
                    x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/2'),
                    fig_size=(400, 200))
    file_path = folder / Path('erosion_hits-%d.pdf' % (j + 1))
    plt.savefig(file_path)

# # Erosion two by two
# for j, a in enumerate(A_2_by_2):
#     a: Activations
#     a.change_tatum(piano_roll.tatum, inplace=True)
#     a.change_extension(piano_roll.extension)
#     plot_piano_roll(a, time_label='Time (m, b)',
#                     x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/4'),
#                     fig_size=(400, 200))
#     file_path = folder / Path('erosion_2_by_2-%d.pdf' % (j + 1))
#     plt.savefig(file_path)
#
# # Dilation
# piano_roll_two_by_two.change_extension(piano_roll.extension)
# plot_piano_roll(piano_roll_two_by_two, time_label='Time (m, b)',
#                 x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/4'),
#                 fig_size=(400, 200))
# file_path = folder / Path('dilation_2_by_2.pdf')
# plt.savefig(file_path)
#
# # Harmonic textures
# for h, harmonic_texture in enumerate(harmonic_textures):
#     harmonic_texture.change_frequency_extension(FrequencyExtension(FrequencyShift(-2), FrequencyShift(9)))
#     plot_piano_roll(harmonic_texture, fig_size=(360, 240),
#                     y_tick_start=FrequencyShift(-2), y_tick_step=FrequencyShift(2))
#     file_path = folder / Path('harmonic_texture_%d.pdf' % (h + 1))
#     plt.savefig(file_path)

# Piano roll
# Big
plot_piano_roll(piano_roll, time_label='Time (m, b)',
                x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/2'),
                fig_size=(800, 400), tight_frame=False)

file_path = folder / Path('piano_roll.pdf')
plt.savefig(file_path)

# # Small
# plot_piano_roll(piano_roll, time_label='Time (m, b)',
#                 x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/4'),
#                 fig_size=(400, 200))
# file_path = folder / Path('example_small.pdf')
# plt.savefig(file_path)

plt.show()
