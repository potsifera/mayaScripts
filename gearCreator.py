from maya import cmds

def createGear(teeth=10, length=0.3):
    """
    This function will create a gear with the given parameters
    :param teeth: The number of teeth to create
    :param length: The length of the teeth
    :return: A tuple of the transform, constructor and extrude node

    #ls-sl  how to use:
    import gearCreator
    reload(gearCreator)
    transform, constructor, extrude = gearCreator.createGear()
    gearCreator.changeTeeth(constructor, extrude, teeth=10)

    """
    #teeth are every alternate face, so spans x 2
    spans = teeth*2

    transform, constructor = cmds.polyPipe(subdivisionsAxis=spans)
    sideFaces = range(spans*2, spans*3, 2) #select faces & then ls -sl in mel

    #clears selection
    cmds.select(clear = True)
    #selects only the faces we need to extrude
    for face in sideFaces:
        #pPipe1.f[41] pPipe1.f[43]  selects every other face in the pipe
        cmds.select('%s.f[%s]' % (transform,face), add=True)

    extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0] #selects only the name from the list

    return transform, constructor, extrude #pPipe1 polyPipe1 polyExtrudeFace1

def changeTeeth(constructor, extrude, teeth=10, length=0.3):
    spans = teeth * 2
    cmds.polyPipe(constructor, edit=True, subdivisionsAxis=spans)

    sideFaces = range(spans*2, spans*3, 2)
    #print cmds.listAttr('polyExtrudeFace1') //lists all the atributes from that polyextrudeface
    #print cmds.getAttr('polyExtrudeFace1.inputComponents') //lists the extrude faces
    #gets the faceNames
    faceNames = []
    for face in sideFaces:
        faceName = 'f[%s]' % (face)
        faceNames.append(faceName)

    #sets the correct faces
    cmds.setAttr('%s.inputComponents' % (extrude), len(faceNames), *faceNames, type="componentList")
    #extrudes
    cmds.polyExtrudeFacet(extrude, edit=True, ltz=length) #edit the polyExtrudeFace1
