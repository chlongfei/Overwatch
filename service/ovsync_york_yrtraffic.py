from ovsync import OVSYNC
from json import loads

class SyncYRT (OVSYNC):
    """Syncronization process for York Region Traffic Cameras
    """

    name = "York Region - Traffic"
    sourceType="city"
    origin="Open Data"
    uri="https://ww8.yorkmaps.ca/arcgis/rest/services/OpenData/Traffic/MapServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"

    def __init__(self):
        super().__init__(self.name, self.sourceType, self.origin, self.uri)
        super()._fetchData(self.__dataProcessingMethod)
        super()._loadEntities(self.__entityLoadingProcedure)

    def __dataProcessingMethod(self, data):
        """Data manipulation procedure

        return:
            JSON array containing the camera entities
        """

        features = loads(data)["features"]
        return features
    
    def __entityLoadingProcedure(self, data, addEntity):
        """Entity loading procedure

        Iterates through the list of entities and loads them into the object

        args:
            data: the data
            addEntity: reference to addEntity operation from tlsync
        """

        for ent in data:

            # add entity
            addEntity(
                id= ent["attributes"]["FACILITYID"],
                mediaType = 'static',
                url= ent["attributes"]["photo"],
                last_updated = "01/01/1970", #TODO: REMOVE THIS
                name = ent["attributes"]["cameralocation"],
                geoLat = str(ent["geometry"]["y"]),
                geoLon = str(ent["geometry"]["x"]),
                additionalN = "null", #TODO: REMOVE THIS
                additionalE = "null", #TODO: REMOVE THIS
                additionalS = "null", #TODO: REMOVE THIS
                additionalW = "null" #TODO: REMOVE THIS
            )