from __future__ import annotations

from LocalDB import ConnectToDB

# Take MainParameters object as input for main function
# put placeholder for now for annotations

# Only possible for verse/chorus format?
SongSegments = [
    "Intro",
    "Verse",
    "PreChorus",
    "Chorus",
    "Bridge",
    "Outro"#, Solo

]


class MainParameters(object):
    ThroughComposed: bool = False


class Structure(object):
    pass


def MainGeneratorFunction(params: MainParameters):
    connDB = ConnectToDB()
    # get params from db?
    # from params, i get stuff from the db, to create the models used
    # ignore db for now

    structure = GenerateStructureSong(params)


