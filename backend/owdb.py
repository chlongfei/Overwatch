"""Handler for performing CRUD actions for the Overwatch application.

    lchen@chlf.dev
    January 2024

    Typical usage example:

        owdb = OWDB()
"""

import mysql.connector
import json
import os

class OWDB:
    """Overwatch database handler class.

    Set of private and public APIs for operating on the Overwatch database.

    Raises:
        Errors and exceptions raised by mysql.connector are re-raised to the caller. This is such that
        the caller can decide remediatory actions on any specific exception raised.

        More information on errors and exceptions raised by mysql.connector can be found at:
        https://dev.mysql.com/doc/connector-python/en/connector-python-api-errors.html    
    """

    # SQL STATEMENT #
    # entities #
    qAddEntity = ("INSERT INTO entity (entityName) VALUES (%s)")
    qGetEntity = ("SELECT * FROM entity")
    qGetEntityByName = ("SELECT * FROM entity WHERE entityName = %s")
    qGetEntityById = ("SELECT * FROM entity WHERE id = %s")
    qDeleteEntity = ("DELETE FROM entity WHERE id = %s")
    # cameras #
    qAddCamera = ("INSERT INTO cameras (camId, entity, friendly, direction, geoPoint, streamType, baseUrl, hasAlt) VALUES (%s,%s,%s,%s,POINT(%s,%s),%s,%s,%s)")
    qGetCameras = ("SELECT id, camId, entity, friendly, direction, ST_X(geoPoint) latitude, ST_Y(geoPoint) longitude, streamType, baseUrl, hasAlt FROM cameras")
    qGetCameraswEntity = ("SELECT cameras.id, cameras.camId, entity.entityName, cameras.friendly, cameras.direction, ST_X(cameras.geoPoint) latitude, ST_Y(cameras.geoPoint) longitude, cameras.streamType, cameras.baseUrl, cameras.hasAlt FROM cameras INNER JOIN entity on cameras.entity = entity.id")
    qGetCameraById = ("SELECT id, camId, entity, friendly, direction, ST_X(geoPoint) latitude, ST_Y(geoPoint) longitude, streamType, baseUrl, hasAlt FROM cameras WHERE id = %s")
    qGetCameraByFriendly = ("SELECT id, camId, entity, friendly, direction, ST_X(geoPoint) latitude, ST_Y(geoPoint) longitude, streamType, baseUrl, hasAlt FROM cameras WHERE friendly = %s")
    qGetCameraByGeopoint = ("SELECT id, camId, entity, friendly, direction, ST_X(geoPoint) latitude, ST_Y(geoPoint) longitude, streamType, baseUrl, hasAlt FROM cameras WHERE geoPoint = POINT(%s,%s)")
    qDeleteCameraById = ("DELETE FROM cameras WHERE camId = %s")
    qDeleteCameraByEntity = ("DELETE FROM cameras WHERE entity = %s")
    qGetCameraCountByCamIDEntity = ("SELECT COUNT(*) FROM camera WHERE (camID = %s) AND (entity = %s)")
    qUpdateCamera = ("UPDATE cameras SET camId = %s, entity = %s, friendly = %s, direction = %s, geoPoint = %s, streamType = %s, baseUrl = %s, hasAlt = %s WHERE camID = %s and entity = %s")
    # functional #
    qGetCameraNearGeopoint = ("SELECT id, camId, entity, friendly, direction, ST_X(geoPoint) latitude, ST_Y(geoPoint) longitude, streamType, baseUrl, hasAlt  FROM cameras WHERE ST_Distance_Sphere(geoPoint, point(%s,%s)) < %s order by ST_Distance_Sphere(geoPoint, point(%s,%s))")



    # INTERNAL METHODS #
    def __connect(self):
        """Connects to the mySQL database.
        
        Database credentials are passed into the function via environment variables.

        Returns:
            A MySQLConnection object upon successful connection to the mySQL database.
        """
        try:
            cnx = mysql.connector.connect( user=os.environ['MYSQL_USER'].strip('\''),
                                            password=os.environ['MYSQL_PASSWORD'].strip('\''),
                                            host=os.environ['DB_HOST'].strip('\''),
                                            database=os.environ['MYSQL_DATABASE'].strip('\''))
            return cnx
        except mysql.connector.Error:
            raise

    
    def __execNoRtn(self, jobName:str, query:str, data:tuple) -> None:
        """Performs a database action with no return.

        This method is good for misc. operations where a return value is not expected, such as DELETE.
        A successful execution of the mthod is one with no exception raised.

        Args:
            jobName: Name given to the execution, this is for error messaging.
            query: A SQL query string for executing on the database.
            data: A tuple listing string values that substitute the `%s` tokens within the SQL query string.
        
        Raises:
            On error execution a mysq.conenctor.Error is raised.
        """
        try:
            cnx = self.__connect()
            cursor = cnx.cursor()
            cursor.execute(query,data)
            cnx.commit()
            cursor.close()
            cnx.close()
        except mysql.connector.Error as err:
            print("Error at",jobName,"::",err)
            raise


    def __execWrite(self, jobName:str, query:str, data:tuple) -> int:
        """Performs a write based action on the mySQL database.

        Although not enforced, this method should be used with write SQL actions such as INSERT or UPDATE.

        Args:
            jobName: Name given to the write execution, this is for error messaging.
            query: A SQL query string for writing into the database, typically an INSERT or UPDATE action.
            data: A tuple listing string values that substitute the `%s` tokens within the SQL query string.
        
        Returns:
            The integer ID of the newly created record in the database.

        Raises:
            On error execution a mysq.conenctor.Error is raised.
        """
        try:
            cnx = self.__connect()
            cursor = cnx.cursor()
            cursor.execute(query,data)
            rtn = cursor.lastrowid
            cnx.commit()
            cursor.close()
            cnx.close()
            return rtn
        except mysql.connector.Error as err:
            print("Error at",jobName,"::",err)
            raise


    def __execRead(self, jobName:str, query:str, data:tuple) -> list:
        """Performs a read based action on the mySQL database.

        Although not enforced, this method should be used with read SQL actions such as a SELECT.

        Args:
            jobName: Name given to the read execution, this is for error messaging.
            query: A SQL query string for reading from the database, typically a SELECT action.
            data: A tuple listing string values that substitute the `%s` tokens within the SQL query string.
        
        Returns:
            A list of tuples representing the results of the query.
            If no rows are available from query, an empty list is returned.

        Raises:
            On error execution a mysq.conenctor.Error is raised.
        """
        try:
            cnx = self.__connect()
            cursor = cnx.cursor()
            cursor.execute(query,data)
            rtn = cursor.fetchall()
            cursor.close()
            cnx.close()        
            return rtn
        except mysql.connector.Error as err:
            print("Error at",jobName,"::",err)
            raise



    # ENTITY METHODS #
    # internal helpers methods #
    def __convertEntityListToJSON(self, entityList:list) -> list:
        """Converts list of tuples from SQL query into JSON list.

        Args:
            entityList: list of tuples from SQL query

        Returns:
            JSON list string with data converted from entityList tuples.
        
        """
        entityJson = []

        for i, ent in enumerate(entityList):
            entityJson.append({"entId":ent[0], "name":ent[1]})
        
        return entityJson
    
    def addEntity(self, name:str) -> int:
        """Adds an entity to the database.

        Args:
            name: the name of the new entity

        Returns:
            An integer ID for the new entity.

        Raises:
            On error execution a mysq.conenctor.Error is raised.
        """
        return self.__execWrite("addEntity",self.qAddEntity,(name, ))
    

    def getEntity(self, asJSON:bool=False) -> list:
        """Reterives all entities in the database.

        Returns:
            List of tuples containing all the entity ID and Name pairs in the database.

        Raises:
            On error execution a mysq.conenctor.Error is raised.
        """
        entityList = self.__execRead("qGetEntity",self.qGetEntity,None)

        if (asJSON):
            return self.__convertEntityListToJSON(entityList)
        else:
            return entityList
    
    
    def getEntityByName(self, name, asJSON:bool=False) -> list:
        """Reterives a specific entity from database specified by Name.

        Args:
            name: the name of the entity to be reterived.
        
        Returns:
            List of tuples containing the ID and Name pair for the entity specified by Name in the database.

        Raises:
            On error execution a mysq.conenctor.Error is raised.
        """
        entityList = self.__execRead("qGetEntityByName",self.qGetEntityByName,(name, ))
    
        if (asJSON):
            return self.__convertEntityListToJSON(entityList)
        else:
            return entityList
    
    
    def getEntityByID(self, id, asJSON:bool=False) -> list:
        """Reterives a specific entity from database specified by ID.

        Args:
            id: the ID of the entity to be reterived.
        
        Returns:
            List of tuples containing the ID and Name pair for the entity specified by ID in the database.

        Raises:
            On error execution a mysq.conenctor.Error is raised.
        """
        entityList = self.__execRead("qGetEntityById",self.qGetEntityById,(id, ))
    
        if (asJSON):
            return self.__convertEntityListToJSON(entityList)
        else:
            return entityList
    
    
  
    def delEntity(self, id:int) -> None:
        """Deletes the entity identified by ID from database

        Args:
            id: the ID of the entity to be deleted.
        
        Raises:
            On error execution a mysq.conenctor.Error is raised.
        """
        self.__execNoRtn("qDeleteEntity",self.qDeleteEntity,(id, ))


    def entityExistsByName(self, name:str) -> bool:
        """Checks if an entity exists by Name given

        Args:
            name: name of the entity to check.

        Returns:
            Boolean value TRUE when entity exists and FALSE otherwise.
        
        Raises:
            On error execution a mysq.conenctor.Error is raised.
        """
        ent = self.__execRead("qGetEntityByName",self.qGetEntityByName,(name,))
        if (len(ent) == 0):
            return False
        else:
            return True


    def entityExistsByID(self, id:int) -> bool:
        """Checks if an entity exists by Name given

        Args:
            id: the id of the entity to check.

        Returns:
            Boolean value TRUE when entity exists and FALSE otherwise.
        
        Raises:
            On error execution a mysq.conenctor.Error is raised.
        """
        ent = self.__execRead("qGetEntityById",self.qGetEntityById,(id,))
        if (len(ent) == 0):
            return False
        else:
            return True



    # CAMERAS #    
    # internal helpers methods #
    def __convertCameraListToJSON(self, cameraList:list) -> list:
        """Converts list of tuples from SQL query into JSON list.

        Args:
            cameraList: list of tuples from SQL query

        Returns:
            JSON list string with data converted from cameraList tuples.
        
        """
        cameraJson = []

        for i, cam in enumerate(cameraList):
            cameraJson.append({"camId":cam[1], "entity":cam[2], "friendly":cam[3], "direction":cam[4], "lat":cam[5], "lon":cam[6], "type":cam[7], "baseUrl":cam[8], "hasAlt":cam[9]})
        
        return cameraJson
    

    # public API #
    def addCamera(self, camId:str, entity:int, friendly:str, direction:str, latitude:str, longitude:str, streamType:str, baseUrl:str, hasAlt:str) -> int:
        """Adds a camera record to the database.

        Args:
            camId: entity issued id for camera.
            entity: entity id.
            friendly: friendly name for camera.
            direction: direction of camera.
            latitude: latitude of geocoordinate of camera location.
            longitude: longitude of geocordinate of camera location.
            streamType: type of the steram 's'=snapshot 'v'=video.
            baseUrl: url of camera stream.
            hasAlt: has alternate streams available.

        Returns:
            The ID of the newly created camera record.
        
        Raises:
            On error execution a mysq.conenctor.Error is raised.
        """
        return self.__execWrite("addCamera", self.qAddCamera,(camId, entity, friendly, direction, latitude, longitude, streamType, baseUrl, hasAlt))


    def getCameras(self, withEntity:bool=False, asJSON:bool=False) -> list:
        """Reterives ALL the camera records in the database.

        This action is very costly in compute, it's useful in development, but should not be used in production.

        Args:
            withEntity: if set to TRUE, query joint query with entity name in return.
            asJSON: if set to TRUE, method output in JSON string.

        Returns:
            A list of tuples, or JSON list if `asJSON` set TRUE, containing all the camera records in the database.
        
        Raises:
            On error execution a mysq.conenctor.Error is raised.
        """
        if (not withEntity):
            cameraList = self.__execRead("getCameras",self.qGetCameras,())
        else:
            cameraList = self.__execRead("getCameras_withEntity",self.qGetCameraswEntity,())

        if (asJSON):
            return self.__convertCameraListToJSON(cameraList)
        else:
            return cameraList
        

    def getCameraById(self, cid:int, asJSON:bool=False) -> list:
        """Reterives a specified camera identified by ID.

        Args:
            cid: id of camera in db.
            asJSON: if set to TRUE, method output in JSON string.

        Returns:
            A list of tuples, or JSON list if `asJSON` set TRUE, containing information about camera quried.
        
        Raises:
            On error execution a mysq.conenctor.Error is raised.
        """
        cameraList = self.__execRead("getCameraById",self.qGetCameraById,(cid,))
    
        if (asJSON):
            return self.__convertCameraListToJSON(cameraList)
        else:
            return cameraList
    

    def getCamerasByEntity(self, entity:int, asJSON:bool=False) -> list:
        """Reterives all cameras associated with an entity.

        Args:
            entity: ID of entity associated with cameras.
            asJSON: if set to TRUE, method output in JSON string.

        Returns:
            A list of tuple, or JSON list if `asJSON` set TRUE, containing the information about cameras quried.
        
        Raises:
            On error execution a mysq.conenctor.Error is raised.
        """
        cameraList = self.__execRead("getCameraByEntity",self.qGetCameraswEntity,(entity,))
    
        if (asJSON):
            return self.__convertCameraListToJSON(cameraList)
        else:
            return cameraList


    def getCamerasByFriendly(self, friendly:str, asJSON:bool=False) -> list:
        """Reterives cameras with the specified friendly name.

        Args:
            friendly: camera friendly name
            asJSON: if set to TRUE, method output in JSON string.

        Returns:
            A list of tuple, or JSON list if `asJSON` set TRUE, containing the information about cameras quried.
        
        Raises:
            On error execution a mysq.conenctor.Error is raised.
        """
        cameraList = self.__execRead("getCamerasByFriendly",self.qGetCameraByFriendly,(friendly,))
    
        if (asJSON):
            return self.__convertCameraListToJSON(cameraList)
        else:
            return cameraList
    

    def getCamerasByGeo(self, lat:str, lon:str, asJSON:bool=False) -> list:
        """Reterives cameras with the specified longitude and latitude coordniates.

        Args:
            lon: camera longitudinal cooridnate.
            lat: camera lattitudinal coordinate.

        Returns:
            A list of tuple, or JSON list if `asJSON` set TRUE, containing the information about cameras quried.
        
        Raises:
            On error execution a mysq.conenctor.Error is raised.
        """
        cameraList = self.__execRead("getCamerasByGeo",self.qGetCameraByGeopoint,(lat, lon))
    
        if (asJSON):
            return self.__convertCameraListToJSON(cameraList)
        else:
            return cameraList
        
    
    def cameraExistsByCamIDEntity(self, camID:int, entity:int) -> bool:
        """Checks to see if camera identified by camID and entity exists

        Args:
            camID: camera id assigned by entity
            entity: entity id
        Returns:
            Boolean indicating if camera exists
        """
        count = self.__execRead("cameraExistsByCamIDEntity",self.qGetCameraCountByCamIDEntity, (camID, entity))
        print(count)

        if (count[0] > 0):
            return True
        else:
            return False
    
    
    def updCamera(self, camId:str, entity:int, friendly:str, direction:str, latitude:str, longitude:str, streamType:str, baseUrl:str, hasAlt:str) -> None:
        """
        updates camera at id
        :param id: camera id
        :returns: new camera record
        """
        self.__execNoRtn("updCamera", self.qUpdateCamera, (camId, entity, friendly, direction, latitude, longitude, streamType, baseUrl, hasAlt, camId, entity))
    
        
    def delCamera(self, cid:int) -> None:
        """
        delete camera at id
        :param id: camera id
        :returns: id of camera deleted
        """
        self.__execNoRtn("delCamera", self.qDeleteCameraById, (cid, ))


    def delCameraByEntity(self, entity:int) -> None:
        """Deletes cameras associated with an entity
        
        Args:
            entity: entity ID of cameras to remove
        """
        self.__execNoRtn("qDeleteCameraByEntity",self.qDeleteCameraByEntity,(entity,))



    # FUNCTIONALS #
    def getCamerasNearGeopoint(self, lat:str, lon:str, rad:int) -> list:
        """
        reterives the ID of cameras within rad of point(lat,lon)
        :param lat: lattitude of query location
        :param lon: longitude of query location
        :param rad: radius of query
        :returns: json with array of camera IDs
        """
        cameraList = self.__execRead("getCameraNearGeopoint", self.qGetCameraNearGeopoint, (lat, lon, rad, lat, lon))        
        return self.__convertCameraListToJSON(cameraList)
