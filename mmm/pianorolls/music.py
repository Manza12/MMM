from __future__ import annotations

from . import *
from .dictionaries import roman_numeral_to_factors_dict
from .utils import midi_number_to_pitch, midi_numbers_to_chromas, gcd, nature_of_list


class Time:
    nature: Optional[str] = None

    @multimethod
    def __init__(self, value: frac):
        if type(self) == Time:
            raise ValueError('Time is an abstract class.')
        else:
            self.value = value

    @multimethod
    def __init__(self, value: int):
        if type(self) == Time:
            raise ValueError('Time is an abstract class.')
        else:
            self.__init__(frac(value))

    @multimethod
    def __init__(self, value: str):
        if type(self) == Time:
            raise ValueError('Time is an abstract class.')
        else:
            self.__init__(frac(value))

    @multimethod
    def __init__(self, numerator: int, denominator: int):
        if type(self) == Time:
            raise ValueError('Time is an abstract class.')
        else:
            self.__init__(frac(numerator, denominator))

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

    def __sub__(self, other) -> Time:
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
    nature = 'shift'

    def __init__(self, *args):
        super().__init__(*args)

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
            return self.value / other.value
        else:
            return TimeShift(self.value / other)

    def __floordiv__(self, other):
        assert isinstance(other, TimeShift) or isinstance(other, int)
        if isinstance(other, TimeShift):
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

    @staticmethod
    def zero():
        return TimeShift(0)

    def gcd(self, *others):
        if len(others) == 0:
            return self
        if len(others) == 1:
            assert isinstance(others[0], TimeShift)
            return TimeShift(gcd(self.value, others[0].value))

        result = self
        for other in others:
            assert isinstance(other, TimeShift), 'TimeShift.gcd() only accepts TimeShifts as arguments.'
            result = result.gcd(other)
        return result


class TimeSignature:
    def __init__(self, numerator: int, denominator: int):
        self.numerator: int = numerator
        self.denominator: int = denominator
        self.duration: TimeShift = TimeShift(numerator, denominator)

    def __str__(self):
        return str(self.numerator) + '/' + str(self.denominator)


class TimePoint(Time):
    nature = 'point'

    @multimethod
    def __init__(self, value: frac, time_signature: Union[Tuple[int, int], TimeSignature] = (4, 4)):
        super().__init__(value)
        if isinstance(time_signature, TimeSignature):
            self.time_signature = time_signature
        else:
            self.time_signature = TimeSignature(*time_signature)

    @multimethod
    def __init__(self, value: int, time_signature: Union[Tuple[int, int], TimeSignature] = (4, 4)):
        super().__init__(value)
        if isinstance(time_signature, TimeSignature):
            self.time_signature = time_signature
        else:
            self.time_signature = TimeSignature(*time_signature)

    @multimethod
    def __init__(self, value: str, time_signature: Union[Tuple[int, int], TimeSignature] = (4, 4)):
        super().__init__(value)
        if isinstance(time_signature, TimeSignature):
            self.time_signature = time_signature
        else:
            self.time_signature = TimeSignature(*time_signature)

    @multimethod
    def __init__(self, numerator: int, denominator: int,
                 time_signature: Union[Tuple[int, int], TimeSignature] = (4, 4)):
        super().__init__(numerator, denominator)
        if isinstance(time_signature, TimeSignature):
            self.time_signature = time_signature
        else:
            self.time_signature = TimeSignature(*time_signature)

    @multimethod
    def __init__(self, measure: int, beat: int, offset: Union[str, int],
                 time_signature: Union[Tuple[int, int], TimeSignature] = (4, 4)):
        self.time_signature = TimeSignature(*time_signature)
        measure_duration = self.time_signature.duration
        beat_duration = TimeShift(1, self.time_signature.denominator)
        offset = TimeShift(offset)
        time_point = (measure - 1) * measure_duration + (beat - 1) * beat_duration + offset
        super().__init__(time_point.value)

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
        assert isinstance(other, TimeShift), 'TimePoint can only be divided by TimeShift.'
        return self.value / other.value

    def __floordiv__(self, other):
        assert isinstance(other, TimeShift), 'TimePoint can only be floordivided by TimeShift.'
        return self.value // other.value

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

    @staticmethod
    def zero(time_signature=(4, 4)):
        return TimePoint(0, time_signature=time_signature)


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

    def __str__(self):
        return '%s - %s (%s)' % (self.start, self.end, self.duration.value)


