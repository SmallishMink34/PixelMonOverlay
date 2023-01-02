import sys
import mainscript
from PyQt5 import QtGui, QtCore, uic
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
import mainapp
import time
from threading import Thread, Event, Timer
#a
class MainWindow(QMainWindow):
    Wx = 1920
    Wy = 1080
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )
        self.image = {}
        self.text = {}
        for i in range(0, 18):
            self.image[str(i)] = QLabel(self)
            self.text[str(i)] = QLabel(self)
        self.old_pk = None
        self.old_height = 1
        self.setGeometry(QtCore.QRect(MainWindow.Wx-80, int(MainWindow.Wy/2-self.old_height/2), 1, 1))

        
    
    def actualize_type(self, pk):
        
        pokemon = mainscript.get_pokemon_res(pk)
        self.old_pk = pk
        if pokemon == None:
            return 0
        
        counter = 0
        for i in pokemon.keys():
            if pokemon[i] != None:
                self.load_image(str(counter),'type/'+str(i)+'.png')
                self.load_text(str(counter),str(pokemon[i]))
                counter += 1
        self.old_height = counter * 70
        
    def load_image(self, name, image):
        
        pixmap = QPixmap(image)
        self.image[name].setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        pixmap2 = pixmap.scaledToWidth(64)
        self.image[name].setGeometry(10, 0+70*int(name), 64, 64)
        self.image[name].setPixmap(pixmap2)
    
    def load_text(self, name, text):
        
        self.text[name].setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.text[name].setGeometry(30, int(name)*70, 100, 64)
        self.text[name].setText(text)
        self.text[name].setStyleSheet("QLabel { color : black; font-size: 20px; font-weight: bold; font-family: Arial; }")
    def actualize(self):
        pk = mainapp.get_pk()
        if mainscript.get_pokemon_res(pk) == 0:
            if self.windowOpacity != 0.1:
                    self.setWindowOpacity(0.1)
        else:
            if pk != self.old_pk:
                self.actualize_type(pk)
                self.setGeometry(QtCore.QRect(MainWindow.Wx-80, int(MainWindow.Wy/2-self.old_height/2), 80, self.old_height))
                if self.windowOpacity != 1:
                    self.setWindowOpacity(1)

    def mousePressEvent(self, event):
        QtWidgets.qApp.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MainWindow()
    mywindow.show()
    timer = QTimer()
    timer.timeout.connect(mywindow.actualize)  # execute `display_time`
    timer.setInterval(500)  # 1000ms = 1s
    timer.start()
    app.exec_()

    
