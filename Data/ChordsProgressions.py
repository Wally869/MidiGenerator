from typing import List

from dataclasses import dataclass
from enum import Enum

from MusiStrata.Enums import Mode


@dataclass
class ChordProgression(object):
    Tones: List[int]
    Mode: Mode


whatev = ChordProgression(
    [0, 4, 5, 3],
    Mode.Major
)


popularKid = ChordProgression(
    [0, 3, 4],
    Mode.Major
)

sensitive = ChordProgression(
    [0, 4, 5, 3],
    Mode.Major
)


jazzCat = ChordProgression(
    [2, 5, 1],
    Mode.Major
)


canon = ChordProgression(
    [0, 4, 5, 2, 3, 0, 3, 4],
    Mode.Major
)
