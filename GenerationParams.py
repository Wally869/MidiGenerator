from __future__ import annotations

from enum import Enum
# from utils import CustomList

from typing import List


class TrackType(Enum):
    Melody = 0
    Accompaniment = 1
    Bass = 2
    Drums = 3


class SongParams(object):
    NbBeats = 4
    MinimumLengthSong = 80
    MaximumLengthSong = 120




class TrackParams(object):
    TrackTypes = []

    def __init__(self, trackTypes: List[TrackType]):
        self.TrackTypes = trackTypes
