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
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        layout.addWidget(scrollArea,1,0,1,2)

    def createLight(self):
            lightType = self.lightTypeCB.currentText()
            func = self.lightTypes[lightType]

            light = func() #executes the func

    def showUI(self):
        ui = LightManager()
        ui.show()
        return ui








