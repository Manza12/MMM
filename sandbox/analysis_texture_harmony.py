import time
import logging

from mmm.pianorolls.music import *
from mmm.pianorolls.midi import create_midi
from mmm.pianorolls.morphology import erosion, dilation
from mmm.pianorolls.plot import plot_piano_roll, plot_activations_graph, plot_activations_stack

# Parameters
full = True
sync = True
sparse = True

load = False
log = True
# TimePoint.__str__ = lambda self: '(%s, %s)' % (self.measure, self.beat, self.offset)

# Path
piece = 'moonlight_3rd' + ('_53-56' if full else '_54') + ('_sync' if sync else '') + ('_sparse' if sparse else '')
folder = Path('..') / Path('..') / Path('phd') / Path('chapter_5') / Path('minimal_activations') / Path(piece)
folder.mkdir(parents=True, exist_ok=True)

# Log
if log:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(folder / 'log.txt'),
            logging.StreamHandler()
        ]
    )

# Textures
texture = Texture(
    Rhythm(
        Hit('0/8', '1/8'),
    ),
    Rhythm(
        Hit('1/8', '1/8'),
        Hit('2/8', '1/8'),
    ),
    Rhythm(
        Hit('3/8', '1/8'),
    ),
)

texture_homogeneous = Texture(
    Rhythm(
        Hit('0', '1/2'),
    ),
    Rhythm(
        Hit('0', '1/2'),
    ),
    Rhythm(
        Hit('0', '1/2'),
    ),
)

# Harmonies
i = Harmony(
    Chord(-12, 0, 12+3, 24, 24+3),
    Chord(3, 7, 24, 24+3),
    Chord(0, 3, 24+3, 24+7),
)
iv = Harmony(
    Chord(-7),
    Chord(5, 8, 24, 24+5),
    Chord(0, 5, 24+5, 24+8),
)
i46 = Harmony(
    Chord(-5),
    Chord(3, 7, 24, 24+3),
    Chord(0, 3, 24+3, 24+7),
)
V24 = Harmony(
    Chord(-7),
    Chord(2, 7, 24-1, 24+2),
    Chord(-1, 2, 24+2, 24+7),
)
i6 = Harmony(
    Chord(-9),
    Chord(7, 12, 12+7, 24+3),
    Chord(0, 3, 24+3, 24+7),
)
Np = Harmony(
    Chord(-7),
    Chord(8, 13, 12+5, 24+1),
    Chord(5, 8, 12+8, 24+5),
)
i46_2 = Harmony(
    Chord(-5),
    Chord(7, 12, 12+3, 24),
    Chord(3, 7, 12+7, 24+3),
)
V = Harmony(
    Chord(-5),
    Chord(5, 11, 12+2, 24-1),
    Chord(-1, 5, 12+5, 24+2),
)

harmonies = [i, iv, i46, V24, i6, Np, i46_2, V]

# Harmonic textures
if full:
    harmonic_textures = PianoRollStack(
        texture * i,
        texture * iv,
        texture * i46,
        texture * V24,
        texture * i6,
        texture * Np,
        texture * i46_2,
        texture * V,
    )
else:
    harmonic_textures = PianoRollStack(
        texture * i46,
        texture * V24,
    )

# Activations
if full:
    start = TimePoint(53, 1, 0)
    Gs3 = FrequencyPoint(56)
    activations_harmonic_textures = ActivationsStack(
        Activations(TimeFrequency(start, Gs3)),
        Activations(TimeFrequency(start + TimeShift(1, 2), Gs3)),
        Activations(TimeFrequency(start + TimeShift(2, 2), Gs3)),
        Activations(TimeFrequency(start + TimeShift(3, 2), Gs3)),
        Activations(TimeFrequency(start + TimeShift(4, 2), Gs3)),
        Activations(TimeFrequency(start + TimeShift(5, 2), Gs3)),
        Activations(TimeFrequency(start + TimeShift(6, 2), Gs3)),
        Activations(TimeFrequency(start + TimeShift(7, 2), Gs3)),
    )
else:
    start = TimePoint(54, 1, 0)
    Gs3 = FrequencyPoint(56)
    activations_harmonic_textures = ActivationsStack(
        Activations(TimeFrequency(start, Gs3)),
        Activations(TimeFrequency(start + TimeShift(1, 2), Gs3)),
    )

# Piano roll
piano_roll = dilation(activations_harmonic_textures, harmonic_textures)

midi_file = create_midi(piano_roll, tempo=120)
midi_path = folder / Path(piece + '.mid')
midi_file.save(midi_path)

# Erosion texture
activations_texture: ActivationsStack = erosion(piano_roll, texture)
activations_texture.change_extension(piano_roll.extension)

# Contract
activations_texture_contracted = activations_texture.contract()
harmonies_contracted = Harmony(*[harmony.contract() for harmony in harmonies])

# Erosion harmony
activations_harmony: ActivationsStack = erosion(activations_texture_contracted, harmonies_contracted)
activations_harmony.change_tatum(piano_roll.tatum, inplace=True)
activations_harmony.change_extension(piano_roll.extension)

# Plots
plot_piano_roll(activations_texture_contracted)
plot_activations_stack(activations_texture)
plot_activations_stack(activations_harmony, time_label='Time (m, b, o)')

plt.show()
