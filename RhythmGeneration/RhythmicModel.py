from typing import List, Tuple, Dict, Union
from .BaseGenerator import BaseRhythmicGenerator

from MusiStrata import Bar, Note, SoundEvent
from random import choice, random

from ..Utils import ComputeCumulativeProbabilitiesFromDict

class RhythmicModel(BaseRhythmicGenerator):
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
        return self.GenerateBarFromRhythmicPreset(
            self.GeneratePreset(nbBeats)
        )
