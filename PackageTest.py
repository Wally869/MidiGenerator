# testing everything in the package to make sure it works

from MidiStructurer.Components import Bar, Track

# RhythmicGenerators
from RhythmicGenerators import *

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
    print("Generating RandomBar")
    print(rp.GenerateRandomBar(payload={}))
    print("Generating SectionFromPattern")
    print(
        rp.GenerateSectionFromPattern(
            payload={
                "Pattern": [0, 1, 0]
            }
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
    print("Generating RandomBar")
    print(
        rm.GenerateRandomBar(
            payload={
                "NbBeats": 4
            }
        )
    )
    print(
        rm.GenerateSectionFromPattern(
            payload={
                "NbBeats": 4,
                "Pattern": [0, 1, 0]
            }
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
    generatedBar = rp.GenerateBar(
        payload={
            "ChosenBar": 0
        }
    )

    print("Creating DrumsBeatColorer instance")
    dbc = DrumsBeatColorer(
        drumsBeatColorerData
    )

    print("Preparing generated bar")
    preppedBar = dbc.PrepareBar(generatedBar)

    [print(se.Note) for se in preppedBar.SoundEvents]
    return dbc, preppedBar
