from tldb import TLDB
from requests import get
from json import loads
from dataclasses import dataclass

@dataclass
class EntityItem:
    id: str
    mediaType: str
    url: str
    last_updated: str
    name: str
    geoLat: str
    geoLon: str
    additionalN: str
    additionalE: str
    additionalS: str
    additionalW: str

class TLSYNC:
    """ Abstract class for data syncronization

    This class is used an abstract class that is inherited by specific classes for the import of source and their entities.
    """

    entityItems = []

    sourceName = None
    sourceType = None
    sourceOrigin = None
    sourceOriginUri = None

    sourceData = None


    def _addSource(self, name, type, origin, uri):
        """Adds the source information

        args:
            name: name of source
            type: source type (e.g. Municipality)
            origin: data origin (e.g. Open Data)
            uri: full url path to the data
        """
        self.sourceName = name
        self.sourceType = type
        self.sourceOrigin = origin
        self.sourceOriginUri = uri

    def _fetchData(self, dataProcessingMethod):
        """Fetches and processes data

        Fetches the data from the specified sourceOriginUri and running the provided data processing
        routine that performs the additional manipulations required before loading.

        args:
            dataProcessingMethod: reference to a method that defines the data manipulation steps required before loading

        raises:
            Exception if request returns a non 200 OK response
        """
        req = get(self.sourceOriginUri)
        if (req.status_code != 200):
            raise Exception("Data fetch returned " + req.status_code)
        else:
            self.sourceData = dataProcessingMethod(req.text)

    def _loadEntities(self, entityLoadingMethod):
        """Loads entities into memory

        Utilizing the provided entity loading method, entities are packaged into EntityItem objects ready for sync.
        """
        entityLoadingMethod(self.sourceData, self.__addEntity)
  
    def __addEntity(self, id, mediaType, url, last_updated, name, geoLat, geoLon, additionalN, additionalE, additionalS, additionalW):
        """Creates Entity Item object list

        Taking in the entity information and loading them into EntityItem and appends them to list.

        args:
            id: source issued id for entity
            url: main media source for entity
            last_updated: date stamp for when entity media was last updated (useful for snapshot based media)
            name: source issued name for entity
            geoLat: geographical latitude of entity
            geoLon: geographical longitude of entity
            additionalN: url of media for NORTH facing view
            additionalE: url of media for EAST facing view
            additionalS: url of media for SOUTH facing view
            additionalW: url of media for WEST facing view
        """
        self.entityItems.append(
            EntityItem(id, mediaType, url, last_updated, name, geoLat, geoLon, additionalN, additionalE, additionalS, additionalW)
        )

    def getEntities(self):
        """Returnst the list of Entities        
        """
        return self.entityItems

    def sync(self):
        """Performs sync action
        """
        sourceId = None

        try:
            with TLDB() as tldb:
                sourceId = loads(tldb.getSourceByName(self.sourceName)[0])["id"]
        except LookupError:
            with TLDB() as tldb:
                sourceId = tldb.addSource(self.sourceName, self.sourceType, self.sourceOrigin, self.sourceOriginUri)[0]

        with TLDB() as tldb:
            for entity in self.entityItems:
                tldb.addEntity(str(sourceId), entity.id, entity.mediaType, entity.url, entity.last_updated, entity.name, entity.geoLat, entity.geoLon, entity.additionalN, entity.additionalE, entity.additionalS, entity.additionalW)