from maya import cmds
from tweenerUI import tween
from gearClassCreator import Gear

class BaseWindow(object):

    windowName = "BaseWindow"

    def show(self):

        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)

        self.buildUI()
        cmds.showWindow()

    def buildUI(self):
        pass

    def reset(self, *args):
        pass
    def close(self, *args):
        cmds.deleteUI(self.windowName)


