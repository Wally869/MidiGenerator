from .AccompanimentNotePickerInterface import AccompanimentNotePickerInterface

from MidiStructurer.Components.Chords import Chord
from MidiStructurer.Components.Structure import Bar, GenerateSoundEventsFromListNotes

from typing import List, Dict


class ChordPicker(AccompanimentNotePickerInterface):
    """
    EXPECTED PAYLOAD FOR THIS MODEL

    payload = {
        AllowedChords: List[Chord],
        ExcludeRootNote: bool,
        BeatsPicked: str  # values in ["One", "Two", "All"]
    }

    for BeatsPicked:
    One means generate a chord based on the first Sound Event in the reference bar
    Two means generate chord based on 2 sound events. Check beats of sound events to try to
    put chords at sufficient distance
    All means all sound events get a chord. Checking if no chord already in refBar?
    """
    AllowedChords = None
    BeatsPicked = None
    RootInOutput = True

    def __str__(self):
        return "<class 'ChordPicker'>"

    def __repr__(self):
        return self.__str__()

    def InitializeModelFromPayload(self, payload: Dict):
        self.AllowedChords: List[Chord] = payload["AllowedChords"]
        self.RootInOutput: bool = payload["RootInOutput"]
        self.BeatsPicked: str = payload["BeatsPicked"]

    def GenerateNextBar(self, referenceBar: Bar):
        from copy import deepcopy as _deepcopy
        from random import choice as _choice

        generatedChordSoundEvents = []
        if self.BeatsPicked == "All":
            soundEvents = _deepcopy(referenceBar.SoundEvents)
        elif self.BeatsPicked == "One":
            soundEvents = [_deepcopy(referenceBar.SoundEvents[0])]
            # check valid length
            if len(soundEvents) == 0:
                return
        else:
            # two sound events, harder to implement...
            # PLACEHOLDER
            soundEvents = _deepcopy(referenceBar.SoundEvents)

        for se in soundEvents:
            # Get a valid chord
            isValidChord = False
            for chord in self.AllowedChords:
                notes, errs = chord(se.Note)
                if sum([val is not None for val in errs]) == 0:
                    # No errors for given scale, break out of loop
                    isValidChord = True
                    break
            # if no valid chord, choose random
            if not isValidChord:
                chord = _choice(self.AllowedChords)

            notes, _ = chord(se.Note, rootInOutput=self.RootInOutput)
            generatedChordSoundEvents += GenerateSoundEventsFromListNotes(
                se.Beat,
                se.Duration,
                notes
            )

        return generatedChordSoundEvents
