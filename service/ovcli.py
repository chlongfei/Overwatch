from ov import OV
from signal import signal, SIGINT

"""
    Command Line Interface for Overwatch application

    To run: python3 ovcli.py
"""


def closeCli(sig=None,frame=None):
    """ Terminates the CLI
    """
    print()
    exit()

def printHelp():
    """ Prints out CLI help page
    """
    with open("ovcli.help","r") as helpfile:
        print("\n" + helpfile.read() + "\n")

def getEntities():
    sourceId = input("source ID: ")
    return OV.getEntitiesBySource(sourceId)

def getEntitiesNearby():
    rad = input("radius (km): ")
    lat = input("latitude: ")
    lon = input("longitude: ")

    return OV.getEntitiesNearby(rad, lat, lon)

def invokeSync():
    sources = ["cot-rescu","york-traffic","511-ont"]
    source = input("source (? to show): ")
    if (source in sources):
        return OV.invokeSync(source)
    elif (source == '?'):
        return sources
    else:
        return "Invalid source"


# REGISTER SIGNAL HANDLER
signal(SIGINT,closeCli) # ctrl-c


# COMMAND HANDLING
# commands registered
cliCommands = {
    "exit":closeCli,
    "help":printHelp,
    "dbalive":OV.isDBAlive,
    "get all sources":OV.getAllSources,
    "get entities":getEntities,
    "get entities nearby":getEntitiesNearby,
    "sync":invokeSync
}

def waitInput():
    """ Handles user input
    """
    inputStr = input("Overwatch-CLI> ")

    if (inputStr in cliCommands.keys()):
        cmdRes = cliCommands.get(inputStr)()
        if (cmdRes != None):
            print(cmdRes)
    else:
        print("Unrecognized command.")


# MAIN INTERFACE
while (True):    
    waitInput()