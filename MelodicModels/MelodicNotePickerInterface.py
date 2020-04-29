from random import choice
from typing import List, Dict


# Placeholder for initialization
# Not sur what I'll do with it so clean later
class MelodicNotePickerInterface:
    def __init__(self, payload):
        self.InitializeModelFromPayload(payload)

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
