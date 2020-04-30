from __future__ import annotations

from MidiStructurer import *
from dataclasses import dataclass, field

from typing import List

COMPONENTS_PARAMETERS_TYPES = ["Melody", "AccompanimentChord", "AccompanimentArpeggiato", "Bass", "Drums"]


class ComponentTypeTracker(object):
    # Values
    Melody = 0
    AccompanimentChord = 0
    AccompanimentArpeggiato = 0
    Bass = 0
    Drums = 0

    def __getitem__(self, item):
        return eval("self.{}".format(item))

    def Increment(self, item):
        if item == "Melody":
            self.Melody += 1
        elif item == "AccompanimentChord":
            self.AccompanimentChord += 1
        elif item == "AccompanimentArpeggiato":
            self.AccompanimentArpeggiato += 1
        elif item == "Bass":
            self.Bass += 1
        elif item == "Drums":
            self.Drums += 1


@dataclass
class SectionComponent:
    Type: str = ""  # "Melody"
    Instrument: str = ""
    Bars: List = field(default_factory=list)
    DependentOnMelody: bool = False


"""
    def GenerateRhythm(self, generator, nbBars: int = 4):
        if not self.DependentOnMelody:
            self.Bars = [
                generator.GenerateRandomBar() for _ in nbBars
            ]
        else:
            self.Bars = [Bar() for _ in range(nbBars)]

    def GenerateNotes(self, generator, dependency=None):
        if self.DependentOnMelody:
            for i in range(len(self.Bars)):
                self.Bars[i] = generator.GenerateBar(dependency.Bars[i])
        else:
            allowedNotes = []
            prevNote = None
            for b in self.Bars:
                for se in b.SoundEvents:
                    se.Note = generator.ChooseNextNote(prevNote, allowedNotes)
                    prevNote = se.Note
"""


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

    def GenerateBars(self, rhythmGenerators, notesGenerators, allowedNotes, nbBarsPerSubsection: int = 4):
        for component in self.Components:
            component.GenerateRhythm(
                rhythmGenerators[component.Type],
                nbBarsPerSubsection
            )

        melodicComponent = list(filter(
            lambda x: x.Type == "Melodic",
            self.Components
        ))[0]

        for component in self.Components:
            component.GenerateNotes(
                notesGenerators[component.Type],
                dependency=melodicComponent
            )


# much better i think?


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


def GenerateRhythm(component: SectionComponent, generator, payload, nbBars) -> SectionComponent:
    if not component.DependentOnMelody:
        component.Bars = [
            generator.GenerateRandomBar(payload) for _ in range(nbBars)
        ]
        # component.Bars = generator.GenerateSectionFromPattern(payload)
    else:
        component.Bars = [Bar() for _ in range(nbBars)]


def GenerateNotes(component: SectionComponent, generator, allowedNotes, dependency=None) -> SectionComponent:
    if component.DependentOnMelody and dependency is not None:
        from copy import deepcopy as _deepcopy
        bars = []
        for b in dependency.Bars:
            # component.Bars[i] = generator.GenerateBar(component.Bars[i])
            refSE = _deepcopy(b.SoundEvents[0])
            chord = Chord([Interval(3, "Major"), Interval(5, "Perfect")])
            if len(b.SoundEvents) > 0:
                refNote = _deepcopy(b.SoundEvents[0].Note)
                notes, _ = chord(refNote)
                soundEvents = []
                for n in notes:
                    curr = _deepcopy(refSE)
                    curr.Note = n
                    soundEvents.append(curr)
            bars.append(
                Bar(SoundEvents=soundEvents)
            )
        component.Bars = bars

    else:
        from random import choice as _choice
        prevNote = _choice(allowedNotes)
        for b in component.Bars:
            for se in b.SoundEvents:
                se.Note = generator.ChooseNextNote(prevNote, allowedNotes)
                prevNote = se.Note
