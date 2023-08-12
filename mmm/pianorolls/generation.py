from __future__ import annotations
from . import *
from .music import *
from .utils import gcd, nature_of_sum, nature_of_list
from .dictionaries import roman_numeral_to_factors_dict


# Time
class Hit:
    def __init__(self, start: str, duration: str, nature: str = 'shift'):
        self.nature = nature

        if nature == 'shift':
            self.start = TimeShift(start)
        elif nature == 'point':
            self.start = TimePoint(start)

        self.duration = TimeShift(duration)

    @property
    def end(self):
        return self.start + self.duration

    def __str__(self):
        return '(%s, %s)' % (self.start, self.duration)


class Rhythm(PianoRoll):
    def __init__(self, *hits: Hit):
        self.hits: Optional[List[Hit]] = list(hits)

        nature = nature_of_list([h.nature for h in hits])

        # Tatum
        tatum = TimeShift(0, 1)
        for hit in hits:
            tatum = TimeShift(gcd(tatum, hit.start, hit.duration))

        # Array size
        if len(hits) > 0:
            extension = ()
            for h, hit in enumerate(hits):
                start_int = hit.start // tatum
                end_int = (hit.start + hit.duration) // tatum
                if h == 0:
                    extension = (start_int, end_int)
                else:
                    extension = (min(extension[0], start_int), max(extension[1], end_int))
            size = (1, extension[1] - extension[0])
            origin = - extension[0]
        else:
            size = (1, 0)
            origin = 0
            tatum = TimeShift(1, 1)

        # Create and fill array
        array = np.zeros(size, dtype=np.uint8)
        for hit in hits:
            start_int = hit.start // tatum
            end_int = (hit.start + hit.duration) // tatum
            array[:, start_int + origin: end_int + origin] = \
                np.maximum(array[:, start_int + origin: end_int + origin], 1)
            array[:, start_int + origin] = np.maximum(array[:, start_int + origin], 2)

        # Create object
        PianoRoll.__init__(self, array, (0, origin), tatum, time_nature=nature)

    @property
    def nature(self):
        return self.time_nature


class Texture(list):
    def __init__(self, *rhythms: Rhythm):
        self.nature = nature_of_list([r.nature for r in rhythms])
        super().__init__(rhythms)

    def __mul__(self, other):
        if isinstance(other, Harmony):
            return HarmonicTexture(self, other)
        elif isinstance(other, Chord):
            return ChordTexture(self, other)
        else:
            raise AssertionError('Product should be done between a Texture and a Harmony.')

    def __rmul__(self, other):
        assert isinstance(other, Harmony), 'Product should be done between a Texture and a Harmony.'
        return HarmonicTexture(self, other)

    @property
    def extension(self):
        if len(self) == 0:
            return None
        result: Extension = self[0].extension
        for r in self[1:]:
            result = result.union(r.extension)
        return result

    @property
    def tatum(self):
        if len(self) == 0:
            return None
        result = self[0].tatum
        for r in self[1:]:
            result = TimeShift(gcd(result, r.tatum))
        return result


# Frequency
class Chord(PianoRoll):
    def __init__(self, *frequencies: int, nature: str = 'shift'):
        self.frequencies = sorted(frequencies)

        # Creation of the PianoRoll
        if len(frequencies) == 0:
            PianoRoll.__init__(self, np.zeros((0, 1), dtype=np.uint8), (0, 0),
                               TimeShift(0, 1), FrequencyShift(1), 'shift', nature)
        else:
            min_freq = min(frequencies)
            ambitus = max(frequencies) - min_freq
            origin = -min_freq
            size = int(ambitus) + 1
            array = np.zeros((size, 1), dtype=np.uint8)
            for p in frequencies:
                array[p - min_freq] = 1

            PianoRoll.__init__(self, array, (origin, 0), TimeShift(0, 1), FrequencyShift(1), 'shift', nature)

    @classmethod
    def from_degree(cls, degree: str, factors: List[Dict[str, str]]):
        degree_dict = roman_numeral_to_factors_dict[degree]
        note_numbers = []
        for factor in factors:
            note_numbers.append(degree_dict[factor['value']] + 12 * int(factor.get('octave', 0)))
        return cls(*note_numbers, nature='shift')

    @property
    def nature(self):
        return self.frequency_nature

    def __len__(self):
        return len(self.frequencies)

    def __str__(self):
        result = '['
        for i, p in enumerate(self.frequencies):
            if i == 0:
                result += '%s' % p
            else:
                result += ', %s' % p
        result += ']'
        return result

    def supremum(self, chord: Chord):
        assert isinstance(chord, Chord), 'Supremum should be done between two Chords.'
        assert self.nature == chord.nature, 'Supremum should be done between two Chords of the same nature.'
        return Chord(*set(self.frequencies).union(chord.frequencies), self.nature)


class Harmony(List):
    def __init__(self, *chords: Chord):
        self.nature = nature_of_list([c.nature for c in chords])
        super().__init__(chords)

    def __mul__(self, other):
        assert isinstance(other, Texture), 'Product should be done between a Texture and a Harmony.'
        return HarmonicTexture(other, self)

    def __rmul__(self, other):
        assert isinstance(other, Texture), 'Product should be done between a Texture and a Harmony.'
        return HarmonicTexture(other, self)

    @property
    def extension(self):
        if len(self) == 0:
            return None
        result: Extension = self[0].extension
        for c in self[1:]:
            result = result.union(c.extension)
        return result


