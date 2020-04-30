from __future__ import annotations

from MidiStructurer import *
from SectionComponents import *
from Database.LocalDB import *
from RhythmicGenerators import RhythmicPreset, RhythmicModel

from MelodicModels.RandomPicker import RandomPickerMelodic
from AccompanimentModels.ChordPicker import ChordPicker

from random import choice

COMPONENTS_PARAMETERS_TYPES = ["Melody", "AccompanimentChord", "AccompanimentArpeggiato", "Bass", "Drums"]


# Looks like is working for now
# WAIT UP
# can have NO distinction between accompaniment models and melodic models?
# also can use a kwarg UseDependency, to allow 2 behaviour from accompaniment model?
def testo():
    allowedInstruments = {
        "Melody": ["Acoustic Grand Piano"],
        "AccompanimentChord": ["Orchestral Harp", "Pizzicato Strings"],
        "AccompanimentArpeggiato": ["Timpani"],
        "Bass": ["Alto Sax"],
        "Drums": ["PlaceHolder"]
    }

    chosenInstruments = {
        field: choice(allowedInstruments[field]) for field in COMPONENTS_PARAMETERS_TYPES
    }

    scale = ScaleSpecs()

    sectionSpecs = SectionSpecs(Scale=scale, ComponentsParameters=[1, 1, 0, 1, 1], Instruments=chosenInstruments)
    section = Section("Intro", 0, sectionSpecs, 2)

    sections = [section]

    # Get Rhythmic Generator settings from Database
    conn = ConnectToDB()
    rhythmicModelSpecs = conn.QueryTableForAll("RhythmicModel")
    rhythmicPresetSpecs = conn.QueryTableForAll("RhythmicPreset")

    # Generate the Rhythmic models from the settings
    rm = RhythmicModel(rhythmicModelSpecs[0])
    rp = RhythmicPreset(rhythmicPresetSpecs[0])

    rhythmGenerators = {
        field: rp for field in COMPONENTS_PARAMETERS_TYPES
    }
    rhythmGenerators["Melody"] = rm

    # placeholder: using RandomPicker model
    rp = RandomPickerMelodic({})
    melodyGenerators = {
        field: rp for field in COMPONENTS_PARAMETERS_TYPES
    }

    melodyGenerators["AccompanimentChord"] = ChordPicker(
        {
            "AllowedChords": [
                Chord(
                    [
                        Interval(3, "Major"),
                        Interval(5, "Perfect")
                    ]
                ),
                Chord(
                    [
                        Interval(3, "Minor"),
                        Interval(5, "Perfect")
                    ]
                )
            ],
            "BeatsPicked": "First",
            "RootInOutput": True
        }
    )
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
        allowedNotes = section.Scale.GetScaleNotes(referenceOctave=4)
        nbBars = 4
        nbBeats = 4
        pattern = [0, 0, 1, 0]
        rhythmicPayload = {
            "Pattern": [0, 0, 1, 0],
            "NbBeats": 4
        }

        # Generate Rhythm
        for comp in section.Components:
            currRhythmGenerator = rhythmGenerators[comp.Type]
            # print(comp.Type, currRhythmGenerator)
            comp.Bars = currRhythmGenerator(nbBars=nbBars, nbBeats=nbBeats, pattern=pattern)

        # then generate notes in similar fashion
        melodicComponent = list(filter(
            lambda x: x.Type == "Melody",
            section.Components
        ))
        if len(melodicComponent) > 0:
            melodicComponent = melodicComponent[0]
        else:
            melodicComponent = None

        for comp in section.Components:
            currNotesGenerator = melodyGenerators[comp.Type]
            currNotesGenerator(comp.Bars, allowedNotes, DependencyBars=melodicComponent.Bars)

    return sections


def testoToSong(sections):
    if len(sections) > 1:
        raise NotImplementedError("Not Implemented yet for more than 1 section")
    section = sections[0]
    s = Song()
    for comp in section.Components:
        t = Track(
            Instrument=comp.Instrument,
            IsDrumsTrack=(comp.Type == "Drums"),
            Bars=comp.Bars
        )
        s.Tracks.append(t)
    MidoConverter.ConvertSong(s, "testonew.mid")


if __name__ == "__main__":
    sections = testo()
    testoToSong(sections)
