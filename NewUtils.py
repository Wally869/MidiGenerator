from __future__ import annotations

from typing import Tuple, List, Dict

"""
Expecting input in format:
  {
    "0.5": 0.5,
    "1":  0.5
  }
  
  Outputting array of values, and array of cumulative probabilities
"""


def ComputeCumulativeProbabilitiesFromDict(inputDict: Dict) -> Tuple[List[float], List[float]]:
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
