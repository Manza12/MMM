from matplotlib.pyplot import show
from mmm.pianorolls.generation import Hit, Rhythm, Texture, Chord
from mmm.pianorolls.plot import plot_piano_roll

t_1 = Texture(
    Rhythm(Hit('0/16', '1/16')),
    Rhythm(Hit('1/16', '5/16')),
    Rhythm(Hit('2/16', '1/16')),
    Rhythm(Hit('3/16', '1/16')),
)

d_min = Chord(50, 57, 62, 65, nature='point')

d_min_1 = t_1 * d_min

plot_piano_roll(d_min_1)

show()
