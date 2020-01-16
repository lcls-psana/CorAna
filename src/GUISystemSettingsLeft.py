#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUISystemSettingsLeft...
#
#------------------------------------------------------------------------

"""GUI sets system parameters"""

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
from ConfigParametersCorAna   import confpars as cp
from CorAna.Logger                   import logger
from GUICCDSettings           import *

#---------------------
#  Class definition --
#---------------------
class GUISystemSettingsLeft ( QtWidgets.QWidget ) :
    """GUI sets system parameters"""

    def __init__ ( self, parent=None ) :
        QtWidgets.QWidget.__init__(self, parent)
        self.setGeometry(200, 400, 350, 300)
        self.setWindowTitle('System Settings Left')
        self.setFrame()

        cp.guiccdsettings = GUICCDSettings()

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addStretch(1) 
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(cp.guiccdsettings)
        self.vbox.addStretch(1) 
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)

        self.showToolTips()
        self.setStyle()

    #-------------------
    #  Public methods --
    #-------------------

    def showToolTips(self):
        msg = 'GUI sets system parameters.'
        #self.tit_sys_ram_size.setToolTip(msg)

    def setFrame(self):
        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken ) #Box, Panel | Sunken, Raised 
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        #self.frame.setVisible(False)

    def setStyle(self):
        self.setMinimumWidth(350)
        self.setStyleSheet(cp.styleBkgd)


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
        try    : del cp.guisystemsettingsleft # GUISystemSettingsLeft
        except : pass

        try    : cp.guiccdsettings.close()
        except : pass


    def onClose(self):
        logger.debug('onClose', __name__)
        self.close()

    def onShow(self):
        logger.debug('onShow - is not implemented yet...', __name__)

    def onApply(self):
        logger.info('onApply - is already applied...', __name__)

#-----------------------------

if __name__ == "__main__" :

    app = QtWidgets.QApplication(sys.argv)
    widget = GUISystemSettingsLeft ()
    widget.show()
    app.exec_()

#-----------------------------
