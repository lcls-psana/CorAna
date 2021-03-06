#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIFiles...
#
#------------------------------------------------------------------------

"""GUI sets path to files"""
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
from .GUIConfigParameters    import *
from .GUIDark                import *
from .GUIData                import *
from .GUIFlatField           import *
from .GUIBlemish             import *
from .GUIWorkResDirs         import *
from CorAna.Logger                 import logger
from .BatchJobPedestals      import bjpeds

#---------------------
#  Class definition --
#---------------------
class GUIFiles ( QtWidgets.QWidget ) :
    """GUI sets path to files"""

    #----------------
    #  Constructor --
    #----------------
    def __init__ ( self, parent=None ) :
        QtWidgets.QWidget.__init__(self, parent)
        self.setGeometry(1, 1, 600, 200)
        self.setWindowTitle('Files')
        self.setFrame()

        self.lab_title  = QtWidgets.QLabel     ('Files')
        self.lab_status = QtWidgets.QLabel     ('Status: ')
        self.but_close  = QtWidgets.QPushButton('&Close') 
        self.but_save   = QtWidgets.QPushButton('&Save') 
        self.but_show   = QtWidgets.QPushButton('Show &Image') 

        self.hboxW = QtWidgets.QHBoxLayout()
        self.hboxB = QtWidgets.QHBoxLayout()
        self.hboxB.addWidget(self.lab_status)
        self.hboxB.addStretch(1)     
        self.hboxB.addWidget(self.but_close)
        self.hboxB.addWidget(self.but_save)
        self.hboxB.addWidget(self.but_show )

        self.list_file_types = ['Dark run', 'Flat field', 'Blemish', 'Data', 'Conf.pars', 'Work/Results']
        self.makeTabBar()
        self.guiSelector()

        self.vbox = QtWidgets.QVBoxLayout()   
        #cp.guiworkresdirs = GUIWorkResDirs()
        #self.vbox.addWidget(cp.guiworkresdirs)
        self.vbox.addWidget(self.lab_title)
        self.vbox.addWidget(self.tab_bar)
        self.vbox.addLayout(self.hboxW)
        self.vbox.addStretch(1)     
        self.vbox.addLayout(self.hboxB)
        self.setLayout(self.vbox)

        self.but_close.clicked.connect(self.onClose)
        self.but_save.clicked.connect(self.onSave)
        self.but_show.clicked.connect(self.onShow)

        self.showToolTips()
        self.setStyle()

    #-------------------
    #  Public methods --
    #-------------------

    def showToolTips(self):
        #msg = 'Edit field'
        self.but_close .setToolTip('Close this window.')
        self.but_save  .setToolTip('Save all current configuration parameters.')
        self.but_show  .setToolTip('Show ...')


    def setFrame(self):
        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken ) #Box, Panel | Sunken, Raised 
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        #self.frame.setVisible(False)

    def setStyle(self):
        self.          setStyleSheet (cp.styleBkgd)
        self.but_close.setStyleSheet (cp.styleButton)
        self.but_save .setStyleSheet (cp.styleButton)
        self.but_show .setStyleSheet (cp.styleButton)

        self.lab_title.setStyleSheet (cp.styleTitleBold)
        self.lab_title .setAlignment(QtCore.Qt.AlignCenter)
        #self.setMinimumWidth (600)
        #self.setMaximumWidth (700)
        #self.setMinimumHeight(300)
        #self.setMaximumHeight(400)
        #self.setFixedWidth (700)
        #self.setFixedHeight(400)
        #self.setFixedHeight(330)
        #self.setFixedSize(550,350)
        #self.setFixedSize(600,360)
        self.setMinimumSize(750,760)
        
    def makeTabBar(self,mode=None) :
        #if mode is not None : self.tab_bar.close()
        self.tab_bar = QtWidgets.QTabBar()

        #Uses self.list_file_types
        self.ind_tab_dark = self.tab_bar.addTab( self.list_file_types[0] )
        self.ind_tab_flat = self.tab_bar.addTab( self.list_file_types[1] )
        self.ind_tab_blem = self.tab_bar.addTab( self.list_file_types[2] )
        self.ind_tab_data = self.tab_bar.addTab( self.list_file_types[3] )
        self.ind_tab_conf = self.tab_bar.addTab( self.list_file_types[4] )
        self.ind_tab_work = self.tab_bar.addTab( self.list_file_types[5] )

        self.tab_bar.setTabTextColor(self.ind_tab_dark, QtGui.QColor('green'))
        self.tab_bar.setTabTextColor(self.ind_tab_flat, QtGui.QColor('red'))
        self.tab_bar.setTabTextColor(self.ind_tab_blem, QtGui.QColor('gray'))
        self.tab_bar.setTabTextColor(self.ind_tab_data, QtGui.QColor('blue'))
        self.tab_bar.setTabTextColor(self.ind_tab_conf, QtGui.QColor('magenta'))
        self.tab_bar.setTabTextColor(self.ind_tab_work, QtGui.QColor('gray'))
        self.tab_bar.setShape(QtWidgets.QTabBar.RoundedNorth)

        #self.tab_bar.setTabEnabled(1, False)
        #self.tab_bar.setTabEnabled(2, False)
        #self.tab_bar.setTabEnabled(3, False)
        #self.tab_bar.setTabEnabled(4, False)
        
        try    :
            tab_index = self.list_file_types.index(cp.current_file_tab.value())
        except :
            tab_index = 3
            cp.current_file_tab.setValue(self.list_file_types[tab_index])
        self.tab_bar.setCurrentIndex(tab_index)

        logger.info(' make_tab_bar - set mode: ' + cp.current_file_tab.value(), __name__)

        self.tab_bar.currentChanged[int].connect(self.onTabBar)


    def guiSelector(self):

        try    : self.gui_win.close()
        except : pass

        try    : del self.gui_win
        except : pass

        if cp.current_file_tab.value() == self.list_file_types[0] :
            self.gui_win = GUIDark(self)
            self.setStatus(0, 'Status: processing for pedestals')
            self.gui_win.setFixedHeight(580)
            
        if cp.current_file_tab.value() == self.list_file_types[1] :
            self.gui_win = GUIFlatField(self)
            self.setStatus(0, 'Status: set file for flat field')
            self.gui_win.setFixedHeight(200)

        if cp.current_file_tab.value() == self.list_file_types[2] :
            self.gui_win = GUIBlemish(self)
            self.setStatus(0, 'Status: set file for blemish mask')
            self.gui_win.setFixedHeight(200)

        if cp.current_file_tab.value() == self.list_file_types[3] :
            self.gui_win = GUIData(self)
            self.setStatus(0, 'Status: processing for data')
            self.gui_win.setFixedHeight(640)

        if cp.current_file_tab.value() == self.list_file_types[4] :
            self.gui_win = GUIConfigParameters(self)
            self.setStatus(0, 'Status: set file for config. pars.')
            self.gui_win.setFixedHeight(200)

        if cp.current_file_tab.value() == self.list_file_types[5] :
            self.gui_win = GUIWorkResDirs(self)
            self.setStatus(0, 'Status: set work and result dirs.')
            self.gui_win.setFixedHeight(200)

        #self.gui_win.setFixedHeight(180)
        #self.gui_win.setFixedHeight(600)
        self.hboxW.addWidget(self.gui_win)

    def onTabBar(self):
        tab_ind  = self.tab_bar.currentIndex()
        tab_name = str(self.tab_bar.tabText(tab_ind))
        cp.current_file_tab.setValue( tab_name )
        logger.info(' ---> selected tab: ' + str(tab_ind) + ' - open GUI to work with: ' + tab_name, __name__)
        self.guiSelector()

    def setParent(self,parent) :
        self.parent = parent

    def resizeEvent(self, e):
        #logger.debug('resizeEvent', __name__) 
        self.frame.setGeometry(self.rect())

    def moveEvent(self, e):
        #logger.debug('moveEvent', __name__) 
        #self.position = self.mapToGlobal(self.pos())
        #self.position = self.pos()
        #logger.debug('moveEvent: new pos:' + str(self.position), __name__)
        pass

    def closeEvent(self, event):
        logger.debug('closeEvent', __name__)

        try    : cp.guimain.butFiles.setStyleSheet(cp.styleButton)
        except : pass

        try    : self.gui_win.close()
        except : pass

        try    : self.tab_bar.close()
        except : pass
        
        try    : del cp.guifiles # GUIFiles
        except : pass # silently ignore

    def onClose(self):
        logger.debug('onClose', __name__)
        self.close()

    def onSave(self):
        logger.debug('onSave', __name__)
        cp.saveParametersInFile( cp.fname_cp.value() )

    def onShow(self):
        logger.debug('onShow - is not implemented yet...', __name__)


    #def on_off_gui_dark(self,but):
    #    logger.debug('on_off_gui_dark', __name__)
    #    self.tab_bar.setCurrentIndex(0)
    #    if bjpeds.status_for_pedestal_file() : but.setStyleSheet(cp.styleButtonGood)
    #    else                                 : but.setStyleSheet(cp.styleButtonBad)

    #def on_off_gui_flat(self,but):
    #    logger.debug('on_off_gui_flat', __name__)
    #    self.tab_bar.setCurrentIndex(1)

    #def on_off_gui_data(self,but):
    #    logger.debug('on_off_gui_data', __name__)
    #    self.tab_bar.setCurrentIndex(2)


    def setStatus(self, status_index=0, msg=''):
        list_of_states = ['Good','Warning','Alarm']
        if status_index == 0 : self.lab_status.setStyleSheet(cp.styleStatusGood)
        if status_index == 1 : self.lab_status.setStyleSheet(cp.styleStatusWarning)
        if status_index == 2 : self.lab_status.setStyleSheet(cp.styleStatusAlarm)

        #self.lab_status.setText('Status: ' + list_of_states[status_index] + msg)
        self.lab_status.setText(msg)


#-----------------------------

if __name__ == "__main__" :

    app = QtWidgets.QApplication(sys.argv)
    widget = GUIFiles ()
    widget.show()
    app.exec_()

#-----------------------------
