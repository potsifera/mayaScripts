from maya import cmds

def createGear(teeth=10, length=0.3):
    """
    This function will create a gear with the given parameters
    :param teeth: The number of teeth to create
    :param length: The length of the teeth
    :return: A tuple of the transform, constructor and extrude node
    """
    #teeth are every alternate face, so spans x 2
    spans = teeth*2

    transform, constructor = cmds.polyPipe(subdivisionsAxis=spans)
    sideFaces = range(spans*2, spans*3, 2)

    cmds.select(clear = True)

    for face in sideFaces:
        #pPipe1.f[41] pPipe1.f[43]  selects every other face in the pipe
        cmds.select('%s.f[%s]' % (transform,face), add=True)

    extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]

    return transform, constructor, extrude

def changeTeeth(constructor, extrude, teeth=10, length=0.3):
    spans = teeth * 2
    cmds.polyPipe(constructor, edit=True,subdivisionsAxis=spans)

    sideFaces = range(spans*2, spans*3,2)
    faceNames = []

    for face in sideFaces:
        faceName = 'f[%s]' % (face)
        faceNames.append(faceName)

    cmds.setAttr('%s.inputComponents' % (extrude), len(faceNames),*faceNames,type="componentList")

    cmds.polyExtrudeFacet(extrude, edit=True, ltz = length)
