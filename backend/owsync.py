"""Parent class of OWSYNC module
This class should never be called directly but rather inherited by child classes.
Methods in the parent class are commonly used by the child classes.

lchen@chlf.dev

March 2024
"""
from dataclasses import dataclass
from owdb import OWDB


@dataclass
class Camera():
    camId:int
    entity:int
    friendly:str
    direction:str
    latitude:float
    longitude:float
    streamType:str
    baseUrl:str
    hasAlt:str


class OWSYNC():
    """Parent class for OWSYNC modules
    This class should be inherited by child modules when composing sync middleware scripts
    """

    def __init__(self, entityName:str):
        self.db = OWDB()
        self._entityName = entityName
        self.__dataList = []

    
    def __isDiff(self, srcHash:str, owHash:str):
        """Compares hash of database record and hash of new data
        
        Args:
            srcHash: hash string from the database
            owHash: hash string calculated from datasource
            
        Returns:
            boolean representation indicating if hash is different
        """
        assert not (srcHash == owHash)

    def __addEntityIfNotExist(self, entityName:str):
        """Creates entity record if not already present in db
        Method also sets the entityId instance variable
        
        Args:
            entityName: string name of entity
        """
        if (not self.db.entityExistsByName(entityName)):
            self.__entityId = self.db.addEntity(entityName)
            print(entityName,":: entity not exists - entity created", self.__entityId)
        else:
            self.__entityId = list(self.db.getEntityByName(entityName)[0])[0]
            print(entityName,":: entity exists - id reterived", self.__entityId)

    def _addCamera(self, camId, friendly, direction, latitude, longitude, streamType, baseUrl, hasAlt):
        """Adds camera to datalist

        Args:
            camId: entity issued id for camera.
            friendly: friendly name for camera.
            direction: direction of camera.
            latitude: latitude of geocoordinate of camera location.
            longitude: longitude of geocordinate of camera location.
            streamType: type of the steram 's'=snapshot 'v'=video.
            baseUrl: url of camera stream.
            hasAlt: has alternate streams available.
        """
        cam = Camera(camId, self.__entityId, friendly, direction, latitude, longitude, streamType, baseUrl, hasAlt)
        self.__dataList.append(cam)

    def syncFull(self):
        """Performs a full replacement of dataset
        This method should remove all the records from the database that is associated with the 
        entityID from the DB and create new records from the datasource.
        
        Raises:
            Method should raise exception when error occur.
        """
        self.__addEntityIfNotExist(self._entityName)
        self._getData()

        self.db.delCameraByEntity(self.__entityId)
        
        for cam in self.__dataList:
            self.db.addCamera(cam.camId, cam.entity, cam.friendly, cam.direction, cam.latitude, cam.longitude, cam.streamType, cam.baseUrl, cam.hasAlt)

    def syncDelta(self):
        """Performs a differencial sync of dataset
        This method should evaluate the hash between existing records and one created by the @dataclass
        utilizing __isDiff() and update records where the hash is different and additing cameras where the entity issued
        ID is not present in the database.

        Raises:
            Method should raise exception when error occur.
        """
        self.db.entityExistsByName(self._entityName)
        self._getData()

        for cam in self.__dataList:
            if (self.db.cameraExistsByCamIDEntity(cam.camId, cam.entity)):
                self.db.updCamera(cam.camId, cam.entity, cam.friendly, cam.direction, cam.latitude, cam.longitude, cam.streamType, cam.baseUrl, cam.hasAlt)
            else:
                self.db.addCamera(cam.camId, cam.entity, cam.friendly, cam.direction, cam.latitude, cam.longitude, cam.streamType, cam.baseUrl, cam.hasAlt)


    # Methods to be defined by child #
    def _getData(self):
        """Retrieves data from datasource and populates datalist
        """
        raise NotImplementedError("method \"__getData\" must be overridden by child")
    
    