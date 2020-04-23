from tinydb import TinyDB


def InitializeDatabase(dbPath: str):
    # Connecting to db creates the file
    conn = TinyDB(dbPath)

    # Creating tables for Rhythm Generation
    # And setting starting values

    # RHYTHMIC MODEL
    currTable = conn.table('RhythmicModel')
    testModel = {
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

    currTable.insert(testModel)

    # RHYTHMIC PRESET
    currTable = conn.table('RhythmicPreset')
    testPreset = {
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

    currTable.insert(testPreset)

    # DRUMS BEAT COLORER
    currTable = conn.table('DrumsBeatColorer')
    testColorer = {
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

    currTable.insert(testColorer)