from .AccompanimentNotePickerInterface import AccompanimentNotePickerInterface
from typing import List, Dict


class CounterpointPicker(AccompanimentNotePickerInterface):
    """
    EXPECTED PAYLOAD FOR THIS MODEL

    payload = {
        Species: int,
        Upper: bool
    }

    Species between 0 and 4, to generate different types of counterpoints,
    with 4 the mixing of the previous 4.
    Upper is a boolean to determine whether the counterpoint has to be generated in a higher
    or lower voice. This has an impact on generation rules (basically, more restrictions)
    """
    def __str__(self):
        return "<class 'CounterPointPicker'>"

    def __repr__(self):
        return self.__str__()

    def InitializeModelFromPayload(self, payload: Dict):
        pass
