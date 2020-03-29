import json
from glob import glob
import os
from typing import Dict, List, Tuple
from random import choice

from MidiStructurer.Components import *
from utils import ReadMultipleJsons, ReadSingleJson


class RhythmicPreset(object):
    def __init__(self, presetSpecs: Dict, useVariants: bool = True):
        self.Presets = [presetSpecs["MainPreset"]]
        if useVariants:
            self.Presets += presetSpecs["Variants"]

    def GenerateSingleSection(self, nbBarsPerSection: int):
        successionPresets = []
        for _ in range(nbBarsPerSection):
            successionPresets.append(
                BarFromPreset(
                    choice(self.Presets)
                )
            )

        return successionPresets


def ReadAllPresetsJsonFile():
    allPresetsSpecsFilepaths = glob("RhythmicPresetsSpecs/*.json")
    return ReadMultipleJsons(allPresetsSpecsFilepaths)

def LoadAllRhythmicPresets():
    jsonData = [preset for preset in ReadAllPresetsJsonFile()]
    rhythmicPresets = [RhythmicPreset(p) for p in jsonData]

    return rhythmicPresets

def LoadSingleRhythmicPreset(filepath: str):
    presetSpecs = ReadSingleJson(filepath)

    return RhythmicPreset(presetSpecs)