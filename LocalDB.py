from __future__ import annotations

from tinydb import TinyDB

from globals import DATABASE_PATH

def ConnectToDB(dbPath: str = DATABASE_PATH):
    conn = TinyDB(dbPath)
    return conn


