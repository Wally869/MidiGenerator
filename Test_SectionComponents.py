from __future__ import annotations

from MidiStructurer import *
from SectionComponents import *

from random import choice

COMPONENTS_PARAMETERS_TYPES = ["Melody", "AccompanimentChord", "AccompanimentArpeggiato", "Bass", "Drums"]


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
    return section
