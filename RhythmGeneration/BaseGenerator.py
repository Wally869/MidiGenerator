from typing import List, Tuple, Dict, Union

from ..Interfaces.RhythmicGenerator import IRhythmicGenerator
from MusiStrata.Components import Bar, Note, SoundEvent

from random import choice
from math import ceil

class BaseRhythmicGenerator(IRhythmicGenerator, object):
    def __str__(self):
        return "<class 'RhythmicGeneratorInterface'>"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def GenerateBreak():
        # Use this to get an empty bar, could serve as break in between generated segments
        return Bar()

    @classmethod
    def GeneratePattern(nbBars: int) -> Tuple[int, List[int]]:
        # how many different bars? use square root of nb bars
        nbSegments = ceil(nbBars ** 0.5)
        return nbSegments, [choice(range(nbSegments)) for _ in range(nbBars)]

    def GenerateBarFromRhythmicPreset(self, rhythmicPreset: List[Dict[str, Union[float, int]]]) -> Bar:
        """
        :param rhythmicPreset: {
            "Beat": float,
            "Duration": float,
            "NoteName": str (facultative),
            "Octave": int (facultative)
        }
        :return: Bar
        """
        outBar = Bar()
        for rp in rhythmicPreset:
            newEvent = SoundEvent(
                Beat=rp["Beat"],
                Duration=rp["Duration"]
            )

            rpKeys = list(rp.keys())
            if "NoteName" in rpKeys and "Octave" in rpKeys:
                newEvent.Note = Note(
                    Name=rp["NoteName"],
                    Octave=rp["Octave"]
                )
            outBar.SoundEvents.append(newEvent)

        return outBar