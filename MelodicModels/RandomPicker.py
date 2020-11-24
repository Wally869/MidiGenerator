from __future__ import annotations

from MusiStrata.Components import Note, Bar

from .MelodicNotePickerInterface import MelodicNotePickerInterface

from random import choice
from typing import List, Dict

"""
EMPTY PAYLOAD

payload = {
}

"""


class RandomPickerMelodic(MelodicNotePickerInterface):
    def __str__(self):
        return "<class 'RandomPickerMelodic'>"

    def __repr__(self):
        return self.__str__()

    def __call__(self, inputBars: List[Bar], allowedNotes: List[Note], **kwargs):
        for b in inputBars:
            for se in b.SoundEvents:
                se.Note = choice(allowedNotes)

    def InitializeModelFromPayload(self, payload: Dict = {}):
        pass

    def ChooseRandomNextNote(self, allowedNotes: List[Note]) -> Note:
        return choice(allowedNotes)

    def ChooseNextNote(self, previousNote: Note, allowedNotes: List[Note]) -> Note:
        return self.ChooseRandomNextNote(allowedNotes)
