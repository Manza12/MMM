import matplotlib.pyplot as plt
from pathlib import Path

from mmm.pianorolls.midi import create_midi
from mmm.pianorolls.music import Hit, Rhythm, Texture, Chord, PianoRoll, \
    Activations, TimeFrequency, TimePoint, TimeShift, FrequencyPoint, \
    FrequencyExtension, FrequencyShift, TimeExtension, Extension
from mmm.pianorolls.morphology import erosion_piano_roll
from mmm.pianorolls.plot import plot_piano_roll

# Path
folder = Path('..') / Path('..') / Path('phd') / Path('chapter_5') / Path('structuring_elements')
folder.mkdir(parents=True, exist_ok=True)

# Texture
t = Texture(
    Rhythm(
        Hit('1/16', '1/16'),
        Hit('3/16', '1/16'),
    ),
    Rhythm(
        Hit('2/16', '1/16'),
    ),
    Rhythm(
        Hit('4/16', '1/16'),
    ),
)

# Chords
i = Chord(0, 3, 7)
VI = Chord(0, 3, 8)
V = Chord(-1, 2, 7)
v = Chord(-2, 2, 7)

patterns = [i, VI, V, v]

# Harmonic textures
harmonic_textures = [t * i, t * VI, t * V, t * v]

# Activations
A4 = FrequencyPoint(69)
activations_chords = [
    Activations(TimeFrequency(TimePoint('0/4'), A4)),
    Activations(TimeFrequency(TimePoint('1/4'), A4)),
    Activations(TimeFrequency(TimePoint('2/4'), A4)),
    Activations(TimeFrequency(TimePoint('3/4'), A4)),
]

# Piano roll
piano_roll = PianoRoll()
for harmonic_texture, activations in zip(harmonic_textures, activations_chords):
    shifted_harmonic_texture = activations + harmonic_texture
    piano_roll = piano_roll + shifted_harmonic_texture
time_extension = TimeExtension(TimePoint('0/4'), piano_roll.extension.time.end + piano_roll.tatum)
frequency_extension = FrequencyExtension(piano_roll.extension.frequency.lower - piano_roll.step,
                                         piano_roll.extension.frequency.higher + piano_roll.step)
extension = Extension(time_extension, frequency_extension)
piano_roll.change_extension(extension)

midi_file = create_midi(piano_roll)
midi_path = folder / Path('example_1.mid')
midi_file.save(midi_path)

# Trivial erosion
hit_16 = Hit('0', '1/16')
activations_16 = erosion_piano_roll(piano_roll, hit_16)

# Figures
# Sixteenth note
plot_piano_roll(hit_16, tight_frame=False, fig_size=(360, 240),
                x_tick_start=TimeShift(0), x_tick_step=TimeShift('1/16'))
file_path = folder / Path('sixteenth_note.pdf')
plt.savefig(file_path)

# Erosion
plot_piano_roll(activations_16, time_label='Time (m, b)',
                x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/4'),
                fig_size=(400, 200))
file_path = folder / Path('erosion_16.pdf')
plt.savefig(file_path)

# Harmonic textures
for h, harmonic_texture in enumerate(harmonic_textures):
    harmonic_texture.change_frequency_extension(FrequencyExtension(FrequencyShift(-2), FrequencyShift(9)))
    plot_piano_roll(harmonic_texture, fig_size=(360, 240),
                    y_tick_start=FrequencyShift(-2), y_tick_step=FrequencyShift(2))
    file_path = folder / Path('harmonic_texture_%d.pdf' % (h + 1))
    plt.savefig(file_path)

# Piano roll
# Big
plot_piano_roll(piano_roll, time_label='Time (m, b)',
                x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/4'),
                fig_size=(480, 300))

file_path = folder / Path('example_1.pdf')
plt.savefig(file_path)

# Small
plot_piano_roll(piano_roll, time_label='Time (m, b)',
                x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/4'),
                fig_size=(400, 200))
file_path = folder / Path('example_small.pdf')
plt.savefig(file_path)

plt.show()