# Time-Frequency
class ActivationTable(PianoRoll, list):
    def __init__(self, activations: List[TimeFrequency]):
        list.__init__(self, activations)
        frequency_nature = nature_of_list([a.frequency.nature for a in activations])
        time_nature = nature_of_list([a.time.nature for a in activations])

        # Time
        value = gcd(*[a.time for a in activations])
        tatum = TimeShift(value) if value != 0 else TimeShift('1')
        earlier_activation = min([a.time for a in activations])
        earlier_index = earlier_activation // tatum
        later_activation = max([a.time for a in activations])
        later_index = later_activation // tatum
        duration = later_index - earlier_index
        origin_time = -earlier_index

        # Frequency
        step = FrequencyShift(1)
        lower_frequency = min([a.frequency for a in activations])
        higher_frequency = max([a.frequency for a in activations])
        ambitus = higher_frequency - lower_frequency
        origin_frequency = -lower_frequency

        # Time-Frequency
        origin = (origin_frequency, origin_time)
        array = np.zeros((int(ambitus) + 1, duration + 1), dtype=bool)
        for a in activations:
            idx_t = a.time // tatum - earlier_index
            idx_f = a.frequency // step - lower_frequency
            array[idx_f, idx_t] = True

        # PianoRoll
        PianoRoll.__init__(self, array, origin, tatum, step, time_nature, frequency_nature)

    def change_tatum(self, new_tatum: TimeShift, inplace=False, null=True):
        if inplace:
            PianoRoll.change_tatum(self, new_tatum, inplace, True)
        else:
            return PianoRoll.change_tatum(self, new_tatum, inplace, True)

    def __add__(self, other):
        assert isinstance(other, PianoRoll)
        from .morphology import dilate_sparse
        return dilate_sparse(self, other)


class HarmonicTexture(PianoRoll):
    def __init__(self, texture: Texture, harmony: Harmony):
        assert isinstance(texture, Texture)
        assert isinstance(harmony, Harmony)
        assert len(texture) == len(harmony)
        self.texture: Texture = texture
        self.harmony: Harmony = harmony

        PianoRoll.__init__(self, time_nature=texture.nature, frequency_nature=harmony.nature)
        for rhythm, chord in zip(texture, harmony):
            rhythm: Rhythm
            chord: Chord
            tensor_product = PianoRoll(chord.array * rhythm.array,
                                       (chord.origin[0], rhythm.origin[1]),
                                       rhythm.tatum, chord.step,
                                       rhythm.nature, chord.nature)
            self.combine(tensor_product, inplace=True)

    def __len__(self):
        return len(self.texture)


class ChordTexture(HarmonicTexture):
    def __init__(self, texture: Texture, chord: Chord):
        self.chord = chord
        harmony = Harmony(*[Chord(c) for c in chord.frequencies])
        HarmonicTexture.__init__(self, texture, harmony)


class HarmonicTextureSequence(PianoRoll, list):
    def __init__(self,
                 activations_sequence: List[ActivationTable],
                 texture_sequence: List[Texture],
                 harmony_sequence: List[Harmony]):
        assert len(activations_sequence) == len(texture_sequence) == len(harmony_sequence)
        list.__init__(self, list(zip(activations_sequence, texture_sequence, harmony_sequence)))

        self.activations_sequence = activations_sequence
        self.texture_sequence = texture_sequence
        self.harmnoy_sequence = harmony_sequence

        PianoRoll.__init__(self)

        for activations, texture, harmony in zip(activations_sequence, texture_sequence, harmony_sequence):
            activations: ActivationTable
            harmonic_texture = HarmonicTexture(texture, harmony)
            d = activations + harmonic_texture
            self.combine(d, True)


class ChordTextureSequence(PianoRoll, list):
    def __init__(self,
                 activations_sequence: List[ActivationTable],
                 texture_sequence: List[Texture],
                 harmony: Harmony):
        assert len(activations_sequence) == len(texture_sequence) == len(harmony)
        list.__init__(self, list(zip(activations_sequence, texture_sequence, harmony)))

        self.activations_sequence = activations_sequence
        self.texture_sequence = texture_sequence
        self.harmony = harmony

        PianoRoll.__init__(self)

        for activations, texture, chord in zip(activations_sequence, texture_sequence, harmony):
            activations: ActivationTable
            chord_texture = ChordTexture(texture, chord)
            d = activations + chord_texture
            self.combine(d, True)


class Component(PianoRoll, list):
    def __init__(self, activation_tables: List[ActivationTable] = (), PianoRolls: List[PianoRoll] = (),
                 dynamics=None):
        list.__init__(self, list(zip(activation_tables, PianoRolls)))
        time_nature = nature_of_sum(nature_of_list([a.time_nature for a in activation_tables]),
                                    nature_of_list([b.time_nature for b in PianoRolls]))
        frequency_nature = nature_of_sum(nature_of_list([a.frequency_nature for a in activation_tables]),
                                         nature_of_list([b.frequency_nature for b in PianoRolls]))
        PianoRoll.__init__(self, time_nature=time_nature, frequency_nature=frequency_nature, dynamics=dynamics)

        for a, b in self:
            a: ActivationTable
            b: PianoRoll
            d = a + b
            self.combine(d, True)

    def append(self, pair: Tuple[ActivationTable, PianoRoll]) -> None:
        a, b = pair
        d = a + b
        self.combine(d, True)
        self.reduce(True)


class Score(Component):
    def __init__(self, activation_tables: List[ActivationTable] = (), PianoRolls: List[PianoRoll] = (),
                 dynamics=None, **metadata):
        Component.__init__(self, activation_tables, PianoRolls, dynamics=dynamics)
        self.metadata = metadata

        self.objects: Dict[str, ...] = {}