# Frequency
class Frequency:
    nature: Optional[str] = None

    def __init__(self, value):
        if type(self) == Frequency:
            raise ValueError('Time is an abstract class.')
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

    def __sub__(self, other) -> Frequency:
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
    nature = 'shift'

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

    @staticmethod
    def zero():
        return FrequencyShift(0)


class FrequencyPoint(Frequency):
    nature = 'point'

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

    @staticmethod
    def zero():
        return FrequencyPoint(0)


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

    def __str__(self):
        return '%s - %s (%s)' % (self.lower, self.higher, self.range)


# Time-Frequency
class TimeFrequency:
    # @multimethod
    def __init__(self, time: Time, frequency: Frequency):
        self.time = time
        self.frequency = frequency

    # @multimethod
    # def __init__(self, time: Time, frequency: int, frequency_nature: str = 'shift'):
    #     self.__init__([time.numerator, time.denominator], frequency, time.nature, frequency_nature)
    #
    # @multimethod
    # def __init__(self, time: str, frequency: Frequency, time_nature: str = 'shift'):
    #     self.__init__('%s/%s' % time, frequency, time_nature, frequency.nature)
    #
    # @multimethod
    # def __init__(self, time: Tuple[int, int], frequency: Frequency, time_nature: str = 'shift'):
    #     self.__init__(time, frequency, time_nature, frequency.nature)
    #
    # @multimethod
    # def __init__(self, time: str, frequency: int,
    #              time_nature: str = 'shift', frequency_nature: str = 'shift'):
    #     # Time
    #     if time_nature == 'shift':
    #         self.time = TimeShift(time)
    #     elif time_nature == 'point':
    #         self.time = TimePoint(time)
    #     else:
    #         raise ValueError("Parameter 'time_nature' should be one of 'shift' and 'point'.")
    #
    #     # Frequency
    #     if frequency_nature == 'shift':
    #         self.frequency = FrequencyShift(frequency)
    #     elif frequency_nature == 'point':
    #         self.frequency = FrequencyPoint(frequency)
    #     else:
    #         raise ValueError("Parameter 'frequency_nature' should be one of 'shift' and 'point'.")
    #
    # @multimethod
    # def __init__(self, time: Tuple[int, int], frequency: int,
    #              time_nature: str = 'shift', frequency_nature: str = 'shift'):
    #     self.__init__('%s/%s' % time, frequency, time_nature, frequency_nature)

    def __eq__(self, other):
        if isinstance(other, TimeFrequency):
            return self.time == other.time and self.frequency == other.frequency
        else:
            return False

    def __add__(self, other):
        assert isinstance(other, TimeFrequency)
        return TimeFrequency(self.time + other.time, self.frequency + other.frequency)

    # @classmethod
    # def zero(cls):
    #     return cls('0', 0)

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

    def __str__(self):
        return 'Time: %s\tFrequency: %s' % (self.time, self.frequency)


