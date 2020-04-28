from MidiStructurer import *

from copy import deepcopy
from random import random, choice

sample_rhythm = [
    {
        "beat": 0.0,
        "duration": 1.0
    },
    {
        "beat": 2.0,
        "duration": 1.0
    },
    {
        "beat": 3.0,
        "duration": 0.33
    },
    {
        "beat": 3.33,
        "duration": 0.33
    },
    {
        "beat": 3.66,
        "duration": 0.33
    }
]


def GenerateExample1():
    nbBars = 12
    sample = Bar(
        SoundEvents=[SoundEvent(Beat=s["beat"], Duration=s["duration"]) for s in sample_rhythm]
    )

    # 4 notes, let's say it does degrees I-IV-V-I
    scale = ScaleSpecs()
    degrees = [0, 3, 4, 3, 0]

    notes = scale.GetScaleNotes()
    for id_bar in range(len(degrees)):
        sample.SoundEvents[id_bar].Note = notes[degrees[id_bar]]

    t = Track(
        Bars=[sample for _ in range(nbBars)]
    )

    s = Song(
        Tracks=[t]
    )

    MidoConverter.ConvertSong(s, "example1.mid")


def GenerateExample2():
    nbBars = 12
    sample = Bar(
        SoundEvents=[SoundEvent(Beat=s["beat"], Duration=s["duration"]) for s in sample_rhythm]
    )

    # 4 notes, let's say it does degrees I-IV-V-I
    scale = ScaleSpecs()
    degrees = [0, 3, 7, 4, 0]

    scales = [scale] + scale.FindNeighbouringScales()
    scales = scales[:2]

    samples = []
    for id_bar in range(nbBars):
        newsample = deepcopy(sample)
        newid = id_bar
        while newid >= len(scales):
            newid -= len(scales)

        notes = scales[newid].GetScaleNotes()

        for id_note in range(len(degrees)):
            newsample.SoundEvents[id_note].Note = notes[degrees[id_note]]
        samples.append(newsample)

    t = Track(
        Bars=samples,
        Instrument="Glockenspiel"
    )

    samples2 = deepcopy(samples)
    for b in samples:
        for se in b.SoundEvents:
            n, err = se.Note + Interval(5, "Perfect")
            if err is not None:
                n, _ = se.Note + Interval(4, "Perfect")
            se.Note = n

    t2 = Track(
        Bars=samples2,
        Instrument="Glockenspiel"
    )

    s = Song(
        Tracks=[t, t2]
    )

    MidoConverter.ConvertSong(s, "example2.mid")


