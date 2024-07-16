from __future__ import annotations

from . import *
from .dictionaries import roman_numeral_to_factors_dict
from .utils import midi_number_to_pitch, midi_number_to_chroma, gcd


class WrongNature(Exception):
    def __init__(self, msg: str = 'Wrong nature'):
        super().__init__(msg)


class Time:
    def __init__(self, value: frac):
        if type(self) == Time:
            raise TypeError('Time is an abstract class.')
        else:
            self.value = value

    @property
    def nature(self) -> str:
        raise NotImplementedError

    @property
    def numerator(self):
        return self.value.numerator

    @property
    def denominator(self):
        return self.value.denominator

    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
        return not self.__eq__(other)

    def __neg__(self) -> Time:
        raise NotImplementedError

    def __add__(self, other) -> Time:
        raise NotImplementedError

    def __sub__(self, other) -> TimeShift:
        raise NotImplementedError

    def __mul__(self, other):
        raise NotImplementedError

    def __rmul__(self, other):
        return self.__mul__(other)

    def __lt__(self, other):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __truediv__(self, other):
        raise NotImplementedError

    def __floordiv__(self, other):
        raise NotImplementedError

    @staticmethod
    def zero():
        raise NotImplementedError


class TimeShift(Time):
    @multimethod
    def __init__(self, value: Union[frac, int, str]):
        super().__init__(frac(value))

    @multimethod
    def __init__(self, numerator: int, denominator: int):
        super().__init__(frac(numerator, denominator))

    @property
    def nature(self):
        return 'shift'

    def __eq__(self, other):
        if isinstance(other, TimeShift):
            return self.value == other.value
        else:
            return False

    def __neg__(self):
        return TimeShift(-self.value)

    def __add__(self, other):
        assert isinstance(other, TimeShift) or isinstance(other, TimePoint)
        if isinstance(other, TimeShift):
            return TimeShift(self.value + other.value)
        else:
            return TimePoint(self.value + other.value)

    def __sub__(self, other):
        assert isinstance(other, TimeShift)
        return TimeShift(self.value - other.value)

    def __mul__(self, other):
        assert isinstance(other, int)
        return TimeShift(self.value * other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        assert isinstance(other, TimeShift) or isinstance(other, int)
        if isinstance(other, TimeShift):
            if other.value == 0:
                return 0
            return self.value / other.value
        else:
            return TimeShift(self.value / other)

    def __floordiv__(self, other):
        assert isinstance(other, TimeShift) or isinstance(other, int)
        if isinstance(other, TimeShift):
            if other.value == 0:
                return 0
            return self.value // other.value
        else:
            return TimeShift(self.value // other)

    def __lt__(self, other):
        assert isinstance(other, TimeShift), 'TimeShift is only comparable with TimeShift.'
        return self.value < other.value

    def __le__(self, other):
        assert isinstance(other, TimeShift), 'TimeShift is only comparable with TimeShift.'
        return self.value <= other.value

    def __gt__(self, other):
        assert isinstance(other, TimeShift), 'TimeShift is only comparable with TimeShift.'
        return self.value > other.value

    def __ge__(self, other):
        assert isinstance(other, TimeShift), 'TimeShift is only comparable with TimeShift.'
        return self.value >= other.value

    def __str__(self):
        return str(self.value)

    def __hash__(self):
        return hash((self.value, self.nature))

    @staticmethod
    def zero():
        return TimeShift(0)

    def gcd(self, *others):
        if len(others) == 0:
            return self
        if len(others) == 1:
            assert isinstance(others[0], Time)
            return TimeShift(gcd(self.value, others[0].value))

        result = self
        for other in others:
            assert isinstance(other, Time), 'GCD only accepts Time as arguments.'
            result = result.gcd(other)
        return result


class TimeSignature:
    @multimethod
    def __init__(self, numerator: int, denominator: int):
        self.numerator: int = numerator
        self.denominator: int = denominator
        self.duration: TimeShift = TimeShift(numerator, denominator)

    @multimethod
    def __init__(self, time_signature: TimeSignature):
        self.__init__(time_signature.numerator, time_signature.denominator)

    @multimethod
    def __init__(self, value: Tuple[int, int]):
        self.__init__(*value)

    def __str__(self):
        return str(self.numerator) + '/' + str(self.denominator)


class TimePoint(Time):
    @multimethod
    def __init__(self, value: Union[frac, int, str], time_signature: Union[Tuple[int, int], TimeSignature] = (4, 4)):
        super().__init__(frac(value))
        if isinstance(time_signature, TimeSignature):
            self.time_signature = time_signature
        else:
            self.time_signature = TimeSignature(*time_signature)

    @multimethod
    def __init__(self, numerator: int, denominator: int,
                 time_signature: Union[Tuple[int, int], TimeSignature] = (4, 4)):
        super().__init__(frac(numerator, denominator))
        if isinstance(time_signature, TimeSignature):
            self.time_signature = time_signature
        else:
            self.time_signature = TimeSignature(*time_signature)

    @multimethod
    def __init__(self, measure: int, beat: int, offset: Union[frac, str, int],
                 time_signature: Union[Tuple[int, int], TimeSignature] = (4, 4)):
        self.time_signature = TimeSignature(time_signature)
        measure_duration = self.time_signature.duration
        beat_duration = TimeShift(1, self.time_signature.denominator)
        offset = TimeShift(offset)
        time_shift = (measure - 1) * measure_duration + (beat - 1) * beat_duration + offset
        super().__init__(time_shift.value)

    @property
    def nature(self):
        return 'point'

    @property
    def measure(self):
        return self.value // self.time_signature.duration.value + 1

    @property
    def beat(self):
        remaining = self.value - (self.measure - 1) * self.time_signature.duration.value
        return remaining // TimeShift(frac(1, self.time_signature.denominator)).value + 1

    @property
    def offset(self):
        remaining = self - (self.measure - 1) * self.time_signature.duration
        return remaining - TimePoint(self.beat - 1, self.time_signature.denominator)

    def __eq__(self, other):
        if isinstance(other, TimePoint):
            return self.value == other.value
        else:
            return False

    def __neg__(self):
        raise ValueError('TimePoint cannot be negated.')

    def __add__(self, other: TimeShift):
        assert isinstance(other, TimeShift), 'TimePoint can only be added with TimeShift.'
        return TimePoint(self.value + other.value, time_signature=self.time_signature)

    def __sub__(self, other):
        assert isinstance(other, TimePoint) or isinstance(other, TimeShift), \
            "Substraction is made between TimePoint and TimePoint or TimePoint and TimeShift"
        if isinstance(other, TimePoint):
            return TimeShift(self.value - other.value)
        else:
            return TimePoint(self.value - other.value, time_signature=self.time_signature)

    def __mul__(self, other):
        raise ValueError('TimePoint cannot be multiplied.')

    def __truediv__(self, other):
        raise ValueError('TimePoint cannot be divided.')

    def __floordiv__(self, other):
        raise ValueError('TimePoint cannot be divided.')

    def __lt__(self, other):
        assert isinstance(other, TimePoint), 'TimePoint is only comparable with TimePoint.'
        return self.value < other.value

    def __le__(self, other):
        assert isinstance(other, TimePoint), 'TimePoint is only comparable with TimePoint.'
        return self.value <= other.value

    def __gt__(self, other):
        assert isinstance(other, TimePoint), 'TimePoint is only comparable with TimePoint.'
        return self.value > other.value

    def __ge__(self, other):
        assert isinstance(other, TimePoint), 'TimePoint is only comparable with TimePoint.'
        return self.value >= other.value

    def __str__(self):
        return '(%s, %s, %s)' % (self.measure, self.beat, self.offset)

    def __hash__(self):
        return hash(self.value)

    @staticmethod
    def zero(time_signature=(4, 4)):
        return TimePoint(0, time_signature=time_signature)


class TimeSeconds(TimePoint):
    def __init__(self, value: float):
        super().__init__(frac(value), time_signature=(1, 1))
        self.value = value

    def __str__(self):
        return str(self.value)

    def __add__(self, other: TimeShift):
        assert isinstance(other, TimeShift), 'TimeSeconds can only be added with TimeShift.'
        return TimeSeconds(float(self.value + other.value))

    def __sub__(self, other: Union[TimeSeconds, TimeShift]):
        assert isinstance(other, TimeSeconds) or isinstance(other, TimeShift), \
            "Substraction is made between TimeSeconds and TimeSeconds or TimeSeconds and TimeShift"
        if isinstance(other, TimeSeconds):
            return TimeShift(frac(self.value - other.value))
        else:
            return TimeSeconds(float(self.value - other.value))


class TimeExtension:
    def __init__(self, start: Time, end: Time):
        assert type(start) == type(end)
        assert start <= end
        self.start = start
        self.end = end

    @property
    def duration(self) -> TimeShift:
        result = self.end - self.start
        if isinstance(result, TimeShift):
            return result
        else:
            raise ValueError('Duration should be a TimeShift.')

    def union(self, other: TimeExtension):
        assert isinstance(other, TimeExtension)
        return TimeExtension(min(self.start, other.start), max(self.end, other.end))

    def __eq__(self, other):
        assert isinstance(other, TimeExtension)
        return self.duration == other.duration

    def __sub__(self, other: TimeExtension):
        assert isinstance(other, TimeExtension)
        return self.start - other.start, self.end - other.end

    def __str__(self):
        return '%s -> %s (%s)' % (self.start, self.end, self.duration.value)


class TimeVector:
    def __init__(self, origin: Time, tatum: TimeShift):
        assert isinstance(origin, Time)
        assert isinstance(tatum, TimeShift)
        self.origin = origin
        self.tatum = tatum

    def __getitem__(self, item):
        return self.origin + self.tatum * item


# Frequency
class Frequency:
    nature: Optional[str] = None

    def __init__(self, value):
        if type(self) == Frequency:
            raise TypeError('Time is an abstract class.')
        else:
            self.value = value

    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
        return not self.__eq__(other)

    def __neg__(self) -> Frequency:
        raise NotImplementedError

    def __add__(self, other) -> Frequency:
        raise NotImplementedError

    def __sub__(self, other) -> FrequencyShift:
        raise NotImplementedError

    def __mul__(self, other):
        raise NotImplementedError

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        raise NotImplementedError

    def __floordiv__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    @staticmethod
    def zero():
        raise NotImplementedError


class FrequencyShift(Frequency):
    def __init__(self, shift: int):
        super().__init__(shift)

    def __eq__(self, other):
        if isinstance(other, FrequencyShift):
            return self.value == other.value
        else:
            return False

    def __neg__(self):
        return FrequencyShift(-self.value)

    def __add__(self, other):
        assert isinstance(other, FrequencyShift) or isinstance(other, FrequencyPoint)
        if isinstance(other, FrequencyShift):
            return FrequencyShift(self.value + other.value)
        else:
            return FrequencyPoint(self.value + other.value)

    def __mul__(self, other):
        return FrequencyShift(self.value * other)

    def __rmul__(self, other):
        return FrequencyShift.__mul__(self, other)

    def __truediv__(self, other):
        assert isinstance(other, FrequencyShift) or isinstance(other, int)
        if isinstance(other, FrequencyShift):
            return self.value / other.value
        else:
            return FrequencyShift(self.value / other)

    def __floordiv__(self, other):
        assert isinstance(other, FrequencyShift) or isinstance(other, int)
        if isinstance(other, FrequencyShift):
            return self.value // other.value
        else:
            return FrequencyShift(self.value // other)

    def __sub__(self, other):
        assert isinstance(other, FrequencyShift)
        return FrequencyShift(self.value - other.value)

    def __lt__(self, other):
        assert isinstance(other, FrequencyShift), 'FrequencyShift is only comparable with FrequencyShift.'
        return self.value < other.value

    def __le__(self, other):
        assert isinstance(other, FrequencyShift), 'FrequencyShift is only comparable with FrequencyShift.'
        return self.value <= other.value

    def __gt__(self, other):
        assert isinstance(other, FrequencyShift), 'FrequencyShift is only comparable with FrequencyShift.'
        return self.value > other.value

    def __ge__(self, other):
        assert isinstance(other, FrequencyShift), 'FrequencyShift is only comparable with FrequencyShift.'
        return self.value >= other.value

    def __str__(self):
        return '%s' % self.value

    def __hash__(self):
        return hash((self.value, self.nature))

    @property
    def nature(self):
        return 'shift'

    @staticmethod
    def zero():
        return FrequencyShift(0)


class FrequencyPoint(Frequency):
    def __init__(self, midi_number: int):
        super().__init__(midi_number)

    def __eq__(self, other):
        if isinstance(other, FrequencyPoint):
            return self.value == other.value
        else:
            return False

    def __neg__(self):
        raise ValueError('FrequencyPoint cannot be negated.')

    def __add__(self, other: FrequencyShift):
        assert isinstance(other, FrequencyShift), 'FrequencyPoint can only be added with FrequencyShift.'
        return FrequencyPoint(self.value + other.value)

    def __sub__(self, other):
        assert isinstance(self, FrequencyPoint) or isinstance(self, FrequencyShift), \
            "Subtraction is made between FrequencyPoint and FrequencyPoint or FrequencyPoint and FrequencyShift"
        if isinstance(other, FrequencyPoint):
            return FrequencyShift(self.value - other.value)
        else:
            return FrequencyPoint(self.value - other.value)

    def __mul__(self, other):
        raise ValueError('FrequencyPoint cannot be multiplied.')

    def __truediv__(self, other):
        raise ValueError('FrequencyPoint cannot be truedivided.')

    def __floordiv__(self, other):
        raise ValueError('FrequencyPoint cannot be floordivided.')

    def __lt__(self, other):
        assert isinstance(other, FrequencyPoint), 'FrequencyPoint is only comparable with FrequencyPoint.'
        return self.value < other.value

    def __le__(self, other):
        assert isinstance(other, FrequencyPoint), 'FrequencyPoint is only comparable with FrequencyPoint.'
        return self.value <= other.value

    def __gt__(self, other):
        assert isinstance(other, FrequencyPoint), 'FrequencyPoint is only comparable with FrequencyPoint.'
        return self.value > other.value

    def __ge__(self, other):
        assert isinstance(other, FrequencyPoint), 'FrequencyPoint is only comparable with FrequencyPoint.'
        return self.value >= other.value

    def __str__(self):
        return midi_number_to_pitch(self.value)

    def __hash__(self):
        return hash(self.value)

    @property
    def nature(self):
        return 'point'

    @staticmethod
    def zero():
        return FrequencyPoint(0)


class ChromaShift(FrequencyShift):
    def __init__(self, shift: int):
        assert 0 <= shift < 12
        super().__init__(shift)

    def __add__(self, other):
        assert isinstance(other, ChromaShift) or isinstance(other, Chroma)
        if isinstance(other, ChromaShift):
            return ChromaShift((self.value + other.value) % 12)
        else:
            return Chroma((self.value + other.value) % 12)

    def __mul__(self, other):
        assert isinstance(other, int)
        return ChromaShift((self.value * other) % 12)

    def __rmul__(self, other):
        return ChromaShift.__mul__(self, other)


class Chroma(FrequencyPoint):
    def __init__(self, number: int):
        assert 0 <= number < 12
        super().__init__(number)

    def __add__(self, other: ChromaShift):
        assert isinstance(other, ChromaShift), 'Chroma can only be added with Shift.'
        return Chroma((self.value + other.value) % 12)

    def __str__(self):
        return midi_number_to_chroma(self.value)


class FrequencyExtension:
    def __init__(self, lower: Frequency, higher: Frequency):
        assert type(lower) == type(higher)
        assert lower <= higher
        self.lower = lower
        self.higher = higher

    @property
    def range(self) -> FrequencyShift:
        result = self.higher - self.lower
        if isinstance(result, FrequencyShift):
            return result
        else:
            raise ValueError('Range should be a FrequencyShift.')

    def union(self, other: FrequencyExtension):
        assert isinstance(other, FrequencyExtension)
        return FrequencyExtension(min(self.lower, other.lower), max(self.higher, other.higher))

    def __eq__(self, other):
        assert isinstance(other, FrequencyExtension)
        return self.range == other.range

    def __sub__(self, other: FrequencyExtension):
        assert isinstance(other, FrequencyExtension)
        return self.lower - other.lower, self.higher - other.higher

    def __str__(self):
        return '%s -> %s (%s)' % (self.lower, self.higher, self.range)


class FrequencyVector:
    def __init__(self, origin: Frequency, step: FrequencyShift):
        assert isinstance(origin, Frequency)
        assert isinstance(step, FrequencyShift)
        self.origin = origin
        self.step = step

    def __getitem__(self, item):
        return self.origin + self.step * item


# Time-Frequency
class TimeFrequency:
    @multimethod
    def __init__(self, time: Time, frequency: Frequency):
        self.time = time
        self.frequency = frequency

    @multimethod
    def __init__(self, time: Union[frac, str, int], frequency: int,
                 time_nature: str = 'shift', frequency_nature: str = 'shift'):
        if time_nature == 'point':
            self.time = TimePoint(time)
        elif time_nature == 'shift':
            self.time = TimeShift(time)
        else:
            raise ValueError('Time nature should be either point or shift.')
        if frequency_nature == 'point':
            self.frequency = FrequencyPoint(frequency)
        elif frequency_nature == 'shift':
            self.frequency = FrequencyShift(frequency)
        else:
            raise ValueError('Frequency nature should be either point or shift.')

    def __eq__(self, other):
        if isinstance(other, TimeFrequency):
            return self.time == other.time and self.frequency == other.frequency
        else:
            return False

    def __add__(self, other: TimeFrequency):
        assert isinstance(other, TimeFrequency)
        return TimeFrequency(self.time + other.time, self.frequency + other.frequency)

    def __sub__(self, other: TimeFrequency):
        assert isinstance(other, TimeFrequency)
        return TimeFrequency(self.time - other.time, self.frequency - other.frequency)

    def __str__(self):
        return '(%s, %s)' % (self.time, self.frequency)


class Extension:
    @multimethod
    def __init__(self, start: TimeFrequency, end: TimeFrequency):
        self.start = start
        self.end = end

    @multimethod
    def __init__(self, time_extension: TimeExtension, frequency_extension: FrequencyExtension):
        self.start = TimeFrequency(time_extension.start, frequency_extension.lower)
        self.end = TimeFrequency(time_extension.end, frequency_extension.higher)

    @property
    def time(self):
        return TimeExtension(self.start.time, self.end.time)

    @property
    def frequency(self):
        return FrequencyExtension(self.start.frequency, self.end.frequency)

    @property
    def duration(self):
        return self.time.duration

    @property
    def range(self):
        return self.frequency.range

    def union(self, other: Extension):
        assert isinstance(other, Extension)
        time_extention = self.time.union(other.time)
        frequency_extension = self.frequency.union(other.frequency)
        return Extension(time_extention, frequency_extension)

    def __eq__(self, other):
        assert isinstance(other, Extension)
        return self.time.duration == other.time.duration and self.frequency.range == other.frequency.range

    def __sub__(self, other: Extension):
        assert isinstance(other, Extension)
        time_extension_diff = self.time - other.time
        frequency_extension_diff = self.frequency - other.frequency
        return (TimeFrequency(time_extension_diff[0], frequency_extension_diff[0]),
                TimeFrequency(time_extension_diff[1], frequency_extension_diff[1]))

    def __str__(self):
        return 'Time: %s\tFrequency: %s' % (self.time, self.frequency)

    def __hash__(self):
        return hash((self.time.duration, self.frequency.range))


class PianoRoll:
    @multimethod
    def __init__(self, **kwargs):
        self.array: np.ndarray = kwargs.get('array', np.zeros((0, 0), dtype=np.int8))
        self.origin: Optional[TimeFrequency] = kwargs.get('origin', None)
        self.tatum: TimeShift = kwargs.get('tatum', TimeShift(0))
        self.step: FrequencyShift = kwargs.get('step', FrequencyShift(0))

        self.dynamics: Optional[Dict[Any, int]] = kwargs.get('dynamics', None)
        self._time_signature: Optional[TimeSignature] = kwargs.get('time_signature', None)
        if 'time_signature' in kwargs:
            self.time_signature = TimeSignature(kwargs['time_signature'])

        assert isinstance(self.tatum, TimeShift)
        assert isinstance(self.step, FrequencyShift)

        self._time_vector = None

    @multimethod
    def __init__(self, array: np.ndarray, **kwargs):
        PianoRoll.__init__(self, array=array, **kwargs)

    @multimethod
    def __init__(self, array: np.ndarray, origin: TimeFrequency, **kwargs):
        PianoRoll.__init__(self, array=array, origin=origin, **kwargs)

    @multimethod
    def __init__(self, array: np.ndarray, origin: TimeFrequency, tatum: TimeShift, **kwargs):
        PianoRoll.__init__(self, array=array, origin=origin, tatum=tatum, **kwargs)

    @multimethod
    def __init__(self, array: np.ndarray, origin: TimeFrequency, resolution: TimeFrequency, **kwargs):
        PianoRoll.__init__(self, array=array, origin=origin, tatum=resolution.time, step=resolution.frequency, **kwargs)

    @multimethod
    def __init__(self, array: np.ndarray, origin: TimeFrequency, tatum: TimeShift, step: FrequencyShift, **kwargs):
        PianoRoll.__init__(self, array=array, origin=origin, tatum=tatum, step=step, **kwargs)

    def __eq__(self, other):
        assert isinstance(other, PianoRoll)
        self_reduced = self.reduce()
        other_reduced = other.reduce()
        if self_reduced.array.shape == other_reduced.array.shape:
            same_array = np.all(self_reduced.array == other_reduced.array)
            same_origin = self_reduced.origin == other_reduced.origin
            same_tatum = self_reduced.tatum == other_reduced.tatum
            same_step = self_reduced.step == other_reduced.step
            same_resolution = same_tatum and same_step
            same_time_nature = self_reduced.origin.time.nature == other_reduced.origin.time.nature
            same_frequency_nature = self_reduced.origin.frequency.nature == other_reduced.origin.frequency.nature
            same_nature = same_time_nature and same_frequency_nature
            return same_array and same_origin and same_resolution and same_nature
        else:
            return False

    def __add__(self, other):
        # Check types
        assert isinstance(other, PianoRoll), 'Cannot add PianoRoll with %s' % type(other)

        # Check trivial cases
        if self.array.size == 0:
            return PianoRoll(other.array, other.origin, other.resolution)
        if other.array.size == 0:
            return PianoRoll(self.array, self.origin, self.resolution)

        # Check natures
        assert self.origin.time.nature == other.origin.time.nature, \
            'Cannot add PianoRoll with different time nature'
        assert self.origin.frequency.nature == other.origin.frequency.nature, \
            'Cannot add PianoRoll with different frequency nature'

        # Origin
        time_origin = min(self.origin.time, other.origin.time)
        frequency_origin = min(self.origin.frequency, other.origin.frequency)
        new_origin = TimeFrequency(time_origin, frequency_origin)

        # Tatum
        new_tatum = self.tatum.gcd(other.tatum, self.origin.time - time_origin, other.origin.time - time_origin)
        new_self = self.change_tatum(new_tatum)
        new_other = other.change_tatum(new_tatum)

        # Step
        if self.step != other.step:
            raise NotImplementedError('Supremum between piano rolls with different step is not implemented.')
        else:
            new_step = self.step

        # Compute extensions
        extension_self = new_self.extension
        extension_other = new_other.extension
        extension = Extension(TimeExtension(min(extension_self.time.start,
                                                extension_other.time.start),
                                            max(extension_self.time.end,
                                                extension_other.time.end)),
                              FrequencyExtension(min(extension_self.frequency.lower,
                                                     extension_other.frequency.lower),
                                                 max(extension_self.frequency.higher,
                                                     extension_other.frequency.higher)))

        # Pad piano rolls
        pad_width_self = (((extension_self.frequency.lower - extension.frequency.lower) // new_step,
                           (extension.frequency.higher - extension_self.frequency.higher) // new_step),
                          ((extension_self.time.start - extension.time.start) // new_tatum,
                           (extension.time.end - extension_self.time.end) // new_tatum))
        array_self = np.pad(new_self.array, pad_width_self)

        pad_width_other = (((extension_other.frequency.lower - extension.frequency.lower) // new_step,
                            (extension.frequency.higher - extension_other.frequency.higher) // new_step),
                           ((extension_other.time.start - extension.time.start) // new_tatum,
                            (extension.time.end - extension_other.time.end) // new_tatum))
        array_other = np.pad(new_other.array, pad_width_other)

        new_array = np.maximum(array_self, array_other)

        result = PianoRoll(new_array, new_origin, new_tatum, new_step)
        result.reduce(inplace=True)

        return result

    def __sub__(self, other: TimeFrequency):
        assert isinstance(other, TimeFrequency)
        return type(self)(self.array, self.origin - other, self.tatum, self.step)

    def __getitem__(self, key):
        assert isinstance(key, tuple) and len(key) == 2, 'PianoRoll can only be indexed with 2 dimensions.'
        assert isinstance(key[0], slice) and isinstance(key[1], slice), 'PianoRoll can only be indexed with slices.'
        time_slice = key[0]
        if time_slice.step is not None:
            raise NotImplementedError()

        frequency_slice = key[1]
        if frequency_slice.step is not None:
            raise NotImplementedError()

        f_start = frequency_slice.start if frequency_slice.start is not None else self.extension.frequency.lower
        f_stop = frequency_slice.stop if frequency_slice.stop is not None else self.extension.frequency.higher

        t_start = time_slice.start if time_slice.start is not None else self.extension.time.start
        t_stop = time_slice.stop if time_slice.stop is not None else self.extension.time.end

        new_origin = TimeFrequency(t_start, f_start)

        f_0 = (f_start - self.origin.frequency) // self.step
        f_1 = (f_stop - self.origin.frequency) // self.step
        t_0 = (t_start - self.origin.time) // self.tatum
        t_1 = (t_stop - self.origin.time) // self.tatum
        new_array = self.array[f_0: f_1, t_0: t_1]

        return type(self)(new_array, new_origin, self.tatum, self.step)

    @property
    def time_nature(self):
        return self.origin.time.nature

    @property
    def frequency_nature(self):
        return self.origin.frequency.nature

    @property
    def resolution(self):
        return TimeFrequency(self.tatum, self.step)

    @property
    def extension(self):
        time_extension = TimeExtension(
            self.origin.time,
            self.origin.time + self.array.shape[-1] * self.tatum
        )
        frequency_extension = FrequencyExtension(
            self.origin.frequency,
            self.origin.frequency + self.array.shape[-2] * self.step
        )

        return Extension(time_extension, frequency_extension)

    @property
    def duration(self):
        return self.array.shape[-1] * self.tatum

    @property
    def time_vector(self):
        return TimeVector(self.origin.time, self.tatum)

    @property
    def frequency_vector(self):
        return FrequencyVector(self.origin.frequency, self.step)

    @property
    def time_signature(self):
        if self._time_signature is None:
            self._time_signature = TimeSignature(4, 4)
        return self._time_signature

    @time_signature.setter
    def time_signature(self, time_signature: TimeSignature):
        self._time_signature = time_signature
        self.origin.time.time_signature = time_signature

    def measure(self, c: dict):
        assert isinstance(c, dict) and len(c) == 2, 'c must be a dict of 2 integers.'
        return c['sustain'] * np.sum(self.array.astype(bool)) * self.tatum.value + c['attack'] * np.sum(self.array == 2)

    def copy(self):
        return deepcopy(self)

    def shift(self, time_frequency: TimeFrequency):
        self.origin += time_frequency

    def supremum(self, other):
        result = self + other
        self.array = result.array
        self.origin = result.origin
        self.tatum = result.tatum
        self.step = result.step

    def change_time_extension(self, new_extension: TimeExtension):
        # Compute difference
        diff = new_extension - self.extension.time
        pad_width = ((0, 0), (-(diff[0] // self.tatum), diff[1] // self.tatum))

        # Update attributes
        self.array = np.pad(self.array, pad_width)
        self.origin.time = new_extension.start

    def change_frequency_extension(self, new_extension: FrequencyExtension):
        # Compute difference
        diff = new_extension - self.extension.frequency
        pad_width = ((-(diff[0] // self.step), diff[1] // self.step), (0, 0))

        # Update attributes
        self.array = np.pad(self.array, pad_width)
        self.origin.frequency = new_extension.lower

    def change_extension(self, new_extension: Extension):
        self.change_time_extension(new_extension.time)
        self.change_frequency_extension(new_extension.frequency)

    def change_tatum(self, new_tatum: TimeShift, inplace=False, sparse=False):
        if self.tatum != new_tatum:
            # Compute ratio
            ratio = self.tatum / new_tatum
            if ratio < 1:
                ratio_int = int(1 / ratio)
                assert ratio_int == 1 / ratio

                # Change array
                new_shape = (self.array.shape[0], self.array.shape[1] // ratio_int)
                new_array = np.zeros(new_shape, dtype=self.array.dtype)

                # Compute array
                for k in range(ratio_int):
                    a = self.array[:, k::ratio_int]
                    new_array = np.maximum(new_array, a[:, :new_array.shape[1]])

            else:
                ratio_int = int(ratio)
                assert ratio_int == ratio

                # Change array
                new_shape = (self.array.shape[0], self.array.shape[1] * ratio_int)
                new_array = np.zeros(new_shape, dtype=self.array.dtype)

                # Compute array
                if sparse:
                    new_array[:, ::ratio_int] = self.array
                else:
                    for k in range(ratio_int):
                        if k == 0:
                            new_array[:, k::ratio_int] = self.array
                        else:
                            new_array[:, k::ratio_int] = self.array.astype(bool).astype(self.array.dtype)

            if inplace:
                self.array = new_array
                self.tatum = new_tatum
            else:
                return PianoRoll(new_array, self.origin, new_tatum, self.step)
        else:
            if not inplace:
                return PianoRoll(self.array, self.origin, self.tatum, self.step)

    def change_type(self, new_type: Union[np.dtype, Type[bool]], inplace: bool = False):
        if inplace:
            self.array = self.array.astype(new_type)
        else:
            type_self = type(self)
            new_piano_roll = type_self(self.array.astype(new_type), self.origin, self.tatum, self.step)
            return new_piano_roll

    def reduce(self, inplace: bool = False):
        low = 0
        for i in range(self.array.shape[0]):
            if np.all(self.array[i, :] == 0):
                low += 1
            else:
                break
        high = 0
        for i in range(self.array.shape[0]-1, 0, -1):
            if np.all(self.array[i, :] == 0):
                high += 1
            else:
                break
        early = 0
        for i in range(self.array.shape[1]):
            if np.all(self.array[:, i] == 0):
                early += 1
            else:
                break
        later = 0
        for i in range(self.array.shape[1]-1, 0, -1):
            if np.all(self.array[:, i] == 0):
                later += 1
            else:
                break

        if inplace:
            self.array = self.array[low: self.array.shape[0] - high, early: self.array.shape[1] - later]
            self.origin = TimeFrequency(self.origin.time + early * self.tatum, self.origin.frequency + low * self.step)
        else:
            return PianoRoll(self.array[low: self.array.shape[0] - high, early: self.array.shape[1] - later],
                             TimeFrequency(self.origin.time + early * self.tatum,
                                           self.origin.frequency + low * self.step),
                             self.tatum, self.step)

    @classmethod
    def empty_like(cls, piano_roll: PianoRoll):
        new_piano_roll = cls(np.zeros_like(piano_roll.array), piano_roll.origin, piano_roll.tatum, piano_roll.step)
        return new_piano_roll

    def collapse_tracks(self, inplace: bool = False, keepdims: bool = False):
        if inplace:
            if len(self.array.shape) == 2:
                pass
            elif len(self.array.shape) == 3:
                self.array = np.max(self.array, 0, keepdims=keepdims)
            elif len(self.array.shape) == 4:
                self.array = np.max(self.array, 1, keepdims=keepdims)
            else:
                raise ValueError
        else:
            raise NotImplementedError

    def to_chroma_roll(self) -> ChromaRoll:
        return ChromaRoll(self)

    def to_binary(self, inplace=False):
        if inplace:
            self.array = self.array > 0
        else:
            return PianoRoll(self.array > 0, self.origin, self.tatum, self.step)


class ChromaRoll(PianoRoll):
    @multimethod
    def __init__(self):
        super().__init__()

    @multimethod
    def __init__(self, array: np.ndarray, origin: TimeFrequency, tatum: TimeShift, step: FrequencyShift):
        assert array.shape[-2] == 12
        super().__init__(array, origin, tatum, step)

    @multimethod
    def __init__(self, piano_roll: PianoRoll):
        array = np.zeros((12, piano_roll.array.shape[1]), piano_roll.array.dtype)
        if piano_roll.origin.frequency.nature == 'shift':
            origin_frequency = ChromaShift(0)
        elif piano_roll.origin.frequency.nature == 'point':
            origin_frequency = Chroma(0)
        else:
            raise ValueError('Invalid nature of origin frequency')
        origin = TimeFrequency(piano_roll.origin.time, origin_frequency)
        for i in range(12):
            idx = (i - piano_roll.origin.frequency.value) % 12
            try:
                array[i, :] = np.max(piano_roll.array[idx::12, :], 0)
            except ValueError:
                pass
        self.__init__(array, origin, piano_roll.tatum, ChromaShift(1))

    @property
    def extension(self):
        time_extension = TimeExtension(
            self.origin.time,
            self.origin.time + self.array.shape[-1] * self.tatum
        )
        frequency_extension = FrequencyExtension(
            self.origin.frequency,
            self.origin.frequency + self.step * 11
        )

        return Extension(time_extension, frequency_extension)


class PianoRollStack(List[PianoRoll]):
    def __init__(self, *piano_rolls: PianoRoll):
        super().__init__(piano_rolls)


class Hit(PianoRoll):
    @multimethod
    def __init__(self, start: Time, duration: TimeShift):
        self.start = start

        array = np.array([[2]], dtype=np.uint8)
        origin = TimeFrequency(start, FrequencyShift(0))
        tatum = duration
        step = FrequencyShift(1)

        super().__init__(array, origin, tatum, step)

    @multimethod
    def __init__(self, start: str, duration: str, nature: str = 'shift'):
        if nature == 'shift':
            self.start = TimeShift(start)
        elif nature == 'point':
            self.start = TimePoint(start)

        self.__init__(self.start, TimeShift(duration))

    @property
    def end(self):
        return self.start + self.duration

    def __str__(self):
        return '(%s, %s)' % (self.start, self.duration)


class Rhythm(PianoRoll):
    def __init__(self, *hits: Hit):
        natures = list({hit.time_nature for hit in hits})
        if len(natures) > 1:
            raise WrongNature('Hits must be of the same nature')

        self.hits: List[Hit] = list(hits)

        super().__init__()
        for hit in hits:
            self.supremum(hit)

    @property
    def nature(self):
        if len(self.hits) == 0:
            return 'shift'
        else:
            return self.hits[0].time_nature


class Texture(PianoRollStack):
    def __init__(self, *rhythms: Rhythm):
        if len({type(rhythm.nature) for rhythm in rhythms}) > 1:
            raise WrongNature('Rhythms must be of the same nature')
        super().__init__(*rhythms)

    @property
    def nature(self):
        if len(self) == 0:
            return 'shift'
        else:
            return self[0].time_nature

    @property
    def extension(self):
        max_time = max([rhythm.extension.time.end for rhythm in self])
        min_time = min([rhythm.extension.time.start for rhythm in self])
        return TimeExtension(min_time, max_time)

    @property
    def tatum(self):
        if len(self) == 0:
            return TimeShift(0)
        return self[0].tatum.gcd(*[r.tatum for r in self[1:]])

    @multimethod
    def __mul__(self, harmony: Harmony) -> HarmonicTexture:
        return HarmonicTexture(self, harmony)

    @multimethod
    def __mul__(self, chord: Chord) -> ChordTexture:
        return ChordTexture(self, chord)


class Chord(PianoRoll):
    # @multimethod
    def __init__(self, *frequencies: int, nature: str = 'shift'):
        self.frequencies = sorted(frequencies)
        self.nature = nature

        # Creation of the PianoRoll
        if len(frequencies) == 0:
            PianoRoll.__init__(self, np.zeros((0, 1), dtype=bool), TimeFrequency(),
                               TimeShift(0, 1), FrequencyShift(1))
        else:
            min_freq = min(frequencies)
            ambitus = max(frequencies) - min_freq

            if nature == 'shift':
                frequency_origin = FrequencyShift(min_freq)
            elif nature == 'point':
                frequency_origin = FrequencyPoint(min_freq)
            else:
                raise WrongNature('Chord nature must be either "shift" or "point"')

            size = ambitus + 1
            array = np.zeros((size, 1), dtype=bool)
            for p in frequencies:
                array[p - min_freq] = True

            PianoRoll.__init__(self, array, TimeFrequency(TimeShift(0), frequency_origin),
                               TimeShift(0, 1), FrequencyShift(1))

    # @multimethod
    # def __init__(self, *frequencies: Frequency):
    #     # Check nature
    #     assert len(list({frequency.nature for frequency in frequencies})) == 1, \
    #         'Frequencies must be of the same nature'
    #
    #     self.__init__(*[f.value for f in frequencies], nature=frequencies[0].nature)

    @classmethod
    def from_degree(cls, degree: str, factors: List[Dict[str, str]]):
        degree_dict = roman_numeral_to_factors_dict[degree]
        note_numbers = []
        factor = None
        try:
            for factor in factors:
                value = degree_dict[factor['value']] + 12 * int(factor.get('octave', 0))
                note_numbers.append(value)
        except KeyError:
            raise ValueError("Factor '%s' of '%s' not found." % (factor['value'], degree))
        return cls(*note_numbers, nature='shift')

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
        new_frequencies = list(set(self.frequencies).union(chord.frequencies))
        return Chord(*new_frequencies, nature=self.nature)


class ChromaChord(Chord, ChromaRoll):
    def __init__(self, *frequencies: int, nature: str = 'shift'):
        for f in frequencies:
            assert 0 <= f < 12, 'ChromaChord frequencies must be between 0 and 11'

        self.frequencies = sorted(frequencies)
        self.nature = nature

        # Creation of the PianoRoll
        if len(frequencies) == 0:
            PianoRoll.__init__(self, np.zeros((12, 1), dtype=bool), TimeFrequency(),
                               TimeShift(0, 1), FrequencyShift(1))
        else:
            if nature == 'shift':
                frequency_origin = ChromaShift(0)
            elif nature == 'point':
                frequency_origin = Chroma(0)
            else:
                raise WrongNature('Chord nature must be either "shift" or "point"')

            array = np.zeros((12, 1), dtype=bool)
            for p in frequencies:
                array[p] = True

            ChromaRoll.__init__(self, array, TimeFrequency(TimeShift(0), frequency_origin),
                                TimeShift(0, 1), ChromaShift(1))


class RomanNumeral(ChromaChord):
    def __init__(self, *frequencies: int, nature: str = 'shift', label: str):
        super().__init__(*frequencies, nature=nature)
        self.label = label


class Harmony(PianoRollStack):
    def __init__(self, *chords: Chord):
        if len({chord.nature for chord in chords}) > 1:
            raise WrongNature('Chords must be of the same nature')
        super().__init__(*chords)

    @property
    def nature(self):
        if len(self) == 0:
            return 'shift'
        else:
            return self[0].frequency_nature

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


class HarmonicTexture(PianoRoll):
    def __init__(self, texture: Texture, harmony: Harmony):
        assert isinstance(texture, Texture)
        assert isinstance(harmony, Harmony)
        assert len(texture) == len(harmony)
        self.texture: Texture = texture
        self.harmony: Harmony = harmony

        PianoRoll.__init__(self)
        for rhythm, chord in zip(texture, harmony):
            rhythm: Rhythm
            chord: Chord
            if rhythm.array.size == 0:
                continue
            rhythmed_chord = PianoRoll(chord.array * rhythm.array,
                                       TimeFrequency(rhythm.origin.time, chord.origin.frequency),
                                       rhythm.tatum, chord.step)
            self.supremum(rhythmed_chord)

    def __len__(self):
        return len(self.texture)


class ChordTexture(HarmonicTexture):
    def __init__(self, texture: Texture, chord: Chord):
        self.chord = chord
        harmony = Harmony(*[Chord(c) for c in chord.frequencies])
        HarmonicTexture.__init__(self, texture, harmony)


class Activations(list, PianoRoll):
    def __init__(self, *values: TimeFrequency):
        if len(values) == 0:
            PianoRoll.__init__(self)
            list.__init__(self, [])
            return

        if len({type(v.time) for v in values}) > 1:
            raise WrongNature('Activations must be of the same time type')
        if len({type(v.frequency) for v in values}) > 1:
            raise WrongNature('Activations must be of the same frequency type')

        list.__init__(self, values)

        # Time
        origin_time = min([a.time for a in values])
        tatum = TimeShift.gcd(*[(a.time - origin_time) for a in values])
        duration = max([a.time for a in values]) - origin_time

        # Frequency
        origin_frequency = min([a.frequency for a in values])
        step = FrequencyShift(1)
        ambitus = max([a.frequency for a in values]) - origin_frequency

        # Time-Frequency
        origin = TimeFrequency(origin_time, origin_frequency)
        array = np.zeros((ambitus // step + 1, duration // tatum + 1), dtype=bool)
        for a in values:
            idx_t = (a.time - origin_time) // tatum
            idx_f = (a.frequency - origin_frequency) // step
            array[idx_f, idx_t] = True

        # PianoRoll
        PianoRoll.__init__(self, array, origin, tatum, step)

    def measure(self, c=None):
        return np.sum(self.array)

    def change_time_extension(self, new_extension: TimeExtension):
        # Compute difference
        diff = new_extension - self.extension.time

        if diff[1] < TimeShift(0):
            if diff[1] < self.tatum:
                new_tatum = self.tatum.gcd(diff[1])
                self.change_tatum(new_tatum, inplace=True)
                self.reduce(inplace=True)
                diff = new_extension - self.extension.time
        pad_width = ((0, 0), (-(diff[0] // self.tatum), diff[1] // self.tatum))

        # Update attributes
        self.array = np.pad(self.array, pad_width)
        self.origin.time = new_extension.start

    def change_tatum(self, new_tatum: TimeShift, inplace=False, sparse=True):
        if inplace:
            if self.tatum.value == 0:
                self.tatum = new_tatum
            else:
                PianoRoll.change_tatum(self, new_tatum, inplace, True)
        else:
            if self.tatum.value == 0:
                new_activations = Activations(*self)
                new_activations.tatum = new_tatum
                return new_activations
            else:
                return PianoRoll.change_tatum(self, new_tatum, inplace, True)

    def append(self, element: TimeFrequency) -> None:
        raise NotImplementedError('Change of array not implemented yet.')

    def __add__(self, other):
        if isinstance(other, PianoRoll):
            from .morphology import dilation
            return dilation(self, other)
        elif isinstance(other, tuple):
            return self + (other[0] + other[1])
        else:
            return self + other.to_piano_roll()


class ActivationsChroma(Activations, ChromaRoll):
    @multimethod
    def __init__(self):
        Activations.__init__(self)
        ChromaRoll.__init__(self)

    @multimethod
    def __init__(self, *values: TimeFrequency):
        if len(values) == 0:
            ChromaRoll.__init__(self)
            Activations.__init__(self)
            return

        if len({type(v.time) for v in values}) > 1:
            raise WrongNature('Activations must be of the same time type')
        if len({type(v.frequency) for v in values}) > 1:
            raise WrongNature('Activations must be of the same frequency type')

        Activations.__init__(self, *values)

        # Time
        origin_time = min([a.time for a in values])
        tatum = TimeShift.gcd(*[(a.time - origin_time) for a in values])
        duration = max([a.time for a in values]) - origin_time

        # Frequency
        origin_frequency = type(values[0].frequency)(0)
        step = ChromaShift(1)

        # Time-Frequency
        origin = TimeFrequency(origin_time, origin_frequency)
        array = np.zeros((12, duration // tatum + 1), dtype=bool)
        for a in values:
            idx_t = (a.time - origin_time) // tatum
            idx_f = (a.frequency - origin_frequency) // step
            array[idx_f, idx_t] = True

        # ChromaRoll
        ChromaRoll.__init__(self, array, origin, tatum, step)

    def reduce(self, inplace: bool = False):
        early = 0
        for i in range(self.array.shape[1]):
            if (self.array[:, i] == 0).all():
                early += 1
            else:
                break
        later = 0
        for i in range(self.array.shape[1]-1, 0, -1):
            if (self.array[:, i] == 0).all():
                later += 1
            else:
                break

        if inplace:
            self.array = self.array[:, early: self.array.shape[1] - later]
            self.origin = TimeFrequency(self.origin.time + early * self.tatum, self.origin.frequency)
        else:
            return PianoRoll(self.array[:, early: self.array.shape[1] - later],
                             TimeFrequency(self.origin.time + early * self.tatum,
                                           self.origin.frequency),
                             self.tatum, self.step)

    @property
    def extension(self):
        time_extension = TimeExtension(
            self.origin.time,
            self.origin.time + self.array.shape[-1] * self.tatum
        )
        frequency_extension = FrequencyExtension(
            self.origin.frequency,
            self.origin.frequency + self.step * 11
        )

        return Extension(time_extension, frequency_extension)

    def change_extension(self, new_extension: Extension):
        self.change_time_extension(new_extension.time)

    def append(self, element: TimeFrequency) -> None:
        raise NotImplementedError('Change of array not implemented yet.')


class ActivationsStack(List[Activations]):
    def __init__(self, *activations_list: Activations):
        super().__init__(activations_list)

    def change_tatum(self, new_tatum=None, inplace=False):
        if new_tatum is None:
            new_tatum = self[0].tatum.gcd(*[a.tatum for a in self[1:]])
        for a in self:
            if len(a) != 0:
                a.change_tatum(new_tatum, inplace=inplace)

    def change_extension(self, extension: Extension):
        for i, a in enumerate(self):
            if len(a) == 0:
                continue
            a.change_extension(extension)

    def synchronize(self):
        activations_stack_array = self.to_array()
        contraction_frequency = np.any(activations_stack_array, axis=-2, keepdims=True)
        contraction_indexes = np.all(contraction_frequency, axis=0, keepdims=True)
        activations_stack_array *= contraction_indexes

        i, m, n = np.where(activations_stack_array)

        activations_list = []
        for k in range(len(self)):
            t = np.array([self[k].origin.time]) + n[i == k] * self[k].tatum
            f = np.array([self[k].origin.frequency]) + m[i == k] * self[k].step
            activations_list.append(Activations(*[TimeFrequency(ti, fi) for ti, fi in zip(t, f)]))

        return ActivationsStack(*activations_list)

    def to_array(self):
        if len({a.tatum for a in self}) != 1:
            new_tatum = self[0].tatum.gcd(*[a.tatum for a in self[1:]])
            a_list = []
            for a in self:
                a_list.append(a.change_tatum(new_tatum))
        else:
            a_list = self

        assert len({a.step for a in a_list}) == 1, 'All activations must have the same step'

        if len({a.extension for a in a_list}) != 1:
            new_extension = a_list[0].extension
            for a in a_list[1:]:
                a_ext = a.extension
                new_extension = new_extension.union(a_ext)
            for a in a_list:
                a.change_extension(new_extension)

        assert len({a.extension for a in a_list}) == 1, 'All activations must have the same extension'

        return np.stack([a.array for a in a_list])

    def contract(self) -> Activations:
        result = Activations()
        for a in self:
            result = PianoRoll.__add__(result, a)
        return result


class ScoreTree:
    def __init__(self, components: List[Tuple[Activations, Union[HarmonicTexture, ScoreTree]]]):
        self.components = components

    def to_piano_roll(self):
        result = None
        for a, b in self.components:
            if isinstance(b, ScoreTree):
                b = b.to_piano_roll()

            if result is None:
                result = a + b
            else:
                d = a + b
                result = result + d

        result.reduce(True)

        return result
