import pprint

from maya import cmds

import controllerLibrary
reload(controllerLibrary)

from PySide2 import QtWidgets, QtCore, QtGui  #from Qt or PySide2

class ControllerLibraryUI(QtWidgets.QDialog):
    """"
    The ControllerLibraryUI is a dialog that lets us save and import controllers
    """

    def __init__(self):
        super(ControllerLibraryUI, self).__init__() #same as QtWidgets.QDialog.__init__(self)

        self.setWindowTitle("controllerLibraryUI")
        self.library = controllerLibrary.ControllerLibrary()

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
        saveBtn.clicked.connect(self.save)
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
        importBtn.clicked.connect(self.load)
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)

        closeBtn = QtWidgets.QPushButton('Close')
        closeBtn.clicked.connect(self.close) #defined in qwidget that q dialog inherits from
        btnLayout.addWidget(closeBtn)



    def populate(self):
        self.listWidget.clear() #clears before adding
        self.library.find()
        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)

            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)
            item.setToolTip(pprint.pformat(info))


    def load(self):
        currentItem = self.listWidget.currentItem()

        if not currentItem:
            return
        name = currentItem.text()
        self.library.load(name)


    def save(self):
        name = self.saveNameField.text()
        if not name.strip():
            cmds.warning("you must give a name")
            return

        self.library.save(name)
        self.populate()
        self.saveNameField.setText('')

def showUI():
    ui = ControllerLibraryUI()
    ui.show()

    return ui
