from pathlib import Path
from time import time
import numpy as np
import matplotlib.pyplot as plt
from mmm.pianorolls.midi import create_midi
from mmm.pianorolls.score import ScoreWhole, TimeSignature
from mmm.pianorolls.music import EntangledTexture as ETexture, EntangledRhythm as ERhythm, EntangledHit as EHit, \
    ActivationsStack, TimeFrequency, Activations, Texture, Rhythm, Hit, PianoRoll
from mmm.pianorolls.plot import plot_piano_roll, plot_activations_stack
from mmm.pianorolls.morphology import erosion, dilation

# Parameters
plot = True

# Paths
root_path = Path('..') / Path('..')
data_path = root_path / Path('data')
musicxml_path = data_path / Path('musicxml')
score_path = musicxml_path / 'swan.musicxml'

# Score
score = ScoreWhole(score_path)

# Merge tied notes
score.merge_tied_notes()

# PianoRoll
piano_roll = score.to_piano_roll(entagle=True)
piano_roll.time_signature = TimeSignature(6, 4)

# Analysis
texture_1 = ETexture(
    ERhythm(EHit('0', '1/8', nature='shift'), EHit('4/8', '1/8')),
    ERhythm(EHit('1/8', '1/8'), EHit('3/8', '1/8'), EHit('5/8', '1/8')),
    ERhythm(EHit('2/8', '1/8')),
)

texture_2 = ETexture(
    ERhythm(EHit('0', '1/16')),
    ERhythm(EHit('1/16', '1/16')),
    ERhythm(EHit('3/16', '1/16')),
    ERhythm(EHit('2/16', '1/16')),
)

texture_1_prime = Texture(
    Rhythm(Hit('0', '3/4')),
    Rhythm(Hit('0', '3/4')),
    Rhythm(Hit('0', '3/4')),
)

texture_2_prime = Texture(
    Rhythm(Hit('0', '1/4')),
    Rhythm(Hit('0', '1/4')),
    Rhythm(Hit('0', '1/4')),
    Rhythm(Hit('0', '1/4')),
)

print("Performing erosion...")
start = time()
activations_1 = erosion(piano_roll, texture_1)
activations_2 = erosion(piano_roll, texture_2)
print(f"Erosion performed. Time elapsed: {time() - start:.3f} s")


def filter_activations(activations):
    # Filter one rhythm absent
    a = np.all(np.any(activations.array, axis=-2, keepdims=True), axis=-3, keepdims=True)
    act = activations.array * a

    # Filter by order of elements
    for t in range(activations.array.shape[-1]):
        # if not a[0, 0, t]:
        #     pass
        ii, ff = np.where(act[:, :, t])
        increasing_idx = all(x <= y for x, y in zip(ii, ii[1:]))
        assert increasing_idx
        increasing = all(x < y for x, y in zip(ff, ff[1:]))
        if not increasing:
            act[:, :, t] = False

    # Create activations list
    activations_lists = []
    for idx in range(activations.array.shape[-3]):
        values_f, values_t = np.where(act[idx, :, :])
        activations_list = []
        for f, t in zip(values_f, values_t):
            t_val = t * piano_roll.tatum + piano_roll.origin.time
            f_val = f * piano_roll.step + piano_roll.origin.frequency
            activations_list.append(TimeFrequency(t_val, f_val))
        activations = Activations(*activations_list)
        activations_lists.append(activations)

    return ActivationsStack(*activations_lists)

print("Filter activations...")
start = time()
filtered_activations_1 = filter_activations(activations_1)
filtered_activations_2 = filter_activations(activations_2)
print(f"Filter activations performed. Time elapsed: {time() - start:.3f} s")

# Build a filtered piano roll
filtered_piano_roll_1: PianoRoll = dilation(filtered_activations_1, texture_1_prime)
# filtered_piano_roll_2: PianoRoll = dilation(filtered_activations_2, texture_2_prime)
filtered_piano_roll = filtered_piano_roll_1  # filtered_piano_roll_1.supremum(filtered_piano_roll_2)

# Save
file_path_filtered_swan = data_path / Path('midi') / Path('filtered_swan.mid')
filtered_piano_roll_midi = create_midi(filtered_piano_roll, tempo=82)
filtered_piano_roll_midi.save(file_path_filtered_swan)

# Plot
if plot:
    plot_piano_roll(piano_roll, v_max=0.99, fig_title='Piano Roll')
    plot_activations_stack(activations_1, fig_title='Activations 1')
    plot_activations_stack(activations_2, fig_title='Activations 2')
    plot_activations_stack(filtered_activations_1, fig_title='Filtered Activations 1')
    plot_activations_stack(filtered_activations_2, fig_title='Filtered Activations 2')
    plot_piano_roll(filtered_piano_roll, v_max=0.99, fig_title='Filtered Piano Roll')
    plt.show()
