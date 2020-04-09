from __future__ import annotations

from MidiStructurer.Components.Structure import Bar, Track
from MidiStructurer.Components.Notes import Note, CreateNoteFromHeight
from MidiStructurer.Drums import GetHeightFromDrums

from copy import deepcopy

from typing import Dict, List


def ConvertDrumInstrumentToNoteObject(drumInstrument: str) -> Note:
    height = GetHeightFromDrums(drumInstrument)
    outNote = CreateNoteFromHeight(height)
    return outNote


def GetNoteFromDrumInstrument(drumInstrument: str) -> Note:
    newNote = ConvertDrumInstrumentToNoteObject(drumInstrument)
    return newNote


class DrumsBeatColorer(object):
    """
    Create a DrumsBeatColorer from definitions of beat and instruments.
    This class allows to set a particular instrument to notes in a Drums track.
    It works by specifying types of beats (primary, secondary...) and associating instruments
    in the definition. Doing it this way allows a given beat to have several drums acting on it if so desired

    NOTE: Will only support instruments defined as DRUMS in MidiStructurer.Drums
    Drums have their own specific channel

    Example Input
    {
        "Name": "TestBeats",
        "Tags": ["Test"],
        "NbBeats": 4,
        "BeatsDecomposition": {
            "Primary": [0.0],
            "Secondary": [0.0, 2.0]
        },
        "DrumsInstruments": {
            "Primary": "Bass Drum 1",
            "Secondary": "High Tom 1",
            "Default": "Snare Drum 1"
        }
    }
    """

    BeatsValueToBeatsClassified = {}
    DrumsInstruments = {}

    def __init__(self, specs: Dict):
        self.DrumsInstruments = specs["DrumsInstruments"]
        self.SetBeatsDecomposition(specs["BeatsDecomposition"])

    def SetBeatsDecomposition(self, beatsDecomposition: Dict) -> None:
        """
            beatsDecomposition in the specs json to be input maps keys to arrays of beats, to make it easy
            to specify new presets for the user.
            Here we reverse this: a beat can be both primary and secondary, and more depending on the specs
            So we create a new dict using the beat as key, and its classifications in an array

            Example:
            {
            "Primary": [0.0],
            "Secondary": [0.0, 2.0]
            }

            will become:
            {
            0.0: ["Primary", "Secondary"],
            2.0: ["Secondary"]
            }
        """
        for key in list(beatsDecomposition.keys()):
            for val in beatsDecomposition[key]:
                if val in list(self.BeatsValueToBeatsClassified.keys()):
                    self.BeatsValueToBeatsClassified[val].append(key)
                else:
                    self.BeatsValueToBeatsClassified[val] = [key]

    def CheckInstrumentsForBeat(self, beat: float) -> List[str]:
        """
        get the instruments to be associated with a given beat

        :param beat: float
        :return: List[str], a list of instrument names
        """
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
        """
        Set drums instruments to notes, depending on beat
        """
        newBars = []
        for bar in track.Bars:
            currBar = Bar()
            for se in bar.SoundEvents:
                noteInstruments = self.CheckInstrumentsForBeat(se.Beat)
                for instrument in noteInstruments:
                    newSoundEvent = deepcopy(se)
                    newSoundEvent.Note = GetNoteFromDrumInstrument(instrument)
                    currBar.SoundEvents.append(newSoundEvent)
            newBars.append(currBar)

        track.Bars = newBars