def GenerateSimpleStrophic():
    # simple example, wishing to create an atmospheric song
    # will have melodic, bass and drums tracks
    targetLen = 32

    # Generate simple rhythmic track
    rhythmicPreset = [
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
            "Duration": 1.0
        }
    ]

    rpBar = GenerateBarFromRhythmicPreset(rhythmicPreset)
    drumsTrack = Track(
        Bars=[rpBar],
        IsDrumsTrack=True
    )
    while len(drumsTrack.Bars) < targetLen:
        drumsTrack += drumsTrack

    # Will need to add a drums beat colourer (by that, I mean: beat X is that instrument, beat Y that one...)

    # NOW can generate melodic and bass
    targetSectionLen = 2
    melodyPreset1 = [
        {
            "Beat": 0.0,
            "Duration": 1.0
        },
        {
            "Beat": 1.0,
            "Duration": 1.0
        },
        {
            "Beat": 3.0,
            "Duration": 1.0
        }
    ]

    melodyPreset2 = [
        {
            "Beat": 0.0,
            "Duration": 1.0
        },
        {
            "Beat": 1.0,
            "Duration": 1.0
        },
        {
            "Beat": 2.0,
            "Duration": 0.5
        },
        {
            "Beat": 2.5,
            "Duration": 0.5
        },
        {
            "Beat": 3.0,
            "Duration": 1.0
        },
    ]

    melodyPresets = [
        melodyPreset1,
        melodyPreset2
    ]

    melodyPresets += melodyPresets

    mpBars = [
        GenerateBarFromRhythmicPreset(mp)
        for mp in melodyPresets
    ]

    # set notes
    # selectedIntervals = MINOR_MAJOR_PERFECT_INTERVALS
    selectedIntervals = [
        Interval(*i[:2])
        for i in MINOR_MAJOR_PERFECT_INTERVALS
    ]

    scaleType = choice(["Major", "Minor"])
    # only diatonic intervals
    scale = ScaleSpecs(
        RefNote="C",
        ScaleType=scaleType
    )

    if scaleType == "Major":
        notChosen = "Minor"
    else:
        notChosen = "Major"

    # intervals: keep to consonances
    selectedIntervals = list(filter(
        lambda x: x.Quality not in [notChosen, "Perfect"], selectedIntervals
    ))
    print("Allowed Intervals:")
    [print(interval) for interval in selectedIntervals]

    nbNotes = sum(
        [len(b.SoundEvents) for b in mpBars]
    )

    # allowedNotes = scale.GetScaleNotes()
    allowedNotes = scale.GetPentatonicScaleNotes()
    allowedNotes = ExtendScaleNotes(allowedNotes, 2)
    maxNote = allowedNotes[0] + 12
    minNote = allowedNotes[0] - 5

    while True:
        # start on first degree
        chosenNotes = [allowedNotes[0]]
        while len(chosenNotes) < nbNotes:
            while True:
                delta = choice([-1, 1])
                interval = choice(selectedIntervals)

                if delta > 0:
                    newNote, err = chosenNotes[-1] + interval
                else:
                    newNote, err = chosenNotes[-1] - interval

                if err is None:
                    break

            if maxNote >= newNote >= minNote:
                chosenNotes.append(newNote)

        # enforce ending on V
        chosenNotes[-1] = allowedNotes[4]
        if chosenNotes[-1] == allowedNotes[4]:
            break

    # set notes to bars
    currId = 0
    for b in mpBars:
        for se in b.SoundEvents:
            se.Note = chosenNotes[currId]
            currId += 1

    # set out to track
    melodicTrack = Track(
        Bars=mpBars,
        Instrument="Glockenspiel"
    )
    while len(melodicTrack.Bars) < targetLen:
        melodicTrack += melodicTrack

    bassPreset = [[
        {
            "Beat": 0.0,
            "Duration": 1.0
        },
        {
            "Beat": 2.0,
            "Duration": 1.0
        }
    ]]

    bassPreset += bassPreset

    bpBars = [
        GenerateBarFromRhythmicPreset(bp)
        for bp in bassPreset
    ]

    for i in range(len(bpBars)):
        newNote, err = mpBars[i].SoundEvents[0].Note - Interval(5, "Perfect")
        if err is not None:
            newNote, _ = mpBars[i] - Interval(5, "Perfect")

        for se in bpBars[i].SoundEvents:
            se.Note = newNote

    bassTrack = Track(
        Bars=bpBars,
        Instrument="Glockenspiel",
        Velocity=int(melodicTrack.Velocity * 0.75)
    )
    while len(bassTrack.Bars) < targetLen:
        bassTrack += bassTrack

    s = Song(
        Tracks=[melodicTrack, bassTrack, drumsTrack]
    )

    return s


