

from typing import Dict, List
from random import random, choice



"""
GenerateBarRythmicPreset

Outputs the rythmic specs for a bar, aka a list of dict entries with fields beat and duration
See GeneratorSpecs.md for details on how generatorSpecs must be written
"""
def GenerateBarRythmicPreset(generatorSpecs: Dict, nbBeats: int) -> List[Dict]:
    return