class PianoRoll:
    @multimethod
    def __init__(self, **kwargs):
        self.array: np.ndarray = kwargs.get('array', np.zeros((0, 0), dtype=np.int8))
        self.origin: Tuple[int, int] = kwargs.get('origin', (0, 0))
        self.tatum: TimeShift = kwargs.get('tatum', TimeShift(0))
        self.step: FrequencyShift = kwargs.get('step', FrequencyShift(1))
        self.time_nature = kwargs.get('time_nature', None)
        self.frequency_nature = kwargs.get('frequency_nature', None)

        self.dynamics: Optional[Dict[Any, int]] = kwargs.get('dynamics', None)
        self.time_signature: TimeSignature = TimeSignature(4, 4)
        if 'time_signature' in kwargs:
            self.time_signature = TimeSignature(*kwargs['time_signature'])

        assert isinstance(self.tatum, TimeShift)
        assert isinstance(self.step, FrequencyShift)
        assert self.time_nature in [None, 'shift', 'point'] and self.frequency_nature in [None, 'shift', 'point']

        self._time_vector = None

    @multimethod
    def __init__(self, array: np.ndarray, **kwargs):
        PianoRoll.__init__(self, array=array, **kwargs)

    @multimethod
    def __init__(self, array: np.ndarray, origin: Tuple[int, int], **kwargs):
        PianoRoll.__init__(self, array=array, origin=origin, **kwargs)

    @multimethod
    def __init__(self, array: np.ndarray, origin: Tuple[int, int], tatum: TimeShift, **kwargs):
        PianoRoll.__init__(self, array=array, origin=origin, tatum=tatum, **kwargs)

    @multimethod
    def __init__(self, array: np.ndarray, origin: Tuple[int, int], resolution: TimeFrequency, **kwargs):
        PianoRoll.__init__(self, array=array, origin=origin, tatum=resolution.time, step=resolution.frequency, **kwargs)

    @multimethod
    def __init__(self, array: np.ndarray, origin: Tuple[int, int], tatum: TimeShift, step: FrequencyShift,
                 time_nature: Optional[str], frequency_nature: Optional[str], **kwargs):
        PianoRoll.__init__(self, array=array, origin=origin, tatum=tatum, step=step,
                           time_nature=time_nature, frequency_nature=frequency_nature, **kwargs)

    def __eq__(self, other):
        assert isinstance(other, PianoRoll)
        self_reduced = self.reduce()
        other_reduced = other.reduce()
        if self_reduced.array.shape == other_reduced.array.shape:
            same_array = (self_reduced.array == other_reduced.array).all()
            same_origin = self_reduced.origin == other_reduced.origin
            same_tatum = self_reduced.tatum == other_reduced.tatum
            same_step = self_reduced.step == other_reduced.step
            same_resolution = same_tatum and same_step
            same_time_nature = self_reduced.time_nature == other_reduced.time_nature
            same_frequency_nature = self_reduced.frequency_nature == other_reduced.frequency_nature
            same_nature = same_time_nature and same_frequency_nature
            return same_array and same_origin and same_resolution and same_nature
        else:
            return False

    def __add__(self, other):
        assert isinstance(other, PianoRoll)
        result = PianoRoll.supremum(self, other)
        result.reduce(inplace=True)
        return result

    @property
    def resolution(self):
        return TimeFrequency(self.tatum, self.step)

    @property
    def extension(self):
        if self.time_nature == 'shift':
            time_extension = TimeExtension(-self.origin[1] * self.tatum,
                                           (self.array.shape[-1] - self.origin[1]) * self.tatum)
        elif self.time_nature == 'point':
            zero = TimePoint(0, time_signature=self.time_signature)
            time_extension = TimeExtension(zero - self.origin[1] * self.tatum,
                                           zero + (self.array.shape[-1] - self.origin[1]) * self.tatum)
        else:
            raise ValueError('Time nature must be either "shift" or "point"')

        if self.frequency_nature == 'shift':
            frequency_extension = FrequencyExtension(
                -self.origin[0] * self.step,
                (self.array.shape[-2] - self.origin[0] - 1) * self.step
            )
        else:
            frequency_extension = FrequencyExtension(
                FrequencyPoint(0) - self.origin[0] * self.step,
                FrequencyPoint(0) + (self.array.shape[-2] - self.origin[0] - 1) * self.step
            )

        return Extension(time_extension, frequency_extension)

    @property
    def duration(self):
        return self.array.shape[1] * self.tatum

    def change_tatum(self, new_tatum: TimeShift, inplace=False, null=False):
        if self.tatum != new_tatum:
            # Compute ratio
            ratio = self.tatum / new_tatum
            if ratio < 1:
                ratio_int = int(1 / ratio)
                assert ratio_int == 1 / ratio

                # Change origin
                new_origin = (self.origin[0], self.origin[1] // ratio_int)

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

                # Change origin
                new_origin = (self.origin[0], self.origin[1] * ratio_int)

                # Change array
                new_shape = (self.array.shape[0], self.array.shape[1] * ratio_int)
                new_array = np.zeros(new_shape, dtype=self.array.dtype)

                # Compute array
                if null:
                    new_array[:, ::ratio_int] = self.array
                else:
                    for k in range(ratio_int):
                        if k == 0:
                            new_array[:, k::ratio_int] = self.array
                        else:
                            new_array[:, k::ratio_int] = self.array.astype(bool).astype(self.array.dtype)

            if inplace:
                self.array = new_array
                self.origin = new_origin
                self.tatum = new_tatum
            else:
                return PianoRoll(new_array, new_origin, new_tatum, self.step, self.time_nature, self.frequency_nature)
        else:
            if not inplace:
                return PianoRoll(self.array, self.origin, self.tatum, self.step, self.time_nature,
                                 self.frequency_nature)

    def change_type(self, new_type: np.dtype, inplace: bool = False):
        if inplace:
            self.array = self.array.astype(new_type)
        else:
            new_block = PianoRoll(self.array.astype(new_type), self.origin, self.tatum, self.step,
                                  self.time_nature, self.frequency_nature)
            return new_block

    def reduce(self, inplace: bool = False):
        low = 0
        for i in range(self.array.shape[0]):
            if (self.array[i, :] == 0).all():
                low += 1
            else:
                break
        high = 0
        for i in range(self.array.shape[0]-1, 0, -1):
            if (self.array[i, :] == 0).all():
                high += 1
            else:
                break
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
            self.array = self.array[low: self.array.shape[0] - high, early: self.array.shape[1] - later]
            self.origin = (self.origin[0] - low, self.origin[1] - early)
        else:
            return PianoRoll(self.array[low: self.array.shape[0] - high, early: self.array.shape[1] - later],
                             (self.origin[0] - low, self.origin[1] - early),
                             self.tatum, self.step, self.time_nature, self.frequency_nature)

    def combine(self, other, inplace: bool = False):
        if inplace:
            new_block = PianoRoll.supremum(self, other)
            self.array = new_block.array
            self.origin = new_block.origin
            self.tatum = new_block.tatum
            self.step = new_block.step
            self.time_nature = new_block.time_nature
            self.frequency_nature = new_block.frequency_nature
            del new_block
        else:
            return PianoRoll.supremum(self, other)

    def subblock(self, start: Time, end: Time):
        assert start <= end, 'Start should be before end.'
        assert start >= self.extension.time.start, 'Start should be positive.'
        assert end <= self.extension.time.end, 'End should be smaller than duration.'

        start_index = start // self.tatum
        end_index = end // self.tatum
        return PianoRoll(self.array[:, start_index: end_index], (self.origin[0], self.origin[1] + start_index),
                         self.tatum, self.step, self.time_nature, self.frequency_nature)

    @staticmethod
    def supremum(block_1: PianoRoll, block_2: PianoRoll):
        # Check types
        assert isinstance(block_1, PianoRoll) and isinstance(block_2, PianoRoll), 'Combine is made between blocks.'
        if block_1.time_nature is None:
            time_nature = block_2.time_nature
        elif block_2.time_nature is None:
            time_nature = block_1.time_nature
        else:
            assert block_1.time_nature == block_2.time_nature, 'Combine should have the same time nature.'
            time_nature = block_1.time_nature
        if block_1.frequency_nature is None:
            frequency_nature = block_2.frequency_nature
        elif block_2.frequency_nature is None:
            frequency_nature = block_1.frequency_nature
        else:
            assert block_1.frequency_nature == block_2.frequency_nature, 'Combine should have the same time nature.'
            frequency_nature = block_1.frequency_nature

        # Check trivial cases
        if block_1.array.size == 0:
            return PianoRoll(block_2.array, block_2.origin, block_2.resolution,
                             time_nature=time_nature, frequency_nature=frequency_nature)
        if block_2.array.size == 0:
            return PianoRoll(block_1.array, block_1.origin, block_1.resolution,
                             time_nature=time_nature, frequency_nature=frequency_nature)

        # Tatum
        new_tatum = block_1.tatum.gcd(block_2.tatum)
        new_block_1 = block_1.change_tatum(new_tatum)
        new_block_2 = block_2.change_tatum(new_tatum)

        # Step
        if block_1.step != block_2.step:
            raise NotImplementedError('Supremum between blocks with different step is not implemented.')
        else:
            new_step = block_1.step

        # Compute extensions
        extension_1 = new_block_1.extension
        extension_2 = new_block_2.extension
        extension = Extension(TimeExtension(min(extension_1.time.start, extension_2.time.start),
                                            max(extension_1.time.end, extension_2.time.end)),
                              FrequencyExtension(min(extension_1.frequency.lower, extension_2.frequency.lower),
                                                 max(extension_1.frequency.higher, extension_2.frequency.higher)))

        # Pad blocks
        pad_width_1 = (((extension_1.frequency.lower - extension.frequency.lower) // new_step,
                       (extension.frequency.higher - extension_1.frequency.higher) // new_step),
                       ((extension_1.time.start - extension.time.start) // new_tatum,
                       (extension.time.end - extension_1.time.end) // new_tatum))
        array_1 = np.pad(new_block_1.array, pad_width_1)

        pad_width_2 = (((extension_2.frequency.lower - extension.frequency.lower) // new_step,
                       (extension.frequency.higher - extension_2.frequency.higher) // new_step),
                       ((extension_2.time.start - extension.time.start) // new_tatum,
                       (extension.time.end - extension_2.time.end) // new_tatum))
        array_2 = np.pad(new_block_2.array, pad_width_2)

        # Create new piano_roll
        zero_time = type(block_1.time_vector[0]).zero()
        zero_frequency = type(block_1.frequency_vector[0]).zero()
        new_origin = (-((extension.frequency.lower - zero_frequency) // new_step),
                      -((extension.time.start - zero_time) // new_tatum))
        new_array = np.maximum(array_1, array_2)

        return PianoRoll(new_array, new_origin, new_tatum, new_step, time_nature, frequency_nature)

    @classmethod
    def empty_like(cls, block):
        block: PianoRoll
        new_block = cls(np.zeros_like(block.array), block.origin,
                        block.tatum, block.step, block.time_nature, block.frequency_nature)
        return new_block

    @property
    def time_vector(self):
        if self._time_vector is None:
            result = []
            start = self.extension.time.start
            for i in range(self.array.shape[-1]):
                result.append(start + i * self.tatum)
            self._time_vector = result
            return result
        else:
            return self._time_vector

    @property
    def frequency_vector(self):
        result = []
        lower = self.extension.frequency.lower
        for i in range(self.array.shape[-2]):
            result.append(lower + i * self.step)
        return result

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

    def to_chroma_block(self) -> ChromaRoll:
        return ChromaRoll(self)

    def to_binary(self, inplace=False):
        if inplace:
            self.array = self.array > 0
        else:
            return PianoRoll(self.array > 0, self.origin, self.tatum, self.step, self.time_nature,
                             self.frequency_nature)


class ChromaRoll(PianoRoll):
    @multimethod
    def __init__(self, array: np.ndarray, origin: Tuple[int, int], tatum: TimeShift, step: FrequencyShift,
                 time_nature: Optional[str], frequency_nature: Optional[str]):
        super().__init__(array, origin, tatum, step, time_nature, frequency_nature)

    @multimethod
    def __init__(self, block: PianoRoll):
        array = np.zeros((12, block.array.shape[1]), block.array.dtype)
        origin = (0, block.origin[1])
        for i in range(12):
            idx = (i + block.origin[0]) % 12
            try:
                array[i, :] = np.max(block.array[idx::12, :], 0)
            except ValueError:
                pass
        self.__init__(array, origin, block.tatum, block.step, block.time_nature, block.frequency_nature)

    def change_type(self, new_type: np.dtype, inplace: bool = False):
        if inplace:
            self.array = self.array.astype(new_type)
        else:
            new_block = ChromaRoll(self.array.astype(new_type), self.origin, self.tatum, self.step,
                                   self.time_nature, self.frequency_nature)
            return new_block

    @classmethod
    def empty_like(cls, block):
        block: ChromaRoll
        new_block = cls(np.zeros_like(block.array), block.origin,
                        block.tatum, block.step, block.time_nature, block.frequency_nature)
        return new_block

    @property
    def frequency_vector(self):
        return midi_numbers_to_chromas([i for i in range(12)])


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
            tatum = tatum.gcd(hit.start, hit.duration)

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

    def __mul__(self, other) -> PianoRoll:
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


class Activations(PianoRoll, list):
    def __init__(self, *values: TimeFrequency):
        list.__init__(self, values)
        frequency_nature = nature_of_list([a.frequency.nature for a in values])
        time_nature = nature_of_list([a.time.nature for a in values])

        # Time
        zero_time = type(values[0].time).zero()
        tatum = TimeShift.gcd(*[(a.time - zero_time) for a in values])
        if tatum == zero_time:
            tatum = TimeShift(1)

        earlier_activation = min([a.time for a in values])
        earlier_index = (earlier_activation - zero_time) // tatum

        later_activation = max([a.time for a in values])
        later_index = (later_activation - zero_time) // tatum

        duration = later_index - earlier_index
        origin_time = -earlier_index

        # Frequency
        zero_frequency = type(values[0].frequency).zero()
        step = FrequencyShift(1)

        lower_frequency = min([a.frequency for a in values])
        higher_frequency = max([a.frequency for a in values])

        ambitus = higher_frequency - lower_frequency

        lower_index = (lower_frequency - zero_frequency) // step
        origin_frequency = -lower_index

        # Time-Frequency
        origin = (origin_frequency, origin_time)
        array = np.zeros((ambitus // step + 1, duration + 1), dtype=bool)
        for a in values:
            idx_t = (a.time - zero_time) // tatum - earlier_index
            idx_f = (a.frequency - zero_frequency) // step - lower_index
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
