
import sys
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QTreeWidgetItemIterator,QPushButton, QTreeWidget, QApplication, QTreeWidgetItem,
                            QDialog, QGroupBox, QTableWidget, QTableWidgetItem)

from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import QRect

class Filters(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.setWindowTitle("Filters")
        self.resize(283,271)

        self.mainIcon = QIcon()
        self.mainIcon.addPixmap(QPixmap("img/IMG-Filter.png"),QIcon.Normal,QIcon.Off)
        self.setWindowIcon(self.mainIcon)

        # Creamos los QGroupBox
        self.groupBoxContainer = QGroupBox(self)
        self.groupBoxContainer.setGeometry(QRect(10,10,261,181))
        self.treeWidget = QTreeWidget(self.groupBoxContainer)
        self.treeWidget.setGeometry(QRect(10,10,241,161))
        self.treeWidget.headerItem().setText(0,"Select Items")

        self.groupBoxResult = QGroupBox(self)
        self.groupBoxResult.setGeometry(QRect(10,200,261,61))

        # Creamos los QButtons
        self.BtnAcept = QPushButton(self.groupBoxResult)
        self.BtnAcept.setGeometry(QRect(10,20,91,23))
        self.BtnAcept.setText("Acept")
        self.BtnAcept.clicked.connect(self.GetSelectedItems)

        self.BtnCancel = QPushButton(self.groupBoxResult)
        self.BtnCancel.setGeometry(QRect(160,20,91,23))
        self.BtnCancel.setText("Cancel")
        self.BtnCancel.clicked.connect(self.CloseWindow)

        self.arrayItems = ["Name","Address","Email","Password","Country"]

        # Create empty array 
        self.arrayResult = []

        self.LoadTree()

    def LoadTree(self):
        parent = QTreeWidgetItem(self.treeWidget)
        parent.setText(0,"Select All")
        parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)

        for item in self.arrayItems:
            child = QTreeWidgetItem(parent)
            child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            child.setText(0, item)
            child.setCheckState(0, Qt.Unchecked)

    def GetSelectedItems(self):
        interator = QTreeWidgetItemIterator(self.treeWidget,QTreeWidgetItemIterator.Checked)
        while(interator.value()):
            item = interator.value()
            self.arrayResult.append(item.text(0))
            interator +=1
        self.close()
       
    def GetArray(self):
        return self.arrayResult

    def CloseWindow(self):
        self.close()
if __name__ == "__main__":
    
    app = QApplication(sys.argv)

    win = Filters()

    win.show()

    sys.exit(app.exec_())