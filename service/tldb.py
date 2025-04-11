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
        self.db.close()

    def addSource(self, sourceName, sourceType, origin, origin_url):
        cursor = self.db.cursor()
        cursor.execute("CALL add_source(\"" + sourceName + "\",\"" + sourceType + "\",\"" + origin + "\",\"" + origin_url +"\", @new_id)")
        cursor.execute("SELECT @new_id")
        newID = cursor.fetchone()
        cursor.close()

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
    

    def getEntitiesBySource(self, sourceID):
        cursor = self.db.cursor()
        cursor.execute("CALL get_entity_by_source(\"" + sourceID + "\")")
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

    def addEntity(self, sourceID, mediaID, mediaType, mediaSource, mediaLastUpdated, mediaName, geoLat, geoLon, additionViewN, additionViewE, additionViewS, additionViewW):
        cursor = self.db.cursor()
        cursor.execute("CALL add_entity(" + sourceID  + ",\"" + mediaID  + "\",\"" + mediaType  + "\",\"" + mediaSource  + "\",\"" + mediaLastUpdated  + "\",\"" + mediaName  + "\",\"" + geoLat  + "\",\"" + geoLon  + "\",\"" + additionViewN  + "\",\"" + additionViewE  + "\",\"" + additionViewS  + "\",\"" + additionViewW + "\", @newID)")
        cursor.close()
