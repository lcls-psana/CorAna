#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUISetupBeamZero...
#
#------------------------------------------------------------------------

"""GUI sets the beam coordinates w.r.t. camera frame for transmission/beam-zero mode"""
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
from CorAna.Logger             import logger

#---------------------
#  Class definition --
#---------------------
class GUISetupBeamZero ( QtWidgets.QWidget ) :
    """GUI sets the beam coordinates w.r.t. camera frame for transmission/beam-zero mode"""

    #----------------
    #  Constructor --
    #----------------
    def __init__ ( self, parent=None ) :
        """Constructor"""

        QtWidgets.QWidget.__init__(self, parent)
        self.setGeometry(200, 400, 500, 30)
        self.setWindowTitle('Transmission parameters')
        self.setFrame()
 
        self.tit_beam_zero = QtWidgets.QLabel('Transm. beam coords in full frame mode (pix):')
        self.tit_x_coord   = QtWidgets.QLabel('x:')
        self.tit_y_coord   = QtWidgets.QLabel('y:')

        self.tit_ccd_pos   = QtWidgets.QLabel('CCD Position In Beam Zero Meas. (mm):')
        self.tit_x0_pos    = QtWidgets.QLabel('x:')
        self.tit_y0_pos    = QtWidgets.QLabel('y:')


        self.edi_x_coord   = QtWidgets.QLineEdit( str( cp.x_coord_beam0.value() ) )        
        self.edi_y_coord   = QtWidgets.QLineEdit( str( cp.y_coord_beam0.value() ) )        
        self.edi_x0_pos    = QtWidgets.QLineEdit( str( cp.x0_pos_in_beam0.value() ) )        
        self.edi_y0_pos    = QtWidgets.QLineEdit( str( cp.y0_pos_in_beam0.value() ) )        


        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.tit_beam_zero,     2, 0, 1, 8)
        self.grid.addWidget(self.tit_x_coord,       3, 2)
        self.grid.addWidget(self.tit_y_coord,       3, 4)
        self.grid.addWidget(self.edi_x_coord,       3, 3)
        self.grid.addWidget(self.edi_y_coord,       3, 5)

        self.grid.addWidget(self.tit_ccd_pos,       0, 0, 1, 8)
        self.grid.addWidget(self.tit_x0_pos ,       1, 2)
        self.grid.addWidget(self.tit_y0_pos ,       1, 4)
        self.grid.addWidget(self.edi_x0_pos ,       1, 3)
        self.grid.addWidget(self.edi_y0_pos ,       1, 5)
  
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.grid)
        self.vbox.addStretch(1) 

        self.setLayout(self.vbox)

        self.edi_x_coord.editingFinished .connect(self.on_edi_x_coord)
        self.edi_y_coord.editingFinished .connect(self.on_edi_y_coord)
        self.edi_x0_pos.editingFinished .connect(self.on_edi_x0_pos)
        self.edi_y0_pos.editingFinished .connect(self.on_edi_y0_pos)
 
 
        self.showToolTips()
        self.setStyle()

    #-------------------
    #  Public methods --
    #-------------------

    def showToolTips(self):
        # Tips for buttons and fields:
        msg = 'Edit coordinate'
        self.tit_beam_zero.setToolTip('This section allows to monitor/modify\nthe beam zero parameters\nin transmission mode')
        self.edi_x_coord.setToolTip( msg )
        self.edi_y_coord.setToolTip( msg )

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

        self.              setStyleSheet(cp.styleBkgd)
        self.tit_beam_zero.setStyleSheet(cp.styleTitle)
        self.tit_ccd_pos  .setStyleSheet(cp.styleTitle)
        self.tit_x_coord  .setStyleSheet(cp.styleLabel)
        self.tit_y_coord  .setStyleSheet(cp.styleLabel)
        self.tit_x0_pos   .setStyleSheet(cp.styleLabel) 
        self.tit_y0_pos   .setStyleSheet(cp.styleLabel) 

        self.tit_x_coord  .setAlignment (QtCore.Qt.AlignRight)
        self.tit_y_coord  .setAlignment (QtCore.Qt.AlignRight)
        self.tit_x0_pos   .setAlignment (QtCore.Qt.AlignRight)
        self.tit_y0_pos   .setAlignment (QtCore.Qt.AlignRight)

        self.edi_x_coord  .setAlignment (QtCore.Qt.AlignRight)
        self.edi_y_coord  .setAlignment (QtCore.Qt.AlignRight)
        self.edi_x0_pos   .setAlignment (QtCore.Qt.AlignRight)
        self.edi_y0_pos   .setAlignment (QtCore.Qt.AlignRight)

        self.tit_x_coord  .setFixedWidth(width_label)
        self.tit_y_coord  .setFixedWidth(width_label)
        self.tit_x0_pos   .setFixedWidth(width_label)
        self.tit_y0_pos   .setFixedWidth(width_label)        

        self.edi_x_coord  .setFixedWidth(width)
        self.edi_y_coord  .setFixedWidth(width)
        self.edi_x0_pos   .setFixedWidth(width)
        self.edi_y0_pos   .setFixedWidth(width)

        self.edi_x_coord  .setStyleSheet(cp.styleEdit) 
        self.edi_y_coord  .setStyleSheet(cp.styleEdit) 
        self.edi_x0_pos   .setStyleSheet(cp.styleEdit) 
        self.edi_y0_pos   .setStyleSheet(cp.styleEdit) 



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

        try    : del cp.guisetupbeamzero # GUISetupBeamZero
        except : pass

    def onClose(self):
        logger.debug('onClose', __name__) 
        self.close()

    def on_edi_x_coord(self):
        cp.x_coord_beam0.setValue( float(self.edi_x_coord.displayText()) )
        logger.info('Set x_coord_beam0 =' + str(cp.x_coord_beam0.value()), __name__)

    def on_edi_y_coord(self):
        cp.y_coord_beam0.setValue( float(self.edi_y_coord.displayText()) )
        logger.info('Set y_coord_beam0 =' + str(cp.y_coord_beam0.value()), __name__)

    def on_edi_x0_pos(self):
        cp.x0_pos_in_beam0.setValue( float(self.edi_x0_pos.displayText()) )
        logger.info('Set x0_pos_in_beam0 =' + str(cp.x0_pos_in_beam0.value()), __name__)

    def on_edi_y0_pos(self):
        cp.y0_pos_in_beam0.setValue( float(self.edi_y0_pos.displayText()) )
        logger.info('Set y0_pos_in_beam0 =' + str(cp.y0_pos_in_beam0.value()), __name__)


#-----------------------------

if __name__ == "__main__" :

    app = QtWidgets.QApplication(sys.argv)
    widget = GUISetupBeamZero ()
    widget.show()
    app.exec_()

#-----------------------------
