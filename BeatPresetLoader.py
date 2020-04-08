import json
from glob import glob
import os

from typing import Dict, List

from MidiStructurer.Components import Note, Track, Bar
from MidiStructurer.Drums import GetHeightFromDrums
from MidiStructurer.ScalesUtils import GetNoteFromHeight

from utils import ReadMultipleJsons, ReadSingleJson

from copy import deepcopy


def ConvertDrumInstrumentToNoteObject(drumInstrument: str):
    height = GetHeightFromDrums(drumInstrument)
    outNote = GetNoteFromHeight(height)
    return outNote


def SetDrumInstrumentToNoteObject(drumInstrument: str, noteToModify: Note) -> None:
    newNoteSpecs = ConvertDrumInstrumentToNoteObject(drumInstrument)

    noteToModify.Octave = newNoteSpecs.Octave
    noteToModify.NoteName = newNoteSpecs.NoteName


class BeatPreset(object):
    BeatsValueToBeatsClassified = {}
    DrumsInstruments = {}

    def __init__(self, specs):
        self.DrumsInstruments = specs["Drums"]
        self.SetBeatsDecomposition(specs["BeatsDecomposition"])

    def SetBeatsDecomposition(self, beatsDecomposition: Dict) -> None:
        for key in list(beatsDecomposition.keys()):
            for val in beatsDecomposition[key]:
                if val in list(self.BeatsValueToBeatsClassified.keys()):
                    self.BeatsValueToBeatsClassified[val].append(key)
                else:
                    self.BeatsValueToBeatsClassified[val] = [key]

    def CheckInstrumentsForBeat(self, beat: float) -> List[str]:
        if beat in list(self.BeatsValueToBeatsClassified.keys()):
            beatCategories = self.BeatsValueToBeatsClassified[beat]
            if type(beatCategories) != list:
                beatCategories = [beatCategories]

            outInstruments = [
                self.DrumsInstruments[
                    cat
                ] for cat in beatCategories
            ]
        else:
            outInstruments = self.DrumsInstruments["Default"]
            if type(outInstruments) != list:
                outInstruments = [outInstruments]

        return outInstruments

    def PrepareTrack(self, track: Track) -> None:
        newBars = []
        for bar in track.Bars:
            currBar = Bar()
            for n in bar.Notes:
                noteInstruments = self.CheckInstrumentsForBeat(n.Beat)
                for instrument in noteInstruments:
                    newNote = deepcopy(n)
                    SetDrumInstrumentToNoteObject(instrument, newNote)
                    currBar.Notes.append(newNote)
            newBars.append(currBar)

        track.Bars = newBars


def ReadAllBeatPresetsJsonFiles():
    allModelsSpecsFilepaths = glob("BeatPresetsSpecs/*.json")
    return ReadMultipleJsons(allModelsSpecsFilepaths)


def LoadAllBeatPresets() -> List[BeatPreset]:
    jsonData = [model for model in ReadAllBeatPresetsJsonFiles()]
    beatPresets = [beatPresets(m) for bp in jsonData]

    return beatPresets


def LoadSingleBeatPreset(filepath: str) -> BeatPreset:
    presetSpecs = ReadSingleJson(filepath)
    # map model specs to an object
    return BeatPreset(presetSpecs)


def LoadRhythmicModelsWithTags(tags: List[str]) -> List[BeatPreset]:
    models = ReadAllBeatPresetsJsonFiles()
    chosenModelsJsons = []
    for m in models:
        for t in tags:
            if t in m["Tags"]:
                chosenModelsJsons.append(m)
                break

    return [presetSpecs(m) for m in chosenModelsJsons]


def LoadRhythmicModelsWithSingleTag(tag: str) -> List[BeatPreset]:
    models = ReadAllModelsJsonFiles()
    chosenModelsJsons = []
    for m in models:
        if tag in m["Tags"]:
            chosenModelsJsons.append(m)

    return [BeatPreset(m) for m in chosenModelsJsons]
