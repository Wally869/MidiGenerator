
from Data.ChordsProgressions import * 

from MusiStrata.Rendering import Play
from MusiStrata.Components import Scale

from MusiStrata.Enums import ScaleChordExtension as sce

# class aliasing  

ch_prog = canon  


s = Scale("A", ch_prog.Mode)  

notes = s.GetScaleNotes(4)


temp = s.GetChordsNotes(4, [[], [sce.Seventh], [sce.Eleventh], [], [], [], []])
# temp = s.GetSingleChord(4, [sce.Seventh])

ch_notes = [temp[i] for i in ch_prog.Tones]
del temp


for ch in ch_notes:
    Play(ch)

