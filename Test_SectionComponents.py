from __future__ import annotations

from MidiStructurer import *
from SectionComponents import *
from Database.LocalDB import *
from RhythmicGenerators import RhythmicPreset, RhythmicModel

from MelodicNotePickerModels.RandomPicker import RandomPicker


from random import choice

COMPONENTS_PARAMETERS_TYPES = ["Melody", "AccompanimentChord", "AccompanimentArpeggiato", "Bass", "Drums"]

# Looks like is working for now
def testo():
    allowed_instruments = {
        "Melody": ["Acoustic Grand Piano"],
        "AccompanimentChord": ["Orchestral Harp", "Pizzicato Strings"],
        "AccompanimentArpeggiato": ["Timpani"],
        "Bass": ["Timpani"],
        "Drums": ["PlaceHolder"]
    }

    chosenInstruments = {
        field: choice(allowed_instruments[field]) for field in COMPONENTS_PARAMETERS_TYPES
    }

    scale = ScaleSpecs()

    sectionSpecs = SectionSpecs(Scale=scale, ComponentsParameters=[1, 1, 0, 1, 1], Instruments=chosenInstruments)
    section = Section("Intro", 0, sectionSpecs, 2)

    sections = [section]

    conn = ConnectToDB()
    rhythmicModelSpecs = conn.QueryTableForAll("RhythmicModel")
    rhythmicPresetSpecs = conn.QueryTableForAll("RhythmicPreset")

    rm = RhythmicModel(rhythmicModelSpecs[0])
    rp = RhythmicPreset(rhythmicPresetSpecs[0])

    # Get the generators
    ##### PROBLEM
    # should I just extract the methods to generate rhythm and notes?

    rhythmGenerators = {
        field: rp for field in COMPONENTS_PARAMETERS_TYPES
    }
    rhythmGenerators["Melody"] = rm
    notesGenerators = {}

    notesGen = RandomPicker({})
    """
    notesGen.InitializeModelFromPayload(
        {
            "DecayFactor": 0.75
        }
    )
    """

    for section in sections:
        # here I can put all the setup:
        # notes selection, getting generators from pool...
        allowedNotes = section.Scale.GetScaleNotes()
        nbBars = 4
        rhythmicPayload = {
            "Pattern": [0, 0, 1, 0],
            "NbBeats": 4
        }

        # Generate Rhythm
        for comp in section.Components:
            currRhythmGenerator = rhythmGenerators[comp.Type]
            GenerateRhythm(comp, currRhythmGenerator, rhythmicPayload, nbBars)

        # then generate notes in similar fashion
        melodicComponent = list(filter(
            lambda x: x.Type == "Melody",
            section.Components
        ))
        if len(melodicComponent) > 0:
            melodicComponent = melodicComponent[0]

        for comp in section.Components:
            currNotesGenerator = notesGen
            #currNotesGenerator = notesGenerators[comp.Type]
            GenerateNotes(comp, currNotesGenerator, allowedNotes, melodicComponent)

    return sections
