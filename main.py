# coding=utf-8

"""
Script was created by Ben Somosi.
Reach me at here for more information!
Linkedin: https://www.linkedin.com/in/bensomosi/
"""

import os
from datetime import datetime

# Python UI package imports
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

# Maya API package imports
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


# Basic settings
WIDTH, HEIGHT = 400, 550
VERSION = "001"
INTRODUCTION = "<br><strong>Nucleus Manager r-"+ VERSION + "</strong><br><br>Select your nCloth, nRigid and Nucleus nodes in your scene easily.<br><br>Visit my Github page for proper documentation!"
WELCOME_LINK = "https://github.com/BenceSomosi/CFX---Nucleus-Manager"



# Core of the script.
class MainWindow(MayaQWidgetDockableMixin, QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.resize(WIDTH, HEIGHT)
        self.setWindowTitle("Nucleus Manager r-" + str(VERSION) +"")

        self.WELCOME_LABEL = QLabel(INTRODUCTION)
        self.WELCOME_LABEL.setAlignment(Qt.AlignCenter)


        linkTemplate = '<a style="color:white;" href={0}>{1}</a>'

        self.WELCOME_LINK_LABEL = HyperlinkLabel(self)
        self.WELCOME_LINK_LABEL.setText(linkTemplate.format('https://github.com/BenceSomosi/CFX---Nucleus-Manager', 'https://github.com/BenceSomosi/CFX---Nucleus-Manager'))



        self.nuclist = QTreeWidget()
        self.nuclist.setRootIsDecorated(False)
        self.nuclist.setHeaderLabels(['Nucleus name'])
        self.nuclist.setStyleSheet("QTreeWidget {background: silver; color: 'black';  font-size: 10pt; } QTreeView::item:hover{background-color:grey; padding: 5px;}")
        self.nuclist.itemClicked.connect(self.selectedItem)

        self.LABEL_showNodes = QLabel("Show these nodes: ")

        self.CHECKBOX_nucleusBox = QCheckBox("Nucleus")
        self.CHECKBOX_nucleusBox.setChecked(True)
        self.CHECKBOX_nucleusBox.stateChanged.connect(self.filterNodes)

        self.CHECKBOX_nClothBox = QCheckBox("nCloth")
        self.CHECKBOX_nClothBox.setChecked(True)
        self.CHECKBOX_nClothBox.stateChanged.connect(self.filterNodes)

        self.CHECKBOX_nRigidBox = QCheckBox("nRigid")
        self.CHECKBOX_nRigidBox.setChecked(True)
        self.CHECKBOX_nRigidBox.stateChanged.connect(self.filterNodes)



        # Set up the layout. (self.layout)
        self.layout.addWidget(self.WELCOME_LABEL, 0, 0, 1, 20)
        self.layout.addWidget(self.WELCOME_LINK_LABEL, 1, 0, 1, 20)
        self.layout.addWidget(QLabel(""), 2, 0, 1, 20)
        self.layout.addWidget(self.nuclist, 3, 0, 1, 20)
        self.layout.addWidget(self.LABEL_showNodes, 4, 0, 1, 1)
        self.layout.addWidget(self.LABEL_showNodes, 4, 0, 1, 1)
        self.layout.addWidget(self.CHECKBOX_nucleusBox, 4, 1, 1, 1)
        self.layout.addWidget(self.CHECKBOX_nClothBox, 4, 2, 1, 1)
        self.layout.addWidget(self.CHECKBOX_nRigidBox, 4, 3, 1, 1)


        # Set up the window
        self.getNucleus()
        self.getnCloth()
        self.getnRigid()

    # Hearth of the script.
    def getNucleus(self):
        TREEVIEW_nucleusList = cmds.ls(type="nucleus")

        for i in TREEVIEW_nucleusList:
            s = QTreeWidgetItem()

            if not cmds.getAttr(i.replace("Shape", "") + ".enable"):
                s.setBackground(0, QBrush(QColor(211, 136, 122)))
            else:
                s.setBackground(0, QColor("white"))

            s.setIcon(0, QIcon(':/nucleus.svg'))
            s.setText(0, str(i))
            self.nuclist.addTopLevelItem(s)

    def getnCloth(self):
        TREEVIEW_nclothList = cmds.ls(type="nCloth")

        for i in TREEVIEW_nclothList:
            s = QTreeWidgetItem()

            if not cmds.getAttr(i + ".isDynamic"):
                s.setBackground(0, QBrush(QColor(211, 136, 122)))
            else:
                s.setBackground(0, QColor("white"))

            s.setIcon(0, QIcon(':/nCloth.svg'))
            s.setText(0, str(i))
            self.nuclist.addTopLevelItem(s)

    def getnRigid(self):
        TREEVIEW_nclothList = cmds.ls(type="nRigid")

        for i in TREEVIEW_nclothList:
            s = QTreeWidgetItem()

            if not cmds.getAttr(i + ".isDynamic"):
                s.setBackground(0, QBrush(QColor(211, 136, 122)))
            else:
                s.setBackground(0, QColor("white"))

            s.setIcon(0, QIcon(':/nRigid.svg'))
            s.setText(0, str(i))
            self.nuclist.addTopLevelItem(s)

    def filterNodes(self):
        self.nuclist.clear()

        if self.CHECKBOX_nucleusBox.isChecked():
            self.getNucleus()

        if self.CHECKBOX_nClothBox.isChecked():
            self.getnCloth()

        if self.CHECKBOX_nRigidBox.isChecked():
            self.getnRigid()

    def selectedItem(self):
        cmds.select(clear=True)
        cmds.select(self.nuclist.currentItem().text(0))

    def enterEvent(self, event):
        self.filterNodes()

    def leaveEvent(self, event):
        self.filterNodes()

    def run(self):
        self.show(dockable = True)

class HyperlinkLabel(QLabel):
    def __init__(self, parent=None):
        super(HyperlinkLabel, self).__init__()
        self.setStyleSheet('color: yellow;')
        self.setOpenExternalLinks(True)
        self.setParent(parent)
        self.setAlignment(Qt.AlignCenter)

if __name__ == "__main__":
    a = MainWindow()
    a.run()

