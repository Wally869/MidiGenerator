from __future__ import annotations
from typing import List

from MusiStrata import ChordsLibrary

import json

"""
This script aims to produce descriptive json files for chord sequences generation
See example.json for example of desired output 
Will also add to a json db of errors? like nb chords with problems


Keeping this as a dev tool/reminder.
Will need to implement rules for chord sequence generation
"""

"A4-M-90-4-(0)_1-MT-F-H-1"  # 0 is instrument.

majorTriad = ChordsLibrary.GetChordFromName("Major Triad")

chordGen = {
    "Degrees": [0, 3, 4],
    "Chords": [majorTriad, majorTriad, majorTriad]
}

name = "gen-0"
tempo = 90
beatsPerBar = 4
referenceNote = "A"
referenceOctave = 4
useMajorScale = True
# 0 indexed degrees

output = {
    "name": name,
    "tempo": tempo,
    "beatsPerBar": 3,
    "referenceNote": "A",
    "referenceOctave": 4,
    "useMajorScale": True,
    "repetitions": 1,
    "instrument": "Acoustic Grand Piano",

}

specsStyle = [{
    "direction": "high",
    "repetitions": 0
    },
    {
    "direction": "high",
    "repetitions": 0
    },
    {
    "direction": "high",
    "repetitions": 0
    }
]

components = [
    {
        "degree": chordGen["Degrees"][idChord],
        "chord": "Major Triad",
        "style": "chord",
        "specsStyle": specsStyle[0]
    } for idChord in range(len(specsStyle))
]

output["components"] = components

with open("test.json", "w+") as f:
    json.dump(output, f)
