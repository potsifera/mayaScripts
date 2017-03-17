from Qt import QtWidgets, QtCore, QtGui
import pymel.core as pm
from functools import partial



class LightManager(QtWidgets.QDialog):

    #stores the names and the functions
    lightTypes = {
        "Point Light": pm.pointLight,
        "Spot Light" : pm.spotLight,
        "Directional Light" : pm.directionalLight,
        "Area Light": partial(pm.shadingNode, 'areaLight', asLight=True),
        "volume Light": partial(pm.shadingNode, 'volumeLight', asLight=True) #partial lets us call the function later and its args
    }

    def __init__(self):
        super(LightManager,self).__init__() #calls the init on QDialog
        self.setWindowTitle('lighting manager')
        self.buildUI()


    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)
        self.lightTypeCB = QtWidgets.QComboBox()
        #adds ligths to comboBox
        for lightType in sorted(self.lightTypes):
            self.lightTypeCB.addItem(lightType)

        layout.addWidget(self.lightTypeCB,0,0)

        createBtn = QtWidgets.QPushButton('Create')
        createBtn.clicked.connect(self.createLight)
        layout.addWidget(createBtn,0,1) #row 0, column 1

        scrollWidget = QtWidgets.QWidget()
        # prevents the ui from stretching when having few lights **bug
        #scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum)
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        layout.addWidget(scrollArea, 1,0,1,2) #adds to row one, column 0, take one row & 2 columns

        scrollWidget = QtWidgets.QWidget()
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        layout.addWidget(scrollArea,1,0,1,2)

    def createLight(self):
        lightType = self.lightTypeCB.currentText()
        func = self.lightTypes[lightType]

        light = func() #executes the func
        widget = LightWidget(light)
        self.scrollLayout.addWidget(widget)


class LightWidget(QtWidgets.QWidget):

    onSolo = QtCore.Signal(bool)

    def __init__(self,light):
        super(LightWidget,self).__init__()
        if isinstance(light,basestring):
            light = pm.PyNode(light)
        self.light = light
        self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)
        self.name = QtWidgets.QCheckBox(str(self.light.getTransform()))
        self.name.setChecked(self.light.visibility.get())
        #anonymous function toggles visibility in the channel box & viewport
        self.name.toggled.connect(lambda val: self.light.getTransform().visibility.set(val))
        layout.addWidget(self.name, 0,0)

        soloBtn = QtWidgets.QPushButton('Solo')
        soloBtn.setCheckable(True)
        soloBtn.toggled.connect(lambda val:self.onSolo.emit(val))
        layout.addWidget(soloBtn,0,1)



def showUI():
    ui = LightManager()
    ui.show()
    return ui








