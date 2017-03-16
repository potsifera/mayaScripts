from Qt import QtWidgets, QtCore, QtGui
import pymel.core as pm

class LightManager(QtWidgets.QDialog):

    def __init__(self):
        super(LightManager,self).__init__() #calls the init on QDialog
        self.setWindowTitle('lighting manager')

    def buildUI(self):
        pass

    def showUI(self):
        ui = LightManager()
        ui.show()
        return ui


