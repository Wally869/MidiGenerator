from __future__ import annotations

from MusiStrata.Components import Bar, GenerateBarFromRhythmicPreset
from utils import ComputeCumulativeProbabilitiesFromDict

from random import random, choice
from math import ceil
from copy import deepcopy

from typing import List, Dict, Union, Tuple


class RhythmicGeneratorInterface(object):
    def __str__(self):
        return "<class 'RhythmicGeneratorInterface'>"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def GenerateBreak():
        # Use this to get an empty bar, could serve as break in between generated segments
        return Bar()

    @staticmethod
    def GeneratePattern(nbBars: int) -> Tuple[int, List[int]]:
        # how many different bars? use square root of nb bars
        nbSegments = ceil(nbBars ** 0.5)
        return nbSegments, [choice(range(nbSegments)) for _ in range(nbBars)]


class RhythmicPreset(RhythmicGeneratorInterface):
    """
    Expecting a Dict following this example:
    {
        "Name": "TestRhythmicPreset1",
        "Tags": ["Test"],
        "Beats": 4,
        "MainPreset": [
            {
                "beat": 0.0,
                "duration": 1.0
            },
            {
                "beat": 2.0,
                "duration": 1.0
            },
            {
                "beat": 3.0,
                "duration": 0.5
            },
            {
                "beat": 3.5,
                "duration": 0.5
            }
        ],
        "Variants": []
    }

    """
    NbBeats = 4

    def __init__(self, parameters: Dict):
        self.NbBeats = parameters["NbBeats"]
        self.Presets = [parameters["MainPreset"]] + parameters["VariantsPreset"]

    def __str__(self):
        return "<class 'RhythmicPreset'>"

    def __repr__(self):
        return self.__str__()

    # override generatepattern
    def GeneratePattern(self, nbBars: int) -> List[int]:
        return [choice(range(len(self.Presets))) for _ in range(nbBars)]

    def __call__(self, nbBars: int, nbBeats: float = 4.0, pattern: List[int] = [], **kwargs):
        if pattern == []:
            pattern = self.GeneratePattern(nbBars)
        return [
            GenerateBarFromRhythmicPreset(
                self.Presets[idPreset]
            ) for idPreset in pattern
        ]


class RhythmicModel(RhythmicGeneratorInterface):
    """
    Expecting a Dict as input with fields:
        - Name: str
        - Tags: List[str]
        - SilenceChance: float (0.0 <= value <= 1.0)
        - Notes: Dict(str: float)
        - Silences: Dict(str: float

    Tags is not mandatory, will be used in DB queries when creating generator parameters
    """

    # From Input Parameters
    Name = ""
    SilenceChance = 0.0

    def __init__(self, parameters: Dict):
        # Tracking Parameters
        self.Name = parameters["Name"]
        self.SilenceChance = parameters["SilenceChance"]

        self.NotesDurations = []
        self.NotesProbabilities = []
        self.SilencesDurations = []
        self.SilencesProbabilities = []

        self.CheckAndSetProbabilities(parameters)

    def __str__(self):
        return "RhythmicModel({})".format(self.Name)

    def __repr__(self):
        return self.__str__()

    def __call__(self, nbBars: int, nbBeats: float = 4.0, pattern: List[int] = [], **kwargs):
        if pattern == []:
            nbSegments, pattern = self.GeneratePattern(nbBars)
        else:
            nbSegments = max(pattern) + 1

        generatedSegments = [
            self.GenerateBar(nbBeats) for _ in range(nbSegments)
        ]

        return [generatedSegments[idPattern] for idPattern in pattern]

    def CheckAndSetProbabilities(self, parameters: Dict):
        vals = []
        for k in ["Notes", "Silences"]:
            vals += ComputeCumulativeProbabilitiesFromDict(
                parameters[k]
            )

        self.NotesDurations = vals[0]
        self.NotesProbabilities = vals[1]
        self.SilencesDurations = vals[2]
        self.SilencesProbabilities = vals[3]

    def GeneratePreset(self, nbBeats: int):
        barPreset = []
        sumDurations = 0.0

        while sumDurations < nbBeats:
            drewSilence = False
            drawn = random()
            if drawn <= self.SilenceChance:
                drewSilence = True
                currDurations = self.SilencesDurations
                currProbabilities = self.SilencesProbabilities
            else:
                currDurations = self.NotesDurations
                currProbabilities = self.NotesProbabilities

            # adding insurance
            nbTries = 0
            while True:
                selectedDuration = 0.0
                drawn = random()
                for idProba in range(len(currProbabilities)):
                    if drawn <= currProbabilities[idProba]:
                        selectedDuration = currDurations[idProba]
                        break

                if sumDurations + selectedDuration <= nbBeats:
                    if not drewSilence:
                        barPreset.append(
                            {
                                "Beat": sumDurations,
                                "Duration": selectedDuration
                            }
                        )

                    sumDurations += selectedDuration
                    break

                nbTries += 1
                if nbTries >= 50:
                    print("Cannot find Solution. Switching between Silences and Notes")
                    if drewSilence:
                        currDurations = self.NotesDurations
                        currProbabilities = self.NotesProbabilities
                        drewSilence = False
                    else:
                        currDurations = self.SilencesDurations
                        currProbabilities = self.SilencesProbabilities
                        drewSilence = True

                if nbTries >= 100:
                    print("Cannot fulfill exit conditions, mismatched Generator specs.")
                    print("Exiting generation loop, think about providing more granularity for model: {}".format(self))
                    print("Returning BarPreset generated until now")
                    print()
                    break

        return barPreset

    def GenerateBar(self, nbBeats: float) -> Bar:
        return GenerateBarFromRhythmicPreset(
            self.GeneratePreset(nbBeats)
        )
