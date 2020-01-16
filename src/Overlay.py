#!/usr/bin/env python

#----------------------------------

from __future__ import division
import sys
#from PyQt4.QtCore import Qt
#from PyQt4.QtGui import QtGui
from PyQt5 import QtCore, QtGui, QtWidgets

class Overlay(QtWidgets.QWidget):
 
    def __init__(self, parent = None, text='xxx'):
 
        QtWidgets.QWidget.__init__(self, parent)
        palette = QtGui.QPalette(self.palette())
        palette.setColor(palette.Background, QtCore.Qt.transparent)
        self.setPalette(palette)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.text = text

 
    def paintEvent(self, event): 
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        self.drawCross(qp)
        self.drawText(qp)
        qp.end()


    def drawCross(self,qp) :
        qp.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0)))
        qp.drawLine(self.width()//8, self.height()//8, 7*self.width()//8, 7*self.height()//8)
        qp.drawLine(self.width()//8, 7*self.height()//8, 7*self.width()//8, self.height()//8)


    def drawText(self,qp) :
        qp.setFont(QtGui.QFont('Decorative', 10))
        #qp.setPen(QtCore.Qt.red)
        qp.setPen(QtGui.QPen(QtGui.QColor(150, 100, 50)))
        qp.drawText(10,10,self.text)

 
#----------------------------------
# TEST stuff:

class MyWindow(QtWidgets.QMainWindow):
 
    def __init__(self, parent = None):
 
        QtWidgets.QMainWindow.__init__(self, parent)
 
        widget = QtWidgets.QWidget(self)
        self.editor = QtWidgets.QTextEdit()
        layout = QtWidgets.QGridLayout(widget)
        layout.addWidget(self.editor,            0, 0, 1, 2)
        layout.addWidget(QtWidgets.QPushButton("Refresh"), 1, 0)
        layout.addWidget(QtWidgets.QPushButton("Cancel"),  1, 1)
 
        self.setCentralWidget(widget)
        self.overlay = Overlay(self.centralWidget())
 
    def resizeEvent(self, event):
 
        self.overlay.resize(event.size())
        event.accept()
 
#----------------------------------
 
if __name__ == "__main__": 
    app = QtWidgets.QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())

#----------------------------------
