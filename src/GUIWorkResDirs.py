#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIWorkResDirs...
#
#------------------------------------------------------------------------

"""GUI for Work/Result directories"""
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
from . import GlobalUtils          as     gu

#---------------------
#  Class definition --
#---------------------
class GUIWorkResDirs ( QtWidgets.QWidget ) :
    """GUI for Work/Result directories"""

    #----------------
    #  Constructor --
    #----------------
    def __init__ ( self, parent=None ) :
        QtWidgets.QWidget.__init__(self, parent)
        self.setGeometry(200, 400, 530, 150)
        self.setWindowTitle('Files')
        self.setFrame()

        self.tit_dir_work = QtWidgets.QLabel('Work / Results output:')

        self.edi_dir_work = QtWidgets.QLineEdit( cp.dir_work.value() )        
        self.but_dir_work = QtWidgets.QPushButton('Dir work:')
        self.edi_dir_work.setReadOnly( True )  

        self.edi_dir_results = QtWidgets.QLineEdit( cp.dir_results.value() )        
        self.but_dir_results = QtWidgets.QPushButton('Dir results:')
        self.edi_dir_results.setReadOnly( True )  

        self.lab_fname_prefix = QtWidgets.QLabel('File prefix:')
        self.edi_fname_prefix = QtWidgets.QLineEdit( cp.fname_prefix.value() )        

        self.grid = QtWidgets.QGridLayout()
        self.grid_row = 0
        self.grid.addWidget(self.tit_dir_work,      self.grid_row,   0, 1, 9)
        self.grid.addWidget(self.but_dir_work,      self.grid_row+1, 0)
        self.grid.addWidget(self.edi_dir_work,      self.grid_row+1, 1, 1, 8)
        self.grid.addWidget(self.but_dir_results,   self.grid_row+2, 0)
        self.grid.addWidget(self.edi_dir_results,   self.grid_row+2, 1, 1, 8)
        self.grid.addWidget(self.lab_fname_prefix,  self.grid_row+3, 0)
        self.grid.addWidget(self.edi_fname_prefix,  self.grid_row+3, 1, 1, 4)
        self.setLayout(self.grid)

        self.but_dir_work.clicked.connect(self.onButDirWork)
        self.but_dir_results.clicked.connect(self.onButDirResults)
        self.edi_fname_prefix.editingFinished .connect(self.onEditPrefix)

        self.showToolTips()
        self.setStyle()

    #-------------------
    #  Public methods --
    #-------------------

    def showToolTips(self):
        self.edi_dir_work    .setToolTip('Click on "Dir work:" button\nto change the directory')
        self.but_dir_work    .setToolTip('Click on this button\nand select the directory')
        self.edi_dir_results .setToolTip('Click on "Dir results:" button\nto change the directory')
        self.but_dir_results .setToolTip('Click on this button\nand select the directory')
        self.edi_fname_prefix.setToolTip('Edit the common file prefix in this field')
        
    def setFrame(self):
        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken ) #Box, Panel | Sunken, Raised 
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        #self.frame.setVisible(False)


    def setStyle(self):
        self.                 setStyleSheet (cp.styleBkgd)
        self.setMinimumWidth(530)

        self.tit_dir_work    .setStyleSheet (cp.styleTitle)
        self.edi_dir_work    .setStyleSheet (cp.styleEditInfo)       
        self.but_dir_work    .setStyleSheet (cp.styleButton) 
        self.edi_dir_results .setStyleSheet (cp.styleEditInfo)       
        self.but_dir_results .setStyleSheet (cp.styleButton) 
        self.lab_fname_prefix.setStyleSheet (cp.styleLabel)
        self.edi_fname_prefix.setStyleSheet (cp.styleEdit)

        self.tit_dir_work    .setAlignment (QtCore.Qt.AlignLeft)
        self.edi_dir_work    .setAlignment (QtCore.Qt.AlignRight)
        self.edi_dir_results .setAlignment (QtCore.Qt.AlignRight)
        self.lab_fname_prefix.setAlignment (QtCore.Qt.AlignRight)

        self.edi_dir_work    .setMinimumWidth(300)
        self.but_dir_work    .setFixedWidth(80)
        self.edi_dir_results .setMinimumWidth(300)
        self.but_dir_results .setFixedWidth(80)


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
        #try    : del cp.guiworkresdirs # GUIWorkResDirs
        #except : pass # silently ignore


    def onClose(self):
        logger.debug('onClose', __name__)
        self.close()


    def onButDirWork(self):
        self.selectDirectory(cp.dir_work, self.edi_dir_work, 'work')


    def onButDirResults(self):
        self.selectDirectory(cp.dir_results, self.edi_dir_results, 'results')


    def selectDirectory(self, par, edi, label=''):        
        logger.debug('Select directory for ' + label, __name__)
        dir0 = par.value()
        path, name = os.path.split(dir0)
        dir = str( QtWidgets.QFileDialog.getExistingDirectory(None,'Select directory for '+label,path) )

        if dir == dir0 or dir == '' :
            logger.info('Directiry for ' + label + ' has not been changed.', __name__)
            return
        edi.setText(dir)        
        par.setValue(dir)
        logger.info('Set directory for ' + label + str(par.value()), __name__)

        gu.create_directory(dir)


    def onEditPrefix(self):
        logger.debug('onEditPrefix', __name__)
        cp.fname_prefix.setValue( str(self.edi_fname_prefix.displayText()) )
        logger.info('Set file name common prefix: ' + str( cp.fname_prefix.value()), __name__ )

#-----------------------------

if __name__ == "__main__" :

    app = QtWidgets.QApplication(sys.argv)
    widget = GUIWorkResDirs ()
    widget.show()
    app.exec_()

#-----------------------------
