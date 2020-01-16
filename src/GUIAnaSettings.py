#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIAnaSettings...
#
#------------------------------------------------------------------------

"""GUI sets parameters for analysis"""
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
from CorAna.Logger                 import logger
from .GUIAnaSettingsLeft     import *
from .GUIAnaSettingsRight    import *
from .GUIListOfTau           import *

#---------------------
#  Class definition --
#---------------------
class GUIAnaSettings ( QtWidgets.QWidget ) :
    """GUI Analysis Settings"""

    #----------------
    #  Constructor --
    #----------------
    def __init__ ( self, parent=None ) :

        QtWidgets.QWidget.__init__(self, parent)

        self.setGeometry(20, 40, 800, 630)
        self.setWindowTitle('Analysis Settings')
        self.setFrame()
 
        self.tit_title  = QtWidgets.QLabel('Analysis Settings')
        self.tit_status = QtWidgets.QLabel('Status:')
        self.but_close  = QtWidgets.QPushButton('Close') 
        self.but_apply  = QtWidgets.QPushButton('Save') 
        self.but_show   = QtWidgets.QPushButton('Show Mask && Partitions') 
        cp.guianasettingsleft  = GUIAnaSettingsLeft()
        cp.guianasettingsright = GUIAnaSettingsRight()
        cp.guilistoftau        = GUIListOfTau()

        self.vboxR = QtWidgets.QVBoxLayout()
        self.vboxR.addWidget(cp.guianasettingsright)
        self.vboxR.addWidget(cp.guilistoftau)

        self.hboxM = QtWidgets.QHBoxLayout()
        self.hboxM.addWidget(cp.guianasettingsleft)
        #self.hboxM.addWidget(cp.guianasettingsright)
        self.hboxM.addLayout(self.vboxR)

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
        # Tips for buttons and fields:
        #self           .setToolTip('This GUI deals with the configuration parameters.')
        #msg_edi = 'WARNING: whatever you edit may be incorrect...\nIt is recommended to use the '
        #self.butInstr  .setToolTip('Select the instrument name from the pop-up menu.')
        pass

    def setFrame(self):
        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken ) #Box, Panel | Sunken, Raised 
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        #self.frame.setVisible(False)

    def setStyle(self):
        self.setMinimumHeight(630)
        self.setMinimumWidth(800)

        self.           setStyleSheet (cp.styleBkgd)
        self.tit_title .setStyleSheet (cp.styleTitleBold)
        self.tit_status.setStyleSheet (cp.styleTitle)
        self.but_close .setStyleSheet (cp.styleButton)
        self.but_apply .setStyleSheet (cp.styleButton) 
        self.but_show  .setStyleSheet (cp.styleButton) 

        self.tit_title .setAlignment(QtCore.Qt.AlignCenter)
        #self.tit_title .setBold()

    def setParent(self,parent) :
        self.parent = parent

    def resizeEvent(self, e):
        #logger.debug('resizeEvent', __name__ ) 
        self.frame.setGeometry(self.rect())

    def moveEvent(self, e):
        #logger.debug('moveEvent', __name__ ) 
        #cp.posGUIMain = (self.pos().x(),self.pos().y())
        pass

    def closeEvent(self, event):
        logger.debug('closeEvent', __name__ )
        try    : cp.guianasettingsleft.close()
        except : pass

        try    : cp.guianasettingsright.close()
        except : pass

        try    : del cp.guianasettings # GUIAnaSettings
        except : pass

    def onClose(self):
        logger.debug('onClose', __name__ )
        self.close()

    def onShow(self):
        logger.debug('onShow - is not implemented yet', __name__ )

    def onApply(self):
        logger.debug('onApply - is already applied...', __name__ )

    def onSave(self):
        fname = cp.fname_cp.value()
        logger.debug('onSave:', __name__)
        cp.saveParametersInFile( fname )



#-----------------------------

if __name__ == "__main__" :

    app = QtWidgets.QApplication(sys.argv)
    widget = GUIAnaSettings ()
    widget.show()
    app.exec_()

#-----------------------------
