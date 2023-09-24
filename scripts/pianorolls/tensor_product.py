import os
from pathlib import Path
from mmm.pianorolls.music import Hit, Rhythm, Chord, TimeShift, TimePoint, HarmonicTexture, Texture, Harmony
from mmm.pianorolls.plot import plot_piano_roll
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "CMU Sans Serif"

# Path
figures_path = Path('.') / Path('phd') / Path('figures')
name = str(os.path.basename(__file__))[:-3] + '.eps'
file_path = figures_path / name

# Piano roll
texture = Texture(
    Rhythm(
        Hit(TimePoint('0/8'), TimeShift('1/8')),
        Hit(TimePoint('1/8'), TimeShift('1/8')),
        Hit(TimePoint('2/8'), TimeShift('1/8')),
        Hit(TimePoint('3/8'), TimeShift('1/8')),
        Hit(TimePoint('4/8'), TimeShift('1/8')),
        Hit(TimePoint('5/8'), TimeShift('1/8')),
        Hit(TimePoint('6/8'), TimeShift('1/8')),
        Hit(TimePoint('7/8'), TimeShift('1/8')),
    )
)
harmony = Harmony(Chord(57, 60, 64, nature='point'))
harmonic_texture = HarmonicTexture(texture, harmony)
harmonic_texture.change_tatum(TimeShift('1/16'), inplace=True)

# Plot score
# time_vector = [(1, 1, 0), None, None, None, (1, 3, 0), None, None, None, (2, 1, 0)]
# freq_vector = midi_numbers_to_pitches([57, None, None, 60, None, None, None, 64])

fig = plot_piano_roll(harmonic_texture, fig_size=(400, 300), x_tick_step=TimeShift())
# time_vector=time_vector, freq_vector=freq_vector,
#                       colorbar=True, colorbar_ticks=[0, 1, 2], colorbar_labels=[0, 1, 2]

# plt.xticks([0, 2, 4, 6, 8])
# plt.yticks([0, 1, 2, 3, 4, 5, 6, 7])

# plt.xlim([-2, 9])
# plt.ylim([-2, 9])
# plt.tight_layout()

# plt.savefig(file_path)
plt.show()
