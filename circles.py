

from MusiStrata import *

# first start with circle of thirds
scale = Scale()
notesNames = scale.GetScaleNotesNames()[:-1]
notes = scale.GetScaleChordsNotes(4)


def GenerateCircle(scale: Scale, circleIndexing: int = 2, initialIndex: int = 0):
    assert(circleIndexing > 0)
    notes = scale.GetScaleChordsNotes()
    keys = []
    while True:
        if initialIndex >= len(notes):
            initialIndex -= len(notes)
        if initialIndex < 0:
            initialIndex += len(notes)
        keys.append(notes[initialIndex])
        initialIndex += circleIndexing
        if (len(keys) > 1 and keys[-1] == keys[0]):
            break
    return keys


keys = GenerateCircle(Scale("C", "Minor"), 3, 0)

track = Track()
for elem in keys:
    track.append(Bar(GenerateSoundEventsFromListNotes(0.0, 3.0, elem)))

s = Song(60, 3, [track])
Rendering.Render(s, "circles4.mid", Rendering.RenderFormats.MIDI)
