from mmm.pianorolls.music import *
from mmm.pianorolls.midi import read_midi
from mmm.pianorolls.morphology import erosion
from mmm.pianorolls.plot import plot_piano_roll

# Parameters
full = True
sync = True
sparse = True

load = False
log = True
# TimePoint.__str__ = lambda self: '(%s, %s)' % (self.measure, self.beat)

# Path
project_folder = Path('..') / Path('..')
folder = project_folder / Path('phd') / Path('defence')
piece = 'anastasia'

# Textures
texture = Texture(
    Rhythm(
        Hit('0/8', '1/8'),
    ),
    Rhythm(
        Hit('1/8', '1/8'),
    ),
    Rhythm(
        Hit('2/8', '1/8'),
    ),
)

# Piano roll
piano_roll = read_midi(folder / Path(piece + '.mid'), time_signature=TimeSignature(6, 8))

# Harmonic texture
harmonic_texture = HarmonicTexture(
    texture,
    Harmony(Chord(0), Chord(3), Chord(7))
)

# Erosion harmonic texture
activations_harmonic_texture = erosion(piano_roll, harmonic_texture)
activations_harmonic_texture.change_extension(piano_roll.extension)

# Plot
plot_piano_roll(activations_harmonic_texture)

plt.show()
