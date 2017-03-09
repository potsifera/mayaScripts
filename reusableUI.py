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

class GearUI(BaseWindow):
    windowName = "gearWindow"

    def __init__(self):
        self.gear = None

    def buildUI(self):
        column = cmds.columnLayout()
        cmds.text(label = "use the slider to modify the gear")

        cmds.rowLayout(numberOfColumns=4)
        self.label = cmds.text(label=10)
        self.slider = cmds.intSlider(min=5, max=30, value=10, step=1, dragCommand= self.modifyGear)
        cmds.button(label="Make gear", command=self.makeGear)
        cmds.button(label="reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="close", command=self.close)


    def makeGear(self,*args):
        
        print "making gear"
        teeth =cmds.intSlider(self.slider, query=True, value=True)
        self.gear = Gear()
        self.gear.createGear(teeth=teeth)

    def modifyGear(self,teeth):
        self.gear.changeTeeth(teeth=teeth)

    def reset(self, *args):
        print "reseting"
