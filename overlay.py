import sys

from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QRect
import d3dshot
import PIL
import numpy

d = d3dshot.create(capture_output="numpy")

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(
            QtWidgets.QStyle.alignedRect(
                QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter,
                QtCore.QSize(2560 , 1440),
                QtWidgets.qApp.desktop().availableGeometry()
        ))
        self.initUI()
     
    def initUI(self):
        self.rects =  []

    def mousePressEvent(self, event):
        QtWidgets.qApp.quit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.blue, 1, Qt.SolidLine))
        #painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        #painter.setBrush(QBrush(Qt.green, Qt.DiagCrossPattern))
        self.findHotSpots()
        for rect in self.rects:
            painter.drawRect(rect)
        self.update()
    def findHotSpots(self):
        try:
            im = d.screenshot()
            c = (200, 0, 0)
            indices = numpy.where(numpy.all(im == c, axis=-1))
            coords = zip(indices[0], indices[1])
            self.rects = []
            for fpixels in coords:
                x = fpixels[0]
                y = fpixels[1]
                self.rects.append(QRect(y-3,x+17,5,5))
        except Exception as e:
           print(e)        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MainWindow()
    mywindow.show()
    app.exec_()
