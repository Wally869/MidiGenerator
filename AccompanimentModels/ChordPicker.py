from .AccompanimentNotePickerInterface import AccompanimentNotePickerInterface

from MusiStrata.Components import Note, Chord, Bar
from MusiStrata.Components.Structure import Bar, GenerateSoundEventsFromListNotes

from typing import List, Dict


class ChordPicker(AccompanimentNotePickerInterface):
    """
    EXPECTED PAYLOAD FOR THIS MODEL

    payload = {
        AllowedChords: List[Chord],
        ExcludeRootNote: bool,
        BeatsPicked: str  # values in ["First", "Two", "All"]
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

    def __call__(self, InputBars: List[Bar], AllowedNotes: List[Note], DependencyBars: List[Bar], **kwargs):
        # will need to standardize calls
        # for now, going with what I got
        for idBar in range(len(InputBars)):
            InputBars[idBar] = Bar(SoundEvents=self.GenerateNextBar(DependencyBars[idBar]))

    def InitializeModelFromPayload(self, payload: Dict):
        self.AllowedChords: List[Chord] = payload["AllowedChords"]
        self.RootInOutput: bool = payload["RootInOutput"]
        self.BeatsPicked: str = payload["BeatsPicked"]

    def GenerateNextBar(self, referenceBar: Bar):
        from copy import deepcopy as _deepcopy
        from random import choice as _choice

        # check first if nothing in referenceBar
        if len(referenceBar.SoundEvents) == 0:
            return []

        generatedChordSoundEvents = []
        if self.BeatsPicked == "All":
            soundEvents = _deepcopy(referenceBar.SoundEvents)
        elif self.BeatsPicked == "First":
            soundEvents = [_deepcopy(referenceBar.SoundEvents[0])]
        else:
            # two sound events, harder to implement...
            # Check if only size one
            soundEvents = _deepcopy(referenceBar.SoundEvents)
            if len(soundEvents) > 2:
                # 1 or 2 Sound events, nothing to do
                # else gotta do some stuff
                # compute estimated nb of beats
                nbBeatsEstimated = soundEvents[-1].Beat + soundEvents[-1].Duration
                # get the beat that is closest to and higher than half of nbBeatsEstimated
                target = nbBeatsEstimated / 2
                closest = None
                closestDelta = 999
                for s in soundEvents:
                    if closest is None:
                        closest = s
                    else:
                        delta = s.Beat - target
                        if 0 < delta < closestDelta:
                            closestDelta = delta
                            closest = s
                soundEvents = [soundEvents[0], closest]

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

            notes, _ = chord(se.Note) #, rootInOutput=self.RootInOutput)
            if (not self.RootInOutput):
                notes = notes[1:]
            generatedChordSoundEvents += GenerateSoundEventsFromListNotes(
                se.Beat,
                se.Duration,
                notes
            )

        return generatedChordSoundEvents
