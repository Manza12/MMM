import mido
import numpy as np
from typing import Optional
from pathlib import Path
from .music import PianoRoll, TimeShift, FrequencyShift, TimeFrequency, TimePoint, FrequencyPoint, TimeSeconds, \
    TimeSignature


def create_midi(piano_roll: PianoRoll, velocity: int = 64, tempo: int = 60, ticks_per_beat: Optional[int] = None,
                instrument: int = 0, time_end: int = 0) -> mido.MidiFile:
    assert piano_roll.frequency_nature == 'point', 'Piano roll frequencies must be point-like.'

    if ticks_per_beat is None:
        ratio = TimeShift(1, 4) / piano_roll.tatum
        if int(ratio) == float(ratio):
            ticks_per_beat = int(ratio)
            factor = 1
        else:
            ticks_per_beat = ratio.denominator
            factor = ratio.numerator
    else:
        factor = int(ticks_per_beat * piano_roll.tatum / TimeShift(1, 4))

    midi_file = mido.MidiFile(ticks_per_beat=ticks_per_beat)
    track = mido.MidiTrack()
    midi_file.tracks.append(track)

    # Tempo
    track.append(mido.MetaMessage(type='set_tempo', tempo=mido.bpm2tempo(tempo)))

    # Instrument
    track.append(mido.Message(type='program_change', program=instrument))

    # Array
    array = np.pad(piano_roll.array, ((0, 0), (0, 1)))

    # Note messages
    index_delta = 0
    on_array = np.zeros(array.shape[0], dtype=int)
    for t in range(array.shape[1]):
        delta = factor * (t - index_delta)

        for n in range(array.shape[0]):
            if array[n, t] == 2:
                if on_array[n] == 0:
                    track.append(mido.Message('note_on',
                                              note=piano_roll.extension.frequency.lower.value + n,
                                              velocity=velocity,
                                              time=delta))
                    on_array[n] = 1

                    if delta != 0:
                        index_delta = t
                        delta = 0
                else:
                    track.append(mido.Message('note_off',
                                              note=piano_roll.extension.frequency.lower.value + n,
                                              velocity=velocity,
                                              time=delta))
                    if delta != 0:
                        index_delta = t
                        delta = 0
                    track.append(mido.Message('note_on',
                                              note=piano_roll.extension.frequency.lower.value + n,
                                              velocity=velocity,
                                              time=delta))
            elif array[n, t] == 1:
                if on_array[n] == 0:
                    track.append(mido.Message('note_on',
                                              note=piano_roll.extension.frequency.lower.value + n,
                                              velocity=velocity,
                                              time=delta))
                    on_array[n] = 1

                    if delta != 0:
                        index_delta = t
                        delta = 0
                else:
                    pass
            elif array[n, t] == 0:
                if on_array[n] != 0:
                    track.append(mido.Message('note_off',
                                              note=piano_roll.extension.frequency.lower.value + n,
                                              velocity=velocity,
                                              time=delta))
                    on_array[n] = 0

                    if delta != 0:
                        index_delta = t
                        delta = 0

    # Turn off all notes
    delta = factor * (piano_roll.array.shape[1] - index_delta)
    for n in range(piano_roll.array.shape[0]):
        if on_array[n] == 1:
            track.append(mido.Message('note_off',
                                      note=int(piano_roll.extension.frequency.lower) + n,
                                      velocity=velocity,
                                      time=delta))
            if delta != 0:
                delta = 0

    track.append(mido.MetaMessage('end_of_track', time=time_end*ticks_per_beat))

    return midi_file


