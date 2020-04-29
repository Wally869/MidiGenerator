from __future__ import annotations

from MidiStructurer.Components import Note

from .MelodicNotePickerInterface import MelodicNotePickerInterface

from random import choice
from typing import List, Dict

"""
EMPTY PAYLOAD

payload = {
}

"""
class RandomPickerMelodic(MelodicNotePickerInterface):
    def InitializeModelFromPayload(self, payload: Dict = {}):
        pass

    def ChooseRandomNextNote(self, allowedNotes):
        return choice(allowedNotes)

    def ChooseNextNote(self, previousNote: str, allowedNotes: List[Dict]) -> Note:
        return self.ChooseRandomNextNote(allowedNotes)

