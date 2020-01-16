#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUISystemSettingsRight...
#
#------------------------------------------------------------------------

"""GUI sets system parameters (right pannel)"""

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
from CorAna.Logger import logger
from ConfigParametersCorAna import confpars as cp

#---------------------
#  Class definition --
#---------------------
class GUISystemSettingsRight ( QtWidgets.QWidget ) :
    """GUI sets system parameters (right panel)"""

    #----------------
    #  Constructor --
    #----------------
    def __init__ ( self, parent=None ) :
        QtWidgets.QWidget.__init__(self, parent)
        self.setGeometry(200, 400, 400, 150)
        self.setWindowTitle('System Settings Right')
        self.setFrame()

        self.tit_thickness         = QtWidgets.QLabel('Thickness normalization options (transmission mode):')
        self.edi_thickness_sample  = QtWidgets.QLineEdit( str( cp.thickness_sample.value() ) )        
        self.edi_thickness_attlen  = QtWidgets.QLineEdit( str( cp.thickness_attlen.value() ) )        
        self.rad_thickness_nonorm  = QtWidgets.QRadioButton('no thickness normalization')
        self.rad_thickness_sample  = QtWidgets.QRadioButton('sample thickness [mm]')
        self.rad_thickness_attlen  = QtWidgets.QRadioButton('sample attenuation length [mm]')
        self.rad_thickness_grp     = QtWidgets.QButtonGroup()
        self.rad_thickness_grp.addButton(self.rad_thickness_nonorm)
        self.rad_thickness_grp.addButton(self.rad_thickness_sample)
        self.rad_thickness_grp.addButton(self.rad_thickness_attlen)
        self.list_thickness_types = ['NONORM', 'SAMPLE', 'ATTLEN']
        if   cp.thickness_type.value() == self.list_thickness_types[1] : self.rad_thickness_sample.setChecked(True)
        elif cp.thickness_type.value() == self.list_thickness_types[2] : self.rad_thickness_attlen.setChecked(True)
        else                                                           : self.rad_thickness_nonorm.setChecked(True)

        self.char_expand         = u' \u25BE' # down-head triangle
        self.tit_detector   = QtWidgets.QLabel('Detector:')
        self.tit_bat_queue  = QtWidgets.QLabel('Queue:')

        self.list_of_dets   = cp.list_of_dets 
        self.box_detector   = QtWidgets.QComboBox( self ) 
        self.box_detector .addItems(self.list_of_dets)
        self.box_detector .setCurrentIndex( self.list_of_dets.index(cp.detector.value()) )

        self.list_of_queues = ['psnehq','psfehq','psanacsq'] 
        self.box_bat_queue  = QtWidgets.QComboBox( self ) 
        self.box_bat_queue.addItems(self.list_of_queues)
        self.box_bat_queue.setCurrentIndex( self.list_of_queues.index(cp.bat_queue.value()) )

        self.grid = QtWidgets.QGridLayout()

        self.grid_row = 0
        self.grid.addWidget(self.tit_thickness,        self.grid_row+1, 0, 1, 8)
        self.grid.addWidget(self.rad_thickness_nonorm, self.grid_row+2, 1, 1, 3)
        self.grid.addWidget(self.rad_thickness_sample, self.grid_row+3, 1, 1, 3)
        self.grid.addWidget(self.rad_thickness_attlen, self.grid_row+4, 1, 1, 3)
        self.grid.addWidget(self.edi_thickness_sample, self.grid_row+3, 4)
        self.grid.addWidget(self.edi_thickness_attlen, self.grid_row+4, 4)
        self.grid.addWidget(self.tit_detector,         self.grid_row+6, 0, 1, 2)
        self.grid.addWidget(self.box_detector,         self.grid_row+6, 2, 1, 2)
        self.grid.addWidget(self.tit_bat_queue,        self.grid_row+7, 0, 1, 2)
        self.grid.addWidget(self.box_bat_queue,        self.grid_row+7, 2, 1, 2)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.grid)
        self.vbox.addStretch(1)

        self.setLayout(self.vbox)

        self.rad_thickness_nonorm.clicked.connect(self.onRadioThickness)
        self.rad_thickness_sample.clicked.connect(self.onRadioThickness)
        self.rad_thickness_attlen.clicked.connect(self.onRadioThickness)

        self.edi_thickness_sample.editingFinished.connect(self.onEdit)
        self.edi_thickness_attlen.editingFinished.connect(self.onEdit)
        self.box_bat_queue.currentIndexChanged[int].connect(self.on_box_bat_queue)
        self.box_detector.currentIndexChanged[int].connect(self.on_box_detector)

        self.showToolTips()
        self.setStyle()

    #-------------------
    #  Public methods --
    #-------------------

    def showToolTips(self):
        self.setToolTip('Right pannel of the System Settings GUI')
        self.box_bat_queue.setToolTip('Select the batch queue')
        self.box_bat_queue.setToolTip('Select the detector type')


    def setFrame(self):
        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken ) #Box, Panel | Sunken, Raised 
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        #self.frame.setVisible(False)

    def setStyle(self):

        width = 60
        self.                     setMinimumWidth(400)
        self.                     setStyleSheet (cp.styleBkgd)

        self.edi_thickness_sample.setStyleSheet(cp.styleEdit) 
        self.edi_thickness_attlen.setStyleSheet(cp.styleEdit) 

        self.edi_thickness_sample.setFixedWidth(width)
        self.edi_thickness_attlen.setFixedWidth(width)

        self.edi_thickness_sample.setAlignment (QtCore.Qt.AlignRight) 
        self.edi_thickness_attlen.setAlignment (QtCore.Qt.AlignRight) 

        self.tit_thickness       .setStyleSheet(cp.styleTitle)
        self.rad_thickness_nonorm.setStyleSheet(cp.styleLabel)
        self.rad_thickness_sample.setStyleSheet(cp.styleLabel)
        self.rad_thickness_attlen.setStyleSheet(cp.styleLabel)

        self.tit_detector        .setStyleSheet(cp.styleTitle)
        self.tit_bat_queue       .setStyleSheet(cp.styleTitle)
        self.tit_detector        .setAlignment (QtCore.Qt.AlignLeft)
        self.tit_bat_queue       .setAlignment (QtCore.Qt.AlignLeft)
        self.box_bat_queue       .setStyleSheet(cp.styleButton)
        self.box_detector        .setStyleSheet(cp.styleButton)


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
        try    : del cp.guisystemsettingsright # GUISystemSettingsRight
        except : pass

    def onClose(self):
        logger.debug('onClose', __name__)
        self.close()

    def on(self):
        logger.debug('on click - is not implemented yet', __name__)

    def onEdit(self):

        if self.edi_thickness_sample.isModified() :            
            self.edi = self.edi_thickness_sample 
            self.par = cp.thickness_sample
            self.tit = 'thickness_sample'

        elif self.edi_thickness_attlen.isModified() :            
            self.edi = self.edi_thickness_attlen
            self.par = cp.thickness_attlen
            self.tit = 'thickness_attlen'

        else : return # no-modification

        self.edi.setModified(False)
        self.par.setValue( self.edi.displayText() )        
        msg = 'onEdit - set value of ' + self.tit  + ': ' + str( self.par.value())
        logger.info(msg, __name__ )


    def onRadioThickness(self): 
        if self.rad_thickness_nonorm.isChecked() : cp.thickness_type.setValue( self.list_thickness_types[0] )
        if self.rad_thickness_sample.isChecked() : cp.thickness_type.setValue( self.list_thickness_types[1] )
        if self.rad_thickness_attlen.isChecked() : cp.thickness_type.setValue( self.list_thickness_types[2] )
        logger.info('onRadioThickness - selected thickness type: ' + cp.thickness_type.value(), __name__ )


    def on_box_bat_queue(self):
        queue_selected = self.box_bat_queue.currentText()
        cp.bat_queue.setValue( queue_selected ) 
        logger.info('on_box_bat_queue - queue_selected: ' + queue_selected, __name__)

    def on_box_detector(self):
        selected = self.box_detector.currentText()
        cp.detector.setValue( selected ) 
        logger.info('on_box_detector - selected: ' + selected, __name__)

#-----------------------------

if __name__ == "__main__" :

    app = QtWidgets.QApplication(sys.argv)
    widget = GUISystemSettingsRight ()
    widget.show()
    app.exec_()

#-----------------------------
