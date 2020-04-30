from __future__ import annotations

from MidiStructurer.Components import Bar, GenerateBarFromRhythmicPreset
from utils import ComputeCumulativeProbabilitiesFromDict

from random import random, choice
from copy import deepcopy

from typing import List, Dict, Union


# Cleaning up previous implementations for Rhythmic Generation
# Getting rid of previous stuff about json, should be handled somewhere else
# Also, would be nice to follow an interface for both types (model & preset) to make
# them easier to use

# Define an interface for inheritance and standardization of usage for different Rhythmic models
# Or maybe even just one model? would be more dirty though
class RhythmicGeneratorInterface(object):
    def __str__(self):
        return "<class 'RhythmicGeneratorInterface'>"

    def __repr__(self):
        return self.__str__()

    def GenerateRandomBarPreset(self):
        return NotImplemented

    def GenerateBarPreset(self):
        return NotImplemented

    def GenerateBar(self):
        return NotImplemented

    @staticmethod
    def GenerateBreak():
        # Use this to get an empty bar, could serve as break in between generated segments
        return Bar()


# Add a GenerateSection, which has in payload a definition of bars successions (for example: [0, 0, 1, 2])
# Could also use combination of elements. Would be great for syncopation?
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

    def __call__(self, nbBars: int, pattern: List[int] = [], **kwargs):
        if pattern == []:
            # generate a pattern
            pattern = [choice(range(len(self.Presets))) for _ in range(nbBars)]
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

    def GenerateRandomBarPreset(self, payload: Dict[str: float] = {"NbBeats": 4.0}) -> List[Dict[str: float]]:
        # Extracting from payload
        nbBeats = payload["NbBeats"]

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

    def GenerateRandomBar(self, payload):
        return GenerateBarFromRhythmicPreset(
            self.GenerateRandomBarPreset(
                payload=payload
            )
        )

    def GenerateBarPreset(self, payload) -> List[Dict]:
        return self.GenerateRandomBarPreset(
            payload=payload
        )

    def GenerateBar(self, payload: Dict[str: float]) -> Bar:
        return self.GenerateRandomBar(
            payload=payload
        )

    def GenerateSectionFromPattern(self, payload: Dict[str, Union[float, List[int]]]) -> List[Bar]:
        # Pattern has shape like [0, 0, 1, 0]
        pattern = payload["Pattern"]
        bars = [
            self.GenerateBar(
                payload=payload
            ) for _ in range(max(pattern) + 1)
        ]
        section = [
            deepcopy(bars[currId]) for currId in pattern
        ]

        return section
