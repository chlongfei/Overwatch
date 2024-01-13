"""
    Overwatch Database Handler
    lchen@chlf.dev

    January 10, 2024

"""

import mysql.connector

import json
import os

class OWDB:
    
    qAddEntity = ("INSERT INTO entity (entityName) VALUES (%s)")
    qGetEntity = ("SELECT * FROM entity WHERE entityName = %s")

    qAddCamera = ("INSERT INTO cameras (camId, entity, friendly, direction, geoPoint, streamType, baseUrl, hasAlt) VALUES (%s,%s,%s,%s,POINT(%s,%s),%s,%s,%s)")
    qGetCameras = ("SELECT id, camId, entity, friendly, direction, ST_X(geoPoint) latitude, ST_Y(geoPoint) longitude, streamType, baseUrl, hasAlt FROM cameras")
    qGetCameraswEntity = ("SELECT cameras.id, cameras.camId, entity.entityName, cameras.friendly, cameras.direction, ST_X(cameras.geoPoint) latitude, ST_Y(cameras.geoPoint) longitude, cameras.streamType, cameras.baseUrl, cameras.hasAlt FROM cameras INNER JOIN entity on cameras.entity = entity.id")
    qGetCameraById = ("SELECT id, camId, entity, friendly, direction, ST_X(geoPoint) latitude, ST_Y(geoPoint) longitude, streamType, baseUrl, hasAlt FROM cameras WHERE id = %s")
    qGetCameraByFriendly = ("SELECT id, camId, entity, friendly, direction, ST_X(geoPoint) latitude, ST_Y(geoPoint) longitude, streamType, baseUrl, hasAlt FROM cameras WHERE friendly = %s")
    qGetCameraByGeopoint = ("SELECT id, camId, entity, friendly, direction, ST_X(geoPoint) latitude, ST_Y(geoPoint) longitude, streamType, baseUrl, hasAlt FROM cameras WHERE geoPoint = %s")

    def __connect(self):
        """
        handles the connection to mysql
        """
        return mysql.connector.connect( user=os.environ['MYSQL_USER'].strip('\''),
                                        password=os.environ['MYSQL_PASSWORD'].strip('\''),
                                        host=os.environ['DB_HOST'].strip('\''),
                                        database=os.environ['MYSQL_DATABASE'].strip('\''))

    def __executeWrite(self, jobName, query, data):
        """
        handles the writing operation to database
        :param jobName: name of the write job - for error handling messages
        :param query: sql query string
        :param data: tuple for sql parameters
        :returns: id of the new record
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

    def __executeRead(self, jobName, query, data):
        """
        handles the reading operation to database
        :param jobName: name of the write job - for error handling messages
        :param query: sql query string
        :param data: tuple for sql parameters
        :returns: record from the query
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

    # Entity Operations
    def addEntity(self, name):
        """
        handle the adding of entities to database
        :param name: name of new entity
        :returns: id of the new entity
        """
        return self.__executeWrite("addEntity",self.qAddEntity,(name,))

    def getEntity(self, name):
        """
        reterives the id of entity query by name
        :param name: name of entity
        :returns: id of entity
        """
        return self.__executeRead("getEntity",self.qGetEntity,(name,))

    def entityExists(self, name):
        """
        checks for the existance of entity by name
        :param name: name of entity
        :returns: boolean representatino if entity exists
        """
        ent = self.__executeRead("getEntity",self.qGetEntity,(name,))
        if (len(ent) == 0):
            return False
        else:
            return True


    # Camera Operations
    def addCamera(self, camId, entity, friendly, direction, latitude, longitude, streamType, baseUrl, hasAlt):
        """
        adds camera to database
        :param camId: entity issued id for camera
        :param entity: entity id
        :param friendly: friendly name for camera
        :param direction: direction of camera
        :param latitude: latitude of geocoordinate of camera location
        :param longitude: longitude of geocordinate of camera location
        :param streamType: type of the steram 's'=snapshot 'v'=video
        :param baseUrl: url of camera stream
        :param hasAlt: has alternate streams available
        """
        return self.__executeWrite("addCamera", self.qAddCamera,(camId, entity, friendly, direction, latitude, longitude, streamType, baseUrl, hasAlt))

    def getCameras(self, withEntity=False):
        """
        reterives all the cameras in the database
        :withEntity: if set to true, query joint query with entity name in return
        :returns: set of all cameras
        """
        if (not withEntity):
            return self.__executeRead("getCameras",self.qGetCameras,())
        else:
            return self.__executeRead("getCameras_withEntity",self.qGetCameraswEntity,())

    def getCamerasJson(self, withEntity=False):
        """
        reterives all the cameras in the database
        :withEntity: if set to true, query joint query with entity name in return
        :returns: json array of camera information
        """
        cameraList = self.getCameras(withEntity=withEntity)
        cameraJson = []

        for i, cam in enumerate(cameraList):
            cameraJson.append({"camId":cam[1], "entity":cam[2], "friendly":cam[3], "direction":cam[4], "lat":cam[5],"lon":cam[6],"type":cam[7], "baseUrl":cam[8], "hasAlt":cam[9]})
        
        return cameraJson


    def getCameraById(self, cid):
        """
        reterives the camera by ID
        :param cid: id of camera in db
        :returns: record set of camera at id
        """
        return self.__executeRead("getCameraById",self.qGetCameraById,(cid,))

    # TODO: create rest of CRUD functions