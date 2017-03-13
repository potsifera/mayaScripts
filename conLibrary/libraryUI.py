from controllerLibrary import ControllerLibrary

from PySide2 import QtWidgets, QtCore, QtGui  #from Qt or PySide2

class ControllerLibraryUI(QtWidgets.QDialog):

    def __init__(self):
        super(ControllerLibraryUI, self).__init__() #same as QtWidgets.QDialog.__init__(self)

        self.setWindowTitle("controllerLibraryUI")
        self.library = ControllerLibrary()

        self.buildUI()
        self.populate()

    def buildUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)

        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)

        saveBtn = QtWidgets.QPushButton('Save')
        saveLayout.addWidget(saveBtn)

        size = 64
        buffer = 12
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setIconSize(QtCore.QSize(size,size))
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size+buffer, size+buffer))
        layout.addWidget(self.listWidget)

        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        importBtn = QtWidgets.QPushButton('Import!')
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton('Refresh')
        btnLayout.addWidget(refreshBtn)

        closeBtn = QtWidgets.QPushButton('Close')
        btnLayout.addWidget(closeBtn)



    def populate(self):
        self.library.find()
        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)

            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)


def showUI():
    ui = ControllerLibraryUI()
    ui.show()

    return ui
