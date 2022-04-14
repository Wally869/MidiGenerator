from MusiStrata.Enums import NoteNames
from MusiStrata import Note, Chord, Scale
from MusiStrata.Components import *

from MusiStrata.Rendering import Render, RenderFormats

sc = Scale("A", "Major")

tones = [0, 4, 5, 3]

# bass will be chords for 4 beats 
chords = [sc.GetSingleChord(t) for t in tones]
sc_notes = [sc.GetScaleNotes(4)[t] for t in tones]

# now can create bass 
track = Track(Name="Bass")

for id_bar in range(len(tones)):
    notes, _ = chords[id_bar](sc_notes[id_bar], [(0, 0), (1, 0), (0, 1)])
    sound_events = GenerateSoundEventsFromListNotes(0.0, 4.0, notes)
    track.append(Bar(sound_events))


song = Song(Tracks=[track])

Render(song, "test.mid", RenderFormats.MIDI)

