from __future__ import annotations
import numpy as np
from abc import ABC
from typing import Tuple, Optional, Dict, Any
from fractions import Fraction as frac
from multimethod import multimethod
from .utils import midi_number_to_pitch, midi_numbers_to_chromas, gcd


# Time
class Time(frac, ABC):
    nature: Optional[str] = None

    def __init__(self, *args):
        if type(self) == Time:
            raise ValueError('Time is an abstract class.')


class TimeShift(Time, ABC):
    nature = 'shift'

    def __new__(cls, *args, **kwargs):
        return Time.__new__(cls, *args, **kwargs)

    def __eq__(self, other):
        if isinstance(other, TimeShift):
            return super().__eq__(other)
        else:
            return False

    def __add__(self, other):
        assert isinstance(other, TimeShift) or isinstance(other, TimePoint)
        if isinstance(other, TimeShift):
            return TimeShift(Time.__add__(self, other))
        else:
            return TimePoint(Time.__add__(self, other))

    def __sub__(self, other):
        assert isinstance(other, TimeShift)
        return TimeShift(Time.__sub__(self, other))

    def __mul__(self, other):
        assert isinstance(other, int)
        return TimeShift(Time.__mul__(self, other))

    def __rmul__(self, other):
        return self * other


class TimeSignature:
    def __init__(self, numerator: int, denominator: int):
        self.numerator: int = numerator
        self.denominator: int = denominator
        self.duration: TimeShift = TimeShift(numerator, denominator)

    def __str__(self):
        return str(self.numerator) + '/' + str(self.denominator)


class TimePoint(Time, ABC):
    nature = 'point'

    def __new__(cls, *args, **kwargs):
        kwargs.pop('time_signature', None)
        return Time.__new__(cls, *args, **kwargs)

    def __init__(self, *args, time_signature: TimeSignature = TimeSignature(4, 4)):
        super().__init__(*args)
        self.time_signature = time_signature

    @property
    def measure(self):
        return self // self.time_signature.duration + 1

    @property
    def beat(self):
        remaining = self - (self.measure - 1) * self.time_signature.duration
        return remaining // TimeShift(1, self.time_signature.denominator) + 1

    @property
    def offset(self):
        remaining = self - (self.measure - 1) * self.time_signature.duration
        return remaining - TimePoint(self.beat - 1, self.time_signature.denominator)

    def __eq__(self, other):
        if isinstance(other, TimePoint):
            return super().__eq__(other)
        else:
            return False

    def __add__(self, other: TimeShift):
        assert isinstance(other, TimeShift), 'TimePoint can only be added with TimeShift.'
        return TimePoint(super().__add__(other), time_signature=self.time_signature)

    def __sub__(self, other):
        assert isinstance(other, TimePoint) or isinstance(other, TimeShift), \
            "Substraction is made between TimePoint and TimePoint or TimePoint and TimeShift"
        if isinstance(other, TimePoint):
            return TimeShift(super().__sub__(other))
        else:
            return TimePoint(super().__sub__(other), time_signature=self.time_signature)

    def __str__(self, time_signature: TimeShift = TimeShift(4, 4)):
        return '(%s, %s, %s)' % (self.measure, self.beat, self.offset)


class TimeExtension:
    def __init__(self, start: Time, end: Time):
        assert type(start) == type(end)
        assert start <= end
        self.start = start
        self.end = end

    @property
    def duration(self):
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
        return '%s - %s (%s)' % (self.start, self.end, frac(self.duration))


# Frequency
class Frequency(int):
    nature: Optional[str] = None

    def __init__(self, _):
        if type(self) == Frequency:
            raise ValueError('Time is an abstract class.')


class FrequencyShift(Frequency):
    nature = 'shift'

    def __new__(cls, *args, **kwargs):
        return Frequency.__new__(cls, *args, **kwargs)

    def __init__(self, shift: int):
        super().__init__(shift)

    def __eq__(self, other):
        if isinstance(other, FrequencyShift):
            return super().__eq__(other)
        else:
            return False

    def __add__(self, other):
        assert isinstance(other, FrequencyShift) or isinstance(other, FrequencyPoint)
        if isinstance(other, FrequencyShift):
            return FrequencyShift(super().__add__(other))
        else:
            return FrequencyPoint(super().__add__(other))

    def __mul__(self, other):
        return FrequencyShift(int(self) * other)

    def __rmul__(self, other):
        return FrequencyShift.__mul__(self, other)

    def __sub__(self, other):
        assert isinstance(other, FrequencyShift)
        return FrequencyShift(super().__sub__(other))

    def __hash__(self):
        return hash((int(self), self.nature))


