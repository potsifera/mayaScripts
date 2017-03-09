print "i am the controller library"

from maya import cmds
import os
import json
import pprint

USERAPPDIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USERAPPDIR, 'controllerLibrary')

def createDirectory(directory=DIRECTORY):
    """
    Creates the given directory if it doesn't exists already
    :param directory (str): The directory to create
    :return:
    """
    if not os.path.exists(directory):
        os.mkdir(directory)

