from __future__ import annotations

from random import random

from MidiStructurer.Components import *

from NewUtils import ComputeCumulativeProbabilitiesFromDict


# Cleaning up previous implementations for Rhythmic Generation
# Getting rid of previous stuff about json, should be handled somewhere else
# Also, would be nice to follow an interface for both types (model & preset) to make
# them easier to use

# Define an interface for inheritance and standardization of usage for different Rhythmic models
# Or maybe even just one model? would be more dirty though
class RhythmicGeneratorInterface(object):
    def GenerateBarPreset(self):
        return NotImplemented

    def GenerateBar(self):
        return NotImplemented


class RhythmicPreset(RhythmicGeneratorInterface):
    pass


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

    # Computed at __init__
    NotesDurations = []
    NotesProbabilities = []
    SilencesDurations = []
    SilencesProbabilities = []

    def __init__(self, parameters: Dict):
        # Tracking Parameters
        self.Name = parameters["Name"]
        self.SilenceChance = parameters["SilenceChance"]

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

    def GenerateBarPreset(self, payload: Dict[str: float] = {"NbBeats": 4.0}) -> List[Dict[str: float]]:
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
                if nbTries >= 100:
                    print("Cannot find Solution. Switching between Silences and Notes")
                    nbTries = 0
                    if drewSilence:
                        currDurations = self.NotesDurations
                        currProbabilities = self.NotesProbabilities
                        drewSilence = False
                    else:
                        currDurations = self.SilencesDurations
                        currProbabilities = self.SilencesProbabilities
                        drewSilence = True

        return barPreset

    def GenerateBar(self, payload: Dict[str: float]) -> Bar:
        return Bar(
            self.GenerateBarPreset(
                payload=payload
            )
        )

