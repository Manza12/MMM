from mmm.pianorolls.score_tree import *
from mmm.pianorolls.midi import create_midi
from mmm.pianorolls.plot import plot_piano_roll
from time import time


# Path
name = 'sonata_16'
root_folder = Path('..') / Path('..')
data_folder = root_folder / Path('data')
output_folder = root_folder / Path('results') / Path('generation')
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

# Create MIDI
start = time()
score_midi = create_midi(piano_roll, tempo=120)
score_midi.save(output_folder / (name + '.mid'))
print("Time to create and save MIDI: %.3f s" % (time() - start))

# Plot score
plot_piano_roll(piano_roll, v_max=2)
plt.show()
