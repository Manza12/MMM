from time import time
from pathlib import Path

import matplotlib.pyplot as plt

from mmm.pianorolls.graphs import TonalGraph
from mmm.pianorolls.music import TimePoint, TimeShift, Harmony, RomanNumeral, ActivationsStack, FrequencyPoint, \
    Texture, Rhythm, Hit
from mmm.pianorolls.score import ScoreWhole
from mmm.pianorolls.plot import plot_piano_roll, plot_activations_stack, plot_tonal_graph
from mmm.pianorolls.morphology import erosion


name = 'prelude_c_major'

# Paths
project_folder = Path('..')
data_folder = project_folder / Path('data')
musicxml_folder = data_folder / Path('musicxml')

# Piano roll
start = time()
score_whole = ScoreWhole(musicxml_folder / (name + '.musicxml'))
print('Time to parse score: %.3f' % (time() - start))

start = time()
piano_roll = score_whole.to_piano_roll()
print('Time to convert score to piano roll: %.3f' % (time() - start))

excerpt = piano_roll[TimePoint(1, 1, 0): TimePoint(12, 1, 0), :]
excerpt_collapsed = excerpt.change_tatum(TimeShift(1, 1))

chroma_roll = excerpt_collapsed.to_chroma_roll()
chroma_roll_binary = chroma_roll.change_type(bool)

# Morphology
harmony = Harmony(
    RomanNumeral(0, 4, 7, label='I'),
    RomanNumeral(2, 5, 9, label='ii'),
    RomanNumeral(4, 7, 11, label='iii'),
    RomanNumeral(5, 9, 0, label='IV'),
    RomanNumeral(7, 11, 2, label='V'),
    RomanNumeral(9, 0, 4, label='vi'),
    RomanNumeral(11, 2, 5, label='viiº'),
    RomanNumeral(0, 4, 7, 11, label='I7'),
    RomanNumeral(2, 5, 9, 0, label='ii7'),
    RomanNumeral(4, 7, 11, 2, label='iii7'),
    RomanNumeral(5, 9, 0, 4, label='IV7'),
    RomanNumeral(7, 11, 2, 5, label='V7'),
    RomanNumeral(9, 0, 4, 7, label='vi7'),
    RomanNumeral(11, 2, 5, 9, label='viiº7'),
)

texture = Texture(
    Rhythm(Hit('0/16', '1/2')),
    Rhythm(Hit('1/16', '7/16')),
    Rhythm(Hit('2/16', '1/16'), Hit('5/16', '1/16')),
    Rhythm(Hit('3/16', '1/16'), Hit('6/16', '1/16')),
    Rhythm(Hit('4/16', '1/16'), Hit('7/16', '1/16')),
)

h_texture = Texture(
    Rhythm(Hit('0/16', '1/16')),
    Rhythm(Hit('0/16', '1/16')),
    Rhythm(Hit('0/16', '1/16')),
    Rhythm(Hit('0/16', '1/16')),
    Rhythm(Hit('0/16', '1/16')),
)

texture_activations: ActivationsStack = erosion(excerpt, texture)
texture_activations_sync = texture_activations.synchronize()
collapsed_piano_roll = texture_activations_sync.contract()

start = time()
activations_stack: ActivationsStack = erosion(chroma_roll_binary, harmony)
activations_stack.change_tatum(chroma_roll_binary.tatum, inplace=True)
activations_stack.change_extension(chroma_roll_binary.extension)
print('Time to erode: %.3f s' % (time() - start))

# Remove empty activations
for activations, chord in zip(activations_stack, harmony):
    if len(activations) == 0:
        activations_stack.remove(activations)
        harmony.remove(chord)

# Tonal graph
tonal_graph = TonalGraph(activations_stack, harmony, activations_stack[0], complete=False)

# Plot
plot_piano_roll(piano_roll[TimePoint(1, 1, 0): TimePoint(5, 1, 0), FrequencyPoint(57):],
                x_tick_step=TimeShift(1, 4), time_label='Time (m, b)')
plot_piano_roll(chroma_roll, v_max=1)
plot_activations_stack(activations_stack,
                       time_label='Time (m, b)',
                       legend=True,
                       legend_params={
                           'columnspacing': 0.2,
                           'labelspacing': 0.,
                           'handletextpad': 0.1,
                           'labels': [rn.label for i, rn in enumerate(harmony) if len(activations_stack[i]) != 0],
                           'outside': True,
                       })
plot_tonal_graph(tonal_graph)
plot_piano_roll(piano_roll[TimePoint(1, 1, 0): TimePoint(5, 1, 0), FrequencyPoint(57):],
                x_tick_step=TimeShift(1, 2), time_label='Time (m, b)')
plot_piano_roll(collapsed_piano_roll[TimePoint(1, 1, 0): TimePoint(5, 1, 0), FrequencyPoint(57):],
                x_tick_step=TimeShift(1, 2), time_label='Time (m, b)')

plt.show()
