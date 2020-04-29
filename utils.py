from __future__ import annotations

from typing import Tuple, List, Dict


def ComputeCumulativeProbabilitiesFromDict(inputDict: Dict) -> Tuple[List[float], List[float]]:
    """
    Expecting input in format:
      {
        "0.5": 0.5,
        "1":  0.5
      }

      Outputting array of values, and array of cumulative probabilities
    """
    allKeys = list(inputDict.keys())
    values = [float(k) for k in allKeys]

    probas = [
        inputDict[k] for k in allKeys
    ]

    # make sure sum probas == 1
    probas = [p / sum(probas) for p in probas]
    # cumulative probabilities
    cumProbas = []
    for idProbas in range(len(probas)):
        currCumProba = probas[idProbas]
        if idProbas > 0:
            currCumProba += cumProbas[-1]
        cumProbas.append(currCumProba)

    return values, cumProbas


# Emulate List
class CustomList(object):
    def __init__(self, elements: List = []):
        self.Elements = elements

    def __repr__(self):
        return self.Elements.__repr__()

    def __len__(self):
        return len(self.Elements)

    def __getitem__(self, item):
        return self.Elements[item]

    def __add__(self, other):
        if type(other) == list:
            self.Elements += other
        elif self.__class__ is other.__class__:
            self.Elements += other.Elements
        else:
            raise NotImplemented

    def append(self, item):
        self.Elements.append(item)

