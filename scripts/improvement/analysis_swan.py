from pathlib import Path
from time import time
import matplotlib.pyplot as plt

from mmm.pianorolls.score import ScoreWhole, TimeSignature
from mmm.pianorolls.music import EntangledTexture as ETexture, EntangledRhythm as ERhythm, EntangledHit as EHit
from mmm.pianorolls.plot import plot_piano_roll, plot_activations_stack
from mmm.pianorolls.morphology import erosion

# Parameters
plot = True

# Paths
root_path = Path('..') / Path('..')
data_path = root_path / Path('data')
musicxml_path = data_path / Path('musicxml')
score_path = musicxml_path / 'swan.musicxml'

# Score
score = ScoreWhole(score_path)

# PianoRoll
piano_roll = score.to_piano_roll(entagle=True)
piano_roll.time_signature = TimeSignature(6, 4)

# Analysis
texture_1 = ETexture(
    ERhythm(EHit('0', '1/8', nature='shift'), EHit('4/8', '1/8')),
    ERhythm(EHit('1/8', '1/8'), EHit('3/8', '1/8'), EHit('5/8', '1/8')),
    ERhythm(EHit('2/8', '1/8')),
)

print("Performing erosion...")
start = time()
activations_1 = erosion(piano_roll, texture_1)
print(f"Erosion performed. Time elapsed: {time() - start:.3f} s")

# Plot
if plot:
    plot_piano_roll(piano_roll, v_max=0.99)
    plot_activations_stack(activations_1)
    plt.show()
