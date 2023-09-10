from pathlib import Path

import matplotlib.pyplot as plt

from mmm.pianorolls.music import TimePoint, TimeShift
from mmm.pianorolls.score import ScoreWhole
from mmm.pianorolls.plot import plot_piano_roll

name = 'nocturne_c_minor'

# Paths
project_folder = Path('..')

data_folder = project_folder / Path('data')

musicxml_folder = data_folder / Path('musicxml')

score_whole = ScoreWhole(musicxml_folder / (name + '.musicxml'))

piano_roll = score_whole.to_piano_roll()

excerpt = piano_roll[TimePoint(1, 1, 0): TimePoint(9, 1, 0), :]
excerpt.change_tatum(TimeShift(1, 2), inplace=True)

chroma_roll = excerpt.to_chroma_roll()
chroma_roll_binary = chroma_roll.change_type(bool)

plot_piano_roll(chroma_roll, v_max=1)
plt.show()
