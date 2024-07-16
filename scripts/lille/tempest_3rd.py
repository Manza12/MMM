import matplotlib.pyplot as plt

from mmm.pianorolls.music import Hit, Rhythm, Texture
from mmm.pianorolls.music import Chord, Harmony
from mmm.pianorolls.music import TimeFrequency, Activations
from mmm.pianorolls.score_tree import ScoreTree, ComponentTree
from mmm.pianorolls.midi import create_midi
from mmm.pianorolls.plot import plot_piano_roll


t1 = Texture(
    Rhythm(Hit('0', '1/16')),
    Rhythm(Hit('1/16', '5/16')),
)

t2 = Texture(
    Rhythm(Hit('0', '1/16')),
    Rhythm(Hit('1/16', '1/16')),
    Rhythm(Hit('2/16', '1/16')),
    Rhythm(Hit('3/16', '1/16')),
)

t3 = Texture(
    Rhythm(Hit('-3/16', '1/16')),
    Rhythm(Hit('-2/16', '1/16')),
    Rhythm(Hit('-1/16', '1/16')),
    Rhythm(Hit('0', '2/16')),
)

h1 = Harmony(Chord(-12), Chord(-7))
h2 = Harmony(Chord(-12), Chord(-7), Chord(0), Chord(3))
h3 = Harmony(Chord(7), Chord(15), Chord(14), Chord(12))

th1 = t1 * h1

b1 = ComponentTree(
    Activations(TimeFrequency(0, 0)),
    t1 * h1,
    t2 * h2,
    t3 * h3,
)

# b2 = ComponentTree(
#     (Activations(TimeFrequency(0, 0)), t1 * h1),
#     (Activations(TimeFrequency(0, 0)), t2 * h2),
#     (Activations(TimeFrequency(0, 0)), t3 * h3),
# )

# dp1 = ComponentTree((Activations(TimeFrequency(0, 0)), b1))

phrase_1 = ComponentTree(Activations(TimeFrequency(0, 0)), demi_phrase_1_1, demi_phrase_1_2)

theme_a = ComponentTree(Activations(TimeFrequency(0, 0)), phrase_1)

score = ScoreTree((Activations(TimeFrequency(0, 62, 'point', 'point')), theme_a))

# To Piano Roll
piano_roll = score.to_piano_roll()

# To MIDI
midi = create_midi(piano_roll)
midi.save('data/midi/tempest_3rd.mid')

# Plot
plot_piano_roll(dp1.to_piano_roll())
plt.show()
