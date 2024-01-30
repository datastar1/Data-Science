from datetime import datetime
import sys
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtWidgets, QtCore, QtGui
from datetime import date
import meteostat_diagramm

#Standardwerte, die von Anfang an gesetzt werden
city_name="Mainz"
startdate=datetime.strptime("1,1,2010","%d,%m,%Y")
enddate=datetime.strptime("1,1,2022","%d,%m,%Y")
dia_type="daily"

#Klasse fürs Hauptfenster mit widgets
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow") #Setzen des Hauptfensters
        MainWindow.resize(1400, 1200)
        self.centralwidget = QtWidgets.QWidget(MainWindow) #Widget für das Fenster
        self.centralwidget.setObjectName("centralwidget")
        self.web = QWebEngineView(MainWindow)  #Widget zur Darstellung von Html-Seiten
        self.web2 = QWebEngineView(MainWindow)
        self.web.load(QtCore.QUrl.fromLocalFile("E:\python_projects\PycharmProjects\Projektarbeit2\Stationen.html")) #Deutschlandkarte eingebaut
        self.web.setGeometry(QtCore.QRect(1, 1, 720, 920))   #Position und Größe (Position x,y. Größe x,y)
        self.web2.load(QtCore.QUrl.fromLocalFile(f"E:\python_projects\PycharmProjects\Projektarbeit2\{city_name}_DataProfil.html"))
        self.web2.setGeometry(QtCore.QRect(700, 1, 700, 800))
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(440, 50, 120, 80))
        self.widget.setObjectName("widget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(430, 190, 120, 80))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.Startdatum = QtWidgets.QDateEdit(self.centralwidget)  #Eingabefenster für das Startdatum
        self.Startdatum.setGeometry(QtCore.QRect(930, 850, 110, 22))
        self.Startdatum.setDateTime(QtCore.QDateTime(QtCore.QDate(2010, 1, 1)))  #Standarddatum gesetzt
        self.Startdatum.setCalendarPopup(True)  # ausklabbarer Kalender
        self.Startdatum.setObjectName("Startdatum")
        self.Startdatum.raise_()
        self.Enddatum = QtWidgets.QDateEdit(self.centralwidget)
        self.Enddatum.setGeometry(QtCore.QRect(1050,850, 110, 22))  #Eingabefenster für das Enddatum
        self.Enddatum.setCalendarPopup(True)
        self.Enddatum.setObjectName("Enddatum")
        self.Enddatum.setDateTime(QtCore.QDateTime(QtCore.QDate(2022, 1, 1)))
        self.Enddatum.raise_()
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(930, 830, 101, 16))
        self.label.setObjectName("label")
        self.label.raise_()
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1050, 830, 101, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.raise_()
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(930, 910, 101, 16))
        self.label_4.setObjectName("label_4")
        self.label_4.raise_()
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(1050, 910, 101, 16))
        self.label_5.setObjectName("label_5")
        self.label_5.raise_()
        self.setstart = QtWidgets.QPushButton(self.centralwidget)  # Knopf zum setzen des Startdatums
        self.setstart.setGeometry(QtCore.QRect(930, 880, 70, 17))
        self.setstart.setObjectName("setstart")
        self.setlast = QtWidgets.QPushButton(self.centralwidget)    # Knopf zum setzen des Enddatums
        self.setlast.setGeometry(QtCore.QRect(1050, 880, 70, 17))
        self.setlast.setObjectName("setlast")
        self.startplot = QtWidgets.QPushButton(self.centralwidget)  # Knopf zum starten eines Plots
        self.startplot.setGeometry(QtCore.QRect(930, 1110, 70, 17))
        self.startplot.setObjectName("startplot")
        self.diaset = QtWidgets.QPushButton(self.centralwidget)
        self.diaset.setGeometry(QtCore.QRect(1050, 1040, 70, 17)) # Knopf setzen des Datenprofils
        self.diaset.setObjectName("startplot")
        self.listView = QtWidgets.QListView(self.centralwidget)  # Liste zur Abgrenzung
        self.listView.setGeometry(QtCore.QRect(920, 830, 256, 330))
        self.listView.setObjectName("listView")
        self.listView.lower()
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(920, 800, 251, 31))
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        #Radio Buttons zur Auswahl der einzelnen Städte
        self.Bremen = QtWidgets.QRadioButton(self.centralwidget) #Radio button zum setzen der Stadt
        self.Bremen.setGeometry(QtCore.QRect(930, 940, 70, 17))
        self.Bremen.setObjectName("Bremen")     # Objektname
        self.Mainz = QtWidgets.QRadioButton(self.centralwidget)
        self.Mainz.setGeometry(QtCore.QRect(930, 960, 70, 17))
        self.Mainz.setObjectName("Mainz")

        self.Mannheim = QtWidgets.QRadioButton(self.centralwidget)
        self.Mannheim.setGeometry(QtCore.QRect(930, 980, 70, 17))
        self.Mannheim.setObjectName("Mannheim")
        self.Berlin = QtWidgets.QRadioButton(self.centralwidget)
        self.Berlin.setGeometry(QtCore.QRect(930, 1000, 70, 17))
        self.Berlin.setObjectName("Berlin")
        self.Leipzig = QtWidgets.QRadioButton(self.centralwidget)
        self.Leipzig.setGeometry(QtCore.QRect(930, 1020, 70, 17))
        self.Leipzig.setObjectName("Leipzig")
        self.Dresden = QtWidgets.QRadioButton(self.centralwidget)
        self.Dresden.setGeometry(QtCore.QRect(930, 1040, 70, 17))
        self.Dresden.setObjectName("Dresden")
        self.Stuttgart = QtWidgets.QRadioButton(self.centralwidget)
        self.Stuttgart.setGeometry(QtCore.QRect(930, 1060, 70, 17))
        self.Stuttgart.setObjectName("Stuttgart")
        self.München = QtWidgets.QRadioButton(self.centralwidget)
        self.München.setGeometry(QtCore.QRect(930, 1080, 70, 17))
        self.München.setObjectName("München")
        self.radioButton_4 = QtWidgets.QRadioButton(self.centralwidget)  # Knopf zum setzen des Zeitraums
        self.radioButton_4.setGeometry(QtCore.QRect(1050, 940, 70, 17))
        self.radioButton_4.setObjectName("radioButton")

        self.radioButton_5 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_5.setGeometry(QtCore.QRect(1050, 960, 70, 17))
        self.radioButton_5.setObjectName("radioButton")
        self.radioButton_6 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_6.setGeometry(QtCore.QRect(1050, 980, 70, 17))
        self.radioButton_6.setObjectName("radioButton")

        self.radioButton_7 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_7.setGeometry(QtCore.QRect(1050, 1000, 70, 17))
        self.radioButton_7.setObjectName("normals")
        #Radio buttons in Gruppen zusammengefasst, damit nur Auswahl untereinander besteht
        self.buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.Bremen)  # Gruppierung der Knöpfe zur Unterscheidung von Städte und Datenknöpfen
        self.buttonGroup.addButton(self.Mainz)
        self.buttonGroup.addButton(self.Mannheim)
        self.buttonGroup.addButton(self.Dresden)
        self.buttonGroup.addButton(self.München)
        self.buttonGroup.addButton(self.Stuttgart)
        self.buttonGroup.addButton(self.Leipzig)
        self.buttonGroup.addButton(self.Berlin)
        self.buttonGroup_2 = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        self.buttonGroup_2.addButton(self.radioButton_4)
        self.buttonGroup_2.addButton(self.radioButton_5)
        self.buttonGroup_2.addButton(self.radioButton_6)
        self.buttonGroup_2.addButton(self.radioButton_7)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.setstart.clicked.connect(self.show_start)  # Codezeile zur Verknüpfung von Knöpfen mit Methoden
        self.setlast.clicked.connect(self.show_last)
        self.startplot.clicked.connect(self.plotter)
        self.diaset.clicked.connect(self.dataprofile)

        self.Bremen.toggled.connect(lambda: self.citystate(self.Bremen))  # Codezeile zur Verknüpfung von gesetzten Radiobuttons
        self.Mainz.toggled.connect(lambda: self.citystate(self.Mainz))
        self.Mannheim.toggled.connect(lambda: self.citystate(self.Mannheim))
        self.Dresden.toggled.connect(lambda: self.citystate(self.Dresden))
        self.München.toggled.connect(lambda: self.citystate(self.München))
        self.Stuttgart.toggled.connect(lambda: self.citystate(self.Stuttgart))
        self.Leipzig.toggled.connect(lambda: self.citystate(self.Leipzig))
        self.Berlin.toggled.connect(lambda: self.citystate(self.Berlin))
        self.radioButton_4.toggled.connect(lambda: self.datestate(self.radioButton_4))
        self.radioButton_5.toggled.connect(lambda: self.datestate(self.radioButton_5))
        self.radioButton_6.toggled.connect(lambda: self.datestate(self.radioButton_6))
        self.radioButton_7.toggled.connect(lambda: self.datestate(self.radioButton_7))
        self.startplot.raise_()

    def retranslateUi(self, MainWindow):    #Beschriftung der verschiedenen Buttons und Zugehörigkeit
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Enter first date"))
        self.label_4.setText(_translate("MainWindow", "Choose station"))
        self.label_5.setText(_translate("MainWindow", "Choose Datatype"))
        self.Startdatum.setToolTip(
            _translate("MainWindow", "<html><head/><body><p>Please input a date!</p></body></html>"))

        self.label_2.setText(_translate("MainWindow", "Enter last date"))
        self.Enddatum.setToolTip(
            _translate("MainWindow", "<html><head/><body><p>Please Enter a date!</p></body></html>"))
        self.setstart.setText(_translate("MainWindow", "Set date"))
        self.setstart.setToolTip(
            _translate("MainWindow", "<html><head/><body><p>Accept the date</p></body></html>"))

        self.setlast.setText(_translate("MainWindow", "Set date"))
        self.setlast.setToolTip(
            _translate("MainWindow", "<html><head/><body><p>Accept the date</p></body></html>"))
        self.startplot.setText(_translate("MainWindow", "start plot"))
        self.startplot.setToolTip(
            _translate("MainWindow", "<html><head/><body><p>start plot</p></body></html>"))
        self.diaset.setText(_translate("MainWindow", "Dataprofile"))
        self.setlast.setToolTip(
            _translate("MainWindow", "<html><head/><body><p>Set Dataprofile of active City</p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "Weatherdata"))

        self.Bremen.setText(_translate("Mainwindow", "Bremen"))
        self.Mainz.setText(_translate("Mainwindow", "Mainz"))
        self.Mannheim.setText(_translate("Mainwindow", "Mannheim"))
        self.Dresden.setText(_translate("Mainwindow", "Dresden"))
        self.München.setText(_translate("Mainwindow", "München"))
        self.Berlin.setText(_translate("Mainwindow", "Berlin"))
        self.Stuttgart.setText(_translate("Mainwindow", "Stuttgart"))
        self.Leipzig.setText(_translate("Mainwindow", "Leipzig"))
        self.radioButton_4.setText(_translate("Mainwindow", "daily"))
        self.radioButton_5.setText(_translate("Mainwindow", "monthly"))
        self.radioButton_6.setText(_translate("Mainwindow", "annually"))
        self.radioButton_7.setText(_translate("Mainwindow", "normals"))

    def show_start(self):  #Setzen des Startdatums
        start= (self.Startdatum.date().getDate())
        global startdate
        start2=date(*start)
        startdate2=start2.strftime("%d,%m,%Y")
        startdate=datetime.strptime(startdate2,"%d,%m,%Y")
        print(startdate)

    def show_last(self):  #Setzen des Enddatums
        last = (self.Enddatum.date().getDate())
        global enddate
        end = date(*last)
        enddate2= end.strftime("%d,%m,%Y")
        enddate= datetime.strptime(enddate2,"%d,%m,%Y")
        print(enddate)

    def citystate(self,b):  # Setzen der Stadt

        if b.isChecked():
            global city_name
            city_name= b.text()

    def datestate(self,c): # Setzen des Datentyps
        if c.isChecked():
            global dia_type
            dia_type= c.text()
            print(dia_type)

    def plotter(self):  # Ansprechen der Plotfuntkion

        Meteo=meteostat_diagramm.diagramm_server(city_name, startdate, enddate, dia_type)
        return Meteo

    def dataprofile(self):  # Änderung des Dataprofile fensters
        self.web2.load(QtCore.QUrl.fromLocalFile(f"E:\python_projects\PycharmProjects\Projektarbeit2\{city_name}_DataProfil.html"))




if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
