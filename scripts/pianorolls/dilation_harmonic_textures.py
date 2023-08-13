from pathlib import Path
import matplotlib.pyplot as plt

from mmm.pianorolls.music import TimeFrequency, TimePoint, FrequencyShift, TimeShift, TimeSignature, \
    Hit, Rhythm, Texture, Chord, Activations
from mmm.pianorolls.plot import plot_piano_roll

t_1 = Texture(
    Rhythm(Hit('0/16', '1/16')),
    Rhythm(Hit('1/16', '5/16')),
    Rhythm(Hit('2/16', '1/16')),
    Rhythm(Hit('3/16', '1/16')),
)

t_2 = Texture(
    Rhythm(Hit('-3/16', '1/16')),
    Rhythm(Hit('0/16', '2/16')),
    Rhythm(Hit('-1/16', '1/16')),
    Rhythm(Hit('-2/16', '1/16')),
)

t_2_prime = Texture(
    Rhythm(Hit('-3/16', '1/16')),
    Rhythm(Hit('-1/16', '1/16')),
    Rhythm(Hit('0/16', '2/16')),
    Rhythm(Hit('-2/16', '1/16')),
)

Dmin = Chord(69, 74, 76, 77, nature='point')
Dm = Chord(50, 57, 62, 65, nature='point')
A7 = Chord(69, 76, 77, 79, nature='point')
AM = Chord(45, 57, 61, 64, nature='point')

Dmin_2 = t_2 * Dmin
Dmin_2_prime = t_2_prime * Dmin
A7_2 = t_2 * A7
A7_2_prime = t_2_prime * A7
Dm_1 = t_1 * Dm
AM_1 = t_1 * AM

b_1 = Dmin_2
b_2 = Dmin_2_prime
b_3 = A7_2
b_4 = A7_2_prime
b_5 = Dm_1
b_6 = AM_1

# t = TimePoint(1, 1, 0, time_signature=(3, 8))
# f = FrequencyShift(0)
# tf = TimeFrequency(t, f)
a_1 = Activations(
    TimeFrequency(TimePoint(1, 1, 0, time_signature=(3, 8)), FrequencyShift(0)),
    TimeFrequency(TimePoint(2, 1, 0, time_signature=(3, 8)), FrequencyShift(0)),
    TimeFrequency(TimePoint(3, 1, 0, time_signature=(3, 8)), FrequencyShift(0)),
)

a_2 = Activations(
    TimeFrequency(TimePoint(4, 1, 0, time_signature=(3, 8)), FrequencyShift(0)),
)

a_3 = Activations(
    TimeFrequency(TimePoint(5, 1, 0, time_signature=(3, 8)), FrequencyShift(0)),
    TimeFrequency(TimePoint(6, 1, 0, time_signature=(3, 8)), FrequencyShift(0)),
    TimeFrequency(TimePoint(7, 1, 0, time_signature=(3, 8)), FrequencyShift(0)),
)

a_4 = Activations(
    TimeFrequency(TimePoint(8, 1, 0, time_signature=(3, 8)), FrequencyShift(0)),
)

a_5 = Activations(
    TimeFrequency(TimePoint(1, 1, 0, time_signature=(3, 8)), FrequencyShift(0)),
    TimeFrequency(TimePoint(2, 1, 0, time_signature=(3, 8)), FrequencyShift(0)),
    TimeFrequency(TimePoint(3, 1, 0, time_signature=(3, 8)), FrequencyShift(0)),
    TimeFrequency(TimePoint(8, 1, 0, time_signature=(3, 8)), FrequencyShift(0)),
)

a_6 = Activations(
    TimeFrequency(TimePoint(4, 1, 0, time_signature=(3, 8)), FrequencyShift(0)),
    TimeFrequency(TimePoint(5, 1, 0, time_signature=(3, 8)), FrequencyShift(0)),
    TimeFrequency(TimePoint(6, 1, 0, time_signature=(3, 8)), FrequencyShift(0)),
    TimeFrequency(TimePoint(7, 1, 0, time_signature=(3, 8)), FrequencyShift(0)),
)

p = (a_1 + b_1) + (a_2 + b_2) + (a_3 + b_3) + (a_4 + b_4) + (a_5 + b_5) + (a_6 + b_6)
p.time_signature = TimeSignature(3, 8)

plot_piano_roll(p, x_tick_start=TimePoint(-3, 8), x_tick_step=TimeShift(3, 8),
                time_label='Time (m, b)', fig_size=(640, 400))

folder = Path(__file__).parent.parent.parent / Path('phd') / Path('chapter_4')
folder.mkdir(parents=True, exist_ok=True)
fig_path = folder / Path('dilation_harmonic_textures.eps')

plt.savefig(fig_path)

plt.show()
