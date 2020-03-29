
from MidiStructurer.Components import *
from MidiStructurer.ScalesUtils import TranslateNote

from random import random
from copy import deepcopy

from dataclasses import dataclass, field
from typing import Dict, List

"""
Need to input specs
generator specs class?
"""

@dataclass
class TrackGeneratorSpecs:
    RythmicModelOrPreset: Dict = field(default_factory=dict)
    MelodicModelOrPreset: Dict = field(default_factory=dict)
    SpecsName: str = ""
    TrackName: str = ""
    TrackType: str = "Melody"

"""
Comping:
- give a track to comp
- above or below ref note
- all notes, or probabilistic, or from preset (from preset: maybe another time)
- degrees diff:3, 5, 7

comping scheme:
{method, params}

"""
def GenerateCompingTrack(refTrack: Track,
                         scales: List[Scale],
                         refOctave: int = 5,
                          aboveOrBelow: str = "below",
                          compingScheme: Dict = {"Scheme": "Probabilistic", "Parameters": {"Threshold": 0.5}},
                          degreesDiff: List[int] = [4, 7]):
    outBars = []
    deltaDegrees = 1
    if aboveOrBelow == "below":
        deltaDegrees = -1

    #refOctave = refTrack.Bars[0].Notes[0].Octave
    for id_bar in range(len(refTrack.Bars)):
        bar = refTrack.Bars[id_bar]
        currBar = Bar()
        for n in bar.Notes:
            appendIt = True
            if compingScheme["Scheme"] == "Probabilistic":
                if random() > compingScheme["Parameters"]["Threshold"]:
                    appendIt = False

            if appendIt:
                for d in degreesDiff:
                    delto = 1
                    if aboveOrBelow == "below":
                        delto = -1

                    if scales[id_bar].Mode == "Minor":
                        degreesDiff = [4, 7]

                    currNote = Note()
                    currNote.Beat = n.Beat
                    currNote.Duration = n.Duration
                    #currNote.Octave = refOctave + delto
                    currNote.NoteName = scales[id_bar].RefNote


                    #currNote = deepcopy(n)
                    currNote = TranslateNote(currNote, d)
                    currNote.Octave = refOctave + delto
                    #print((n, currNote))
                    #print()

                    currBar.Notes.append(
                        currNote
                    )
        outBars.append(currBar)

    outTrack = Track(
        Bars=outBars
    )

    return outTrack

# Map sounds to beats
def GenerateDrumsTrack(rythmGenerator, drumsModel, targetLen):
    pass

