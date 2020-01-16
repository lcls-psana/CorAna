#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUISetupData...
#
#------------------------------------------------------------------------

"""GUI sets the beam and spec coordinates w.r.t. camera frame for specular mode"""
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

#---------------------
#  Class definition --
#---------------------
class GUISetupData ( QtWidgets.QWidget ) :
    """GUI sets the beam and spec coordinates w.r.t. camera frame for specular mode"""

    #----------------
    #  Constructor --
    #----------------
    def __init__ ( self, parent=None ) :
        """Constructor"""

        QtWidgets.QWidget.__init__(self, parent)
        self.setGeometry(200, 400, 500, 30)
        self.setWindowTitle('Specularly Reflected Beam Parameters')
        self.setFrame()

        self.titCameraPos  = QtWidgets.QLabel('CCD Position In Data Collection (mm):')
        self.tit_frame_x   = QtWidgets.QLabel('x:')
        self.tit_frame_y   = QtWidgets.QLabel('y:')
 
        self.edi_x0_pos_in_data  = QtWidgets.QLineEdit( str( cp.x0_pos_in_data .value() ) )        
        self.edi_y0_pos_in_data  = QtWidgets.QLineEdit( str( cp.y0_pos_in_data .value() ) )        

        self.grid = QtWidgets.QGridLayout()

        self.grid.addWidget(self.titCameraPos,       0, 0, 1,8)
        self.grid.addWidget(self.tit_frame_x ,       1, 2)
        self.grid.addWidget(self.tit_frame_y ,       1, 4)
        self.grid.addWidget(self.edi_x0_pos_in_data,    1, 3)
        self.grid.addWidget(self.edi_y0_pos_in_data,    1, 5)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.grid)
        self.vbox.addStretch(1) 
        self.setLayout(self.vbox)

        self.edi_x0_pos_in_data.editingFinished .connect(self.on_edi_x0_pos_in_data)
        self.edi_y0_pos_in_data.editingFinished .connect(self.on_edi_y0_pos_in_data)
 
        self.showToolTips()
        self.setStyle()

    #-------------------
    #  Public methods --
    #-------------------

    def showToolTips(self):
        # Tips for buttons and fields:
        msg = 'Edit field'
        self.edi_x0_pos_in_data.setToolTip( msg )
        self.edi_y0_pos_in_data.setToolTip( msg )

    def setFrame(self):
        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken ) #Box, Panel | Sunken, Raised 
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        self.frame.setVisible(False)

    def setStyle(self):
        self.setFixedHeight(150)

        width = 80
        width_label = 50

        self.              setStyleSheet (cp.styleBkgd)
        self.titCameraPos .setStyleSheet (cp.styleTitle) 
        self.tit_frame_x  .setStyleSheet (cp.styleLabel) 
        self.tit_frame_y  .setStyleSheet (cp.styleLabel) 

        self.tit_frame_x  .setAlignment(QtCore.Qt.AlignRight)
        self.tit_frame_y  .setAlignment(QtCore.Qt.AlignRight)

        self.tit_frame_x  .setFixedWidth(width_label)
        self.tit_frame_y  .setFixedWidth(width_label)

        self.edi_x0_pos_in_data.setAlignment(QtCore.Qt.AlignRight)
        self.edi_y0_pos_in_data.setAlignment(QtCore.Qt.AlignRight)

        self.edi_x0_pos_in_data.setFixedWidth(width)
        self.edi_y0_pos_in_data.setFixedWidth(width)

        self.edi_x0_pos_in_data.setStyleSheet(cp.styleEdit) 
        self.edi_y0_pos_in_data.setStyleSheet(cp.styleEdit) 


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
        try    : del cp.guisetupdata # GUISetupData
        except : pass # silently ignore

    def onClose(self):
        logger.debug('onClose', __name__) 
        self.close()

    def on_edi_x0_pos_in_data(self):
        cp.x0_pos_in_data.setValue( float(self.edi_x0_pos_in_data.displayText()) )
        logger.info('Set x0_pos_in_data =' + str(cp.x0_pos_in_data.value()), __name__)

    def on_edi_y0_pos_in_data(self):
        cp.y0_pos_in_data.setValue( float(self.edi_y0_pos_in_data.displayText()) )
        logger.info('Set y0_pos_in_data =' + str(cp.y0_pos_in_data.value()), __name__)

#-----------------------------

if __name__ == "__main__" :

    app = QtWidgets.QApplication(sys.argv)
    widget = GUISetupData ()
    widget.show()
    app.exec_()

#-----------------------------
