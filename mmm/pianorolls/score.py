from .music import FrequencyPoint, Time, TimePoint, FrequencyExtension, TimeExtension, PianoRoll, \
    TimeFrequency, FrequencyShift, TimeSignature
from .utils import duration_whole_to_unicode, gcd
from .musicxml import *


class Note:
    def __init__(self, note_number: Optional[int], start: Time, duration: Time):
        assert type(self) is not Note, 'Note is an abstract class.'
        if note_number is None:
            self.frequency = None
        else:
            self.frequency = FrequencyPoint(note_number)

        self.start = start
        self.duration = duration

    @property
    def end(self):
        return self.start + self.duration

    def __str__(self):
        duration_str = str(duration_whole_to_unicode(self.duration.value))
        return str(self.frequency) + ' - ' + str(self.start) + ' - ' + duration_str


class NoteWhole(Note):
    def __init__(self, note_number: Optional[int], start: TimePoint, duration: TimeShift, dynamic: str = ''):
        Note.__init__(self, note_number, start, duration)
        self.dynamic = dynamic
        self.tied = False


class TempoMark:
    def __init__(self, note_value: TimeShift, per_minute: Union[int, float]):
        self.note_value: TimeShift = note_value
        self.per_minute: Union[int, float] = per_minute

    def __str__(self):
        return str(self.note_value) + ' = ' + str(self.per_minute)


class Score:
    def __init__(self):
        assert not type(self) == Score, 'Score is an abstract class'

        self.title: Optional[str] = None
        self.composer: Optional[str] = None

        self.notes: List[NoteWhole] = []

        self.__time_extension = None
        self.__frequency_extension = None
        self.__tatum = None

    @property
    def frequency_extension(self):
        if self.__frequency_extension is None:
            self.__frequency_extension = self.compute_frequency_extension()
        return self.__frequency_extension

    def compute_frequency_extension(self):
        if len(self.notes) == 0:
            return None
        else:
            minimum = self.notes[0].frequency
            maximum = self.notes[0].frequency
            for note in self.notes:
                if note.frequency is not None:
                    if minimum is None:
                        minimum = note.frequency
                    else:
                        minimum = min(minimum, note.frequency)

                    if maximum is None:
                        maximum = note.frequency
                    else:
                        maximum = max(maximum, note.frequency)
            return FrequencyExtension(minimum, maximum)

    @property
    def time_extension(self):
        if self.__time_extension is None:
            self.__time_extension = self.compute_time_extension()
        return self.__time_extension

    def compute_time_extension(self):
        if len(self.notes) == 0:
            return None
        else:
            minimum = self.notes[0].start
            maximum = self.notes[0].end
            for note in self.notes:
                minimum = min(minimum, note.start)
                maximum = max(maximum, note.end)
            return TimeExtension(minimum, maximum)

    @property
    def tatum(self):
        if self.__tatum is None:
            self.__tatum = self.compute_tatum()
        return self.__tatum

    def compute_tatum(self):
        if len(self.notes) == 0:
            return None
        else:
            tatum = gcd(self.notes[0].start.value, self.notes[0].end.value)
            for note in self.notes:
                tatum = gcd(tatum, note.start.value, note.end.value)
            return TimeShift(tatum)

    @property
    def duration(self):
        return self.time_extension.duration

    @property
    def range(self):
        return self.frequency_extension.range


