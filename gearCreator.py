#controls how many teeth a gear has



from maya import cmds

def createGear(teeth=10, length=0.3):
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
