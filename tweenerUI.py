#how to use
#import tweenerUI
#reload(tweenerUI)
#tweenerUI.tween(10)
#tweenerUI.TweenWindow().show()

from maya import cmds

def tween(percentage, obj=None, attrs=None, selection=True):

    #if obj is not given and selection is set to False, error early
    if not obj and not selection:
        raise ValueError("No object given to tween")

    #if no obj is specified, get it from the first selection
    if not obj:
        obj = cmds.ls(selection=True)[0]

    if not attrs:
        attrs = cmds.listAttr(obj, keyable = True)

    currentTime = cmds.currentTime(query=True)
    #print currentTime

    for attr in attrs:
        #construct the full name of the attribute with its object example: pCube1.scaleY
        attrFull = '%s.%s' % (obj, attr)

        #get the keyframes of the attribute on this object
        keyframes = cmds.keyframe(attrFull,query=True)

        #if there are not keyframes, then continue
        if not keyframes:
            continue

        previousKeyframes = []

        for k in keyframes:
            if k < currentTime:
                previousKeyframes.append(k)

        laterKeyframes = [frame for frame in keyframes if frame > currentTime]

        if not previousKeyframes and not laterKeyframes:
            continue

        if previousKeyframes:
            previousFrame = max(previousKeyframes)
        else:
            previousFrame = None

        nextFrame = min(laterKeyframes) if laterKeyframes else None

        if not previousFrame or not nextFrame:
            continue

        previousValue = cmds.getAttr(attrFull, time=previousFrame)
        nextValue = cmds.getAttr(attrFull, time=nextFrame)



        difference = nextValue - previousValue

        weightedDifference = (difference * percentage) / 100.0
        currentValue = previousValue + weightedDifference

        cmds.setKeyframe(attrFull, time=currentTime, value=currentValue)



class TweenWindow(object):

    windowName = "TweenerWindow"

    def show(self):

        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)

        self.buildUI()
        cmds.showWindow()

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

    def close(self, *args):
        cmds.deleteUI(self.windowName)






