from MusiStrata.Rendering import NotePlayer
from MusiStrata import *

from RhythmGenerator2 import *

from Utils import flatten

import json

# reading the data from the file
with open('RhythmicPresetsSpecs/test3.json') as f:
    data = f.read()

js = json.loads(data)


rg = RhythmPresetGenerator.from_dict(
    js
)


pattern = rg.gen_pattern([PresetPart.Main, PresetPart.Main], 3)

# extend
sc = Scale("C", "Major")

chords = sc.get_scale_chords()

progression = [0, 3, 4]

bars: List[Bar] = []



for id_progression in range(len(progression)):
    base_note_id = progression[id_progression]
    current_pattern = pattern[id_progression]
    ses = []
    for id_rhythm_elem in range(len(current_pattern)):
        rhythm_elem = current_pattern[id_rhythm_elem]
        if id_rhythm_elem == 0:
            notes = chords[base_note_id](sc.get_note(base_note_id))
            se = SoundEvent.FromNotes(
                rhythm_elem.beat, rhythm_elem.duration, notes
            ) 
            ses += se
        else:
            notes = chords[base_note_id](sc.get_note(base_note_id) + 12, 0)
            se = SoundEvent.FromNotes(
                rhythm_elem.beat, rhythm_elem.duration, notes
            ) 
            ses += se
    bars.append(
        Bar(ses)
    )


"""
bars = [Bar(flatten([
    SoundEvent.FromNotes(
        rhythm_elem.beat, rhythm_elem.duration, notes
    ) for rhythm_elem in pattern_elem
])) for pattern_elem in pattern]
"""

#NotePlayer.PlayBars(bars)
#Rendering.Play(bars, tempo=120)

song = Track(Bars=bars).to_song(80, 3)
Rendering.Render(song, "test.mid", Rendering.RenderFormats.MIDI)


