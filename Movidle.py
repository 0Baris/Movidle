from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox, QLineEdit,QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, QLineEdit
from PyQt5.QtGui import QIcon,QKeySequence
import sqlite3
import random
import sys

class Ui_Movidle(object):

    def __init__(self):
        super().__init__()

        ## veri tabanı bağlama
        self.conn = sqlite3.connect('data\Movidle.db')
        self.cursor = self.conn.cursor()
        self.listWidget = QtWidgets.QListWidget()


        ## film türleri seçme
        self.cursor.execute('SELECT isim, turler FROM filmler')
        self.films = self.cursor.fetchall()
        self.selected_films = []

    ## ARAYÜZ
    def setupUi(self, Movidle):
        Movidle.setObjectName("Movidle")
        Movidle.setWindowModality(QtCore.Qt.ApplicationModal)
        Movidle.setFixedSize(640, 680)
        icon = QtGui.QIcon('data\icon.png')
        icon.addPixmap(QtGui.QPixmap("Untitled.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Movidle.setWindowIcon(icon)
        Movidle.setStatusTip("")
        Movidle.setAutoFillBackground(False)
        Movidle.setInputMethodHints(QtCore.Qt.ImhNone)
        Movidle.setProperty("Logo", QtGui.QPixmap("data\logo1.png"))
        self.centralwidget = QtWidgets.QWidget(Movidle)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 641, 661))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")

        #Yazı
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 310, 637, 15))
        font = QtGui.QFont()
        font.setFamily("Montserrat ExtraBold")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setMouseTracking(False)
        self.label.setObjectName("label")

        ## Temizleme
        self.sil = QtWidgets.QPushButton(Movidle)
        self.sil.setGeometry(QtCore.QRect(10, 10, 50, 20))
        self.sil.clicked.connect(self.temizle)

        ## HTML Olarak Kaydet
        self.kaydet = QtWidgets.QPushButton(Movidle)
        self.kaydet.setGeometry(QtCore.QRect(10, 30, 50, 20))
        self.kaydet.clicked.connect(self.htmlkaydet)

        ## Arama Kısmı
        self.arama = QLineEdit(Movidle)
        self.arama.setPlaceholderText("Arama yapın...")
        self.arama.setGeometry(QtCore.QRect(10, 93, 620, 20))

        #Yazı
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 410, 637, 15))
        font = QtGui.QFont()
        font.setFamily("Montserrat ExtraBold")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        #Logo
        self.photo = QtWidgets.QLabel(self.groupBox)
        self.photo.setGeometry(QtCore.QRect(240, 0, 141, 91))
        self.photo.setText("")
        self.photo.setPixmap(QtGui.QPixmap("data\movidlelogoüst.png"))
        self.photo.setObjectName("photo")

        #Üst Buton
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(10, 280, 621, 23))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        #Alt buton
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 620, 621, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.cikis)

        #Film Listesi
        self.list_Widget = QtWidgets.QListWidget(self.groupBox)
        self.list_Widget.setSelectionMode(QListWidget.MultiSelection)
        self.list_Widget.setGeometry(QtCore.QRect(10, 120, 621, 151))
        self.list_Widget.setObjectName("listWidget")

        ## Filmleri listeye aktarma
        for i, (film_isim, film_tur) in enumerate(self.films, start=1):
            self.list_Widget.addItem(f"{i}. {film_isim}")

        #Seçilen Filmler
        self.list_Widget_2 = QtWidgets.QListWidget(self.groupBox)
        self.list_Widget_2.setGeometry(QtCore.QRect(10, 330, 621, 71))
        self.list_Widget_2.setObjectName("listWidget_2")


        #Önerilen Filmler
        self.list_Widget_3 = QtWidgets.QListWidget(self.groupBox)
        self.list_Widget_3.setGeometry(QtCore.QRect(10, 430, 621, 151))
        self.list_Widget_3.setObjectName("listWidget_3")
        self.list_Widget_3.setSelectionMode(QListWidget.MultiSelection)


        Movidle.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Movidle)
        self.statusbar.setObjectName("statusbar")
        Movidle.setStatusBar(self.statusbar)
        self.retranslateUi(Movidle)
        QtCore.QMetaObject.connectSlotsByName(Movidle)

        # Butonları Bağlama
        self.pushButton.clicked.connect(self.algo)
        self.arama.textChanged.connect(self.aramafiltresi)

    ## UI Yazıları
    def retranslateUi(self, Movidle):
        _translate = QtCore.QCoreApplication.translate
        Movidle.setWindowTitle(_translate("Movidle", "Movidle"))
        self.label.setText(_translate("Movidle", "Seçilen Filmler:"))
        self.label_3.setText(_translate("Movidle", "Önerilen Filmler:"))
        self.pushButton.setText(_translate("Movidle", "Seçilen Filmleri Göster"))
        self.pushButton_2.setText(_translate("Movidle", "Çık"))
        self.sil.setText(_translate("Movidle", "Temizle"))
        self.kaydet.setText(_translate("Movidle", "Kaydet"))

    ## Filmleri Gösteren Algoritma
    def algo(self):
        #seçilen filmler
        selected_items = self.list_Widget.selectedItems()

        if len(selected_items) != 4:
            QMessageBox.critical(self.groupBox, 'Movidle', 'Lütfen sadece 4 tane film seçin!', QMessageBox.Ok)
            return
        self.selected_films = [int(item.text().split(".")[0]) for item in selected_items]

        #ekrana yazdırma
        self.list_Widget_2.clear()
        for i in self.selected_films:
            film_isim, film_tur = self.films[i - 1] 
            self.list_Widget_2.addItem(f"{film_isim}")

        #öneri
        film_oneri = []
        for _ in range(10):
            randomfilm = random.choice(self.films)
            film_oneri.append(randomfilm)

        #gösterme
        self.list_Widget_3.clear()
        for film_isim, film_tur in film_oneri:
            self.list_Widget_3.addItem(f'{film_isim}')


    ## Arama Filtresi
    def aramafiltresi(self):
        metin = self.arama.text().lower()

        for i in range(self.list_Widget.count()):
            item = self.list_Widget.item(i)
            if metin in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    ## Listeleri Temizleme
    def temizle(self):
        self.list_Widget_3.clear()
        self.list_Widget_2.clear()
        self.arama.clear()
        self.list_Widget.selectionModel().clear()
        QMessageBox.information(self.groupBox, 'Movidle', 'Temizlendi.', QMessageBox.Ok)

    ## HTML Dosyasına Kaydetme
    def htmlkaydet(self):
        htmlicerigi = "<html><body>"

        for film in range(self.list_Widget_3.count()):
            item = self.list_Widget_3.item(film)
            yazı = item.text()
            htmlicerigi += f"<p>{yazı}</p>"

        with open("kaydedilen.html", "w") as file:
            file.write(htmlicerigi)

        QMessageBox.information(self.groupBox, 'Movidle', 'Filmler klasörün konumuna kaydedildi.', QMessageBox.Ok)

    ## Çıkış Sorgusu
    def cikis(self):
        cikis = QMessageBox.question(self.groupBox, 'Movidle', 'Çıkmak ister misiniz?', QMessageBox.Yes | QMessageBox.No)
        if cikis == QMessageBox.Yes:
            sys.exit()


## Client Oluşturma,Döngüye Sokma
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Movidle = QtWidgets.QMainWindow()
    ui = Ui_Movidle()
    ui.setupUi(Movidle)
    Movidle.show()
    sys.exit(app.exec_())