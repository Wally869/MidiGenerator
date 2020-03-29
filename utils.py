import json

from typing import List

# JSON utils
def ReadSingleJson(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def ReadMultipleJsons(filepaths: List[str]):
    outJsons = [ReadSingleJson(f) for f in filepaths]
    return outJsons

# Subsetting utils
def CheckForDesiredTagInTagsList(desiredTag: str, tagsList: List[str]):
    return desiredTag in tagsList