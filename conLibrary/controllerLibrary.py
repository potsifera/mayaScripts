from maya import cmds
import os
import json
import pprint

USERAPPDIR = cmds.internalVar(userAppDir=True) #the directory where maya is
DIRECTORY = os.path.join(USERAPPDIR, 'controllerLibrary') #creates controllerLibrary directory string

def createDirectory(directory=DIRECTORY):
    """
    Creates the given directory if it doesn't exists already
    :param directory (str): The directory to create
    :return:
    """
    if not os.path.exists(directory):
        os.mkdir(directory)

class ControllerLibrary(dict): #self is a dictionary

    #any variables that are not part of the function  will be stored in the info variable
    def save(self, name, directory=DIRECTORY, screenshot=True, **info):

        createDirectory(directory)
        #makes a .ma and .json path variables
        path = os.path.join(directory,'%s.ma' % name)
        infoFile = os.path.join(directory, '%s.json' % name)

        info['name'] = name
        info['path'] = path

        #renames the file to the complete path
        cmds.file(rename=path)
        #saves only the selected things on the .ma file
        if cmds.ls(selection=True):
            cmds.file(force=True, type='mayaAscii', exportSelected=True)
        #if nothing is selected it saves everything on the .ma file
        else:
            cmds.file(save=True,type='mayaAscii',force=True) #force saves the file if it already exists

        #saves a screenshot of the file
        if screenshot:
            info['screenshot'] = self.saveScreenshot(name, directory=directory)
        #saves the json data
        with open(infoFile, 'w') as f: # w means open in write mode
            json.dump(info, f, indent=4) #dump info into the file f

        self[name]=info #updates the self list of itemes every time we save


#   #finds all the maya files
    def find(self, directory=DIRECTORY):

        self.clear()
        #if the directory doesn't exist return
        if not os.path.exists(directory):
            return
        #gets only the mayaFiles
        files  = os.listdir(directory)
        mayaFiles = [f for f in files if f.endswith('.ma')]

        #for esach mayaFile
        for ma in mayaFiles:

            name, ext = os.path.splitext(ma)
            path = os.path.join(directory, ma)
            #builds json name
            infoFile = '%s.json' % name
            #loads the json
            if infoFile in files:
                infoFile = os.path.join(directory, infoFile)
                with open(infoFile, 'r') as f:
                    info = json.load(f)
                    #pprint.pprint(info)
            else:
                info = {}

            screenshot = '%s.jpeg' % name
            #saves in info the screenshot, the name and the path
            if screenshot in files:
                info['screenshot'] = os.path.join(directory,name)

            info['name'] = name
            info['path'] = path
            #saves in self each file info
            self[name] = info

        #pprint.pprint(self)


    def load(self,name):
        path=self[name]['path']
        cmds.file(path, i=True, usingNamespaces=False) #i is for import, usingNamespaces false doesnt load the controller in a separate one

    def saveScreenshot(self, name, directory=DIRECTORY):
        path = os.path.join(directory, '%s.jpg' % name)
        cmds.viewFit()
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)

        cmds.playblast(completeFilename=path,forceOverwrite=True,format='image', width=200, height=200, showOrnaments=False,
                       startTime=1, endTime=1, viewer=False)
        return  path