def read_midi(file_path: Path, keep_velocity: bool = False, time_signature: TimeSignature = TimeSignature(4, 4)):
    midi_file = mido.MidiFile(file_path)

    # Time and frequency extension
    min_midi_number = None
    max_midi_number = None
    max_time = None
    for track in midi_file.tracks:
        current_time = 0
        for msg in track:
            if msg.type == 'note_on':
                if min_midi_number is None:
                    min_midi_number = msg.note
                    max_midi_number = msg.note
                else:
                    min_midi_number = min(min_midi_number, msg.note)
                    max_midi_number = max(max_midi_number, msg.note)
            current_time += msg.time
        if max_time is None:
            max_time = current_time
        else:
            max_time = max(max_time, current_time)
    ambitus = max_midi_number - min_midi_number + 1

    # Create array
    if keep_velocity:
        shape = (2, len(midi_file.tracks), ambitus, max_time)
    else:
        shape = (len(midi_file.tracks), ambitus, max_time)

    array = np.zeros(shape, dtype=np.uint8)

    # Fill array
    on_notes = np.zeros(ambitus, dtype=bool)
    velocities = np.zeros(ambitus, dtype=np.uint8)
    for t, track in enumerate(midi_file.tracks):
        current_time = 0
        for msg in track:
            if msg.time != 0:
                if keep_velocity:
                    array[0, t, on_notes, current_time: current_time + msg.time] = \
                        np.maximum(array[0, t, on_notes, current_time: current_time + msg.time], 1)
                    array[1, t, :, current_time: current_time + msg.time] = np.expand_dims(velocities, 1)
                else:
                    array[t, on_notes, current_time: current_time + msg.time] = \
                        np.maximum(array[t, on_notes, current_time: current_time + msg.time], 1)

            if msg.type == 'note_on' and msg.velocity == 0:
                msg_type = 'note_off'
            else:
                msg_type = msg.type

            if msg_type == 'note_on':
                on_notes[msg.note - min_midi_number] = True
                velocities[msg.note - min_midi_number] = msg.velocity

                if keep_velocity:
                    array[0, t, msg.note - min_midi_number, current_time + msg.time] = 2
                    array[1, t, msg.note - min_midi_number, current_time + msg.time] = msg.velocity
                else:
                    array[t, msg.note - min_midi_number, current_time + msg.time] = 2
            elif msg_type == 'note_off':
                on_notes[msg.note - min_midi_number] = False
                velocities[msg.note - min_midi_number] = 0

            current_time += msg.time

    tatum = TimeShift(1, 4 * midi_file.ticks_per_beat)
    step = FrequencyShift(1)
    # dynamics = {v: v for v in range(0, 128)} if keep_velocity else None
    piano_roll = PianoRoll(np.max(array, axis=0), origin=TimeFrequency(TimePoint(0, time_signature=time_signature),
                                                                       FrequencyPoint(min_midi_number)),
                           tatum=tatum, step=step)
    return piano_roll


def read_midi_seconds(file_path: Path, bins_per_second=1000):
    midi_file = mido.MidiFile(file_path)
    ticks_per_beat = midi_file.ticks_per_beat
    microseconds_per_tick = 500000

    durations_seconds = []
    min_note = None
    max_note = None
    for track in midi_file.tracks:
        current_time_seconds = 0.
        for m in track:
            if m.type == 'set_tempo':
                microseconds_per_tick = m.tempo
            current_time_seconds += m.time * microseconds_per_tick / ticks_per_beat / 1000000
            try:
                note = m.note
                if min_note is None:
                    min_note = note
                elif note < min_note:
                    min_note = note

                if max_note is None:
                    max_note = note
                elif note > max_note:
                    max_note = note
            except AttributeError:
                pass

        durations_seconds.append(current_time_seconds)
    duration_second = max(durations_seconds)

    piano_rolls = []
    for track in midi_file.tracks:
        current_time_seconds = 0.
        origin_freq = - min_note
        array = np.zeros((max_note - min_note + 1, int(duration_second * bins_per_second)), dtype=np.uint8)
        for m in track:
            time_sec = m.time * microseconds_per_tick / ticks_per_beat / 1000000
            t_sec = current_time_seconds + time_sec
            t = int(t_sec * bins_per_second)
            if m.type == 'note_on' and m.velocity > 0:
                if origin_freq is None:
                    origin_freq = - m.note
                    f = m.note + origin_freq
                elif m.note - origin_freq < 0:
                    origin_freq = - m.note
                    f = m.note + origin_freq
                else:
                    f = m.note + origin_freq

                if array is None:
                    array = np.zeros((1, 1), dtype=np.uint8)
                elif f >= array.shape[0]:
                    array = np.pad(array, ((0, f - array.shape[0] + 1), (0, 0)), 'constant')

                if t >= array.shape[1]:
                    array = np.pad(array, ((0, 0), (0, t - array.shape[1] + 1)), 'constant')

                array[f, t] = 2
            elif m.type == 'note_off' or (m.type == 'note_on' and m.velocity == 0):
                if t >= array.shape[1]:
                    array = np.pad(array, ((0, 0), (0, t - array.shape[1] + 1)), 'constant')

                delta_t = 0
                while True:
                    f = m.note + origin_freq

                    if array[f, t - delta_t] == 2:
                        array[f, t - delta_t + 1: t] = 1
                        break
                    else:
                        delta_t += 1
            elif m.type == 'set_tempo':
                microseconds_per_tick = m.tempo

            current_time_seconds += time_sec

        tatum = TimeShift(1, bins_per_second)
        step = FrequencyShift(1)
        piano_roll = PianoRoll(array, origin=TimeFrequency(TimeSeconds(0.), FrequencyPoint(min_note)),
                               tatum=tatum, step=step)
        piano_rolls.append(piano_roll)
    return piano_rolls
