from __future__ import annotations

from MusiStrata.Components import Note, Bar

from random import choice
from typing import List, Dict


# Placeholder for initialization
# Not sur what I'll do with it so clean later
class MelodicNotePickerInterface:
    def __init__(self, payload):
        self.InitializeModelFromPayload(payload)

    # adding call. Much much better I think for handling behind?
    # still need to decide what i am generating...
    # Single note, or bar, or full section?
    # I think for melodicmodels, can be full section
    # use kwargs, should be nice?
    def __call__(self, inputBars: List[Bar], allowedNotes: List[Note], **kwargs):
        pass

    def __str__(self):
        return "<class 'MelodicNotePickerInterface'>"

    def __repr__(self):
        return self.__str__()

    def InitializeModelFromPayload(self):
        raise NotImplementedError

    def ChooseRandomNextNote(self, allowedNotes) -> List[Dict]:
        return choice(allowedNotes)

    def ChooseNextNote(self):
        raise NotImplementedError