class FrequencyPoint(Frequency):
    nature = 'point'

    def __new__(cls, *args, **kwargs):
        return Frequency.__new__(cls, *args, **kwargs)

    def __init__(self, midi_number: int):
        super().__init__(midi_number)

    def __eq__(self, other):
        if isinstance(other, FrequencyPoint):
            return super().__eq__(other)
        else:
            return False

    def __add__(self, other: FrequencyShift):
        assert isinstance(other, FrequencyShift), 'FrequencyPoint can only be added with FrequencyShift.'
        return FrequencyPoint(super().__add__(other))

    def __sub__(self, other):
        assert isinstance(self, FrequencyPoint) or isinstance(self, FrequencyShift), \
            "Subtraction is made between FrequencyPoint and FrequencyPoint or FrequencyPoint and FrequencyShift"
        if isinstance(self, FrequencyPoint):
            return FrequencyShift(super().__sub__(other))
        else:
            return FrequencyPoint(super().__sub__(other))

    def __str__(self):
        return midi_number_to_pitch(self)


class FrequencyExtension:
    def __init__(self, lower: Frequency, higher: Frequency):
        assert type(lower) == type(higher)
        assert lower <= higher
        self.lower = lower
        self.higher = higher

    @property
    def range(self):
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
        return '%s - %s (%d)' % (self.lower, self.higher, self.range)


# Time-Frequency
class TimeFrequency:
    @multimethod
    def __init__(self, time: Time, frequency: Frequency):
        self.time = time
        self.frequency = frequency

    @multimethod
    def __init__(self, time: str, frequency: int,
                 time_nature: str = 'shift', frequency_nature: str = 'shift'):
        # Time
        if time_nature == 'shift':
            self.time = TimeShift(time)
        elif time_nature == 'point':
            self.time = TimePoint(time)
        else:
            raise ValueError("Parameter 'time_nature' should be one of 'shift' and 'point'.")

        # Frequency
        if frequency_nature == 'shift':
            self.frequency = FrequencyShift(frequency)
        elif frequency_nature == 'point':
            self.frequency = FrequencyPoint(frequency)
        else:
            raise ValueError("Parameter 'frequency_nature' should be one of 'shift' and 'point'.")

    @multimethod
    def __init__(self, time: Tuple[int, int], frequency: int,
                 time_nature: str = 'shift', frequency_nature: str = 'shift'):
        self.__init__('%s/%s' % time, frequency, time_nature, frequency_nature)

    def __eq__(self, other):
        if isinstance(other, TimeFrequency):
            return self.time == other.time and self.frequency == other.frequency
        else:
            return False

    def __add__(self, other):
        assert isinstance(other, TimeFrequency)
        return TimeFrequency(self.time + other.time, self.frequency + other.frequency)

    @classmethod
    def zero(cls):
        return cls('0', 0)

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
                 time_nature: Optional[str], frequency_nature: Optional[str]):
        PianoRoll.__init__(self, array=array, origin=origin, tatum=tatum, step=step,
                           time_nature=time_nature, frequency_nature=frequency_nature)

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
        return PianoRoll.supremum(self, other)

    @property
    def resolution(self):
        return TimeFrequency(self.tatum, self.step)

    @property
    def extension(self):
        if self.time_nature == 'shift':
            time_extension = TimeExtension(-self.origin[1] * self.tatum,
                                           (self.array.shape[-1] - self.origin[1]) * self.tatum)
        else:
            time_extension = TimeExtension(TimePoint(-self.origin[1] * self.tatum),
                                           TimePoint((self.array.shape[-1] - self.origin[1]) * self.tatum))

        if self.frequency_nature == 'shift':
            frequency_extension = FrequencyExtension(
                FrequencyShift(-self.origin[0] * self.step),
                FrequencyShift((self.array.shape[-2] - self.origin[0] - 1) * self.step))
        else:
            frequency_extension = FrequencyExtension(
                FrequencyPoint(-self.origin[0] * self.step),
                FrequencyPoint((self.array.shape[-2] - self.origin[0] - 1) * self.step))

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
    def supremum(block_1, block_2):
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
        new_tatum = TimeShift(gcd(block_1.tatum, block_2.tatum))
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

        # Create new block
        new_origin = (-(extension.frequency.lower // new_step), -(extension.time.start // new_tatum))
        new_array = np.maximum(array_1, array_2)

        return PianoRoll(new_array, new_origin, new_tatum, new_step, time_nature, frequency_nature)

    @classmethod
    def empty_block_like(cls, block):
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
    def empty_block_like(cls, block):
        block: ChromaRoll
        new_block = cls(np.zeros_like(block.array), block.origin,
                        block.tatum, block.step, block.time_nature, block.frequency_nature)
        return new_block

    @property
    def frequency_vector(self):
        return midi_numbers_to_chromas([i for i in range(12)])
