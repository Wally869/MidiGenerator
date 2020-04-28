from __future__ import annotations

# NOTE: i also want possibility to transpose or augment/diminish?
"""
SAVING THIS stuff coz might be needed



@dataclass
class Identifier:
    Section: str = ""
    SectionId: int = -1
    TrackType: str = ""
    TrackTypeId: int = 0


class SongComponent(object):
    Master = None

    def __init__(self, identifier):
        self.Identifier = identifier
        self.Bars = []

    def GenerateBars(self, payload: Dict):
        # call master and make it generate stuff
        if self.Master is not None:
            self.Master.GenerateBars(payload)
            self.Bars = self.Master.Bars
        elif self.Bars != []:
            # already generated so pass
            pass
        else:
            # do stuff
            pass
            
class PoolComponents(object):
    def __init__(self, Components: List[SongComponent]):
        self.Components = Components

"""

from enum import Enum
from random import choice

from typing import Dict


class TrackType(Enum):
    Melody = 0
    Accompaniment = 1
    Bass = 2
    Drums = 3


class SectionType(Enum):
    Intro = "Intro"
    Chorus = "Chorus"
    Refrain = "Refrain"
    Outro = "Outro"


# song params, to apply some styling?
class SongParams(object):
    Style = ""
    NbBeats = 4
    # IntroComponents: maybe a param to handle case where
    # add components as it goes. Nah is a random somewhere i guess


sectionsNames = [
    "Intro", "Refrain", "Chorus", "Refrain", "Chorus", "Outro"
]

styleSong = "Samba"

# find overarching from style song? like samba has parent Latin
# overarching could serve as fallback is not found
# query db for relevant section specs
# conn.GetSectionSpecs(styleSong)
ssdTest = {
    "NbMelodies": [0, 1],
    "NbAccompaniments": [0, 2],
    "NbBass": [0, 2],
    "NbDrums": [0, 2]
}


# This is a wrapper around what's gotten from database
class SectionSpecsDrawer(object):
    def __init__(self, specsRanges):
        sr = specsRanges
        self.NbMelodies = sr["NbMelodies"]
        self.NbAccompaniments = sr["NbAccompaniments"]
        self.NbBass = sr["NbBass"]
        self.NbDrums = sr["NbDrums"]

    def __getitem__(self, item):
        return eval("self.{}".format(item))

    def DrawSpecs(self, excludeMelody=False, enforceMelody=False):
        # might be better to enforce desired behaviour from outside
        from random import randint as _randint
        drawnSpecs = [_randint(*self[field]) for field in ["NbMelodies", "NbAccompaniments", "NbBass", "NbDrums"]]
        if enforceMelody:
            drawnSpecs[0] = max(1, drawnSpecs[0])
        elif excludeMelody:
            drawnSpecs[0] = 0
        return drawnSpecs


# section specs into object for method
ssd = SectionSpecsDrawer(ssdTest)


# Then I need to link section to generators
# SO I can use pool of generators I guess :pepeyes:
# MAYBE ALSO a static class, that handles ID generation for section segments
# I would REALLY like to have subsections buddy. But later, for now gotta work for 1
class Section(object):
    # object referencing
    # Name = ""
    Type: SectionType = None
    ID = -1

    # Tracks Attributes
    NbMelody = 0
    NbAccompaniment = 0
    NbBass = 0
    NbDrums = 0

    # generation attributes
    Scale = None  # MidiStructurer.Components.ScaleSpecs? or List[Note]?
    RhythmGenerators = None
    NoteGenerators = None

    # Transformation attributes, if dependent on other section
    Master = None
    Transformations = None

    # The output stuff
    OutputTracks = []

    def __init__(self, sectionType: str):  # , sectionSpecs: SectionSpecsDrawer):
        self.Type = SectionType[sectionType]
        # self.DrawSpecs(sectionSpecs)

    def __str__(self):
        return "Section({}-{})".format(self.Type.name, self.ID)

    def __repr__(self):
        return self.__str__()

    def GetName(self):
        return self.__str__()

    def SetSpecs(self, sectionSpecs: Dict):
        # Directly set values from dict
        for key, value in enumerate(sectionSpecs):
            eval("self.{} = {}".format(key, value))

    def DrawSpecs(self, sectionSpecs: SectionSpecsDrawer):
        # draw random from SectionSpecsDrawer object
        self.NbMelody, self.NbAccompaniment, self.NbBass, self.NbDrums = sectionSpecs.DrawSpecs()

    def SetMaster(self, master):
        self.Master = master

    def CopyMaster(self):
        self = self.Master

    def SetTransformations(self, transformations):
        self.Transformations = transformations

    def ApplyTransformations(self):
        # I have master so be careful to return a new object and not modify master
        pass

    def SetRhythmGenerators(self, generators: Dict):
        fields = ["Melody", "Accompaniment", "Bass", "Drums"]
        selectedGenerators = {field: [] for field in fields}
        for field in fields:
            for _ in range(eval("self.Nb{}".format(field))):
                selectedGenerators[field].append(choice(generators[field]))
        self.RhythmGenerators = selectedGenerators


class SectionPool(object):
    # Pooling section objects
    # Basically emulating list with special methods
    def __init__(self):
        self.Sections = []

    @staticmethod
    def __str__():
        return "<class 'SectionPool'>"

    @classmethod
    def __repr__(cls):
        return cls.__str__()

    def __len__(self):
        return len(self.Sections)

    def __getitem__(self, item: int):
        return self.Sections[item]

    def AddSection(self, newSection: Section, findMaster: bool = False):
        # Get Id of new section
        similars = list(
            filter(
                lambda x: x.Type == newSection.Type,
                self.Sections
            )
        )
        newSection.ID = len(similars)

        if findMaster:
            if newSection.ID != 0:
                newSection.SetMaster(similars[0])

        self.Sections.append(newSection)

        # Now that I have pool of Sections, I can use presets from DB to set instruments and generators?

    def SetRhythmGenerators(self, generators: Dict):
        for section in self.Sections:
            section.SetRhythmGenerators(generators)


sections = [Section(s) for s in sectionsNames]
pool = SectionPool()
for s in sections:
    pool.AddSection(s)

generators = {"Melody": ["m0"], "Accompaniment": ["a0", "a1"], "Bass": ["b0"], "Drums": ["d0", "d1", "d2"]}
# problem: i need rhythm generator AND notes generator... :monkaHmm:
