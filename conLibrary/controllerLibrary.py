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

class ControllerLibrary(dict): #self is a dictionary

    def save(self, name, directory=DIRECTORY):

        createDirectory(directory)

        path = os.path.join(directory,'%s.ma' % name)

        cmds.file(rename=path)
        #saves the selected things
        if cmds.ls(selection=True):
            cmds.file(force=True, type='mayaAscii', exportSelected=True)
        #if nothing is selected it saves everything
        else:
             cmds.file(save=True,type='mayaAscii',force=True)

        self[name]=path #updates the self list of itemes every time we save



    def find(self, directory=DIRECTORY):

        if not os.path.exists(directory):
            return

        files  = os.listdir(directory)
        mayaFiles = [f for f in files if f.endswith('.ma')]


        for ma in mayaFiles:
            name, ext = os.path.splitext(ma)
            path = os.path.join(directory, ma)

            self[name] = path

        pprint.pprint(self)


    def load(self,name):
        path=self[name]
        cmds.file(path, i=True, usingNamespaces=False) #i is for import, usingNamespaces false doesnt load the controller in a separate one




