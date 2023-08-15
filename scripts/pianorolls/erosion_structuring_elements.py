import matplotlib.pyplot as plt
from pathlib import Path

from mmm.pianorolls.music import Hit, Rhythm, Texture, Chord, PianoRoll, \
    Activations, TimeFrequency, TimePoint, TimeShift, FrequencyShift
from mmm.pianorolls.plot import plot_piano_roll

texture = Texture(
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

Am = Chord(69, 72, 76)
FM = Chord(69, 72, 77)
EM = Chord(68, 71, 76)
Em = Chord(68, 71, 75)

chords = [Am, FM, EM, Em]
activations_chords = [
    Activations(TimeFrequency(TimePoint('0/4'), FrequencyShift(0))),
    Activations(TimeFrequency(TimePoint('1/4'), FrequencyShift(0))),
    Activations(TimeFrequency(TimePoint('2/4'), FrequencyShift(0))),
    Activations(TimeFrequency(TimePoint('3/4'), FrequencyShift(0))),
]
piano_roll = PianoRoll()
for chord, activations in zip(chords, activations_chords):
    piano_roll += activations + texture * chord

plot_piano_roll(piano_roll, time_label='Time (m, b)', x_tick_start=TimePoint(0), x_tick_step=TimeShift('1/4'))

folder = Path('..') / Path('..') / Path('phd') / Path('chapter_5')
folder.mkdir(parents=True, exist_ok=True)
file_path = folder / Path('example_1.pdf')
plt.savefig(file_path)

plt.show()
