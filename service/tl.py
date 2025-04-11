from tldb import TLDB;

class TL:

    def getAllSources():
        with TLDB() as db:
            return db.getSources()

    def getEntitiesBySource(sourceID):
        with TLDB() as db:
            return db.getEntitiesBySource(sourceID)