def GenerateMultiChannelStrophicWithNoteInScaleRestriction():
    melodyPreset1 = [
        {
            "Beat": 0.0,
            "Duration": 1.0
        },
        {
            "Beat": 1.0,
            "Duration": 1.0
        },
        {
            "Beat": 3.0,
            "Duration": 1.0
        }
    ]

    melodyPreset2 = [
        {
            "Beat": 0.0,
            "Duration": 1.0
        },
        {
            "Beat": 1.0,
            "Duration": 1.0
        },
        {
            "Beat": 2.0,
            "Duration": 0.5
        },
        {
            "Beat": 2.5,
            "Duration": 0.5
        },
        {
            "Beat": 3.0,
            "Duration": 1.0
        },
    ]

    melodyPresets = [
        melodyPreset1,
        melodyPreset2 #,
        # melodyPreset1
    ]

    melodyPresets += melodyPresets

    mpBars = [
        GenerateBarFromRhythmicPreset(mp)
        for mp in melodyPresets
    ]

    scaleType = choice(["Major", "Minor"])
    #scaleType = "MinorMelodic"
    scale = ScaleSpecs(
        RefNote=choice(ALL_NOTES),  # "C",
        ScaleType=scaleType
    )

    allowedIntervals = CHROMATIC_AND_DIATONIC_INTERVALS
    """
    allowedIntervals = list(filter(
        lambda elem: (elem.Quality == scaleType or elem.Quality == "Perfect") and elem.IntervalNumber != 1, allowedIntervals
    ))
    """

    allowedIntervals = list(filter(
        lambda elem: (elem.Quality == scaleType or elem.Quality == "Perfect") and 1 < elem.IntervalNumber <= 5,
        allowedIntervals
    ))
    print("Allowed Intervals:")
    [print(interval) for interval in allowedIntervals]
    print()

    # allowedNotes = scale.GetPentatonicScaleNotes()
    allowedNotes = scale.GetPentatonicScaleNotes(mode=choice(ScaleModes.GetAllNames()))
    #allowedNotes = scale.GetScaleNotes(mode=choice(ScaleModes.GetAllNames()))
    #allowedNotes = scale.GetScaleNotes(mode="Phrygian")
    allowedNotes = ExtendScaleNotes(allowedNotes, 1)

    targetLen = sum(
        [
            len(elem.SoundEvents) for elem in mpBars
        ]
    )

    maxNote = allowedNotes[0] + 12
    minNote = allowedNotes[0]

    nbTries = 0
    while True:
        chosenNotes = [allowedNotes[0]]
        # chosenNotes = [choice(allowedNotes)]
        while len(chosenNotes) < targetLen:
            #potentialPositiveIntervals = chosenNotes[-1].GetValidIntervalsFromSelected(allowedIntervals, True)
            potentialPositiveIntervals = Interval.GetValidIntervals(
                chosenNotes[-1],
                allowedIntervals,
                True
            )
            #potentialNegativeIntervals = chosenNotes[-1].GetValidIntervalsFromSelected(allowedIntervals, False)
            potentialNegativeIntervals = Interval.GetValidIntervals(
                chosenNotes[-1],
                allowedIntervals,
                False
            )

            # get potential end notes on these intervals
            potentialNextNotes = [
                (chosenNotes[-1] + interval)[0] for interval in potentialPositiveIntervals
            ]
            potentialNextNotes += [
                (chosenNotes[-1] - interval)[0] for interval in potentialNegativeIntervals
            ]

            # Filter potentialNextNotes to only keep those in allowed Notes
            reducedNextNotes = list(filter(
                lambda x: x in allowedNotes, potentialNextNotes
            ))

            if len(reducedNextNotes) > 0:
                nextNote = choice(reducedNextNotes)
            else:
                nextNote = chosenNotes[-1] + 2

            chosenNotes.append(
                nextNote
            )

        nbTries += 1
        if nbTries >= 25:
            print("Didn't find a solution. Forced a valid end ")
            chosenNotes[-1] = allowedNotes[4]

        if chosenNotes[-1] == allowedNotes[4]:
            break

    # set notes to melodypresets bars
    currId = 0
    for b in mpBars:
        for se in b.SoundEvents:
            se.Note = chosenNotes[currId]
            currId += 1

    t = Track(
        Bars=mpBars,
        Instrument="Orchestral Harp"
    )


    tFrozen = deepcopy(t)
    for i in range(3):
        t += tFrozen

    accompBars = []
    interval = Interval(5, "Perfect")
    for bar in t.Bars:
        se = deepcopy(bar.SoundEvents[0])
        n, _ = se.Note + interval
        #n2 = se.Note + 8
        se1 = deepcopy(se)
        se1.Note = n
        #se2 = deepcopy(se)
        #se2.Note = n2
        accompBars.append(
            Bar(SoundEvents=[se1])#, se2])
        )

    taccomp = Track(
        Bars=accompBars,
        Instrument="Orchestral Harp",
        Velocity=40
    )

    rhythmicPreset = [
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
            "Duration": 1.0
        }
    ]

    rpBar = GenerateBarFromRhythmicPreset(rhythmicPreset)
    drumsTrack = Track(
        Bars=[rpBar],
        IsDrumsTrack=True
    )
    frozenDrums = deepcopy(drumsTrack)
    while len(drumsTrack.Bars) < len(t.Bars):
        drumsTrack += frozenDrums

    song = Song(
        Tracks=[t, taccomp, drumsTrack],
        Tempo=100
    )

    return song


if __name__ == "__main__":
    # GenerateExample1()
    # GenerateExample2()
    # s = GenerateSimpleStrophic()
    s = GenerateMultiChannelStrophicWithNoteInScaleRestriction()
    MidoConverter.ConvertSong(s, "strophic.mid")
