from __future__ import annotations

from .MelodicNotePickerInterface import MelodicNotePickerInterface
from MusiStrata import Note, Interval, Bar

from typing import List, Dict

"""
EXPECTED PAYLOAD FOR THIS MODEL

payload = {
    AllowedIntervals: List[Interval] 
}
"""


# add an initial note parameter to the __call__ method?
class FromIntervalPickerMelodic(MelodicNotePickerInterface):
    AllowedIntervals = []

    def InitializeModelFromPayload(self, payload: Dict):
        self.AllowedIntervals = payload["AllowedIntervals"]

    def __str__(self):
        return "<class 'FromIntervalPickerMelodic'>"

    def __repr__(self):
        return self.__str__()

    def __call__(self, inputBars: List[Bar], allowedNotes: List[Note], **kwargs):
        prevNote = None
        for b in inputBars:
            for se in b.SoundEvents:
                prevNote = self.ChooseNextNote(prevNote, allowedNotes)
                se.Note = prevNote

    def ChooseNextNote(self, refNote: Note, allowedNotes: List[Note]):
        from random import choice as _choice
        if refNote is None:
            return _choice(allowedNotes)
        else:
            possibleNotes = []
            for interval in self.AllowedIntervals:
                currNote, err = refNote + interval
                if err is None:
                    possibleNotes.append(currNote)
                currNote, err = refNote - interval
                if err is None:
                    possibleNotes.append(currNote)
            filteredNotes = list(
                filter(
                    lambda x: x in allowedNotes,
                    possibleNotes
                )
            )
            return _choice(filteredNotes)
