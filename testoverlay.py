import sys
import mainscript
from PyQt5 import QtGui, QtCore, uic
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QWidget
import mainapp
import time
from threading import Thread, Event, Timer


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
        self.old_height = 1
        self.old_pk = None
        self.setMouseTracking(True)

        self.image = {}
        self.text = {}
        for i in range(0, 18):
            self.image[str(i)] = QLabel(self)
            self.text[str(i)] = QLabel(self)

        self.styles = {"default": default(self), "info": info(self)}
        self.style = "default"

    def mouseMoveEvent(self, event):
         #print(event.x(), event.y())
         pass

    def change_style(self, style):
        self.style = style
        self.styles[style].initialisation(self)

    def mousePressEvent(self, event):
        QtWidgets.qApp.quit()

    def load_image(self, name, image, x, y, size=64, height=64):
        pixmap = QPixmap(image)
        self.image[name].setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        pixmap2 = pixmap.scaledToWidth(size)
        self.image[name].setGeometry(x, y, size, height)
        self.image[name].setPixmap(pixmap2)
    
    def load_text(self, name, text, x, y):
        self.text[name].setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.text[name].setGeometry(x, y, 100, 64)
        self.text[name].setText(text)
        self.text[name].setStyleSheet("QLabel { color : black; font-size: 20px; font-weight: bold; font-family: Arial; }")


    def actualize(self):
        pk = mainapp.get_pk()
        if mainscript.get_pokemon_res_csv(pk) == 0:
            if self.windowOpacity != 0.1:
                    self.setWindowOpacity(0.1)
        else:
            if pk != self.old_pk:
                self.styles[self.style].actualize_type(pk)
                self.styles[self.style].setGeometry()
                if self.windowOpacity != 1:
                    self.setWindowOpacity(1)

class default():
    def __init__(self, mainwindow):
        self.style = "default"
        
    
    def initialisation(self, mainwindow):
        self.mainwindow = mainwindow
        self.mainwindow.setGeometry(QtCore.QRect(MainWindow.Wx-80, int(MainWindow.Wy/2-self.mainwindow.old_height/2), 1, 1))

    def setGeometry(self):
        self.mainwindow.setGeometry(QtCore.QRect(MainWindow.Wx-80, int(MainWindow.Wy/2-self.mainwindow.old_height/2), 80, self.mainwindow.old_height))

    def actualize_type(self, pk):
        pokemon, pk, other = mainscript.get_pokemon_res_csv(pk)
        self.mainwindow.old_pk = pk
        if pokemon == None:
            return 0
        
        counter = 0
        for i in pokemon.keys():
            if pokemon[i] != None:
                self.mainwindow.load_image(str(counter),'type/'+str(i)+'.png', 10, counter*70)
                self.mainwindow.load_text(str(counter),str(pokemon[i]), 30, counter*70)
                counter += 1
        self.mainwindow.old_height = counter * 70

class info:
    def __init__(self, mainwindow):
        self.style = "info"
        mainwindow.text["name"] = QLabel(mainwindow)
        mainwindow.text["weight"] = QLabel(mainwindow)
        mainwindow.text["speed"] = QLabel(mainwindow)

        mainwindow.text["x025"] = QLabel(mainwindow)
        mainwindow.text["x05"] = QLabel(mainwindow)
        mainwindow.text["x1"] = QLabel(mainwindow)
        mainwindow.text["x2"] = QLabel(mainwindow)
        mainwindow.text["x4"] = QLabel(mainwindow)

        mainwindow.image["line1"] = QLabel(mainwindow)
        mainwindow.image["line2"] = QLabel(mainwindow)
        mainwindow.image["line3"] = QLabel(mainwindow)
        mainwindow.image["line4"] = QLabel(mainwindow)
        mainwindow.image["line5"] = QLabel(mainwindow)
        mainwindow.image["line6"] = QLabel(mainwindow)

        
    def setGeometry(self):
        self.mainwindow.setGeometry(QtCore.QRect(MainWindow.Wx-400, 20, 380, 380))

    def initialisation(self, mainwindow):
        self.mainwindow = mainwindow
        self.mainwindow.setGeometry(QtCore.QRect(MainWindow.Wx-400, 20, 380, 380))

    def actualize_type(self, pk):
        pokemon, pk, other = mainscript.get_pokemon_res_csv(pk)
        self.mainwindow.old_pk = pk
        if pokemon == None:
            return 0
        
        lvl = 100
        base = other[2]

        max_speed = int((((2*base+31+(252/4)) * lvl) / 100 + 5)*1.1)
        self.mainwindow.load_text("name", pk, 10, 5)
        self.mainwindow.load_text("weight", str(other[3])+"kg", 300, 5)
        self.mainwindow.load_text("speed", str(max_speed), 300, 25)

        self.mainwindow.load_text("x025", "x0.25", 10, 80)
        self.mainwindow.load_text("x05", "x0.5", 10, 120)
        self.mainwindow.load_text("x1", "x0", 10, 160)
        self.mainwindow.load_text("x2", "x2", 10, 200)
        self.mainwindow.load_text("x4", "x4", 10, 240)

        self.mainwindow.load_image("line1", "image/line.png", 10, 88, 360, 5)
        self.mainwindow.load_image("line2", "image/line.png", 10, 128, 360, 5)
        self.mainwindow.load_image("line3", "image/line.png", 10, 168, 360, 5)
        self.mainwindow.load_image("line4", "image/line.png", 10, 208, 360, 5)
        self.mainwindow.load_image("line5", "image/line.png", 10, 248, 360, 5)
        self.mainwindow.load_image("line6", "image/line.png", 10, 288, 360, 5)


        counter = {"80":0, "120":0, "160":0, "200":0, "240":0}
        new_counter = 0
        for i in pokemon.keys():
            if pokemon[i] != None:

                if pokemon[i] == 0.25:
                    y = 80
                    counter[str(y)] += 1
                elif pokemon[i] == 0.5:
                    y = 120
                    counter[str(y)] += 1
                elif pokemon[i] == 0:
                    y = 160
                    counter[str(y)] += 1
                elif pokemon[i] == 2:
                    y = 200
                    counter[str(y)] += 1
                elif pokemon[i] == 4:
                    y = 240
                    counter[str(y)] += 1

                self.mainwindow.load_image(str(new_counter),'type/'+str(i)+'.png', 35+counter[str(y)]*35, y+15, 30, 30)
                new_counter += 1





if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MainWindow()

    style = input("Quelle Style voulez vous ? (default, info) : ")
    styles = ["default", "info"]

    while style not in styles:
        style = input("Quelle Style voulez vous ? (default, info) : ")

    mywindow.change_style(style)
    mywindow.show()
    timer = QTimer()
    timer.timeout.connect(mywindow.actualize)  
    timer.setInterval(100)  # 1000ms = 1s
    timer.start()
    app.exec_()

    
