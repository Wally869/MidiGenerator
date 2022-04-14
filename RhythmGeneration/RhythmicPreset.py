from typing import List, Tuple, Dict, Union
from .BaseGenerator import BaseRhythmicGenerator

from MusiStrata import Bar, Note, SoundEvent
from random import choice


class RhythmicPreset(BaseRhythmicGenerator):
    """
    Expecting a Dict following this example:
    {
        "Name": "TestRhythmicPreset1",
        "Tags": ["Test"],
        "Beats": 4,
        "MainPreset": [
            
                "beat": 0.0,
                "duration": 1.0
            },
            {
                "beat": 2.0,
                "duration": 1.0
            },
            {
                "beat": 3.0,
                "duration": 0.5
            },
            {
                "beat": 3.5,
                "duration": 0.5
            }
        ],
        "Variants": []
    }

    """

    def __init__(self, parameters: Dict):
        self.NbBeats = parameters["NbBeats"]
        self.Presets = [parameters["MainPreset"]] + parameters["VariantsPreset"]

    def __str__(self):
        return "<class 'RhythmicPreset'>"

    def __repr__(self):
        return self.__str__()

    # override generatepattern
    def GeneratePattern(self, nbBars: int) -> List[int]:
        return [choice(range(len(self.Presets))) for _ in range(nbBars)]

    def __call__(self, nbBars: int, nbBeats: float = 4.0, pattern: List[int] = [], **kwargs):
        if pattern == []:
            pattern = self.GeneratePattern(nbBars)
        return [
            self.GenerateBarFromRhythmicPreset(
                self.Presets[idPreset]
            ) for idPreset in pattern
        ]
