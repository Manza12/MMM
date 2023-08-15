from pathlib import Path
import matplotlib.pyplot as plt

from mmm.pianorolls.midi import create_midi
from mmm.pianorolls.music import TimeFrequency, TimePoint, FrequencyPoint, TimeShift, TimeSignature,\
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

Qmin = Chord(-5, 0, 2, 3, nature='point')
Qm = Chord(0, 7, 12, 15, nature='point')
Q7 = Chord(-5, 2, 3, 5, nature='point')
QM = Chord(-5, 7, 11, 2, nature='point')

Qmin_2 = t_2 * Qmin
Qmin_2_prime = t_2_prime * Qmin
Q7_2 = t_2 * Q7
Q7_2_prime = t_2_prime * Q7
Qm_1 = t_1 * Qm
QM_1 = t_1 * QM

b_1 = Qmin_2
b_2 = Qmin_2_prime
b_3 = Q7_2
b_4 = Q7_2_prime
b_5 = Qm_1
b_6 = QM_1

a_1 = Activations(
    TimeFrequency(TimePoint(1, 1, 0, time_signature=(3, 8)), FrequencyPoint(74)),
    TimeFrequency(TimePoint(2, 1, 0, time_signature=(3, 8)), FrequencyPoint(74)),
    TimeFrequency(TimePoint(3, 1, 0, time_signature=(3, 8)), FrequencyPoint(74)),
)

a_2 = Activations(
    TimeFrequency(TimePoint(4, 1, 0, time_signature=(3, 8)), FrequencyPoint(74)),
)

a_3 = Activations(
    TimeFrequency(TimePoint(5, 1, 0, time_signature=(3, 8)), FrequencyPoint(74)),
    TimeFrequency(TimePoint(6, 1, 0, time_signature=(3, 8)), FrequencyPoint(74)),
    TimeFrequency(TimePoint(7, 1, 0, time_signature=(3, 8)), FrequencyPoint(74)),
)

a_4 = Activations(
    TimeFrequency(TimePoint(8, 1, 0, time_signature=(3, 8)), FrequencyPoint(74)),
)

a_5 = Activations(
    TimeFrequency(TimePoint(1, 1, 0, time_signature=(3, 8)), FrequencyPoint(50)),
    TimeFrequency(TimePoint(2, 1, 0, time_signature=(3, 8)), FrequencyPoint(50)),
    TimeFrequency(TimePoint(3, 1, 0, time_signature=(3, 8)), FrequencyPoint(50)),
    TimeFrequency(TimePoint(8, 1, 0, time_signature=(3, 8)), FrequencyPoint(50)),
)

a_6 = Activations(
    TimeFrequency(TimePoint(4, 1, 0, time_signature=(3, 8)), FrequencyPoint(50)),
    TimeFrequency(TimePoint(5, 1, 0, time_signature=(3, 8)), FrequencyPoint(50)),
    TimeFrequency(TimePoint(6, 1, 0, time_signature=(3, 8)), FrequencyPoint(50)),
    TimeFrequency(TimePoint(7, 1, 0, time_signature=(3, 8)), FrequencyPoint(50)),
)

p = (a_1 + b_1) + (a_2 + b_2) + (a_3 + b_3) + (a_4 + b_4) + (a_5 + b_5) + (a_6 + b_6)
p.time_signature = TimeSignature(3, 8)

midi_file = create_midi(p, tempo=120)

plot_piano_roll(p, x_tick_start=TimePoint(-3, 8), x_tick_step=TimeShift(3, 8),
                time_label='Time (m, b)', fig_size=(640, 400))

folder = Path(__file__).parent.parent.parent / Path('phd') / Path('chapter_4')
folder.mkdir(parents=True, exist_ok=True)
midi_path = folder / Path('dilation_harmonic_textures_default.mid')
fig_path = folder / Path('dilation_harmonic_textures.pdf')

plt.savefig(fig_path)
midi_file.save(midi_path)

plt.show()
