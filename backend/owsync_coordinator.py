"""Sync dispatcher
API for handling sync actions utilizing the middlware scripts in /sync to sync data into db

lchen@chlf.dev
March 2024
"""

# ENTITY SYNC MODULES #
from owsync_ca_on_tor_rescu import CA_ON_TOR_RESCU


class OWSyncCoordinator():

    syncModDict = {
        'ca-on-tor-rescu': CA_ON_TOR_RESCU
    }

    def fullSyncByEntity(self, entityName:str):
        """Performs a full sync on the specified entity by name
        Raises:
            KeyError when entity name provided is not in syncModDict
        """
        try:
            entInst = self.syncModDict[entityName]()
            entInst.syncFull()
        except KeyError:
            raise


    def deltaSyncByEntity(self, entityName:str):
        """Performs a differential sync on the specified entity by name
        Raises:
            KeyError when entity name provided is not in syncModDict
        """
        try:
            entInst = self.syncModDict[entityName]()
            entInst.syncDelta()
        except KeyError:
            raise


    def fullSync(self):        
        """Performs a full sync on all entities
        """
        for ent in self.syncModDict.keys():
            entInst = self.syncModDict[ent]()
            entInst.syncFull()


    def deltaSync(self):        
        """Performs a differential sync on all entities
        """
        for ent in self.syncModDict.keys():
            entInst = self.syncModDict[ent]()
            entInst.syncDelta()
