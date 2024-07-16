from mmm import *
from mmm.pianorolls.music import TimeShift
from mmm.pianorolls.plot import plot_piano_roll
from mmm.pianorolls.midi import read_midi

# Parameters
name = 'nocturne_c_minor-start'

# Paths
project_folder = Path('..') / Path('..')

data_folder = project_folder / Path('data')

midi_folder = data_folder / Path('midi')

output_folder = Path('.')
output_folder.mkdir(parents=True, exist_ok=True)

# Read MIDI file
piano_roll = read_midi(midi_folder / (name + '.mid'))
piano_roll.change_tatum(TimeShift(1, 16), inplace=True)
# piano_roll.array = piano_roll.array[:, 24:]
# piano_roll.time_signature = TimeSignature(3, 4)

# Plot piano roll
plot_piano_roll(piano_roll, fig_size=(8. * 100, 4.5 * 100),
                x_tick_step=TimeShift(4, 4), time_label='Time (m, b)')
# plt.xlim([-1, float(16 * piano_roll.time_signature.duration / TimeShift(1, 8))])

# Set colors
plt.gcf().patch.set_facecolor('white')
plt.gcf().patch.set_alpha(0.)

plt.gca().patch.set_facecolor('white')

plt.savefig(output_folder / (name + '_pianoroll.svg'), transparent=True)
plt.savefig(output_folder / (name + '_pianoroll.png'), transparent=True)

plt.show()
