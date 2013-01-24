#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUILoadResults...
#
#------------------------------------------------------------------------

"""GUI Load Results"""

#------------------------------
#  Module's version from CVS --
#------------------------------
__version__ = "$Revision: 4 $"
# $Source$

#--------------------------------
#  Imports of standard modules --
#--------------------------------
import sys
import os

from PyQt4 import QtGui, QtCore
#import time   # for sleep(sec)

#-----------------------------
# Imports for other modules --
#-----------------------------

from ConfigParametersCorAna import confpars as cp
from Logger                 import logger
from ViewResults            import *

#---------------------
#  Class definition --
#---------------------
class GUILoadResults ( QtGui.QWidget ) :
    """GUI Load Results"""

    def __init__ ( self, parent=None, fname=None ) :
        #super(GUILoadResults, self).__init__()
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(200, 400, 500, 400)
        self.setWindowTitle('Load Results')
        self.setFrame()

        self.setFileName(fname)

        self.vr  = ViewResults(cp.res_fname.value())
        self.list_of_tau = self.vr.get_list_of_tau_from_file(fnm.path_cora_merge_tau())
        #print 'self.list_of_tau =', self.list_of_tau
        self.g_ind   = 0
        self.tau_ind = 0
        self.arr = None
        
        self.tit    = QtGui.QLabel('Load Results')
        self.edi    = QtGui.QLineEdit( os.path.basename(cp.res_fname.value()) )        
        self.but    = QtGui.QPushButton('File')
        self.but_gi = QtGui.QPushButton('<g_i>')
        self.but_gk = QtGui.QPushButton('<g_k>')
        self.but_g2 = QtGui.QPushButton('<g_2>')
        self.but_G2 = QtGui.QPushButton('100 x G2')

        self.sli = QtGui.QSlider(QtCore.Qt.Horizontal, self)        
        self.sli.setValue(0)
        self.sli.setRange(0, self.list_of_tau.shape[0]-1)
        self.sli.setTickInterval(1)
        self.edi_tau = QtGui.QLineEdit('tau(ind)')


        self.grid = QtGui.QGridLayout()
        self.grid_row = 1
        self.grid.addWidget(self.tit,      self.grid_row,   0, 1, 9)
        self.grid.addWidget(self.but,      self.grid_row+1, 0)
        self.grid.addWidget(self.edi,      self.grid_row+1, 1, 1, 9)
        self.grid.addWidget(self.edi_tau,  self.grid_row+2, 0)
        self.grid.addWidget(self.sli,      self.grid_row+2, 1, 1, 9)
        self.grid.addWidget(self.but_gi,   self.grid_row+3, 0)
        self.grid.addWidget(self.but_gk,   self.grid_row+3, 1)
        self.grid.addWidget(self.but_g2,   self.grid_row+3, 2)
        self.grid.addWidget(self.but_G2,   self.grid_row+3, 3)

        self.grid_row += 3

        #self.connect(self.edi, QtCore.SIGNAL('editingFinished()'),        self.onEdit )
        self.connect(self.but,    QtCore.SIGNAL('clicked()'),         self.onBut )
        self.connect(self.but_gi, QtCore.SIGNAL('clicked()'),         self.onButView )
        self.connect(self.but_gk, QtCore.SIGNAL('clicked()'),         self.onButView )
        self.connect(self.but_g2, QtCore.SIGNAL('clicked()'),         self.onButView )
        self.connect(self.but_G2, QtCore.SIGNAL('clicked()'),         self.onButView )
        self.connect(self.sli,    QtCore.SIGNAL('valueChanged(int)'), self.onSlider )
        self.connect(self.sli,    QtCore.SIGNAL('sliderReleased()'),  self.onSliderReleased )
 
        self.setLayout(self.grid)

        self.showToolTips()
        self.setStyle()
        self.onSlider()

        #self.overlay = Overlay(self,'Load Results')
                
    #-------------------
    #  Public methods --
    #-------------------

    def setFileName(self, fname=None) :
        if fname == None : pass
        else : cp.res_fname.setValue(fname)


    def showToolTips(self):
        msg = 'Use this GUI to set partitions.'
        self.setToolTip(msg)
        self.edi.setToolTip('Click on "File"\nto select the file')
        self.but.setToolTip('Click on this button\nand select the file')


    def setFrame(self):
        self.frame = QtGui.QFrame(self)
        self.frame.setFrameStyle( QtGui.QFrame.Box | QtGui.QFrame.Sunken ) #Box, Panel | Sunken, Raised 
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        #self.frame.setVisible(False)


    def setStyle(self):
        self.setMinimumWidth(400)
        self.setStyleSheet(cp.styleBkgd)

        width = 80
        self.but.setFixedWidth(width)
        self.tit.setStyleSheet(cp.styleTitle)
        self.edi.setStyleSheet(cp.styleEditInfo) # cp.styleEditInfo
        self.but.setStyleSheet(cp.styleButton) 
        self.edi.setAlignment (QtCore.Qt.AlignLeft)
        self.edi.setReadOnly  (True)  
        self.edi_tau.setFixedWidth(width)
        self.edi_tau.setStyleSheet(cp.styleEditInfo) # cp.styleEditInfo
        self.edi_tau.setReadOnly  (True)
        self.edi_tau.setAlignment (QtCore.Qt.AlignCenter)
        self.but_gi.setStyleSheet(cp.styleButton)
        self.but_gk.setStyleSheet(cp.styleButton)
        self.but_g2.setStyleSheet(cp.styleButton)
        self.but_G2.setStyleSheet(cp.styleButton)



    def resizeEvent(self, e):
        self.frame.setGeometry(self.rect())
        e.accept()


    def moveEvent(self, e):
        #cp.posGUIMain = (self.pos().x(),self.pos().y())
        pass


    def closeEvent(self, event):
        logger.debug('closeEvent', __name__)
        try    : del cp.guiloadresults # GUILoadResults
        except : pass # silently ignore


    def onClose(self):
        logger.debug('onClose', __name__)
        self.close()


    def onEdit(self):
        logger.debug('onEdit', __name__)
        edi = self.edi
        par = cp.res_fname
        par.setValue( str(edi.displayText()) )
        logger.info('Set parameter = ' + str( par.value()), __name__ )

        
    def onBut(self):
        logger.debug('onBut - xelect file', __name__)
        but = self.but
        edi = self.edi
        par = cp.res_fname
        #dir = cp.dir_results.value() # is not used

        path0 = par.value()
        path  = str( QtGui.QFileDialog.getOpenFileName(self,'Select file',path0) )
        dname, fname = os.path.split(path)

        if dname == '' or fname == '' :
            logger.warning('Input directiry name or file name is empty... keep file name unchanged...', __name__)
            return

        edi.setText (os.path.basename(path))
        par.setValue(path)
        logger.info('selected the file name: ' + str(par.value()), __name__ )


    def onButView(self):
        logger.info('onButView', __name__)
        self.arr = self.vr.get_cor_array_from_binary_file()

        if self.but_gi.hasFocus() :
            logger.info('<g_i> is selected', __name__)
            self.g_ind = 0

        if self.but_gk.hasFocus() :
            logger.info('<g_k> is selected', __name__)
            self.g_ind = 1

        if self.but_g2.hasFocus() :
            logger.info('<g_2> is selected', __name__)
            self.g_ind = 2

        if self.but_G2.hasFocus() :
            logger.info('G2 is selected', __name__)
            self.g_ind = -1

        self.drawPlot()
  


    def drawPlot(self):
        if self.arr == None : return

        self.setImgArray()
        try :
            cp.plotimgspe.close()
        except :
            cp.plotimgspe = PlotImgSpe(None,self.arr2d) 
            #self.plotimgspe_g.set_image_array(self.arr2d)
            #cp.plotimgspe.move(QtCore.QPoint(50,50))
            cp.plotimgspe.move(self.parentWidget().parentWidget().pos().__add__(QtCore.QPoint(850,20)))
            cp.plotimgspe.show()


    def redrawPlot(self):
        if self.arr == None : return

        self.setImgArray()
        try :
            cp.plotimgspe.set_image_array(self.arr2d)
        except :
            pass


    def setImgArray(self):
        if self.g_ind < 0 :
            gi = self.arr[self.tau_ind, 0,...] 
            gk = self.arr[self.tau_ind, 1,...] 
            g2 = self.arr[self.tau_ind, 2,...] 

            self.arr2d = 100*g2/gi/gk
        else :
            self.arr2d = self.arr[self.tau_ind, self.g_ind,...] 
        #print 'arr2d:\n', self.arr2d 


    def onSlider(self):
        self.tau_ind = self.sli.value()
        self.tau_val = self.list_of_tau[self.tau_ind]        
        value_str = u"\u03C4" + str( '(' + str(self.tau_ind) + ')=' + str(self.tau_val) )
        #logger.info('onSlider: value = ' + value_str , __name__)
        self.edi_tau.setText(value_str)


    def onSliderReleased(self):
        #print 'onSliderReleased'
        self.tau_ind = self.sli.value()
        self.tau_val = self.list_of_tau[self.tau_ind]
        value_str = str( 'tau(' + str(self.tau_ind) + ')=' + str(self.tau_val) )
        logger.info('onSliderReleased: ' + value_str , __name__)
        self.redrawPlot()
        

#-----------------------------

if __name__ == "__main__" :

    app = QtGui.QApplication(sys.argv)
    widget = GUILoadResults ()
    widget.show()
    app.exec_()

#-----------------------------
