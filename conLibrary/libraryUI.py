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

        # the library variable points to an instance of our controller library
        self.library = controllerLibrary.ControllerLibrary()

        #every time we create a new instance, we will automatically build a UI and populate it
        self.buildUI()
        self.populate()

    def buildUI(self):
        """This method builds the UI"""
        #this is the master layout
        layout = QtWidgets.QVBoxLayout(self)

        #this is the child horizontal widget
        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)

        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)

        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)

        #these are the params for our thumbnail size
        size = 64
        buffer = 12

        #this will create a grid list widget to display our controller thumbnails

        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setIconSize(QtCore.QSize(size,size))
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size+buffer, size+buffer))
        layout.addWidget(self.listWidget)

        #this is our child widget that holds all the buttons
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
        """THis clears the listWidget and repopulates it with the library"""
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
        """loads the current selected controller"""
        currentItem = self.listWidget.currentItem()

        if not currentItem:
            return
        name = currentItem.text()
        self.library.load(name)


    def save(self):
        """saves the controller with the given file name"""
        name = self.saveNameField.text()
        if not name.strip():
            cmds.warning("you must give a name")
            return

        self.library.save(name)
        self.populate()
        self.saveNameField.setText('')

def showUI():
    """
    shows and returns a handle to the ui
    Returns:
            QDialog
    """
    ui = ControllerLibraryUI()
    ui.show()

    return ui
