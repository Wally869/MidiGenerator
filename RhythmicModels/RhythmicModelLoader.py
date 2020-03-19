import json
from glob import glob
import os
from random import random
from typing import Dict, List, Tuple

### NEED TO IMPORT COMPONENTS


class RhythmicModel(object):
    NotesDurations = []
    NotesCumulativeProbabilities = []
    SilencesDurations = []
    SilencesCumulativeProbabilities = []

    def __init__(self, modelSpecs: Dict):
        # Setting base values
        self.Name = modelSpecs["Name"]
        self.Tags = modelSpecs["Tags"]
        self.SilenceChance = modelSpecs["SilenceChance"]

        # Perform checks on probabilities
        self.CheckAndSetProbabilities(modelSpecs)

    def CheckAndSetProbabilities(self, modelSpecs):
        vals = []
        for k in ["Notes", "Silences"]:
            vals += self.ComputeCumulativeProbasForKeyType(k, modelSpecs)

        self.NotesDurations = vals[0]
        self.NotesCumulativeProbabilities = vals[1]
        self.SilencesDurations = vals[2]
        self.SilencesCumulativeProbabilities = vals[3]

    # In this function, ensure probabilities for notes and silences sum to 1
    # and compute cumulative probabilities
    #KeyType = "Notes" || "Silences"
    def ComputeCumulativeProbasForKeyType(self, keyType, modelSpecs) -> Tuple[List, List]:
        keysDurations = list(modelSpecs[keyType].keys())
        durations = [float(k) for k in keysDurations]
        probas = [modelSpecs[keyType][key] for key in keysDurations]

        # make sure sum probas = 1
        probas = [p/sum(probas) for p in probas]
        # cumulative probabilities
        cumProbas = []
        for idProbas in range(len(probas)):
            currCumProba = probas[idProbas]
            if idProbas > 0:
                currCumProba += cumProbas[-1]
            cumProbas.append(currCumProba)

        return durations, cumProbas

    def GenerateBarPreset(self, nbBeats: int):
        preset = []
        sumDurations = 0.0

        while (sumDurations < nbBeats):
            drewSilence = False
            drawn = random()
            if drawn <= self.SilenceChance:
                currDurations = self.SilencesDurations
                currProbabilities = self.SilencesCumulativeProbabilities
                drewSilence = True
            else:
                currDurations = self.NotesDurations
                currProbabilities = self.NotesCumulativeProbabilities

            while True:
                drawn = random()
                for id_proba in range(len(currProbabilities)):
                    if (drawn <= currProbabilities[id_proba]):
                        selectedDuration = currDurations[id_proba]
                        break

                if (sumDurations + selectedDuration <= nbBeats):
                    if drewSilence == False:
                        preset.append(
                            {
                                "beat": sumDurations,
                                "duration": selectedDuration
                            }
                        )

                    sumDurations += selectedDuration
                    break

        return preset

    def GenerateSingleSectionPreset(self, nbBarsPerSection: int, nbBeatsPerBar: int):
        return [self.GenerateBarPreset(nbBeatsPerBar) for _ in range(nbBarsPerSection)]

    def GenerateSectionsPresets(self, nbSections: int, nbBarsPerSection: int, nbBeatsPerBar: int):
        return [self.GenerateSingleSectionPreset(nbBarsPerSection, nbBeatsPerBar) for _ in range(nbSections)]



def LoadAllRhythmicModels() -> List[RhythmicModel]:
    allModelsSpecsFilepaths = glob("*.json")
    rhythmicModels = [LoadSingleRhythmicModel(filepath) for filepath in allModelsSpecsFilepaths]

    return rhythmicModels


def LoadSingleRhythmicModel(filepath: str) -> RhythmicModel:
    with open(filepath, "r") as f:
        modelSpecs = json.load(f)

    # map model specs to an object
    return RhythmicModel(modelSpecs)

