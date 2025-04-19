from tldb import TLDB
from tlsync_cot_rescu import SyncCotRescu

class TL:

    def isDBAlive():
        try:
            TLDB()
            return True
        except Exception:
            return False

    def getAllSources():
        with TLDB() as db:
            return db.getSources()

    def getEntitiesBySource(sourceID):
        with TLDB() as db:
            return db.getEntitiesBySource(sourceID)

    def getEntitiesNearby(geo_rad, geo_lat, geo_lon):
        with TLDB() as db:
            return db.getEntityNearby(geo_rad, geo_lat, geo_lon)
        
    def invokeSync(source):
        sources = {
            "cot-rescu":SyncCotRescu
        }
        sync = sources.get(source)()
        return sync.sync()