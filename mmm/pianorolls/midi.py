import mido
from . import *
from .music import PianoRoll, TimeShift


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
