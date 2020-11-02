import sys, csv
from PyQt5.Qt import Qt
from faker import Faker
from PyQt5.QtWidgets import (QPushButton, QDialog, QLineEdit, QLabel, QTreeWidget, QApplication,QMainWindow,QGroupBox, 
                            QComboBox,QTableWidget,QTableWidgetItem)

from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import QRect
from Filters import Filters

class MainApplication(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Fake Random")
        self.resize(950,295)
        self.mainIcon = QIcon()
        self.mainIcon.addPixmap(QPixmap("img/Anonymous-Mask.png"),QIcon.Normal,QIcon.Off)
        self.setWindowIcon(self.mainIcon)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        # Creamos la instancia a Faker
        self.faker = Faker()

        # Creamos los QGroupBox
        self.groupBoxData = QGroupBox(self)
        self.groupBoxData.setGeometry(QRect(10,10,321,281))
        self.groupBoxData.setTitle("Generate Data")

        self.groupBoxTools = QGroupBox(self.groupBoxData)
        self.groupBoxTools.setGeometry(QRect(10,180,301,91))
        self.groupBoxTools.setTitle("Tools")

        # Creamos una funte pricipal
        self.masterFont = QFont()
        self.masterFont.setFamily("Century Gothic")
        self.masterFont.setPointSize(10)
        self.masterFont.setWeight(50)

        # Creamos las Etiquetas
        self.lblNames = QLabel(self.groupBoxData)
        self.lblNames.setGeometry(QRect(10,40,131,16))
        self.lblNames.setFont(self.masterFont)
        self.lblNames.setText("Number of Names:")

        self.lblCustomized = QLabel(self.groupBoxData)
        self.lblCustomized.setGeometry(QRect(10,70,141,16))
        self.lblCustomized.setFont(self.masterFont)
        self.lblCustomized.setText("Customized Number:")

        self.lblSaveFile = QLabel(self.groupBoxTools)
        self.lblSaveFile.setGeometry(QRect(10,40,61,21))
        self.lblSaveFile.setFont(self.masterFont)
        self.lblSaveFile.setText("Save as:")

        # Creamos las cajas de texto y combobox
        self.CboNumbers = QComboBox(self.groupBoxData)
        self.CboNumbers.setGeometry(QRect(160,40,151,22))

        self.CboTools = QComboBox(self.groupBoxTools)
        self.CboTools.setGeometry(QRect(80,40,141,22))        

        self.txtNumber = QLineEdit(self.groupBoxData)
        self.txtNumber.setGeometry(QRect(160,70,151,20))

        # Creamos los Botones
        self.iconFilter = QIcon()
        self.iconFilter.addPixmap(QPixmap("img/IMG-Filter.png"),QIcon.Normal,QIcon.Off)
        self.BtnFilter = QPushButton(self.groupBoxData)
        self.BtnFilter.setGeometry(QRect(10,100,301,23))
        self.BtnFilter.setIcon(self.iconFilter)
        self.BtnFilter.setText("Filters")
        self.BtnFilter.clicked.connect(self.OpenFilters)

        self.iconGenerate = QIcon()
        self.iconGenerate.addPixmap(QPixmap("img/IMG-Generate.png"),QIcon.Normal,QIcon.Off)
        self.BtnGenerate = QPushButton(self.groupBoxData)
        self.BtnGenerate.setIcon(self.iconGenerate)
        self.BtnGenerate.setGeometry(QRect(10,140,90,31))
        self.BtnGenerate.setText("Generate")
        self.BtnGenerate.clicked.connect(self.Generate)

        self.iconClean = QIcon()
        self.iconClean.addPixmap(QPixmap("img/IMG-Clean.png"),QIcon.Normal,QIcon.Off)
        self.BtnClean = QPushButton(self.groupBoxData)
        self.BtnClean.setIcon(self.iconClean)
        self.BtnClean.setGeometry(QRect(220,140,91,31))
        self.BtnClean.setText("Clean")
        self.BtnClean.clicked.connect(self.Clean)

        self.BtnSaveFile = QPushButton(self.groupBoxTools)
        self.BtnSaveFile.setGeometry(QRect(230,40,61,23))
        self.BtnSaveFile.setText("Save")
        self.BtnSaveFile.clicked.connect(self.SaveFile)

        # Creamos el tablewidget
        self.fakeTable = QTableWidget(self)
        self.fakeTable.setGeometry(QRect(340,20,600,261))
        self.fakeTable.setColumnCount(0)
        self.fakeTable.setRowCount(0)
        self.fakeTable.setAlternatingRowColors(True)
        self.fakeTable.setEditTriggers(QTableWidget.AllEditTriggers)
        self.fakeTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.fakeTable.setSelectionMode(QTableWidget.SingleSelection)

        self.InitComoBox()

        self.arrayItems = ["Name","Address","Email","Password","Country"]

        self.result = []

        self.existFilters = False


    def OpenFilters(self):
        winFilters = Filters()
        winFilters.setWindowModality(Qt.ApplicationModal)
        winFilters.exec_()
        self.result = winFilters.GetArray()
        if(len(self.result) == 0):
            self.existFilters = False
        else:
            self.UpdateTable()
            self.existFilters = True
    
    def UpdateTable(self):
        self.result.pop(0)
        self.fakeTable.clear()
        self.fakeTable.setColumnCount(len(self.result))
        self.fakeTable.setHorizontalHeaderLabels(self.result)
    
    def SearchMatches(self,list1,list2):
        for i in list1:
            for position, j in enumerate(list2):
                if i == j:
                    yield position

    def Generate(self):
        # Gets selected item from combobox
        selectedCboNumber  = self.CboNumbers.currentText()
        # Gets Numeber from customized textbox
        selectedtextNumber = self.txtNumber.text()

        if(self.existFilters):
            if(self.CboNumbers.currentIndex() != 0):
                for item in range(int(selectedCboNumber)-1):
                    self.GeneratewithFilters()
            if(len(self.txtNumber.text()) != 0):
                for item in range(int(selectedtextNumber)):
                    self.GeneratewithFilters()
            else:
                self.GeneratewithFilters()

        if(self.existFilters == False):
            if(self.CboNumbers.currentIndex() != 0):
                for item in range(int(selectedCboNumber)-1):
                    self.LoadTable()
            if(len(self.txtNumber.text()) != 0):
                for item in range(int(selectedtextNumber)):
                    self.LoadTable()
            else:
                self.LoadTable()

    def Clean(self):
        self.txtNumber.clear()
        self.CboNumbers.setCurrentIndex(0)

        while(self.fakeTable.rowCount() > 0):
            self.fakeTable.removeRow(0)
        self.fakeTable.setColumnCount(0)
        self.existFilters = False
        self.CboTools.setCurrentIndex(0)

    def GeneratePassword(self):
        resultPassword = self.faker.lexify(text='????????')
        return resultPassword
    
    def InitComoBox(self):
        self.CboNumbers.addItems(['Select Number','5','10','15'])
        self.CboTools.addItems(["Select Option","CSV","TXT"])

    def LoadTable(self):
        self.fakeTable.setColumnCount(len(self.arrayItems))
        self.fakeTable.setHorizontalHeaderLabels(self.arrayItems)

        password = self.GeneratePassword()

        rowPosition = self.fakeTable.rowCount()
        self.fakeTable.insertRow(rowPosition)

        self.fakeTable.setItem(rowPosition,0,QTableWidgetItem(str(self.faker.name())))
        self.fakeTable.setItem(rowPosition,1,QTableWidgetItem(str(self.faker.address())))
        self.fakeTable.setItem(rowPosition,2,QTableWidgetItem(str(self.faker.email())))
        self.fakeTable.setItem(rowPosition,3,QTableWidgetItem(str(password)))
        self.fakeTable.setItem(rowPosition,4,QTableWidgetItem(str(self.faker.country())))
    
    # Generate dinamic Data from the filters
    def GeneratewithFilters(self):
        # Generate Password
        password = self.GeneratePassword()

        rowPosition = self.fakeTable.rowCount()
        self.fakeTable.insertRow(rowPosition)

        # Create array of Objects
        self.arrayFakes = self.faker.name(), self.faker.address(),self.faker.email(), password, self.faker.country()

        position = 0
        for item in self.SearchMatches(self.result,self.arrayItems):
            self.fakeTable.setItem(rowPosition,position,QTableWidgetItem(str(self.arrayFakes[item])))
            position += 1

    # Create File CSV or TXT
    def CreateFile(self,fileName):
        with open(fileName, 'w') as stream:
            writer = csv.writer(stream, lineterminator='\n')          
            for row in range(self.fakeTable.rowCount()):
                rowdata = []
                for column in range(self.fakeTable.columnCount()):
                    item = self.fakeTable.item(row, column)
                    if item is not None:
                        rowdata.append(item.text())                   
                    else:
                        rowdata.append('')
                writer.writerow(rowdata)

    # Save selected Option
    def SaveFile(self):
        selectedOption = self.CboTools.currentIndex()
        if(selectedOption == 1):
            self.CreateFile('SaveData.csv')
        if(selectedOption == 2):
            self.CreateFile('SaveData.txt')

      

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    
    win = MainApplication()
    
    win.show()
    
    sys.exit(app.exec_())
