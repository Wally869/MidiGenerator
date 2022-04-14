# testing everything in the package to make sure it works

from MusiStrata import *

# RhythmicGenerators
from RhythmGeneration import *

rhythmicPresetData = {
    "Name": "TestRhythmicPreset1",
    "Tags": ["Test"],
    "NbBeats": 4,
    "MainPreset": [
        {
            "Beat": 0.0,
            "Duration": 1.0
        },
        {
            "Beat": 2.0,
            "Duration": 1.0
        }
    ],
    "VariantsPreset": [
        [
            {
                "Beat": 0.0,
                "Duration": 1.0
            },
            {
                "Beat": 2.0,
                "Duration": 1.0
            },
            {
                "Beat": 3.0,
                "Duration": 0.5
            },
            {
                "Beat": 3.5,
                "Duration": 0.5
            }
        ]
    ]
}


def Test_RhythmicPreset():
    print("Testing Rhythmic Preset")
    rp = RhythmicPreset(rhythmicPresetData)
    print("Generating 4-Bars Segment")
    print(
        rp(
            nbBars=4,
            nbBeats=4
        )
    )
    return rp


rhythmicModelData = {
    "Name": "TestRhythmicModel",
    "Tags": ["Test"],
    "SilenceChance": 0.1,
    "Notes": {
        "0.5": 0.1,
        "1": 0.5,
        "1.5": 0.4
    },
    "Silences": {
        "0.5": 0.5,
        "1": 0.5
    }
}


def Test_RhythmicModel():
    print("Testing Rhythmic Model")
    rm = RhythmicModel(rhythmicModelData)
    print("Generating 4-Bars Segment")
    print(
        rm(
            nbBars=2,
            nbBeats=4
        )
    )
    return rm


# Drums Beat Colorer

from DrumsBeatColorer import DrumsBeatColorer

drumsBeatColorerData = {
    "Name": "TestBeats",
    "Tags": ["Test"],
    "NbBeats": 4,
    "BeatsDecomposition": {
        "Primary": [0.0],
        "Secondary": [0.0, 2.0]
    },
    "DrumsInstruments": {
        "Primary": "Bass Drum 1",
        "Secondary": "High Tom 1",
        "Default": "Snare Drum 1"
    }
}


def Test_DrumsBeatColorer():
    print("Loading RhythmicPreset to generate rhythmic test")
    rp = RhythmicPreset(rhythmicPresetData)
    generatedSegment = rp(
            nbBars=4,
            nbBeats=4
    )

    print("Creating DrumsBeatColorer instance")
    dbc = DrumsBeatColorer(
        drumsBeatColorerData
    )

    print("Preparing generated bar")
    for i in range(len(generatedSegment)):
        generatedSegment[i] = dbc.PrepareBar(generatedSegment[i])
        #preppedBar = dbc.PrepareBar(generatedSegment)

    #[print(se.Note) for se in preppedBar.SoundEvents]
    return dbc, Track(Bars=generatedSegment)

