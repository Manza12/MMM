import unittest
from fractions import Fraction as frac


class TestTime(unittest.TestCase):
    def test_time(self):
        from mmm.pianorolls.music import Time, TimeShift, TimePoint, TimeSignature

        # Time
        try:
            Time(frac(1, 2))
            raise Exception('Time should not be instantiable')
        except TypeError:
            pass

        # TimeShift
        TimeShift(frac(1, 2))
        TimeShift(1)
        TimeShift('1/2')
        TimeShift(1, 2)

        # TimeSignature
        ts = TimeSignature(6, 8)
        TimeSignature(ts)

        # TimePoint
        time_signatures = [(6, 8), ts]
        values = [frac(1, 2), 1, '1/2']
        for time_signature in time_signatures:
            for value in values:
                TimePoint(value)
                TimePoint(value, time_signature=time_signature)
            TimePoint(1, 2)
            TimePoint(1, 2, time_signature=time_signature)

        offsets = [frac(1, 2), 0, '1/2']
        for offset in offsets:
            for time_signature in time_signatures:
                TimePoint(1, 1, offset)
                TimePoint(1, 1, offset, time_signature=time_signature)


class TestFrequency(unittest.TestCase):
    def test_frequency(self):
        from mmm.pianorolls.music import Frequency, FrequencyShift, FrequencyPoint

        # Frequency
        try:
            Frequency(1)
            raise Exception('Frequency should not be instantiable')
        except TypeError:
            pass

        # FrequencyShift
        FrequencyShift(1)

        # FrequencyPoint
        FrequencyPoint(1)


class TestTimeFrequency(unittest.TestCase):
    def test_time_frequency(self):
        from mmm.pianorolls.music import TimeShift, FrequencyShift, TimeFrequency, TimePoint, FrequencyPoint

        times = [TimeShift(1), TimePoint(1)]
        frequencies = [FrequencyShift(1), FrequencyPoint(60)]

        for time in times:
            for frequency in frequencies:
                TimeFrequency(time, frequency)

        times = [frac(0), 0, '0/1']
        natures = ['shift', 'point']

        for time in times:
            for time_nature in natures:
                for frequency_nature in natures:
                    TimeFrequency(time, 0, time_nature, frequency_nature)


class TestHarmonicTexture(unittest.TestCase):
    def test_texture(self):
        from mmm.pianorolls.music import Hit, Rhythm, Texture, WrongNature

        h_1 = Hit('0/8', '1/8')
        h_2 = Hit('2/8', '1/8', 'shift')
        h_3 = Hit('0/8', '1/8', 'point')

        try:
            Rhythm(h_1, h_2, h_3)
            raise Exception('Cannot mix hits of different natures')
        except WrongNature:
            pass
        r_1 = Rhythm(h_1, h_2)
        h_4 = Hit('0/4', '1/4', 'shift')
        r_2 = Rhythm(h_1, h_4)

        Texture(r_1, r_2)

    def test_harmony(self):
        from mmm.pianorolls.music import Chord, Harmony, WrongNature

        c_1 = Chord(0, 4, 7)
        c_2 = Chord(0, 4, 7, nature='shift')
        c_3 = Chord(60, 64, 67, nature='point')

        try:
            Harmony(c_1, c_2, c_3)
            raise Exception('Cannot mix chords of different natures')
        except WrongNature:
            pass
        Harmony(c_1, c_2)

    def test_harmonic_texture(self):
        from mmm.pianorolls.music import Chord, Harmony, Hit, Rhythm, Texture

        h_1 = Hit('0/8', '1/8')
        h_2 = Hit('2/8', '1/8', 'shift')
        h_4 = Hit('0/4', '1/4', 'shift')
        r_1 = Rhythm(h_1, h_2)
        r_2 = Rhythm(h_1, h_4)

        t_1 = Texture(r_1, r_2)

        c_1 = Chord(4, 7)
        c_2 = Chord(2, 5, 7)

        h_1 = Harmony(c_1, c_2)

        t_1 * h_1
        t_1 * c_1
