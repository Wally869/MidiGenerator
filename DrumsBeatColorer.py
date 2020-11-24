from __future__ import annotations

from MusiStrata.Components.Structure import Bar, Track
from MusiStrata.Components.Notes import Note
from MusiStrata.Drums import GetHeightFromDrumsInstrumentName

from copy import deepcopy

from typing import Dict, List


def GetNoteFromDrumInstrument(drumInstrument: str) -> Note:
    height = GetHeightFromDrumsInstrumentName(drumInstrument)
    outNote = Note.FromHeight(height)
    return outNote


class DrumsBeatColorer(object):
    """
    Create a DrumsBeatColorer from definitions of beat and instruments.
    This class allows to set a particular instrument to notes in a Drums track.
    It works by specifying types of beats (primary, secondary...) and associating instruments
    in the definition. Doing it this way allows a given beat to have several drums acting on it if so desired

    NOTE: Will only support instruments defined as DRUMS in MusiStrata.Drums
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

    def __init__(self, specs: Dict):
        # Dicts are mutable so DO NOT SET THEM as cls property
        self.BeatsValueToBeatsClassified = {}
        self.DrumsInstruments = {}

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

            NOTE: 0.0 and 0 are considered the same thing when used as key in a dict
        """
        self.BeatsValueToBeatsClassified = {}
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

    def PrepareBar(self, inputBar: Bar) -> Bar:
        newBar = Bar()
        for se in inputBar.SoundEvents:
            noteInstruments = self.CheckInstrumentsForBeat(se.Beat)
            for instrument in noteInstruments:
                newSoundEvent = deepcopy(se)
                newSoundEvent.Note = GetNoteFromDrumInstrument(instrument)
                newBar.SoundEvents.append(newSoundEvent)

        return newBar

    def PrepareTrack(self, track: Track) -> None:
        """
        Set drums instruments to notes, depending on beat
        """
        newBars = []
        for bar in track.Bars:
            newBars.append(
                self.PrepareBar(
                    bar
                )
            )

        track.Bars = newBars
