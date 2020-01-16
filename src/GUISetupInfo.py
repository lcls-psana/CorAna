#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUISetupInfo...
#
#------------------------------------------------------------------------

"""GUI Setup Info"""
from __future__ import absolute_import

#------------------------------
#  Module's version from CVS --
#------------------------------
__version__ = "$Revision$"
# $Source$

#--------------------------------
#  Imports of standard modules --
#--------------------------------
import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
#import time   # for sleep(sec)

#-----------------------------
# Imports for other modules --
#-----------------------------

from .ConfigParametersCorAna import confpars as cp

from .GUISetupInfoLeft   import *
from .GUISetupInfoRight  import *
from CorAna.Logger             import logger

#---------------------
#  Class definition --
#---------------------
class GUISetupInfo ( QtWidgets.QWidget ) :
    """GUI Setup Info"""

    #----------------
    #  Constructor --
    #----------------
    def __init__ ( self, parent=None ) :

        QtWidgets.QWidget.__init__(self, parent)

        self.setGeometry(200, 400, 500, 630)
        self.setWindowTitle('Setup Info')
        self.setFrame()
 
        self.tit_title  = QtWidgets.QLabel('Setup Info')
        self.tit_status = QtWidgets.QLabel('Status: ')
        self.but_close  = QtWidgets.QPushButton('Close') 
        self.but_apply  = QtWidgets.QPushButton('Save') 
        self.but_show   = QtWidgets.QPushButton('Show Image')
        cp.guisetupinfoleft  = GUISetupInfoLeft()
        cp.guisetupinforight = GUISetupInfoRight()

        self.hboxM = QtWidgets.QHBoxLayout()
        self.hboxM.addWidget(cp.guisetupinfoleft)
        self.hboxM.addWidget(cp.guisetupinforight)

        self.hboxB = QtWidgets.QHBoxLayout()
        self.hboxB.addWidget(self.tit_status)
        self.hboxB.addStretch(1)     
        self.hboxB.addWidget(self.but_close)
        self.hboxB.addWidget(self.but_apply)
        self.hboxB.addWidget(self.but_show )

        self.vbox  = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.tit_title)
        self.vbox.addLayout(self.hboxM)
        self.vbox.addLayout(self.hboxB)
        self.setLayout(self.vbox)
        
        self.but_close.clicked.connect(self.onClose)
        self.but_apply.clicked.connect(self.onSave)
        self.but_show.clicked.connect(self.onShow)

        self.showToolTips()
        self.setStyle()

    #-------------------
    #  Public methods --
    #-------------------

    def showToolTips(self):
        #self           .setToolTip('This GUI deals with the configuration parameters.')
        self.but_close .setToolTip('Close this window.')
        self.but_apply .setToolTip('Apply changes to configuration parameters.')
        self.but_show  .setToolTip('Show ...')

    def setFrame(self):
        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken ) #Box, Panel | Sunken, Raised 
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        #self.frame.setVisible(False)

    def setStyle(self):
        self.setMinimumHeight(630)

        self.           setStyleSheet (cp.styleBkgd)
        self.tit_title .setStyleSheet (cp.styleTitleBold)
        self.tit_status.setStyleSheet (cp.styleTitle)
        self.but_close .setStyleSheet (cp.styleButton)
        self.but_apply .setStyleSheet (cp.styleButton) 
        self.but_show  .setStyleSheet (cp.styleButton) 

        self.tit_title .setAlignment(QtCore.Qt.AlignCenter)
        #self.titTitle .setBold()

    def setParent(self,parent) :
        self.parent = parent

    def resizeEvent(self, e):
        #logger.debug('resizeEvent', __name__) 
        self.frame.setGeometry(self.rect())

    def moveEvent(self, e):
        #logger.debug('moveEvent', __name__) 
        #cp.posGUIMain = (self.pos().x(),self.pos().y())
        pass

    def closeEvent(self, event):
        logger.debug('closeEvent', __name__)

        try    : cp.guisetupinfoleft.close()
        except : pass

        try    : cp.guisetupinforight.close()
        except : pass

        try    : del cp.guisetupinfo # GUISetupInfo
        except : pass

    def onClose(self):
        logger.debug('onClose', __name__)
        self.close()

    def onSave(self):
        fname = cp.fname_cp.value()
        logger.debug('onSave:', __name__)# - save all configuration parameters in file: ' + fname, __name__)
        cp.saveParametersInFile( fname )


    def onShow(self):
        logger.debug('onShow - is not implemented yet...', __name__)

#-----------------------------

if __name__ == "__main__" :

    app = QtWidgets.QApplication(sys.argv)
    widget = GUISetupInfo ()
    widget.show()
    app.exec_()

#-----------------------------
