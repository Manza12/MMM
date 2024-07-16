from time import time
import matplotlib.pyplot as plt
import numpy as np
from mmm.pianorolls.score_tree import *
from mmm.pianorolls.plot import plot_piano_roll


# Path
name = 'sonata_16_4'
root_folder = Path('..')
data_folder = root_folder / Path('data')
output_folder = Path('figures')
output_folder.mkdir(parents=True, exist_ok=True)
xml_folder = data_folder / Path('scorexml')
xml_file_name = name + '.xml'
xml_file_path = xml_folder / xml_file_name

# Read XML
start = time()
score = ScoreTree(xml_file_path)
print("Time to create score: %.3f s" % (time() - start))

# Compile into piano roll
start = time()
piano_roll = score.to_piano_roll()
print("Time to compile into piano roll: %.3f s" % (time() - start))

dynamics_array = np.copy(piano_roll.array)
dynamics_array[dynamics_array > 0] = 1

piano_roll.array = np.stack((piano_roll.array, dynamics_array))
piano_roll.dynamics = ['$\\bot$', 'p', 'f']

plot_piano_roll(piano_roll,
                x_tick_step=TimeShift(1, 1),
                time_label='Time (wholes)',
                cb_discrete=True,
                colorbar_labels=['$\\bot$', 'p', 'f'],
                colorbar_ticks=[0.5, 1.5, 2.5],
                marker_size=100,
                v_max=3,
                v_min=0,
                )
plt.show()
