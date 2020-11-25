from __future__ import annotations
from typing import List, Dict

from MusiStrata import *

import json

"""
TO BE DEPRECATED BY ChordSequencer.py

Generate Midi and Wav files from Descriptor files

"""


def GenerateFlattenedBar(comp: Dict, scaleNotes: List[Note], beatsPerBar: float) -> Bar:
    currBar = Bar()
    currRefNote = scaleNotes[comp["degree"]]
    currChord = ChordsLibrary.GetChordFromName(comp["chord"])
    chordNotes, _ = currRefNote + currChord
    if (comp["specsStyle"]["direction"] == "low"):
        chordNotes = chordNotes[::-1]
    currBeat = 0.0
    deltaBeat = 1.0 / (comp["specsStyle"]["repetitions"] + 1)
    for _ in range(comp["specsStyle"]["repetitions"] + 1):
        for cn in chordNotes:
            currBar.SoundEvents.append(
                SoundEvent(currBeat, deltaBeat, cn)
            )
            currBeat += deltaBeat
    return currBar

def GenerateChordBar(comp: Dict, scaleNotes: List[Note], beatsPerBar: float) -> Bar:
    currRefNote = scaleNotes[comp["degree"]]
    currChord = ChordsLibrary.GetChordFromName(comp["chord"])
    chordNotes, _ = currRefNote + currChord
    nbRepetitions = comp["specsStyle"]["repetitions"] + 1
    bar = Bar()
    for i in range(nbRepetitions):
        bar.SoundEvents += GenerateSoundEventsFromListNotes(i * beatsPerBar / nbRepetitions, beatsPerBar / nbRepetitions, chordNotes)
    return bar


# refactor the generation functions, to pass chordNotes as input
# or put first 3 lines in seperate function
def GeneratePairsBar(comp: Dict, scaleNotes: List[Note], beatsPerBar: float) -> Bar:
    currRefNote = scaleNotes[comp["degree"]]
    currChord = ChordsLibrary.GetChordFromName(comp["chord"])
    chordNotes, _ = currRefNote + currChord
    bar = Bar()
    nbPairs = len(currChord) - 1
    nbRepetitions = comp["specsStyle"]["repetitions"] + 1
    for idRepetition in range(nbRepetitions):
        if (comp["specsStyle"]["uprooted"]):
            idBaseNote = 0
            for i in range(nbPairs):
                if (idBaseNote >= nbPairs):
                    idBaseNote = 0
                bar.SoundEvents += GenerateSoundEventsFromListNotes((idRepetition * nbPairs + i) * beatsPerBar / (nbPairs*nbRepetitions), beatsPerBar / (nbPairs*nbRepetitions), chordNotes[idBaseNote:idBaseNote + 2])
                idBaseNote += 1
        else:
            idPairedNote = 1
            for i in range(nbPairs):
                if (idPairedNote >= nbPairs + 1):
                    idPairedNote = 1
                bar.SoundEvents += GenerateSoundEventsFromListNotes((idRepetition * nbPairs + i) * beatsPerBar / (nbPairs*nbRepetitions), beatsPerBar / (nbPairs*nbRepetitions), [chordNotes[0], chordNotes[idPairedNote]])
                idPairedNote += 1
    return bar



def GenerateTrackFromDescriptorObject(descriptor: Dict, deltaOctave: int = 0) -> Track:
    descriptor["referenceOctave"] += deltaOctave
    typeScale = "Major"
    if (not descriptor["useMajorScale"]):
        typeScale = "Minor"

    scaleSpecs = ScaleSpecs(descriptor["referenceNote"], typeScale)
    scaleNotes = scaleSpecs.GetScaleNotes(descriptor["referenceOctave"])

    bars = []
    for _ in range(descriptor["repetitions"] + 1):
        for comp in descriptor["components"]:
            if (comp["style"] == "chord"):
                currBar = GenerateChordBar(comp, scaleNotes, descriptor["beatsPerBar"])
            elif (comp["style"] == "pairs"):
                currBar = GeneratePairsBar(comp, scaleNotes, descriptor["beatsPerBar"])
            else:
                currBar = GenerateFlattenedBar(comp, scaleNotes, descriptor["beatsPerBar"])

            bars.append(currBar)

    track = Track(Bars=bars, Instrument=descriptor["instrument"])
    return track

def GenerateAudioFromDescriptorFile(filename: str):
    with open(filename, "r") as f:
        descriptor = json.load(f)
    track = GenerateTrackFromDescriptorObject(descriptor)
    song = Song(Tracks=[track], BeatsPerBar=descriptor["beatsPerBar"], Tempo=descriptor["tempo"])
    MidoConverter.ConvertSong(song, descriptor["name"] + ".mid")

if __name__ == "__main__":
    #GenerateAudioFromDescriptorFile("test.json")
    with open("test3.json", "r") as f:
        descriptor = json.load(f)
    t1 = GenerateTrackFromDescriptorObject(descriptor, deltaOctave=-1)
    with open("test2.json", "r") as f:
        descriptor = json.load(f)
    t2 = GenerateTrackFromDescriptorObject(descriptor)
    song = Song(Tracks=[t1, t2], BeatsPerBar=descriptor["beatsPerBar"], Tempo=descriptor["tempo"])
    MidoConverter.ConvertSong(song, descriptor["name"] + ".mid")
