from . import *
import xml.etree.ElementTree as ET

from .music import TimeShift
from .utils import pitch_to_note_number, beat_unit_to_tuple


class XMLScore:
    def __init__(self):
        self.part_list: XMLPartList = XMLPartList()
        self.work: Optional[XMLWork] = None
        self.identification: Optional[XMLIdentification] = None
        self.movement_number: Optional[Union[int, str]] = None
        self.movement_title: Optional[str] = None

    @classmethod
    def read_score_partwise(cls, root):
        score = cls()

        for child in root:
            if child.tag == 'part-list':
                score.part_list = XMLPartList.read_part_list(child)
            elif child.tag == 'part':
                score.part_list[child.attrib['id']] = XMLPart.read_part(child, score)
            elif child.tag == 'work':
                score.work = XMLWork.read_work(child)
            elif child.tag == 'identification':
                score.identification = XMLIdentification.read_identification(child)
            elif child.tag == 'movement-number':
                score.movement_number = XMLMovementNumber.read_movement_number(child)
            elif child.tag == 'movement-title':
                score.movement_title = XMLMovementTitle.read_movement_title(child)
            elif child.tag == 'defaults':
                pass
            elif child.tag == 'credit':
                pass
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, root.tag))

        return score


class XMLMovementNumber:
    def __init__(self, number: Union[str, int]):
        self.number: Union[str, int] = number

    @classmethod
    def read_movement_number(cls, element: ET.Element):
        movement_number = cls(element.text)

        return movement_number


class XMLMovementTitle:
    def __init__(self, title: str):
        self.title: str = title

    @classmethod
    def read_movement_title(cls, element: ET.Element):
        movement_title = cls(element.text)

        return movement_title


class XMLPartList(dict):
    def __init__(self):
        super().__init__()

    @classmethod
    def read_part_list(cls, element: ET.Element):
        part_list = cls()

        for child in element:
            if child.tag == 'score-part':
                identifier = child.attrib['id']
                part_list[identifier] = XMLPart(identifier)
            elif child.tag == 'part-group':
                pass
                # raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))

        return part_list


class XMLPart:
    def __init__(self, identifier: str):
        self.id: str = identifier
        self.measures: list = []

    @classmethod
    def read_part(cls, element: ET.Element, score: XMLScore):
        part = score.part_list[element.attrib['id']]

        for child in element:
            if child.tag == 'measure':
                part.measures.append(XMLMeasure.read_measure(child))
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))

        return part


class XMLMeasure:
    def __init__(self):
        self.attributes: Optional[XMLAttributes] = None
        self.notes: list = []
        self.direction: Optional[List[XMLDirection]] = None

        self.measure_number: Optional[int] = None

    @classmethod
    def read_measure(cls, element: ET.Element):
        measure = cls()

        try:
            number = element.attrib['number']
            measure.measure_number = number
        except KeyError:
            pass

        for child in element:
            if child.tag == 'attributes':
                if measure.attributes is None:
                    measure.attributes = XMLAttributes.read_attributes(child)
                else:
                    measure.attributes.add_attribute(child)
            elif child.tag == 'note':
                measure.notes.append(XMLNote.read_note(child))
            elif child.tag == 'direction':
                if not measure.direction:
                    measure.direction = []
                measure.direction.append(XMLDirection.read_direction(child))
            elif child.tag == 'barline':
                pass
            elif child.tag == 'print':
                pass
            elif child.tag == 'backup':
                measure.notes.append(XMLBackup.read_backup(child))
            elif child.tag == 'forward':
                pass
            elif child.tag == 'harmony':
                pass
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))

        return measure


class XMLBackup:
    def __init__(self):
        self.duration: Optional[int] = None

    @classmethod
    def read_backup(cls, element: ET.Element):
        backup = cls()

        for child in element:
            if child.tag == 'duration':
                backup.duration = int(child.text)
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))

        return backup


class XMLAttributes:
    def __init__(self):
        self.divisions: Optional[int] = None
        self.key: Optional[XMLKey] = None
        self.time: Optional[XMLTime] = None
        self.clef: Optional[XMLClef] = None
        self.staves: Optional[int] = None

    @classmethod
    def read_attributes(cls, element: ET.Element):
        attributes = cls()
        attributes.add_attribute(element)
        return attributes

    def add_attribute(self, element: ET.Element):
        for child in element:
            if child.tag == 'divisions':
                self.divisions = int(child.text)
            elif child.tag == 'key':
                self.key = XMLKey.read_key(child)
            elif child.tag == 'time':
                self.time = XMLTime.read_time(child)
            elif child.tag == 'clef':
                self.clef = XMLClef.read_clef(child)
            elif child.tag == 'staves':
                self.staves = int(child.text)
            elif child.tag == 'staff-details':
                pass
            elif child.tag == 'transpose':
                pass
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))


