import xml.etree.ElementTree as ET
from .music import *


class ComponentTree:
    def __init__(self, activations: Activations, *components: PianoRoll):
        self.activations: Activations = activations
        self.components: List[Union[ComponentTree, PianoRoll]] = list(components)

    def to_piano_roll(self) -> PianoRoll:
        result = PianoRoll()
        for component in self.components:
            if isinstance(component, ComponentTree):
                piano_roll = component.to_piano_roll()
            else:
                piano_roll = component
            result += self.activations + piano_roll
        return result


class ScoreTree:
    def __init__(self, file_path: Path):
        self.file_path = file_path

        self.name = None
        self.composer = None

        self.objects = {}

        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()

        for child in self.root:
            if child.tag == 'component-tree':
                self.component_tree = self.decode(child)
            else:
                self.decode(child)

    def to_piano_roll(self) -> PianoRoll:
        return self.component_tree.to_piano_roll()

    def decode(self, element: ET.Element):
        if element.tag == 'name':
            self.name = element.text
        elif element.tag == 'composer':
            self.composer = element.text
        elif element.tag == 'textures':
            for child in element:
                texture = self.decode(child)
                self.objects[child.attrib['id']] = texture
        elif element.tag == 'chords':
            for child in element:
                chord = self.decode(child)
                self.objects[child.attrib['id']] = chord
        elif element.tag == 'harmonies':
            for child in element:
                harmony = self.decode(child)
                self.objects[child.attrib['id']] = harmony
        elif element.tag == 'component-tree':
            activations: Activations = self.decode(element[0])
            components: List[Union[ComponentTree, PianoRoll]] = []
            for child in element[1:]:
                component = self.decode(child)
                components.append(component)
            return ComponentTree(activations, *components)
        elif element.tag == 'chord-texture':
            texture = self.decode(element[0])
            chord = self.decode(element[1])
            return ChordTexture(texture, chord)
        elif element.tag == 'harmonic-texture':
            texture = self.decode(element[0])
            harmony = self.decode(element[1])
            return HarmonicTexture(texture, harmony)
        elif element.tag == 'texture':
            if element[0].tag == 'id':
                return self.objects[element[0].text]
            else:
                rhythms = []
                for child in element:
                    rhythm = self.decode(child)
                    rhythms.append(rhythm)
                texture = Texture(*rhythms)
                try:
                    self.objects[element.attrib['id']] = texture
                except KeyError:
                    pass
                return texture
        elif element.tag == 'rhythm':
            hits = []
            for child in element:
                hit = self.decode(child)
                hits.append(hit)
            return Rhythm(*hits)
        elif element.tag == 'hit':
            start = self.decode(element[0])
            duration = self.decode(element[1])
            return Hit(start, duration)
        elif element.tag == 'start':
            if 'nat' not in element.attrib.keys():
                element.attrib['nat'] = 'shift'
            if element.attrib['nat'] == 'shift':
                return TimeShift(int(element.attrib['num']), int(element.attrib['den']))
            elif element.attrib['nat'] == 'point':
                return TimePoint(int(element.attrib['num']), int(element.attrib['den']))
            else:
                raise ValueError
        elif element.tag == 'duration':
            return TimeShift(int(element.attrib['num']), int(element.attrib['den']))
        elif element.tag == 'chord':
            if len(element) == 0:
                return Chord()
            else:
                if element[0].tag == 'id':
                    return self.objects[element[0].text]
                else:
                    if element[0].tag == 'degree':
                        degree = element[0].text
                        factors = [factor.attrib for factor in element[1:]]
                        return Chord.from_degree(degree, factors)
                    else:
                        pitches = []
                        for child in element:
                            pitches.append(self.decode(child))
                        return Chord(*pitches)
        elif element.tag == 'harmony':
            if element[0].tag == 'id':
                return self.objects[element[0].text]
            else:
                chords = []
                for child in element:
                    chords.append(self.decode(child))
                return Harmony(*chords)
        elif element.tag == 'pitch':
            return Frequency(element.attrib['value'])
        elif element.tag == 'activations':
            acts = []
            for child in element:
                time_frequency: TimeFrequency = self.decode(child)
                acts.append(time_frequency)
            activation_table = Activations(*acts)
            return activation_table
        elif element.tag == 'activation':
            time = self.decode(element[0])
            frequency = self.decode(element[1])
            return TimeFrequency(time, frequency)
        elif element.tag == 'time-frequency':
            time = self.decode(element[0])
            frequency = self.decode(element[1])
            return TimeFrequency(time, frequency)
        elif element.tag == 'time':
            if 'nat' not in element.attrib.keys():
                element.attrib['nat'] = 'shift'
            if element.attrib['nat'] == 'shift':
                return TimeShift(int(element.attrib['num']), int(element.attrib['den']))
            elif element.attrib['nat'] == 'point':
                return TimePoint(int(element.attrib['num']), int(element.attrib['den']))
            else:
                raise ValueError
        elif element.tag == 'frequency':
            if 'nat' not in element.attrib.keys():
                element.attrib['nat'] = 'shift'
            if element.attrib['nat'] == 'shift':
                return FrequencyShift(int(element.attrib['value']))
            elif element.attrib['nat'] == 'point':
                return FrequencyPoint(int(element.attrib['value']))
            else:
                raise ValueError
        else:
            raise NotImplementedError("Tag '%s' not implemented." % element.tag)
