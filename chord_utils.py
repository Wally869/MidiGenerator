from typing import List

from MusiStrata import Note, SoundEvent

from itertools import permutations


def arpeggiate(notes: List[Note], initial_beat: float = 0.0, delta: float = 0.1, sustain_time: float = 4.0, stop_together: bool = True) -> List[SoundEvent]:
    """
        Create an arpeggio from a list of notes.
        Delta is the interval of time in beats between notes.
        stop_together determines if all notes should be release at the same time. 
    """
    output: List[SoundEvent] = []
    for id_note in range(len(notes)):
        if stop_together:
            output.append(SoundEvent(
                beat=initial_beat + delta * id_note,
                duration=sustain_time - delta * id_note,
                note=notes[id_note]
            ))
        else:
            output.append(SoundEvent(
                beat=initial_beat + delta * id_note,
                duration=sustain_time,
                note=notes[id_note]
            ))

    return output


def minimize_chords_distance(chord_1: List[Note], chord_2: List[Note], pad: bool = True) -> List[Note]:
    """
        Minimize pair-wise distance between chords. 
        Route to private functions 
    """
    if len(chord_1) == len(chord_2):
        return _minimize_chords_distance_same_len(chord_1, chord_2)
    elif pad:
        return _minimize_chords_distance_diff_len_padded(chord_1, chord_2)
    else:
        return _minimize_chords_distance_diff_len_no_padded(chord_1, chord_2)


def _minimize_chords_distance_diff_len_padded(chord_1: List[Note], chord_2: List[Note]) -> List[Note]:
    raise NotImplementedError()


def _minimize_chords_distance_diff_len_no_padded(chord_1: List[Note], chord_2: List[Note]) -> List[Note]:
    raise NotImplementedError()


def _minimize_chords_distance_same_len(chord_1: List[Note], chord_2: List[Note]) -> List[Note]:
    """
        Minimize pair-wise distance between chords with the same number of elements 
    """
    # find all permutations of notes in chord_2
    perms = list(permutations(chord_2))
    distance_scores = []
    for perm in perms:
        distance_scores.append(sum(
            [
                chord_1[i].get_circle_distance(perm[i])
                for i in range(len(chord_1))
            ]
        ))

    # out chord is the one that minimises pairwise distance using note names
    out_chord = list(perms[distance_scores.index(min(distance_scores))])

    # Now need to adjust height to minimize height distance
    for id_note in range(len(out_chord)):
        while out_chord[id_note].height - chord_1[id_note].height > 6:
            out_chord[id_note] -= 12
        while out_chord[id_note].height - chord_1[id_note].height < -6:
            out_chord[id_note] += 12

    return out_chord


from MusiStrata import Chord, Bar, Rendering
notes = Chord("m")(Note() - 12) + Chord("m7")(Note())
bar = Bar(
    arpeggiate(notes, 0.0, 0.1, 4.0)
)
print(bar.SoundEvents)

Rendering.Render(
    bar.to_song(beats_per_bar=4, instrument="Orchestral Harp"),
    "arpegiate.mid",
    Rendering.RenderFormats.MIDI
)
