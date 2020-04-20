import dbSpells as dbsp
import feats
import formatInfo
import os
import races
import re
import spells
import sqlite3
import string
import sys

class DatabaseError(Exception): pass
class DnD_DB:
    __pathDB = "Database/"
    __pathData = __pathDB+"Data/"
    __pathSQL = __pathDB+"SQL/"
    __schools = None
    __sizes = None
    __sfxs = ("st", "nd", "rd", "th", "th", "th", "th", "th", "th", "th")
    def __init__(self):
        dbsp.getSchoolIndex = self.getSchoolIndex
        spells.getSchoolIndex = self.getSchoolIndex
        races.getSizeIndex = self.getSizeIndex
        if not os.path.isfile(self.__pathDB+"DnD_5e.db"):
            self.db = sqlite3.connect(self.__pathDB+"DnD_5e.db")
            self.install(self.__pathSQL+"tables.sql")
            print("Set up database tables.")
            self.install(self.__pathSQL+"references.sql")
            print("Installed references.")
            self.__schools = self.db.execute("select school from spellSchools")
            self.__schools = tuple([ii[0] for ii in self.__schools.fetchall()])
            self.__sizes = self.db.execute("select ct_size from creatureSizes")
            self.__sizes = tuple([ii[0] for ii in self.__sizes.fetchall()])
            for ii in ["abcde", "fghij", "klmno", "pqrstu", "vwxyz"]:
                self.install(self.__pathData+"phb_"+ii[0]+"-"+ii[-1]+".sp")
                print("Installed spells "+ii[0]+"-"+ii[-1]+" from the PHB.")
            self.install(self.__pathData+"xge_ee_scag.sp")
            print("Installed spells from XGE, EE, and SCAG.")
            self.install(self.__pathData+"homebrew.sp")
            print("Installed homebrew spells.")
            self.install(self.__pathSQL+"feats.sql")
            print("Installed feats.")
            self.install(self.__pathSQL+"feats_racial.sql")
            print("Installed racial feats.")
            self.install(self.__pathSQL+"races.sql")
            print("Installed races.")
        else:
            self.db = sqlite3.connect(self.__pathDB+"DnD_5e.db")
            self.__schools = self.db.execute("select school from spellSchools")
            self.__schools = tuple([ii[0] for ii in self.__schools.fetchall()])
            self.__sizes = self.db.execute("select ct_size from creatureSizes")
            self.__sizes = tuple([ii[0] for ii in self.__sizes.fetchall()])
    def install(self, filename):
        if filename.endswith(".sp"):
            self.db.executescript(dbsp.load(filename))
        elif filename.endswith(".sql"):
            fin = open(filename, "r", encoding="utf8")
            string = ""
            for ii in fin:
                string += ii
            fin.close()
            self.db.executescript(string)
        else:
            raise DatabaseError("Tried to install invalid script: "+filename)
    def close(self):
        self.db.close()
    def query(self, table, command):
        if table == "feats":
            cmd, params = feats.interpret(feats.feats.compile(command), [])
            return self.db.execute(cmd, params).fetchall()
        if table == "races":
            cmd, params = races.interpret(races.races.compile(command), [])
            return self.db.execute(cmd, params).fetchall()
        if table == "sources":
            string = "select * from sources where abbr=?"
            return self.db.execute(string, (command,)).fetchall()
        if table == "spells":
            cmd, params = spells.interpret(spells.spells.compile(command), [])
            return self.db.execute(cmd, params).fetchall()
        return self.db.execute(command).fetchall()
    def export(self):
        path = "Database/Data/"
        query = "select * from spells where lower(sp_name) like \"{}\""
        query += " and instr(sp_src, \"PHB\")"
        for ii in ["abcde", "fghij", "klmno", "pqrstu", "vwxyz"]:
            with open(path+"phb_"+ii[0]+"-"+ii[-1]+".sp", "w") as fout:
                for jj in ii:
                    spells = self.db.execute(query.format(jj+"%")).fetchall()
                    spells = [formatInfo.spellEntry(self, kk) for kk in spells]
                    fout.write("".join(spells))
        query = "select * from spells where instr(sp_src, \"XGE\")"
        query += "or instr(sp_src, \"EE\") or instr(sp_src, \"SCAG\")"
        with open(path+"xge_ee_scag.sp", "w") as fout:
            spells = self.db.execute(query).fetchall()
            spells = [formatInfo.spellEntry(self, jj) for jj in spells]
            fout.write("".join(spells))
        query = "select * from spells where not instr(sp_src, \"PHB\")"
        query += "and not instr(sp_src, \"XGE\") and not instr(sp_src, \"EE\")"
        query += "and not instr(sp_src, \"SCAG\")"
        with open(path+"homebrew.sp", "w") as fout:
            spells = self.db.execute(query).fetchall()
            spells = [formatInfo.spellEntry(self, jj) for jj in spells]
            fout.write("".join(spells))
    def getSfx(self, number):
        return self.__sfxs[number]
    def getSchoolString(self, index):
        return self.__schools[index]
    def getSchoolIndex(self, string):
        return self.__schools.index(string.lower())
    def getSizeString(self, index):
        return self.__sizes[index].capitalize()
    def getSizeIndex(self, string):
        return self.__sizes.index(string.lower())


