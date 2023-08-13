from pathlib import Path
import matplotlib.pyplot as plt

from mmm.pianorolls.generation import Hit, Rhythm, Texture, Chord, Activations
from mmm.pianorolls.music import TimeFrequency, TimePoint, FrequencyShift, TimeShift, TimeSignature
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

d_min = Chord(69, 74, 76, 77, nature='point')
d_m = Chord(50, 57, 62, 65, nature='point')
a_7 = Chord(69, 76, 77, 79, nature='point')
a_m = Chord(45, 57, 61, 64, nature='point')

d_min_2 = t_2 * d_min
d_min_2_prime = t_2_prime * d_min
a_7_2 = t_2 * a_7
a_7_2_prime = t_2_prime * a_7
d_m_1 = t_1 * d_m
a_m_1 = t_1 * a_m

b_1 = d_min_2
b_2 = d_min_2_prime
b_3 = a_7_2
b_4 = a_7_2_prime
b_5 = d_m_1
b_6 = a_m_1

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
