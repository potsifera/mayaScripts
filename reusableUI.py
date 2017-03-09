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


class TweenerUI(BaseWindow):
    windowName = "tweenerWindow"

    def buildUI(self):
        column = cmds.columnLayout()
        cmds.text(label="use this slider to set the tween amount")

        row = cmds.rowLayout(numberOfColumns=2)
        self.slider = cmds.floatSlider(min=0, max =100, value=50, step=1, changeCommand=tween)
        cmds.button(label="reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close",command=self.close)

    def reset(self, *args):
        cmds.floatSlider(self.slider, edit=True, value=50)

    
