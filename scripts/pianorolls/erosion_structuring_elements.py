from mmm.pianorolls.music import *
from mmm.pianorolls.algorithms import redundancy
from mmm.pianorolls.midi import create_midi
from mmm.pianorolls.morphology import erosion, dilation
from mmm.pianorolls.plot import plot_piano_roll, plot_activations_stack

# Parameters
mpl.rcParams['figure.max_open_warning'] = 25
c_attack = {'attack': 1, 'sustain': 0}
c_sustain = {'attack': 0, 'sustain': 1}

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
harmonic_textures = PianoRollStack(
    t_1 * IP,
    t_1 * Harmony(I_full, I_full64),
    t_2 * I64,
    t_2 * I5,
    t_2 * I6,
)

# Activations
start = TimePoint('0/4')
CS2 = FrequencyPoint(61-12-12)
activations_harmonic_textures = ActivationsStack(
    Activations(*[TimeFrequency(start + TimeShift(k, 4), CS2) for k in range(7)]),
    Activations(TimeFrequency(start + TimeShift(7, 4), CS2)),
    Activations(*[TimeFrequency(start + TimeShift(3 * k, 4), CS2 + FrequencyShift(12 * k)) for k in range(3)]),
    Activations(*[TimeFrequency(start + TimeShift(1 + 3 * k, 4), CS2 + FrequencyShift(12 * (k+1))) for k in range(2)]),
    Activations(*[TimeFrequency(start + TimeShift(2 + 3 * k, 4), CS2 + FrequencyShift(12 * (k+1))) for k in range(2)]),
)

# Piano roll
piano_roll = dilation(activations_harmonic_textures, harmonic_textures)
print('Measure of the piano roll (attack):', piano_roll.measure(c_attack))
print('Measure of the piano roll (sustain):', piano_roll.measure(c_sustain))
print()

midi_file = create_midi(piano_roll, tempo=120)
midi_path = folder / Path('moonlight_3rd.mid')
midi_file.save(midi_path)

# Trivial erosion
hit_8 = Hit('0', '1/8')
hit_16 = Hit('0', '1/16')
note_values = PianoRollStack(hit_8, hit_16)
activations_note_values: ActivationsStack = erosion(piano_roll, note_values)

# Redundancy
print('Measure of A_8:', activations_note_values[0].measure())
print('Measure of A_16:', activations_note_values[1].measure())
print()
print('Redundancy of note_values (attack): %.1f%%' % redundancy(piano_roll, note_values, c_attack))
print('Redundancy of note_values (sustain): %.1f%%' % redundancy(piano_roll, note_values, c_sustain))
print()

# Optimal erosion
activations_harmonic_textures: ActivationsStack = erosion(piano_roll, harmonic_textures)

# Measure and redundancy
for a, activations in enumerate(activations_harmonic_textures):
    print('Measure of activations %d:' % (a + 1), activations.measure())
print()
print('Redundancy of harmonic_textures (attack): %.1f%%' % redundancy(piano_roll, harmonic_textures, c_attack))
print('Redundancy of harmonic_textures (sustain): %.1f%%' % redundancy(piano_roll, harmonic_textures, c_sustain))
print()

# Figures
# Piano roll
plot_piano_roll(piano_roll, time_label='Time (m, b)',
                x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/2'),
                fig_size=(800, 400), tight_frame=False)

file_path = folder / Path('piano_roll.pdf')
plt.savefig(file_path)

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
                    fig_size=(360, 300), marker_size=10)
    file_path = folder / Path('erosion_note_values-%d.pdf' % (j + 1))
    plt.savefig(file_path)

# Dilation trivial
for j, pair in enumerate(zip(activations_note_values, note_values)):
    activations, note_value = pair
    d: PianoRoll = dilation(activations, note_value)
    d.change_tatum(piano_roll.tatum, inplace=True)
    plot_piano_roll(d, time_label='Time (m, b)', tight_frame=False,
                    x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/2'),
                    fig_size=(360, 300))
    file_path = folder / Path('dilation_note_values-%d.pdf' % (j + 1))
    plt.savefig(file_path)

# Harmonic textures
fig_sizes = [(216, 216), (324, 216), (324, 216), (324, 216), (216, 216)]
for h, harmonic_texture in enumerate(harmonic_textures):
    plot_piano_roll(harmonic_texture, fig_size=fig_sizes[h], tight_frame=False,
                    x_tick_start=TimeShift(0), x_tick_step=TimeShift('1/8'))
    file_path = folder / Path('harmonic_texture-%d.pdf' % (h + 1))
    plt.savefig(file_path)

# Erosion optimal
activations_harmonic_textures.change_tatum(inplace=True)
activations_harmonic_textures.change_extension(piano_roll.extension)
plot_activations_stack(activations_harmonic_textures,
                       time_label='Time (m, b)', tight_frame=False,
                       x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/2'),
                       fig_size=(360, 300), marker_size=20, legend=True,
                       legend_params={'loc': 'upper left', 'ncol': 2, 'columnspacing': 0.8,
                                      'labelspacing': 0.1})
file_path = folder / Path('erosion_harmonic_textures.pdf')
plt.savefig(file_path)

# Dilation optimal
for j, pair in enumerate(zip(activations_harmonic_textures, harmonic_textures)):
    activations, note_value = pair
    d: PianoRoll = dilation(activations, note_value)
    d.change_tatum(piano_roll.tatum, inplace=True)
    d.reduce(inplace=True)
    d.change_extension(piano_roll.extension)
    plot_piano_roll(d, time_label='Time (m, b)', tight_frame=False,
                    x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/2'),
                    fig_size=(360, 300))
    file_path = folder / Path('dilation_harmonic_textures-%d.pdf' % (j + 1))
    plt.savefig(file_path)

# Dilation optimal (reduced)
d = dilation(activations_harmonic_textures, harmonic_textures)

plot_piano_roll(d, time_label='Time (m, b)',
                x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/2'),
                fig_size=(800, 400), tight_frame=False)

file_path = folder / Path('dilation_harmonic_textures.pdf')
plt.savefig(file_path)

plt.show()
