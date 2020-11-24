from .MelodicNotePickerInterface import MelodicNotePickerInterface

from MusiStrata.Components import Note, Bar
from .utils import ComputeCumulativeProbabilities, PickFromCumulativeArray, FindIdElemInList

from random import choice
from typing import List, Dict

"""
EXPECTED PAYLOAD FOR THIS MODEL

payload = {
    DecayFactor: float 
    ExcludeCurrent: bool
}

DecayFactor in [0, 1.0]
"""


class DistancePickerMelodic(MelodicNotePickerInterface):
    DecayFactor = 0.7
    ExcludeCurrent = False

    def __str__(self):
        return "<class 'DistancePickerMelodic'>"

    def __repr__(self):
        return self.__str__()

    def __call__(self, inputBars: List[Bar], allowedNotes: List[Note], **kwargs):
        prevNote = None
        for b in inputBars:
            for se in b.SoundEvents:
                prevNote = self.ChooseNextNote(prevNote, allowedNotes)
                se.Note = prevNote

    def InitializeModelFromPayload(self, payload: Dict):
        self.DecayFactor = payload["DecayFactor"]
        self.ExcludeCurrent = payload["ExcludeCurrent"]

    def ChooseRandomNextNote(self, allowedNotes: List[Note]) -> Note:
        return choice(allowedNotes)

    def ChooseNextNote(self, previousNote: Note, allowedNotes: List[Note]) -> Note:
        if previousNote is None:
            return choice(allowedNotes)
        refId = FindIdElemInList(previousNote, allowedNotes)
        probas = self.ComputeDecayingProbabilities(refId, len(allowedNotes))
        cumProbas = ComputeCumulativeProbabilities(probas)
        idNoteChosen = PickFromCumulativeArray(cumProbas)
        return allowedNotes[idNoteChosen]

    def ComputeDecayingProbabilities(self, idRefNote: int, lenProbas: int) -> List[float]:
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

        if self.ExcludeCurrent:
            probas[idRefNote] = 0

        # scale to 1
        scaledProbas = [p / sum(probas) for p in probas]

        return scaledProbas
