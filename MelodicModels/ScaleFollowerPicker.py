from .MelodicNotePickerInterface import MelodicNotePickerInterface

from .utils import FindIdElemInList

from typing import List, Dict

"""
EXPECTED PAYLOAD FOR THIS MODEL

payload = {
    Reversed: bool,
    Skip: int
}

"""


class ScaleFollowerPickerMelodic(MelodicNotePickerInterface):
    Reversed = False
    Skip = 0

    def __str__(self):
        return "<class 'ScaleFollowerPickerMelodic'>"

    def __repr__(self):
        return self.__str__()

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
