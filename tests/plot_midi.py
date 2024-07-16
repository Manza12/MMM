from pathlib import Path
from mmm.pianorolls.midi import read_midi
from mmm.pianorolls.plot import plot_piano_roll
import matplotlib.pyplot as plt

project_root = Path('..')
file_path = project_root / Path('data') / Path('midi') / 'toccata_fuga.mid'
piano_roll = read_midi(file_path)
piano_roll.change_tatum()
print()
# plot_piano_roll(piano_roll)
# plt.show()
