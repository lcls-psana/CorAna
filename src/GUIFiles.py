#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIFiles...
#
#------------------------------------------------------------------------

"""GUI sets path to files"""

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
from GUIConfigParameters    import *
from GUIDark                import *
from Logger                 import logger
from BatchJobPedestals      import bjpeds

#---------------------
#  Class definition --
#---------------------
class GUIFiles ( QtGui.QWidget ) :
    """GUI sets path to files"""

    #----------------
    #  Constructor --
    #----------------
    def __init__ ( self, parent=None ) :
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(200, 400, 500, 30)
        self.setWindowTitle('Files')
        self.setFrame()

        self.sect_fields  = []

        self.tit_dir_work = QtGui.QLabel('Work/Results')

        self.lab_dir_work = QtGui.QLabel('Dir work:')
        self.edi_dir_work = QtGui.QLineEdit( cp.dir_work.value() )        
        self.but_dir_work = QtGui.QPushButton('Browse')
        self.edi_dir_work.setReadOnly( True )  

        self.lab_dir_results = QtGui.QLabel('Dir results:')
        self.edi_dir_results = QtGui.QLineEdit( cp.dir_results.value() )        
        self.but_dir_results = QtGui.QPushButton('Browse')
        self.edi_dir_results.setReadOnly( True )  

        self.lab_fname_prefix = QtGui.QLabel('File prefix:')
        self.edi_fname_prefix = QtGui.QLineEdit( cp.fname_prefix.value() )        

        self.tit_status = QtGui.QLabel     ('Status: ')
        self.but_close  = QtGui.QPushButton('Close') 
        self.but_save   = QtGui.QPushButton('Save') 
        self.but_show   = QtGui.QPushButton('Show Image') 

        self.hboxW = QtGui.QHBoxLayout()
   
        self.hboxB = QtGui.QHBoxLayout()
        self.hboxB.addWidget(self.tit_status)
        self.hboxB.addStretch(1)     
        self.hboxB.addWidget(self.but_close)
        self.hboxB.addWidget(self.but_save)
        self.hboxB.addWidget(self.but_show )

        self.list_file_types = ['Dark-run', 'Flat-field', 'Data', 'Conf.pars']
        self.makeTabBar()
        self.guiSelector()

        self.grid = QtGui.QGridLayout()
        self.grid_row = 0
        self.guiSection(self.list_file_types[0], cp.in_dir_dark, cp.in_file_dark)
        self.guiSection(self.list_file_types[1], cp.in_dir_flat, cp.in_file_flat)
        self.guiSection(self.list_file_types[2], cp.in_dir_data, cp.in_file_data) 

        self.grid.addWidget(self.tit_dir_work,      self.grid_row,   0, 1, 9)
        self.grid.addWidget(self.lab_dir_work,      self.grid_row+1, 1)
        self.grid.addWidget(self.edi_dir_work,      self.grid_row+1, 2, 1, 7)
        self.grid.addWidget(self.but_dir_work,      self.grid_row+1, 9)

        self.grid.addWidget(self.lab_dir_results,   self.grid_row+2, 1)
        self.grid.addWidget(self.edi_dir_results,   self.grid_row+2, 2, 1, 7)
        self.grid.addWidget(self.but_dir_results,   self.grid_row+2, 9)

        self.grid.addWidget(self.lab_fname_prefix,  self.grid_row+3, 1)
        self.grid.addWidget(self.edi_fname_prefix,  self.grid_row+3, 2, 1, 7)

        self.grid.addWidget(self.tab_bar,           self.grid_row+4, 0, 1, 10)
        #self.grid.addWidget(cp.guiconfigparameters, self.grid_row+5, 0, 1, 10)        
        self.grid.addLayout(self.hboxW,             self.grid_row+5, 0, 1, 10)
        self.grid.addLayout(self.hboxB,             self.grid_row+6, 0, 1, 10)
        self.setLayout(self.grid)

        self.connect( self.but_dir_work,     QtCore.SIGNAL('clicked()'),          self.onButDirWork )
        self.connect( self.but_dir_results,  QtCore.SIGNAL('clicked()'),          self.onButDirResults )
        self.connect( self.edi_fname_prefix, QtCore.SIGNAL('editingFinished ()'), self.onEditPrefix )

        self.connect( self.but_close,    QtCore.SIGNAL('clicked()'), self.onClose )
        self.connect( self.but_save,     QtCore.SIGNAL('clicked()'), self.onSave )
        self.connect( self.but_show ,    QtCore.SIGNAL('clicked()'), self.onShow )

        self.showToolTips()
        self.setStyle()

    #-------------------
    #  Public methods --
    #-------------------

    def showToolTips(self):
        #msg = 'Edit field'
        self.but_close .setToolTip('Close this window.')
        self.but_save .setToolTip('Apply changes to configuration parameters.')
        self.but_show  .setToolTip('Show ...')
        self.edi_dir_work.setToolTip('Click on "Browse"\nto change the directory.')
        self.but_dir_work.setToolTip('Click on this button\nand select the directory.')
        self.edi_dir_results.setToolTip('Click on "Browse"\nto change the directory.')
        self.but_dir_results.setToolTip('Click on this button\nand select the directory.')

    def setFrame(self):
        self.frame = QtGui.QFrame(self)
        self.frame.setFrameStyle( QtGui.QFrame.Box | QtGui.QFrame.Sunken ) #Box, Panel | Sunken, Raised 
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        self.frame.setVisible(False)


    def makeTabBar(self,mode=None) :
        #if mode != None : self.tab_bar.close()
        self.tab_bar = QtGui.QTabBar()

        #Uses self.list_file_types

        self.ind_tab_dark = self.tab_bar.addTab( self.list_file_types[0] )
        self.ind_tab_flat = self.tab_bar.addTab( self.list_file_types[1] )
        self.ind_tab_data = self.tab_bar.addTab( self.list_file_types[2] )
        self.ind_tab_conf = self.tab_bar.addTab( self.list_file_types[3] )

        self.tab_bar.setTabTextColor(self.ind_tab_dark, QtGui.QColor('green'))
        self.tab_bar.setTabTextColor(self.ind_tab_flat, QtGui.QColor('red'))
        self.tab_bar.setTabTextColor(self.ind_tab_data, QtGui.QColor('blue'))
        self.tab_bar.setTabTextColor(self.ind_tab_conf, QtGui.QColor('magenta'))
        self.tab_bar.setShape(QtGui.QTabBar.RoundedNorth)

        self.tab_bar.setTabEnabled(1, False)
        self.tab_bar.setTabEnabled(2, False)
        
        logger.info(' make_tab_bar - set mode: ' + cp.ana_type.value(), __name__)

        self.tab_bar.setCurrentIndex(self.list_file_types.index(cp.current_file_tab.value()))
        #self.tab_bar.setCurrentIndex(3)

        self.connect(self.tab_bar, QtCore.SIGNAL('currentChanged(int)'), self.onTabBar)


    def guiSelector(self):
        try    : self.gui_win.close()
        except : pass

        #try    : cp.guiconfigparameters.close()
        #except : pass

        #try    : cp.guidark.close()
        #except : pass

        if cp.current_file_tab.value() == self.list_file_types[0] :
            self.gui_win = cp.guidark = GUIDark()
            
        if cp.current_file_tab.value() == self.list_file_types[3] :
            self.gui_win = cp.guiconfigparameters = GUIConfigParameters()

        self.gui_win.setFixedHeight(150)
        self.hboxW.addWidget(self.gui_win)

    def onTabBar(self):
        tab_ind  = self.tab_bar.currentIndex()
        tab_name = str(self.tab_bar.tabText(tab_ind))
        cp.current_file_tab.setValue( tab_name )
        logger.info(' ---> selected tab: ' + str(tab_ind) + ' - open GUI to work with: ' + tab_name, __name__)
        self.guiSelector()

    def setStyle(self):
        self.                 setStyleSheet (cp.styleBkgd)
        self.tit_status      .setStyleSheet (cp.styleLabel)
        self.tit_dir_work    .setStyleSheet (cp.styleTitle)
        self.lab_dir_work    .setStyleSheet (cp.styleLabel)
        self.edi_dir_work    .setStyleSheet (cp.styleEditInfo)       
        self.but_dir_work    .setStyleSheet (cp.styleButton) 
        self.lab_dir_results .setStyleSheet (cp.styleLabel)
        self.edi_dir_results .setStyleSheet (cp.styleEditInfo)       
        self.but_dir_results .setStyleSheet (cp.styleButton) 
        self.lab_fname_prefix.setStyleSheet (cp.styleLabel)
        self.edi_fname_prefix.setStyleSheet (cp.styleEdit)
        self.tit_dir_work    .setAlignment (QtCore.Qt.AlignLeft)
        self.lab_dir_work    .setAlignment (QtCore.Qt.AlignRight)
        self.edi_dir_work    .setAlignment (QtCore.Qt.AlignRight)
        self.lab_dir_results .setAlignment (QtCore.Qt.AlignRight)
        self.edi_dir_results .setAlignment (QtCore.Qt.AlignRight)
        self.lab_fname_prefix.setAlignment (QtCore.Qt.AlignRight)
        self.lab_dir_work    .setMinimumWidth(90)
        self.edi_dir_work    .setMinimumWidth(300)
        self.but_dir_work    .setFixedWidth(80)
        self.lab_dir_results .setMinimumWidth(90)
        self.edi_dir_results .setMinimumWidth(300)
        self.but_dir_results .setFixedWidth(80)
        self.but_close       .setStyleSheet (cp.styleButton)
        self.but_save        .setStyleSheet (cp.styleButton)
        self.but_show        .setStyleSheet (cp.styleButton)

    def guiSection(self, title, par_dir, par_file) :

        tit_sect= QtGui.QLabel(title)
        tit_dir = QtGui.QLabel('Dir:')
        tit_file= QtGui.QLabel('File:')
        edi_dir = QtGui.QLineEdit( par_dir .value() )        
        edi_file= QtGui.QLineEdit( par_file.value() )        
        but_dir = QtGui.QPushButton('Browse')
        but_file= QtGui.QPushButton('Browse')
        but_proc= QtGui.QPushButton('Check status')

        edi_dir .setReadOnly( True )  
        edi_file.setReadOnly( True )  

        msg_info = 'Use button "Browse"\nto change this field.'
        msg_file = 'Click on this button\nand select the file.'
        msg_dir  = 'Click on this butto\nand select the directory.'
        edi_dir .setToolTip(msg_info)
        edi_file.setToolTip(msg_info)
        but_dir .setToolTip(msg_dir)
        but_file.setToolTip(msg_file)
        but_proc.setToolTip('Click on this button\nto check if the output\nfile is available.')

        self.grid.addWidget(tit_sect, self.grid_row+0, 0, 1, 2)
        self.grid.addWidget(but_proc, self.grid_row+0, 2)
        self.grid.addWidget(tit_dir,  self.grid_row+1, 1)
        self.grid.addWidget(edi_dir,  self.grid_row+1, 2, 1, 7)
        self.grid.addWidget(but_dir,  self.grid_row+1, 9)
        self.grid.addWidget(tit_file, self.grid_row+2, 1)
        self.grid.addWidget(edi_file, self.grid_row+2, 2, 1, 7)
        self.grid.addWidget(but_file, self.grid_row+2, 9)
        self.grid_row += 3

        tit_sect   .setStyleSheet (cp.styleTitle)
        tit_dir    .setStyleSheet (cp.styleLabel)
        tit_file   .setStyleSheet (cp.styleLabel)
        edi_dir    .setStyleSheet (cp.styleEditInfo) 
        edi_file   .setStyleSheet (cp.styleEditInfo) 
        but_dir    .setStyleSheet (cp.styleButton) 
        but_file   .setStyleSheet (cp.styleButton) 
        but_proc   .setStyleSheet (cp.styleButtonBad) 

        tit_dir    .setAlignment (QtCore.Qt.AlignRight)
        tit_file   .setAlignment (QtCore.Qt.AlignRight)
        edi_dir    .setAlignment (QtCore.Qt.AlignRight)
        edi_file   .setAlignment (QtCore.Qt.AlignRight)

        width = 60
        but_dir    .setFixedWidth(width)
        but_file   .setFixedWidth(width)
        but_proc   .setFixedWidth(90)

        self.connect(edi_dir,  QtCore.SIGNAL('editingFinished ()'), self.onEditDir )
        self.connect(edi_file, QtCore.SIGNAL('editingFinished ()'), self.onEditFile)
        self.connect(but_dir,  QtCore.SIGNAL('clicked()'),          self.onButDir  )
        self.connect(but_file, QtCore.SIGNAL('clicked()'),          self.onButFile )
        self.connect(but_proc, QtCore.SIGNAL('clicked()'),          self.onButProc )
 
        self.sect_fields.append( (tit_sect, tit_dir, tit_file, edi_dir, edi_file, but_dir, but_file, par_dir, par_file, but_proc ) )


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

        try    : cp.guiconfigparameters.close()
        except : pass

        try    : cp.guidark.close()
        except : pass

        try    : cp.guiflat.close()
        except : pass

        try    : cp.guidata.close()
        except : pass

        try    : del cp.guifiles # GUIFiles
        except : pass # silently ignore

    def onClose(self):
        logger.debug('onClose', __name__)
        self.close()

    def onSave(self):
        logger.debug('onSave', __name__)
        cp.guiconfigparameters.onWrite()

    def onShow(self):
        logger.debug('onShow - is not implemented yet...', __name__)


    def onEditDir(self):
        logger.debug('onEditDir')
        for fields in self.sect_fields :
            edi = fields[3]
            par = fields[7]
            if edi.isModified() :            
                edi.setModified(False)
                par.setValue( str(edi.displayText()) )
                logger.info('Set dir = ' + str( par.value()), __name__ )


    def onEditFile(self):
        logger.debug('onEditFile', __name__)
        for fields in self.sect_fields :
            edi = fields[4]
            par = fields[8]
            if edi.isModified() :            
                edi.setModified(False)
                par.setValue( str(edi.displayText()) )
                logger.info('Set dir = ' + str( par.value()), __name__ )

        
    def onButDir(self):
        logger.debug('onButDir', __name__)
        for fields in self.sect_fields :
            but = fields[5]
            if but.hasFocus() :
                tit = fields[0]
                edi = fields[3]
                par = fields[7]
                dir0 = par.value()
                logger.info('Section: ' + str(tit.text()) + ' - browser for directory.', __name__)
                path, name = os.path.split(dir0)
                dir = str( QtGui.QFileDialog.getExistingDirectory(self,'Select directory',path) )

                if dir == dir0 or dir == '' :
                    logger.info('Input directiry has not been changed.', __name__)
                    return

                edi.setText(dir)        
                par.setValue(dir)
                logger.info('Set directory: ' + str(par.value()), __name__)


    def onButFile(self):
        logger.debug('onButFile', __name__)
        for fields in self.sect_fields :
            but = fields[6]
            if but.hasFocus() :
                tit = fields[0]
                edi = fields[4]
                par = fields[8]
                dir = fields[7].value()
                #dir   = edi.text()
                logger.info('Section: ' + str(tit.text()) + ' - browser for file', __name__ )
                path  = str( QtGui.QFileDialog.getOpenFileName(self,'Select file',dir) )
                dname, fname = os.path.split(path)

                if dname == '' or fname == '' :
                    logger.warning('Input directiry name or file name is empty... keep file name unchanged...')
                    return

                edi.setText(fname)
                par.setValue(fname)
                logger.info('selected the file name: ' + str(par.value()), __name__ )


    def onButProc(self):
        logger.debug('onButProc', __name__)
        for fields in self.sect_fields :
            but = fields[9]
            if but.hasFocus() :
                tit = fields[0]
                str_sec = str(tit.text())
                logger.info('Section: ' + str_sec + ' - pre-processing', __name__ )

                if   str_sec == self.list_file_types[0] : self.on_off_gui_dark(but)
                elif str_sec == self.list_file_types[1] : self.on_off_gui_flat(but) 
                elif str_sec == self.list_file_types[2] : self.on_off_gui_data(but)


    def on_off_gui_dark(self,but):
        logger.debug('on_off_gui_dark', __name__)
        self.tab_bar.setCurrentIndex(0)
        if bjpeds.status_for_pedestals() : but.setStyleSheet(cp.styleButtonGood)
        else                             : but.setStyleSheet(cp.styleButtonBad)