class ScoreWhole(Score):
    def __init__(self, file_path: Path):
        super().__init__()
        self.parts: Dict[str, ...] = {}
        self.tempo_marks: Optional[Dict] = None
        self.time_signatures: Optional[Dict] = None

        self.parse_xml(file_path)

    def parse_xml(self, file_path: Path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        if root.tag == 'score-partwise':
            score_xml = XMLScore.read_score_partwise(root)
        else:
            raise NotImplementedError('Only partwise scores implemented currently.')

        # Get title
        try:
            self.title = score_xml.work.work_title
        except AttributeError:
            pass

        # Get composer
        try:
            self.composer = score_xml.identification.composer
        except AttributeError:
            pass

        for key in score_xml.part_list.keys():
            part = score_xml.part_list[key]
            self.parts[key] = []

            current_point = TimePoint(0, time_signature=TimeSignature(12, 8))
            divisions = None
            for measure in part.measures:
                measure: XMLMeasure

                # Get Measure Attributes
                if measure.attributes is not None:
                    # Get Divisions
                    if measure.attributes.divisions is not None:
                        divisions = measure.attributes.divisions

                    # Get Time signature
                    if measure.attributes.time is not None:
                        time_signature = measure.attributes.time

                        # Add Time Signature to score
                        if time_signature is not None:
                            if self.time_signatures is None:
                                self.time_signatures = {}
                            k = str(current_point)
                            self.time_signatures[k] = TimeSignature(time_signature.beats, time_signature.beat_type)
                            current_point = TimePoint(current_point.value, time_signature=self.time_signatures[k])

                # Get Measure Directions
                if measure.direction:
                    for d in measure.direction:
                        if isinstance(d.direction_type, XMLMetronome):
                            metronome = d.direction_type

                            if self.tempo_marks is None:
                                self.tempo_marks = {}

                            note_value = TimeShift(*beat_unit_to_tuple(metronome.beat_unit, metronome.beat_unit_dot))
                            self.tempo_marks[str(current_point)] = TempoMark(note_value, metronome.per_minute)

                for note_xml in measure.notes:
                    if isinstance(note_xml, XMLNote):
                        if note_xml.chord:
                            current_point -= note_xml.to_duration_wholes()

                        if note_xml.rest:
                            note_number = None
                        else:
                            note_number = note_xml.pitch.note_number()
                        if note_xml.duration is None:
                            warnings.warn('Ornement has been skiped.')
                        else:
                            if note_xml.rest and note_xml.type == 'whole':
                                duration_wholes = TimeShift(note_xml.duration // divisions) / 4
                            else:
                                duration_wholes = note_xml.to_duration_wholes()
                            note = NoteWhole(note_number, current_point, duration_wholes, note_xml.dynamic)

                            note.voice = note_xml.voice

                            if note_xml.tie is not None:
                                if 'stop' in note_xml.tie:
                                    note.tied = True

                            self.notes.append(note)
                            self.parts[key].append(note)

                            current_point += duration_wholes
                    elif isinstance(note_xml, XMLBackup):
                        duration_wholes = TimeShift(note_xml.duration // divisions) / 4
                        current_point = current_point - duration_wholes
                    else:
                        raise ValueError('Variable note_xml should be a XMLNote.')

    def to_piano_roll(self, part_ids: Union[str, List[str]] = 'all', dynamics=False) -> PianoRoll:
        if dynamics:
            raise NotImplementedError('Dynamics is not supported yet.')

        tatum = self.tatum
        step = FrequencyShift(1)
        origin = TimeFrequency(self.time_extension.start, self.frequency_extension.lower)

        array_shape = (self.range.value + 1, self.duration // self.tatum)
        array = np.zeros(array_shape, dtype=np.uint8)

        for part_id in self.parts.keys():
            if part_ids != 'all':
                if part_id not in part_ids:
                    continue

            notes = self.parts[part_id]
            for note in notes:
                note: NoteWhole
                if note.frequency is not None:
                    k = (note.frequency - self.frequency_extension.lower) // step
                    n_0 = (note.start - self.time_extension.start) // tatum
                    n_1 = (note.end - self.time_extension.start) // tatum

                    array[k, n_0: n_1] = np.maximum(array[k, n_0: n_1], np.ones_like(array[k, n_0: n_1]))
                    if not note.tied:
                        array[k, n_0] = 2

        piano_roll = PianoRoll(array, origin, tatum, step)
        return piano_roll
