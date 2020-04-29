from .NotePickerInterface import NotePickerInterface

from .utils import ComputeCumulativeProbabilities, PickFromCumulativeArray, FindIdElemInList

from random import choice
from typing import List, Dict

"""
EXPECTED PAYLOAD FOR THIS MODEL

payload = {
    DecayFactor: float 

}

DecayFactor in [0, 1.0]
"""


class DistancePicker(NotePickerInterface):
    DecayFactor = 0.7

    def InitializeModelFromPayload(self, payload: Dict):
        self.DecayFactor = payload["DecayFactor"]

    def ChooseRandomNextNote(self, allowedNotes: List[Dict]) -> Dict:
        return choice(allowedNotes)

    def ChooseNextNote(self, previousNote: str, allowedNotes: List[Dict]) -> Dict:
        refId = FindIdElemInList(previousNote, allowedNotes)
        probas = self.ComputeDecayingProbabilities(refId, len(allowedNotes))
        cum_probas = ComputeCumulativeProbabilities(probas)
        idNoteChosen = PickFromCumulativeArray(cum_probas)
        return allowedNotes[idNoteChosen]

    def ComputeDecayingProbabilities(self, idRefNote: int, lenProbas: int):
        probas = [0.0 for _ in range(lenProbas)]
        probas[idRefNote] = 1.0

        currId = idRefNote
        currProba = 1.0
        while currId > 0:
            currId -= 1
            currProba *= self.DecayFactor
            probas[currId] = currProba

        currProba = 1.0
        currId = idRefNote
        while currId < lenProbas - 1:
            currId += 1
            currProba *= self.DecayFactor
            probas[currId] = currProba

        # scale to 1
        scaledProbas = [p / sum(probas) for p in probas]

        return scaledProbas
