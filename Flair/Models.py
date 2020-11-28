from typing import List, Union

from MusiStrata import *

testBar = Bar(
    SoundEvents=[
        SoundEvent(0.0, 2.0, Note()),
        SoundEvent(2.0, 0.5, Note() + 7),
        SoundEvent(2.5, 0.5, Note() + 5),
        SoundEvent(3.0, 0.5, Note()),
    ]
    
)

# need information on length in seconds? Disregard for now I guess
def Trill(bar: Bar, positionToApply: int = 0, repetitions: int = 1, trillDuration: float = 0.5, isUpper: bool = True):
    se = bar.SoundEvents[0]
    noteDuration = se.Duration
    note = se.Note
    elapsed = 0
    
    newSE = []
    for i in range(repetitions):
        newSE.append(
            SoundEvent(
                Beat=(i*2)*trillDuration/2/repetitions,
                Duration=trillDuration/2/repetitions,
                Note=note
            )
        )
        if isUpper:
            newSE.append(
                SoundEvent(
                    Beat=(i*2 + 1)*trillDuration/repetitions/2,  # + trillDuration/repetitions/2,
                    Duration=trillDuration/2/repetitions,
                    Note=note+1
                )
            )
        else:
            newSE.append(
                SoundEvent(
                    Beat=(i*2 + 1)*trillDuration/repetitions/2,  # + trillDuration/repetitions/2,
                    Duration=trillDuration/2/repetitions,
                    Note=note-1
                )
            )
        """
        newSE.append(
            SoundEvent(
                Beat=2*trillDuration/3/repetitions * (i+1),
                Duration=trillDuration/3/repetitions,
                Note=note
            )
        )
        """

    # maybe threshold, so that no need to go back to base note if duration too low
    if trillDuration < noteDuration:
        newSE.append(
            SoundEvent(
                Beat=trillDuration,
                Duration=noteDuration-trillDuration,
                Note=note
            )
        )
    

    for se in bar.SoundEvents[1:]:
        newSE.append(se)

    b = Bar(SoundEvents=newSE)
    return b


outBar = Trill(testBar, repetitions=4, trillDuration=1.0, isUpper=False)
#NotePlayer.PlayBar(testBar)
#NotePlayer.PlayBar(outBar)
s = Song(Tracks=[Track(Bars=[outBar])])
MidoConverter.ConvertSong(s, "test.mid")
