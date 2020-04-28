from __future__ import annotations

from dataclasses import dataclass, field

from typing import List

COMPONENTS_PARAMETERS_TYPES = ["Melody", "AccompanimentChord", "AccompanimentArpeggiato", "Bass", "Drums"]


class ComponentTypeTracker(object):
    # Values
    Melody = 0
    AccompanimentChord = 1
    AccompanimentArpeggiato = 2
    Bass = 3
    Drums = 4

    def __getitem__(self, item):
        return eval("self.{}".format(item))

    def Increment(self, item):
        if item == "Melody":
            self.Melody += 1
        elif item == "Accompaniment":
            self.Accompaniment += 1
        elif item == "Bass":
            self.Bass += 1
        elif item == "Drums":
            self.Drums += 1


@dataclass
class SectionComponent:
    Type: str = ""  # "Melody"
    Instrument: str = ""
    Bars: List = field(default_factory=list)


class Section(object):
    # get name and id out of section specs?
    def __init__(self, Name: str, idSection: int, sectionSpecs: SectionSpecs, NbSubSections: int = 1):
        self.Name = Name
        self.ID = idSection
        self.Scale = sectionSpecs.Scale
        self.NbSubSections = NbSubSections
        self.Components = []
        self.GenerateComponents(sectionSpecs)

    def __str__(self):
        return "Section({}-{})".format(self.Name, self.ID)

    def __repr__(self):
        return self.__str__()

    def GenerateComponents(self, sectionSpecs: SectionSpecs):
        instruments = sectionSpecs.Instruments
        componentsParameters = sectionSpecs.ComponentsParameters
        for idType, value in enumerate(COMPONENTS_PARAMETERS_TYPES):
            for _ in range(componentsParameters[idType]):
                self.Components.append(
                    SectionComponent(
                        Type=value,
                        Instrument=instruments[value]
                    )
                )

    def GenerateBars(self, rhythmGenerators, noteGenerators, nbBarsPerSubsection: int = 4):
        pass


# much better i think?
"""
@dataclass
class SectionSpecs:
    Scale = None
    ComponentsParameters: List[int] = None  # field(default_factory=[1, 1, 0, 1, 1])
    Instruments = {
        field: "Acoustic Grand Piano" for field in COMPONENTS_PARAMETERS_TYPES
    }
"""

dfltInstruments = {
    field: "Acoustic Grand Piano" for field in COMPONENTS_PARAMETERS_TYPES
}


class SectionSpecs(object):
    def __init__(self, Scale=None,
                 ComponentsParameters=[1, 1, 0, 1, 1],
                 Instruments=dfltInstruments):
        self.Scale = Scale
        self.ComponentsParameters = ComponentsParameters
        self.Instruments = Instruments

    def __str__(self):
        return "<class 'SectionSpecs'>"

    def __repr__(self):
        return self.__str__()


specs = SectionSpecs(
    ComponentsParameters=[1, 1, 0, 1, 1]
)

intro = Section("Intro", 0, specs, 2)