class XMLKey:
    def __init__(self):
        self.fifths: Optional[int] = None
        self.mode: Optional[str] = None

    @classmethod
    def read_key(cls, element: ET.Element):
        key = cls()

        for child in element:
            if child.tag == 'fifths':
                key.fifths = int(child.text)
            elif child.tag == 'mode':
                key.mode = child.text
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))

        return key


class XMLTime:
    def __init__(self):
        self.beats: Optional[int] = None
        self.beat_type: Optional[int] = None

    @classmethod
    def read_time(cls, element: ET.Element):
        time = cls()

        for child in element:
            if child.tag == 'beats':
                time.beats = int(child.text)
            elif child.tag == 'beat-type':
                time.beat_type = int(child.text)
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))

        return time


class XMLClef:
    def __init__(self):
        self.sign: Optional[str] = None
        self.line: Optional[int] = None
        self.clef_octave_change: int = 0

    @classmethod
    def read_clef(cls, element: ET.Element):
        clef = cls()

        for child in element:
            if child.tag == 'sign':
                clef.sign = child.text
            elif child.tag == 'line':
                clef.line = int(child.text)
            elif child.tag == 'clef-octave-change':
                clef.clef_octave_change = int(child.text)
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))

        return clef


class XMLTimeModification:
    def __init__(self):
        self.actual_notes: Optional[int] = None
        self.normal_notes: Optional[int] = None

    @classmethod
    def read(cls, element: ET.Element):
        time_modification = cls()

        for child in element:
            if child.tag == 'actual-notes':
                time_modification.actual_notes = int(child.text)
            elif child.tag == 'normal-notes':
                time_modification.normal_notes = int(child.text)
            elif child.tag == 'normal-type':
                pass
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))

        return time_modification


class XMLNote:
    def __init__(self):
        self.pitch: Optional[XMLPitch] = None
        self.duration: Optional[int] = None
        self.type: Optional[str] = None
        self.voice: Optional[int] = None
        self.notations: Optional[XMLNotations] = None
        self.dot: bool = False
        self.rest: bool = False
        self.tie: Optional[List[str]] = None
        self.chord: bool = False
        self.staff: Optional[int] = None
        self.time_modification: Optional[XMLTimeModification] = None
        self.dynamic: str = ''

    @classmethod
    def read_note(cls, element: ET.Element):
        note = cls()

        note.dynamic = str(XMLDynamics.current_dynamic)

        for child in element:
            if child.tag == 'pitch':
                note.pitch = XMLPitch.read_pitch(child)
            elif child.tag == 'duration':
                note.duration = int(child.text)
            elif child.tag == 'type':
                note.type = child.text
            elif child.tag == 'voice':
                note.voice = int(child.text)
            elif child.tag == 'notations':
                note.notations = XMLNotations.read_notations(child)
            elif child.tag == 'dot':
                note.dot = True
            elif child.tag == 'rest':
                note.rest = True
            elif child.tag == 'tie':
                if note.tie is None:
                    note.tie = [child.attrib['type']]
                else:
                    note.tie.append(child.attrib['type'])
            elif child.tag == 'time-modification':
                note.time_modification = XMLTimeModification.read(child)
            elif child.tag == 'chord':
                note.chord = True
            elif child.tag == 'staff':
                note.staff = int(child.text)
            elif child.tag == 'stem':
                pass
            elif child.tag == 'beam':
                pass
            elif child.tag == 'accidental':
                pass
            elif child.tag == 'lyric':
                pass
            elif child.tag == 'grace':
                pass
            elif child.tag == 'cue':
                pass
            elif child.tag == 'instrument':
                pass
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))

        return note

    def to_duration_wholes(self):
        num, dem = beat_unit_to_tuple(self.type, self.dot)
        if self.time_modification is not None:
            num *= self.time_modification.normal_notes
            dem *= self.time_modification.actual_notes
        return TimeShift(num, dem)


class XMLPitch:
    def __init__(self):
        self.step: Optional[str] = None
        self.octave: Optional[int] = None
        self.alter: Optional[int] = None

    @classmethod
    def read_pitch(cls, element: ET.Element):
        pitch = cls()

        for child in element:
            if child.tag == 'step':
                pitch.step = child.text
            elif child.tag == 'octave':
                pitch.octave = int(child.text)
            elif child.tag == 'alter':
                pitch.alter = int(child.text)
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))

        return pitch

    def note_number(self) -> int:
        return pitch_to_note_number(self.step, self.octave, self.alter)


class XMLDirection:
    def __init__(self):
        self.direction_type: XMLDirectionType = XMLDirectionType()
        self.voice: Optional[int] = None
        self.staff: Optional[int] = None

    @classmethod
    def read_direction(cls, element: ET.Element):
        direction = cls()

        for child in element:
            if child.tag == 'direction-type':
                direction.direction_type = XMLDirectionType.read_direction_type(child)
            elif child.tag == 'voice':
                direction.voice = int(child.text)
            elif child.tag == 'staff':
                direction.staff = int(child.text)
            elif child.tag == 'sound':
                pass
            elif child.tag == 'offset':
                pass
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))

        return direction


class XMLDirectionType:
    @classmethod
    def read_direction_type(cls, element: ET.Element):
        direction_type = cls()

        for child in element:
            if child.tag == 'metronome':
                direction_type = XMLMetronome.read_metronome(child)
            elif child.tag == 'dynamics':
                direction_type = XMLDynamics.read_dynamics(child)
            elif child.tag == 'words':
                pass
            elif child.tag == 'pedal':
                pass
            elif child.tag == 'wedge':
                pass
            elif child.tag == 'other-direction':
                pass
            elif child.tag == 'segno':
                pass
            elif child.tag == 'octave-shift':
                pass
            elif child.tag == 'dashes':
                pass
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))

        return direction_type


class XMLDynamics(XMLDirectionType):
    current_dynamic = None

    def __init__(self):
        self.value: str = ''

    @classmethod
    def read_dynamics(cls, element: ET.Element):
        dynamic = cls()
        if len(element) != 1:
            warnings.warn('Dynamics element has more than one child')
            return dynamic

        child = element[0]
        dynamic.value = child.tag

        XMLDynamics.current_dynamic = dynamic.value

        return dynamic


class XMLMetronome(XMLDirectionType):
    def __init__(self):
        self.beat_unit: str = ''
        self.beat_unit_dot: bool = False
        self.per_minute: Union[str, int] = ''

    @classmethod
    def read_metronome(cls, element: ET.Element):
        metronome = cls()

        for child in element:
            if child.tag == 'beat-unit':
                metronome.beat_unit = child.text
            elif child.tag == 'beat-unit-dot':
                metronome.beat_unit_dot = True
            elif child.tag == 'per-minute':
                try:
                    metronome.per_minute = int(child.text)
                except ValueError:
                    metronome.per_minute = child.text
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))

        return metronome


class XMLWork:
    def __init__(self):
        self.work_title: Optional[str] = None

    @classmethod
    def read_work(cls, element: ET.Element):
        work = cls()

        for child in element:
            if child.tag == 'work-title':
                work.work_title = child.text
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))

        return work


class XMLIdentification:
    def __init__(self):
        self.composer: Optional[str] = None

    @classmethod
    def read_identification(cls, element: ET.Element):
        identification = cls()

        for child in element:
            if child.tag == 'creator':
                if child.attrib['type'] == 'composer':
                    identification.composer = child.text
            elif child.tag == 'rights':
                pass
            elif child.tag == 'encoding':
                pass
            elif child.tag == 'source':
                pass
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))

        return identification


class XMLNotations:
    def __init__(self):
        self.fermata: Optional[str] = None
        self.tied: Optional[List[str]] = None

    @classmethod
    def read_notations(cls, element: ET.Element):
        notations = cls()

        for child in element:
            if child.tag == 'fermata':
                notations.fermata = child.text
            elif child.tag == 'tied':
                if notations.tied is None:
                    notations.tied = [child.attrib['type']]
                else:
                    notations.tied.append(child.attrib['type'])
            elif child.tag == 'slur':
                pass
            elif child.tag == 'tuplet':
                pass
            elif child.tag == 'articulations':
                pass
            elif child.tag == 'ornaments':
                pass
            elif child.tag == 'arpeggiate':
                pass
            elif child.tag == 'technical':
                pass
            elif child.tag == 'non-arpeggiate':
                pass
            else:
                raise ValueError('Tag %s in %s not implemented' % (child.tag, element.tag))

        return notations
