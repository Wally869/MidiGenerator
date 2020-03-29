import json
from glob import glob
import os
from random import random
from typing import Dict, List, Tuple

from MidiStructurer.Components import *
from utils import ReadMultipleJsons, ReadSingleJson


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

    def CheckAndSetProbabilities(self, modelSpecs) -> None:
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

            nbTries = 0
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

                # adding this to ensure existence of solution?
                # need to perform check on presets, to see if possible to solve problem
                nbTries += 1
                if nbTries >= 100:
                    nbTries = 0
                    if drewSilence:
                        currDurations = self.NotesDurations
                        currProbabilities = self.NotesCumulativeProbabilities
                    else:
                        currDurations = self.SilencesDurations
                        currProbabilities = self.SilencesCumulativeProbabilities
        return preset
        #return BarFromPreset(preset)

    def GenerateBar(self, nbBeats: int) -> Bar:
        return BarFromPreset(self.GenerateBarPreset(nbBeats))

    def GenerateMultipleBars(self, nbBarsToGenerate: int, nbBeatsPerBar: int):
        return [self.GenerateBar(nbBeatsPerBar) for _ in range(nbBarsToGenerate)]

    def GenerateSections(self, nbSections: int, nbBarsPerSection: int, nbBeatsPerBar: int):
        return [self.GenerateMultipleBars(nbBarsPerSection, nbBeatsPerBar) for _ in range(nbSections)]


def ReadAllModelsJsonFiles():
    allModelsSpecsFilepaths = glob("RhythmicModelsSpecs/*.json")
    return ReadMultipleJsons(allModelsSpecsFilepaths)


def LoadAllRhythmicModels() -> List[RhythmicModel]:
    jsonData = [model for model in ReadAllModelsJsonFiles()]
    rhythmicModels = [RhythmicModel(m) for m in jsonData]

    return rhythmicModels

def LoadSingleRhythmicModel(filepath: str) -> RhythmicModel:
    modelSpecs = ReadSingleJson(filepath)
    # map model specs to an object
    return RhythmicModel(modelSpecs)

def LoadRhythmicModelsWithTags(tags: List[str]) -> List[RhythmicModel]:
    models = ReadAllModelsJsonFiles()
    chosenModelsJsons = []
    for m in models:
        for t in tags:
            if t in m["Tags"]:
                chosenModelsJsons.append(m)
                break

    return [RhythmicModel(m) for m in chosenModelsJsons]


def LoadRhythmicModelsWithSingleTag(tag: str) -> List[RhythmicModel]:
    models = ReadAllModelsJsonFiles()
    chosenModelsJsons = []
    for m in models:
        if tag in m["Tags"]:
            chosenModelsJsons.append(m)

    return [RhythmicModel(m) for m in chosenModelsJsons]