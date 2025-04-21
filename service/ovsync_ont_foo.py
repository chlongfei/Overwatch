from ovsync import OVSYNC
from json import loads

class SyncOntFoo (OVSYNC):
    """Syncronization process for Ontario 511 cameras
    """

    name = "Ontario 511"
    sourceType="511"
    origin="Open Data"
    uri="https://511on.ca/api/v2/get/cameras"

    def __init__(self):
        super().__init__(self.name, self.sourceType, self.origin, self.uri)
        super()._fetchData(self.__dataProcessingMethod)
        super()._loadEntities(self.__entityLoadingProcedure)

    def __dataProcessingMethod(self, data):
        """Data manipulation procedure

        return:
            JSON array containing the camera entities
        """

        features = loads(data)
        return features
    
    def __entityLoadingProcedure(self, data, addEntity):
        """Entity loading procedure
        
        Iterates through the list of entities and loads them into the object

        args:
            data: the data
            addEntity: reference to addEntity operation from tlsync
        """

        doNotSyncSources = [
            "City of Toronto"
        ]

        for ent in data:
            if (ent["Source"] not in doNotSyncSources):
                for view in ent["Views"]:
                    # add entity
                    addEntity(
                        id= view["Id"],
                        mediaType = 'static',
                        url= view["Url"],
                        last_updated = "01/01/1970", #TODO: REMOVE THIS
                        name = ent["Location"] + " " + view["Description"],
                        geoLat = str(ent["Latitude"]),
                        geoLon = str(ent["Longitude"]),
                        additionalN = "null", #TODO: REMOVE THIS
                        additionalE = "null", #TODO: REMOVE THIS
                        additionalS = "null", #TODO: REMOVE THIS
                        additionalW = "null" #TODO: REMOVE THIS
                    )