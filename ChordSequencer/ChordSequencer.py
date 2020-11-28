from typing import List, Dict

from MusiStrata.Components import *
from MusiStrata import MidoConverter

from random import choice, shuffle

"""
Doing this as script first, rewrite later

"""

majTriad = ChordsLibrary.GetChordFromName("Major Triad")
minTriad = ChordsLibrary.GetChordFromName("Minor Triad")

majSeventh = ChordsLibrary.GetChordFromName("Major Seventh")
minSeventh = ChordsLibrary.GetChordFromName("Minor Seventh")



# song settings
tempo = 80
beatsPerBar = 4
barsToGenerate = 4

melodyVelocity = 60
bassVelocity = 30

repeatSegment = True

# instruments
instrumentMelody = "Orchestral Harp"
instrumentBass = "Acoustic Grand Piano"


allowedChords = [minTriad, majTriad, majSeventh, minSeventh]
bassDistance = Interval(8, "Perfect")  # we'll put the bass one octave below

referenceNote = Note("C", 5)
# create array of ref Notes?
refNotes = [Note("C", 5), Note("D", 5), Note("E", 5), Note("F", 5)]


trackMelodic = Track(Name="Melodic", Instrument=instrumentMelody)    # track for our flattened chord
trackHarmonic = Track(Name="Harmonic", Instrument=instrumentBass)    # track for chord unflattened (bass)

for _ in range(barsToGenerate):
    barMelodic = Bar()
    barHarmonic = Bar()
    
    #chordNotes, errors = choice(allowedChords)(referenceNote)
    chordNotes, errors = choice(allowedChords)(choice(refNotes))
    # we can create a solution to the knapsack problem of fitting notes durations in a bar
    # maybe create couple position/duration, and pop from it?
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
        # setting notes and related soundevents in barHarmonic
        currNote, _ = chordNotes[idNote] - bassDistance
        se = SoundEvent(Beat=0.0, Duration=beatsPerBar, Note=currNote, Velocity=bassVelocity)
        barHarmonic.append(se)
        # now in melody
        # selecting random note
        currNote = chordNotes[availableIds.pop()]
        loc = couples[idNote]  # get location of sound event (beat and duration)
        se = SoundEvent(Beat=loc[0], Duration=loc[1], Note=currNote, Velocity=melodyVelocity)
        barMelodic.append(se)
    trackMelodic.append(barMelodic)
    trackHarmonic.append(barHarmonic)


# repeat segment in bars?
if repeatSegment:
    trackHarmonic.append(trackHarmonic.Bars)
    trackMelodic.append(trackMelodic.Bars)
    
s = Song(Tempo=tempo, BeatsPerBar=beatsPerBar, Tracks=[trackMelodic, trackHarmonic])
MidoConverter.ConvertSong(s, "ChordSequencer.mid")