import matplotlib.pyplot as plt
from pathlib import Path

from mmm.pianorolls.midi import create_midi
from mmm.pianorolls.music import Hit, Rhythm, Texture, Chord, PianoRoll, \
    Activations, TimeFrequency, TimePoint, TimeShift, FrequencyPoint, \
    FrequencyExtension, FrequencyShift
from mmm.pianorolls.plot import plot_piano_roll

# Path
folder = Path('..') / Path('..') / Path('phd') / Path('chapter_5') / Path('structuring_elements')
folder.mkdir(parents=True, exist_ok=True)

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

i = Chord(0, 3, 7)
VI = Chord(0, 3, 8)
V = Chord(-1, 2, 7)
v = Chord(-2, 2, 7)

patterns = [i, VI, V, v]

harmonic_textures = [t * i, t * VI, t * V, t * v]

for h, harmonic_texture in enumerate(harmonic_textures):
    harmonic_texture.change_frequency_extension(FrequencyExtension(FrequencyShift(-2), FrequencyShift(9)))
    plot_piano_roll(harmonic_texture, fig_size=(360, 240),
                    y_tick_start=FrequencyShift(-2), y_tick_step=FrequencyShift(2))
    plt.savefig(folder / Path('harmonic_texture_%d.pdf' % (h + 1)))

A4 = FrequencyPoint(69)
activations_chords = [
    Activations(TimeFrequency(TimePoint('0/4'), A4)),
    Activations(TimeFrequency(TimePoint('1/4'), A4)),
    Activations(TimeFrequency(TimePoint('2/4'), A4)),
    Activations(TimeFrequency(TimePoint('3/4'), A4)),
]
piano_roll = PianoRoll()
for harmonic_texture, activations in zip(harmonic_textures, activations_chords):
    shifted_harmonic_texture = activations + harmonic_texture
    piano_roll = piano_roll + shifted_harmonic_texture

midi_file = create_midi(piano_roll)

plot_piano_roll(piano_roll, time_label='Time (m, b)', x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/4'),
                fig_size=(480, 360))

midi_path = folder / Path('example_1.mid')
file_path = folder / Path('example_1.pdf')

midi_file.save(midi_path)
plt.savefig(file_path)

plt.show()
