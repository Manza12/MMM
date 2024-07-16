from mmm.pianorolls.score_tree import *
from mmm.pianorolls.midi import create_midi
from mmm.pianorolls.plot import plot_piano_roll
from time import time


# Path
name = 'tempest-3rd'
root_folder = Path('..') / Path('..')
data_folder = root_folder / Path('data')
output_folder = root_folder / Path('scripts') / Path('lille')
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
# piano_roll.change_tatum(TimeShift(1, 16), inplace=True)
piano_roll.time_signature = TimeSignature(3, 8)
piano_roll.origin.time.time_signature = TimeSignature(3, 8)

# Create MIDI
start = time()
score_midi = create_midi(piano_roll, tempo=120, time_end=1)  # 49: 'String Ensemble 1'
score_midi.save(output_folder / (name + '.mid'))
print("Time to create and save MIDI: %.3f s" % (time() - start))

# Plot score
plot_piano_roll(piano_roll, v_max=2, x_tick_step=TimeShift(3, 8),
                time_label='Time (m, b)', fig_size=(1250, 250))
plt.savefig(output_folder / (name + '.svg'), transparent=True)
plt.show()
