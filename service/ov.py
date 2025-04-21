from ovdb import OVDB
from ovsync_cot_rescu import SyncCotRescu
from ovsync_york_yrtraffic import SyncYRT

class OV:

    def isDBAlive():
        try:
            OVDB()
            return True
        except Exception:
            return False

    def getAllSources():
        with OVDB() as db:
            return db.getSources()

    def getEntitiesBySource(sourceID):
        with OVDB() as db:
            return db.getEntitiesBySource(sourceID)

    def getEntitiesNearby(geo_rad, geo_lat, geo_lon):
        with OVDB() as db:
            return db.getEntityNearby(geo_rad, geo_lat, geo_lon)
        
    def invokeSync(source):
        sources = {
            "cot-rescu":SyncCotRescu,
            "york-traffic":SyncYRT
        }
        sync = sources.get(source)()
        return sync.sync()