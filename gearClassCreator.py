from maya import cmds

class Gear(object):

    def createGear(self, teeth=10, length=0.3):
        spans=teeth*2
        transform, constructor = cmds.polyPipe(subdivisionsAxis=spans)
        sideFaces = range(spans*2, spans*3, 2)

        cmds.select(clear = True)

        for face in sideFaces:
            #pPipe1.f[41] pPipe1.f[43]  selects every other face in the pipe
            cmds.select('%s.f[%s]' % (transform,face), add=True)

        extrude = cmds.polyExtrudeFacet(localTranslateZ= length)[0]

        return transform, constructor, extrude

    def changeTeeth(self,constructor, extrude, teeth=10, length=0.3):
        spans = teeth * 2
        cmds.polyPipe(constructor, edit=True,subdivisionsAxis=spans)

        sideFaces = range(spans*2, spans*3,2)
        faceNames = []

        for face in sideFaces:
            faceName = 'f[%s]' % (face)
            faceNames.append(faceName)

        cmds.setAttr('%s.inputComponents' % (extrude), len(faceNames),*faceNames,type="componentList")

        cmds.polyExtrudeFacet(extrude, edit=True, ltz = length)

