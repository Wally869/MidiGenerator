from random import choice
from typing import List, Dict


# Placeholder for initialization
# Not sur what I'll do with it so clean later
class MelodicNotePickerInterface:
    def __init__(self, payload):
        self.InitializeModelFromPayload(payload)

    def InitializeModelFromPayload(self):
        raise NotImplementedError

    def ChooseRandomNextNote(self, allowedNotes) -> List[Dict]:
        return choice(allowedNotes)

    def ChooseNextNote(self):
        raise NotImplementedError