#        try :
#            cp.guidark.close()
#            but.setStyleSheet(cp.styleButtonBad)
#        except : # AttributeError: #NameError 
#            cp.guidark = GUIDark()
#            cp.guidark.setParent(self)
#            cp.guidark.move(self.pos().__add__(QtCore.QPoint(20,82))) # open window with offset w.r.t. parent
#            cp.guidark.show()
#            but.setStyleSheet(cp.styleButtonGood)


    def on_off_gui_flat(self,but):
        logger.debug('on_off_gui_flat', __name__)
        self.tab_bar.setCurrentIndex(1)

    def on_off_gui_data(self,but):
        logger.debug('on_off_gui_data', __name__)
        self.tab_bar.setCurrentIndex(2)



    def onButDirWork(self):
        logger.debug('onButDirWork - Select work directory.', __name__)
        dir0 = cp.dir_work.value()
        path, name = os.path.split(dir0)
        dir = str( QtGui.QFileDialog.getExistingDirectory(self,'Select directory',path) )

        if dir == dir0 or dir == '' :
            logger.info('Work directiry has not been changed.', __name__)
            return
        self.edi_dir_work.setText(dir)        
        cp.dir_work.setValue(dir)
        logger.info('Set directory: ' + str(cp.dir_work.value()), __name__)


    def onButDirResults(self):
        logger.debug('onButDirResults - Select results directory.', __name__)
        dir0 = cp.dir_results.value()
        path, name = os.path.split(dir0)
        dir = str( QtGui.QFileDialog.getExistingDirectory(self,'Select directory',path) )

        if dir == dir0 or dir == '' :
            logger.info('Results directiry has not been changed.', __name__)
            return
        self.edi_dir_results.setText(dir)        
        cp.dir_results.setValue(dir)
        logger.info('Set directory: ' + str(cp.dir_results.value()), __name__)


    def onEditPrefix(self):
        logger.debug('onEditPrefix', __name__)
        cp.fname_prefix.setValue( str(self.edi_fname_prefix.displayText()) )
        logger.info('Set file name common prefix: ' + str( cp.fname_prefix.value()), __name__ )

#-----------------------------

if __name__ == "__main__" :

    app = QtGui.QApplication(sys.argv)
    widget = GUIFiles ()
    widget.show()
    app.exec_()

#-----------------------------