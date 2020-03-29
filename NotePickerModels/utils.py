
from random import random

from typing import List

def ComputeCumulativeProbabilities(probas: List[float]) -> List[float]:
    cum_probas = [probas[0]]
    for p in probas[1:]:
        cum_probas.append(p + cum_probas[-1])

    return cum_probas

def PickFromCumulativeArray(probas: List[float]) -> int:
    drawn = random()
    for id_chosen in range(len(probas)):
        if drawn <= probas[id_chosen]:
            break

    return id_chosen