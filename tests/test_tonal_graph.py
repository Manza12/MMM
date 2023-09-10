from time import time
from pathlib import Path

import matplotlib.pyplot as plt

from mmm.pianorolls.music import TimePoint, TimeShift, Harmony, RomanNumeral, ActivationsStack
from mmm.pianorolls.score import ScoreWhole
from mmm.pianorolls.plot import plot_piano_roll, plot_activations_stack
from mmm.pianorolls.morphology import erosion


name = 'nocturne_c_minor'

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

excerpt = piano_roll[TimePoint(1, 1, 0): TimePoint(9, 1, 0), :]
excerpt.change_tatum(TimeShift(1, 2), inplace=True)

chroma_roll = excerpt.to_chroma_roll()
chroma_roll_binary = chroma_roll.change_type(bool)

# Morphology
harmony = Harmony(
    RomanNumeral(0, 3, 7, label='i'),
    RomanNumeral(0, 3, 8, label='VI'),
)

start = time()
activations_stack: ActivationsStack = erosion(chroma_roll_binary, harmony)
activations_stack.change_extension(chroma_roll_binary.extension)
print('Time to erode: %.3f s' % (time() - start))

# Remove empty activations
for activations, chord in zip(activations_stack, harmony):
    if len(activations) == 0:
        activations.remove(activations)
        harmony.remove(chord)

# Plot
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
plt.show()
