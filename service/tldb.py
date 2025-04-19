from os import environ
from mysql import connector
from json import loads

class TLDB():

    def __init__(self):
        self.db = connector.connect (
            user = environ['MYSQL_USER'],
            password = environ['MYSQL_PASSWORD'],
            host = environ['MYSQL_HOST'],
            database = environ['MYSQL_DATABASE']
        )

    def __enter__(self):
        return self
    
    def __exit__(self, exec_type, exec_value, exec_traceback):
        self.closeConnection()

    def closeConnection(self):
        self.db.close()

    # SOURCES
    def addSource(self, sourceName, sourceType, origin, origin_url):
        cursor = self.db.cursor()
        cursor.execute("CALL add_source(\"" + sourceName + "\",\"" + sourceType + "\",\"" + origin + "\",\"" + origin_url +"\", @new_id)")
        cursor.execute("SELECT @new_id")
        newID = cursor.fetchone()
        cursor.close()
        self.db.commit()

        while newID is not None:
            return newID
        

    def getSources(self):
        cursor = self.db.cursor()
        cursor.execute("CALL get_sources()")
        source = cursor.fetchall()
        cursor.close()

        response = []

        for ln in source:
            response.append(loads(ln[0]))

        return response
    
   
    def getSourceByName(self, sourceName):
        cursor = self.db.cursor()
        cursor.execute("CALL get_source_by_name(\"" + sourceName + "\")")
        source = cursor.fetchone()
        cursor.close()

        if source is None:
            raise LookupError("No source found with name " + sourceName)
        else:
            return source

    # ENTITIES
    def addEntity(self, sourceID:str, mediaID:str, mediaType:str, mediaSource:str, mediaLastUpdated:str, mediaName:str, geoLat:str, geoLon:str, additionViewN:str, additionViewE:str, additionViewS:str, additionViewW:str):
        cursor = self.db.cursor()
        cursor.execute("CALL add_entity(" + sourceID  + ",\"" + mediaID  + "\",\"" + mediaType  + "\",\"" + mediaSource  + "\", str_to_date(\"" + mediaLastUpdated  + "\",\"%m/%d/%Y\"),\"" + mediaName  + "\",\"" + geoLat  + "\",\"" + geoLon  + "\",\"" + additionViewN  + "\",\"" + additionViewE  + "\",\"" + additionViewS  + "\",\"" + additionViewW + "\", @newID)")
        cursor.close()
        self.db.commit()

    
    def getEntitiesBySource(self, sourceID):
        cursor = self.db.cursor()
        cursor.execute("CALL get_entity_by_source(\"" + sourceID + "\")")
        source = cursor.fetchall()
        cursor.close()

        response = []

        for ln in source:
            response.append(loads(ln[0]))

        return response

    
    def getEntity(self, entityID):
        cursor = self.db.cursor()
        cursor.execute("CALL get_entity(\"" + entityID + "\")")
        source = cursor.fetchall()
        cursor.close()

        response = []

        for ln in source:
            response.append(loads(ln[0]))

        return response     
    

    def getEntityNearby(self, geo_rad, geo_lat, geo_lon):
        cursor = self.db.cursor()
        cursor.execute("CALL get_entities_nearby(" + str(geo_rad) + ", " + str(geo_lat) + ", " + str(geo_lon) + ")")
        source = cursor.fetchall()
        cursor.close()

        response = []

        for ln in source:
            response.append(loads(ln[0]))

        return response     