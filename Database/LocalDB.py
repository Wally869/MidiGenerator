from __future__ import annotations

from InitDB import InitializeDatabase

from tinydb import TinyDB, Query, where

from os.path import exists

from typing import List, Tuple

DATABASE_PATH = "db.json"


# Overloading the TinyDB object to be able to get a Query object from a connection
# makes more sense to be able to create a query wherever the db is used, instead of
# having to import Query every time it's needed
class ExtendedTinyDB(TinyDB):
    @staticmethod
    def GetQueryObject():
        return Query()

    def QueryTableForFields(self, tableName: str, fields: List[Tuple]):
        """
        Function to be added as method to the TinyDB object for better search of DB
        by
        """
        currTable = self.table(tableName)

        queries = []
        for idField in range(len(fields)):
            currField = fields[idField]
            print(currField)
            if type(currField[2]) == list and currField[1] == "in":
                # Best to handle this somewhere else? DB shouldn't be too big so is ok to do this
                # actually use query.type.any?
                addedQuery = "Query().{}.any({})".format(currField[0], currField[2])

            else:
                if type(currField[2]) == int or type(currField[2]) == float or type(currField[2]) == list:
                    addedQuery = 'where("{}") {} {}'.format(
                        str(currField[0]), str(currField[1]), currField[2]
                    )
                else:
                    addedQuery = 'where("{}") {} "{}"'.format(
                        str(currField[0]), str(currField[1]), currField[2]
                    )

            queries.append(addedQuery)

        strQuery = ""
        for i, query in enumerate(queries):
            strQuery += query
            if i != len(queries) - 1:
                strQuery += " and "

        results = currTable.search(eval(strQuery))

        # Here I would like to operate on tags
        return results


def ConnectToDB(dbPath: str = DATABASE_PATH):
    if not exists(dbPath) and dbPath == DATABASE_PATH:
        InitializeDatabase(dbPath)
    conn = ExtendedTinyDB(dbPath)
    return conn


def testQueryTable():
    conn = ConnectToDB()
    resp1 = conn.QueryTableForFields("DrumsBeatColorer", [("Name", "==", "TestBeats")])
    print("resp1: {}".format(resp1))
    print()
    resp2 = conn.QueryTableForFields("DrumsBeatColorer", [("Name", "==", "TestBeats"), ("NbBeats", "==", 4)])
    print("resp2: {}".format(resp2))
    print()
    resp3 = conn.QueryTableForFields("DrumsBeatColorer", [("Name", "==", "TestBeats"), ("NbBeats", "==", "4")])
    print("resp3: {}".format(resp3))
    print()
    resp4 = conn.QueryTableForFields("DrumsBeatColorer", [("NbBeats", "==", 4)])
    print("resp4: {}".format(resp4))
    print()
    resp5 = conn.QueryTableForFields("DrumsBeatColorer", [("NbBeats", "==", "4")])
    print("resp5: {}".format(resp5))
    print()
    resp6 = conn.QueryTableForFields("DrumsBeatColorer", [("Tags", "in", ['Test', 'New'])])
    print("resp6: {}".format(resp6))
    resp7 = conn.QueryTableForFields("DrumsBeatColorer", [("Tags", "==", ['Test', 'New'])])
    print("resp7: {}".format(resp7))
    resp8 = conn.QueryTableForFields("DrumsBeatColorer", [("Tags", "==", ['Test'])])
    print("resp8: {}".format(resp8))
    resp9 = conn.QueryTableForFields("DrumsBeatColorer", [("NbBeats", "==", 4), ("Tags", "in", ['Test', 'New'])])
    print("resp9: {}".format(resp9))


if __name__ == "__main__":
    testQueryTable()
