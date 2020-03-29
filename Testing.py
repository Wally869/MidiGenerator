from RhythmicModelLoader import *
from RhythmicPresetLoader import *

from NotePickerModels.DistancePicker import DistancePicker

from MidiStructurer.Components import SongSegment, Scale, Track
from MidiStructurer.CircleOfFifths import GetAllowedScales
from MidiStructurer.ScalesUtils import GeneratePentatonicScaleNotesWithOctaveDelta, ALL_NOTES

from random import choice

# pass generator to this GenerateMelodyFunction
def GenerateMelodicTrack(nbBeats: int = 4,
                   nbBarsPerSection: int = 6,
                   nbPossiblePresetsPerSection: int = 4,
                   nbSections: int = 6,
                   targetBarLength: int = 30):
    rhythmGenerator = LoadSingleRhythmicModel("RhythmicModelsSpecs/test.json")

    # Generating segments of the song
    songSegments = []
    for _ in range(nbSections):
        presetsSection = rhythmGenerator.GenerateMultipleBars(nbPossiblePresetsPerSection, nbBeats)
        # how do they chain? here is defined
        sectionBars = []
        for _ in range(nbBarsPerSection):
            sectionBars.append(
                choice(presetsSection)
            )

        songSegments.append(
            SongSegment(
                Bars=sectionBars
            )
        )

    mainScale = Scale(
        RefNote=choice(ALL_NOTES),
        Mode=choice(["Minor", "Major"])
    )

    allowedScales = GetAllowedScales(mainScale)

    for s in songSegments:
        s.ScaleSegment = choice(allowedScales)

    notePicker = DistancePicker(
        {
            "DecayFactor": 0.7
        }
    )

    chosenOctave = choice([4, 5])
    chosenOctave = 5
    for s in songSegments:
        allowedNotes = GeneratePentatonicScaleNotesWithOctaveDelta(s.ScaleSegment)
        for idBar in range(len(s.Bars)):
            for idNote in range(len(s.Bars[idBar].Notes)):
                noteChosen = choice(allowedNotes)
                if idBar == 0 and idNote == 0:
                    noteChosen = choice(allowedNotes)
                else:
                    noteChosen = notePicker.ChooseNextNote(noteChosen["noteName"], allowedNotes)

                currNote = s.Bars[idBar].Notes[idNote]
                currNote.NoteName = noteChosen["noteName"]
                currNote.Octave = chosenOctave + noteChosen["octaveDelta"]
                # just to make sure
                s.Bars[idBar].Notes[idNote] = currNote


    track = Track(Name="Melodic", Instrument="Orchestral Harp")

    allChosenScales = []
    while len(track.Bars) < targetBarLength:
        seg = choice(songSegments)
        track.Bars += seg.Bars
        for _ in seg.Bars:
            allChosenScales.append(seg.ScaleSegment)


    return track, allChosenScales


def GetCommonNotesScales(s1: Scale, s2: Scale) -> List[str]:
    from MidiStructurer.ScalesUtils import GeneratePentatonicScale
    notes_s1 = set(
        GeneratePentatonicScale(s1)
    )
    notes_s2 = set(
        GeneratePentatonicScale(s2)
    )

    commonNotes = set(notes_s1).intersection(set(notes_s2))
    return list(commonNotes)

def EnsureMelodicConsistency(mTrack: Track, scales: List[Scale]) -> Track:
    bars = mTrack.Bars
    for id_bar in range(len(bars) - 1):
        # preventing error if no notes on one or both of two following bars
        if len(bars[id_bar].Notes) > 0 or len(bars[id_bar].Notes) + 1 > 0:
            commons = GetCommonNotesScales(scales[id_bar], scales[id_bar + 1])
            if bars[id_bar].Notes[-1].NoteName not in commons:
                bars[id_bar].Notes[-1].NoteName = choice(commons)




from BeatPresetLoader import BeatPreset, LoadSingleBeatPreset

def GenDrumsTrack(targetLen: int):
    beatPreset = LoadSingleBeatPreset("BeatPresetsSpecs/test.json")

    rhythmGenerator = LoadSingleRhythmicModel("RhythmicModelsSpecs/test.json")
    presetsSection = rhythmGenerator.GenerateMultipleBars(4, 4)
    # how do they chain? here is defined
    sectionBars = []
    for _ in range(8):
        sectionBars.append(
            choice(presetsSection)
        )

    generatedRhythm = []
    while len(generatedRhythm) < targetLen:
        for s in sectionBars:
            generatedRhythm.append(s)


    generatedRhythm = generatedRhythm[:targetLen]
    drumsTrack = Track(
        Name="DrumsTrack",
        Bars=generatedRhythm,
        IsDrumsTrack=True
    )

    beatPreset.PrepareTrack(drumsTrack)
    return drumsTrack


from TracksGenerators import *
from MidiStructurer.MidoConverter import ConvertSong

def JustDoIt():
    m, scales = GenerateMelodicTrack()
    m.Instrument = "Acoustic Grand Piano"
    EnsureMelodicConsistency(m, scales)

    t = GenerateCompingTrack(m, scales)
    t.Instrument = m.Instrument
    t.Instrument = "Acoustic Grand Piano"
    t.Velocity = int(m.Velocity * 0.75)

    d = GenDrumsTrack(len(m.Bars))
    d.Velocity = int(m.Velocity * 0.6)
    song = Song(Tracks=[m, d, t])
    #song = Song(Tracks=[m])

    s = ConvertSong(song, "ayaya.mid")
    return s

if __name__ == "__main__":
    JustDoIt()