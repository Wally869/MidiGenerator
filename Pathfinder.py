from typing import List, Optional
from MusiStrata import Note, Scale, Interval

from dataclasses import dataclass


@dataclass
class NoteRange:
    """
        Inclusive range 
    """
    lower_bound: Optional[Note] = None
    upper_bound: Optional[Note] = None

    def is_note_in(self, note: Note) -> bool:
        return ((self.lower_bound is None) or (note >= self.lower_bound)) and ((self.upper_bound is None) or (note <= self.upper_bound))


def find_path(initial_note: Note, target_note: Note, path_len: int, scale: Optional[Scale], 
            allowed_intervals: List[Interval], allowed_range: Optional[NoteRange]) -> List[Note]:
    path = [None for _ in range(path_len)]
    path[0] = initial_note
    path[-1] = target_note

    for i in range(1, len(path_len) - 2):
        is_valid = True
        new_note = Note()
        if scale:
            if not scale.is_note_in_scale(new_note):
                is_valid = False
        if allowed_range:
            if not allowed_range.is_note_in(new_note):
                is_valid = False
        if is_valid:
            path[i] = new_note
    
    return path
