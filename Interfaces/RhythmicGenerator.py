from typing import List, Tuple
from MusiStrata.Components import Bar


class IRhythmicGenerator(object):
    @classmethod
    def GeneratePattern(cls, nbBars: int) -> Tuple[int, List[int]]:
        raise NotImplementedError(str(cls) + " - GeneratePattern Not Implemented")

