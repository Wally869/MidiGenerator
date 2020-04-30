from __future__ import annotations

from MidiStructurer import *
from dataclasses import dataclass, field

from typing import List

COMPONENTS_PARAMETERS_TYPES = ["Melody", "AccompanimentChord", "AccompanimentArpeggiato", "Bass", "Drums"]


@dataclass
class SectionComponent:
    Type: str = ""  # "Melody"
    Instrument: str = ""
    Bars: List = field(default_factory=list)
    DependentOnMelody: bool = False


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
                dependent = False
                if value == "AccompanimentChord":
                    dependent = True
                self.Components.append(
                    SectionComponent(
                        Type=value,
                        Instrument=instruments[value],
                        DependentOnMelody=dependent
                    )
                )
