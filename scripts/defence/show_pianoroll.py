from mmm import *
from mmm.pianorolls.music import TimeShift
from mmm.pianorolls.plot import plot_piano_roll
from mmm.pianorolls.midi import read_midi

# Parameters
phd = True
name = 'anastasia'

# Paths
project_folder = Path('..') / Path('..')

data_folder = project_folder / Path('data')

midi_folder = data_folder / Path('midi')

output_folder = Path('.')
output_folder.mkdir(parents=True, exist_ok=True)

# Read MIDI file
piano_roll = read_midi(midi_folder / (name + '.mid'))
piano_roll.change_tatum(TimeShift(1, 8), inplace=True)

# Plot piano roll
plot_piano_roll(piano_roll, fig_size=(8. * 100, 4. * 100))
plt.savefig(output_folder / (name + '_pianoroll.jpeg'))

plt.show()
