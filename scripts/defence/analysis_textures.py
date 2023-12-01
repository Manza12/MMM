from mmm.pianorolls.music import *
from mmm.pianorolls.midi import create_midi
from mmm.pianorolls.morphology import erosion, dilation
from mmm.pianorolls.plot import plot_piano_roll
from mmm.pianorolls.music import FrequencyPoint


# Parameters
mpl.rcParams['figure.max_open_warning'] = 25
mpl.rcParams['mathtext.fontset'] = 'dejavusans'
c_attack = {'attack': 1, 'sustain': 0}
c_sustain = {'attack': 0, 'sustain': 1}

# Path
folder = Path('..') / Path('..') / Path('phd') / Path('defence')
folder.mkdir(parents=True, exist_ok=True)

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
    Chord(3, 7, 24, 24+7),
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
    Chord(2, 5, 12+5, 24+2),
)

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

harmonic_textures_collapsed = PianoRollStack(
    texture_homogeneous * i,
    texture_homogeneous * iv,
    texture_homogeneous * i46,
    texture_homogeneous * V24,
    texture_homogeneous * i6,
    texture_homogeneous * Np,
    texture_homogeneous * i46_2,
    texture_homogeneous * V,
)

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

# Piano roll
piano_roll: PianoRoll = dilation(activations_harmonic_textures, harmonic_textures)

midi_file = create_midi(piano_roll, tempo=120)
midi_path = folder / Path('moonlight_3rd.mid')
midi_file.save(midi_path)

# Erosion
activations_texture: ActivationsStack = erosion(piano_roll, texture)
activations_texture.change_extension(piano_roll.extension)

activations_texture_contracted = activations_texture.contract()
activations_texture_contracted.change_extension(piano_roll.extension)

activations_texture_synchronized = activations_texture.synchronize()
activations_texture_synchronized_contracted = activations_texture_synchronized.contract()
activations_texture_synchronized_contracted.change_extension(piano_roll.extension)

activations_texture_filtered_contracted = activations_texture_synchronized.contract()
activations_texture_filtered_contracted.array[:, 1::4] = 0
activations_texture_filtered_contracted.change_extension(piano_roll.extension)

# Collapsed
piano_roll_collapsed: PianoRoll = dilation(activations_harmonic_textures, harmonic_textures_collapsed)
piano_roll_collapsed.change_extension(piano_roll.extension)
piano_roll_collapsed.change_tatum(TimeShift(1, 16), inplace=True)

midi_file = create_midi(piano_roll_collapsed, tempo=120)
midi_path = folder / Path('moonlight_3rd_collapsed.mid')
midi_file.save(midi_path)

# Figures
# Piano roll
piano_roll.change_tatum(TimeShift(1, 16), inplace=True)
plot_piano_roll(piano_roll, time_label='Time (measure)',
                x_tick_start=TimePoint(0), x_tick_step=TimeShift('1'),
                fig_size=(1000, 500), tight_frame=False)

file_path_svg = folder / Path('piano_roll_texture.svg')
file_path_pdf = folder / Path('piano_roll_texture.pdf')
plt.savefig(file_path_pdf)
plt.savefig(file_path_svg)

# Activations raw
plot_piano_roll(activations_texture_contracted, time_label='Time (measure)',
                x_tick_start=TimePoint(0), x_tick_step=TimeShift('1'),
                fig_size=(1000, 500), tight_frame=False)
file_path = folder / Path('activations_texture_raw.svg')
plt.savefig(file_path)

# Activations raw
plot_piano_roll(activations_texture_synchronized_contracted, time_label='Time (measure)',
                x_tick_start=TimePoint(0), x_tick_step=TimeShift('1'),
                fig_size=(1000, 500), tight_frame=False)
file_path = folder / Path('activations_texture_synchronized.svg')
plt.savefig(file_path)

# Activations filtered
plot_piano_roll(activations_texture_filtered_contracted, time_label='Time (measure)',
                x_tick_start=TimePoint(0), x_tick_step=TimeShift('1'),
                fig_size=(1000, 500), tight_frame=False)
file_path = folder / Path('activations_texture_filtered.svg')
plt.savefig(file_path)

plt.show()
