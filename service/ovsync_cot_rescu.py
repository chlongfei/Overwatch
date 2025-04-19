from ovsync import OVSYNC
from json import loads

class SyncCotRescu (OVSYNC):
    """Syncronization process for City of Toronto RESCU camera source
    """

    name = "City of Toronto - RESCU"
    sourceType="city"
    origin="Open Data"
    uri="https://opendata.toronto.ca/transportation/tmc/rescucameraimages/Data/tmcearthcameras.json"

    def __init__(self):
        super()._addSource(self.name, self.sourceType, self.origin, self.uri)
        super()._fetchData(self.__dataProcessingMethod)
        super()._loadEntities(self.__entityLoadingProcedure)

    def __dataProcessingMethod(self, data):
        """Data manipulation procedure

        Trims leading and trailing spaces and removes non json-compliant text

        return:
            json array containing entities        
        """
        # cleanup data
        data = data.lstrip()
        data = data.rstrip()
        data = data.removeprefix("jsonTMCEarthCamerasCallback(")
        data = data.removesuffix(");")
        
        return loads(data)["Data"]
    
    def __entityLoadingProcedure(self, data, addEntity):
        """Entity loading procedure

        Iterates through the list of entities and loads them into the object

        args:
            data: the data
            addEntity: reference to addEntity operation from tlsync
        """

        for ent in data:

            # handle optional directional cameras
            northCam = "null" if len(ent["D1"]) <= 0 else "https://opendata.toronto.ca/transportation/tmc/rescucameraimages/ComparisonImages/loc" + ent["Number"] + ent["D1"] + ".jpg"
            eastCam = "null" if len(ent["D2"]) <= 0 else "https://opendata.toronto.ca/transportation/tmc/rescucameraimages/ComparisonImages/loc" + ent["Number"] + ent["D2"] + ".jpg"
            southCam = "null" if len(ent["D3"]) <= 0 else "https://opendata.toronto.ca/transportation/tmc/rescucameraimages/ComparisonImages/loc" + ent["Number"] + ent["D3"] + ".jpg"
            westCam = "null" if len(ent["D4"]) <= 0 else "https://opendata.toronto.ca/transportation/tmc/rescucameraimages/ComparisonImages/loc" + ent["Number"] + ent["D4"] + ".jpg"

            # add entity
            addEntity(
                id= ent["Number"],
                mediaType = 'static',
                url= "https://opendata.toronto.ca/transportation/tmc/rescucameraimages/CameraImages/loc" + ent["Number"] + ".jpg",
                last_updated = "01/01/1970",
                name = ent["Name"],
                geoLat = ent["Latitude"],
                geoLon = ent["Longitude"],
                additionalN = str(northCam),
                additionalE = str(eastCam),
                additionalS = str(southCam),
                additionalW = str(westCam)
            )