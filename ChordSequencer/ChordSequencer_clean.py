from typing import List, Dict

from MusiStrata.Components import *
from MusiStrata import MidoConverter

from random import choice, shuffle





def GenerateMelodicSegmentFromChordSequence(referenceNote: Note, chords: List[Chord], beatsPerBar: float = 4.0, instrument: str = "Acoustic Grand Piano"):
    track = Track(Instrument=instrument)
    for ch in chords:
        bar = Bar()
        chordNotes, err = ch(referenceNote)

        # replace by knapsacking / using a generative model?
        if len(chordNotes) == 3:
            if beatsPerBar == 3:
                couples = [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0)]
            else:
                # assuming 4 beats
                # hardcoding for now, will do something smarter later
                couples = [(0.0, 2.0), (2.0, 1.0), (3.0, 1.0)]
        else:
            # assuming 4 chord notes
            if beatsPerBar == 4:
                couples = [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)]
            else:
                couples = [(0.0, 1.0), (2.0, 1.0), (3.0, 0.5),  (3.5, 0.5)] 

        availableIds = list(range(len(chordNotes)))
        shuffle(availableIds)
        for idNote in range(len(chordNotes)):
            currNote = chordNotes[availableIds.pop()]
            loc = couples[idNote]  # get location of sound event (beat and duration)
            se = SoundEvent(Beat=loc[0], Duration=loc[1], Note=currNote)
            bar.append(se)
        track.append(bar)
    return track


def GenerateHarmonicSegmentFromChordSequence(referenceNote: Note, chords: List[Chord], beatsPerBar: float = 4.0, instrument: str = "Acoustic Grand Piano"):
    track = Track(Instrument=instrument)
    for ch in chords:
        bar = Bar()
        chordNotes, err = ch(referenceNote)
        for currNote in chordNotes:
            # setting notes and related soundevents in barHarmonic
            se = SoundEvent(Beat=0.0, Duration=beatsPerBar, Note=currNote)
            bar.append(se)
        track.append(bar)
    return track
        
        
if __name__ == "__main__":
    print("testing")
    # test values
    majTriad = ChordsLibrary.GetChordFromName("Major Triad")
    minTriad = ChordsLibrary.GetChordFromName("Minor Triad")
    majSeventh = ChordsLibrary.GetChordFromName("Major Seventh")
    minSeventh = ChordsLibrary.GetChordFromName("Minor Seventh")
    allowedChords = [minTriad, majTriad, majSeventh, minSeventh]
    referenceNote = Note("C", 5)
    # generate melody
    t = GenerateMelodicSegmentFromChordSequence(referenceNote, allowedChords)
    t += t
    t.Instrument = "Orchestral Harp"
    t2 = GenerateHarmonicSegmentFromChordSequence(referenceNote - 12, allowedChords)
    t2 += t2
    s = Song(Tracks=[t, t2])
    MidoConverter.ConvertSong(s, "test.mid")
