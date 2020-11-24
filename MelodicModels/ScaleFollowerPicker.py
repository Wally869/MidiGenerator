from __future__ import annotations

from .MelodicNotePickerInterface import MelodicNotePickerInterface

from MusiStrata import Note, Bar
from .utils import FindIdElemInList

from typing import List, Dict

"""
EXPECTED PAYLOAD FOR THIS MODEL

payload = {
    Reversed: bool,
    Skip: int
}

maybe call this pattern follower
and have as payload degrees used?
=> other model I think bud

"""


class ScaleFollowerPickerMelodic(MelodicNotePickerInterface):
    Reversed = False
    Skip = 0

    def __str__(self):
        return "<class 'ScaleFollowerPickerMelodic'>"

    def __repr__(self):
        return self.__str__()

    def __call__(self, inputBars: List[Bar], allowedNotes: List[Note], **kwargs):
        pass

    def InitializeModelFromPayload(self, payload: Dict):
        self.Reversed = payload["Reversed"]
        self.Skip = payload["Skip"]

    def ChooseNextNote(self, previousNote: str, allowedNotes: List[Dict]) -> Dict:
        refId = FindIdElemInList(previousNote, allowedNotes)

        signDelta = 1
        if self.Reversed:
            signDelta = -1

        newId = refId + signDelta * self.Skip + signDelta * 1
        if newId >= len(allowedNotes):
            newId -= len(allowedNotes)
        elif newId < 0:
            newId += len(allowedNotes)

        return allowedNotes[newId]
