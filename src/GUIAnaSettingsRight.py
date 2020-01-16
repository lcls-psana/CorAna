#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIAnaSettingsRight...
#
#------------------------------------------------------------------------

"""GUI sets parameters for analysis (right pannel)"""
from __future__ import print_function

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
from FileNameManager        import fnm
from MaskEditor             import *
import GlobalUtils          as     gu

#---------------------
#  Class definition --
#---------------------
class GUIAnaSettingsRight ( QtWidgets.QWidget ) :
    """GUI sets parameters for analysis (right panel)"""

    #----------------
    #  Constructor --
    #----------------
    def __init__ ( self, parent=None ) :
        QtWidgets.QWidget.__init__(self, parent)
        self.setGeometry(20, 40, 390, 30)
        self.setWindowTitle('Analysis Settings Right')
        self.setFrame()

        self.list_mask_types = ['no-mask', 'from-file']

        self.tit_lld      = QtWidgets.QLabel('Low Level Discrimination (LLD):')
        self.edi_lld_adu  = QtWidgets.QLineEdit( str( cp.lld_adu.value() ) )        
        self.edi_lld_rms  = QtWidgets.QLineEdit( str( cp.lld_rms.value() ) )        
        self.rad_lld_none = QtWidgets.QRadioButton('no LLD')
        self.rad_lld_adu  = QtWidgets.QRadioButton('ADU threshold:')
        self.rad_lld_rms  = QtWidgets.QRadioButton('dark RMS threshold:')
        self.rad_lld_grp  = QtWidgets.QButtonGroup()
        self.rad_lld_grp.addButton(self.rad_lld_none)
        self.rad_lld_grp.addButton(self.rad_lld_adu )
        self.rad_lld_grp.addButton(self.rad_lld_rms )
        self.list_lld_types = ['NONE', 'ADU', 'RMS']
        if   cp.lld_type.value() == self.list_lld_types[1] : self.rad_lld_adu .setChecked(True)
        elif cp.lld_type.value() == self.list_lld_types[2] : self.rad_lld_rms .setChecked(True)
        else                                               : self.rad_lld_none.setChecked(True)

        self.tit_mask_set  = QtWidgets.QLabel('Mask Settings:')
        self.rad_mask_none = QtWidgets.QRadioButton('no mask (use all pixels)')
        self.rad_mask_file = QtWidgets.QRadioButton('from existing file')
        self.rad_mask_grp  = QtWidgets.QButtonGroup()
        self.rad_mask_grp.addButton(self.rad_mask_none)
        self.rad_mask_grp.addButton(self.rad_mask_file)
        if cp.ana_mask_type.value() == self.list_mask_types[0] : self.rad_mask_none.setChecked(True)
        if cp.ana_mask_type.value() == self.list_mask_types[1] : self.rad_mask_file.setChecked(True)

        self.but_mask_poly = QtWidgets.QPushButton('ROI Mask Editor')
        self.but_file      = QtWidgets.QPushButton('File:')
        self.edi_mask_file = QtWidgets.QLineEdit( fnm.path_roi_mask() )       
        self.edi_mask_file.setReadOnly( True )  

        self.tit_res_sets        = QtWidgets.QLabel('Result saving settings:')
        self.cbx_res_ascii_out   = QtWidgets.QCheckBox('ASCII output', self)
        self.cbx_res_fit1        = QtWidgets.QCheckBox('Perform Fit1', self)
        self.cbx_res_fit2        = QtWidgets.QCheckBox('Perform Fit2', self)
        self.cbx_res_fit_cust    = QtWidgets.QCheckBox('Perform Custom Fit', self)
        self.cbx_res_png_out     = QtWidgets.QCheckBox('Create PNG Files', self)
        self.cbx_res_save_log    = QtWidgets.QCheckBox('Save Log-file', self)

        self.cbx_res_ascii_out.setChecked( cp.res_ascii_out.value() )
        self.cbx_res_fit1     .setChecked( cp.res_fit1     .value() )
        self.cbx_res_fit2     .setChecked( cp.res_fit2     .value() )
        self.cbx_res_fit_cust .setChecked( cp.res_fit_cust .value() )
        self.cbx_res_png_out  .setChecked( cp.res_png_out  .value() )
        self.cbx_res_save_log .setChecked( cp.res_save_log .value() )

        self.grid = QtWidgets.QGridLayout()

        self.grid_row = 0
        self.grid.addWidget(self.tit_lld,           self.grid_row+1, 0, 1, 8)
        self.grid.addWidget(self.rad_lld_none,      self.grid_row+2, 1, 1, 4)
        self.grid.addWidget(self.rad_lld_adu,       self.grid_row+3, 1, 1, 4)
        self.grid.addWidget(self.edi_lld_adu,       self.grid_row+3, 5)
        self.grid.addWidget(self.rad_lld_rms,       self.grid_row+4, 1, 1, 4)
        self.grid.addWidget(self.edi_lld_rms,       self.grid_row+4, 5)

        self.grid_row = 4
        self.grid.addWidget(self.tit_mask_set,      self.grid_row+1, 0, 1, 9)
        self.grid.addWidget(self.rad_mask_none,     self.grid_row+2, 1, 1, 6)
        self.grid.addWidget(self.rad_mask_file,     self.grid_row+3, 1, 1, 6)
        self.grid.addWidget(self.but_mask_poly,     self.grid_row+3, 7, 1, 3)
        self.grid.addWidget(self.but_file,          self.grid_row+4, 0, 1, 2)
        self.grid.addWidget(self.edi_mask_file,     self.grid_row+4, 2, 1, 8)

        self.grid_row = 9
        self.grid.addWidget(self.tit_res_sets,      self.grid_row+1, 0, 1, 8)     
        self.grid.addWidget(self.cbx_res_fit1,      self.grid_row+2, 1, 1, 4)     
        self.grid.addWidget(self.cbx_res_fit2,      self.grid_row+3, 1, 1, 4)          
        self.grid.addWidget(self.cbx_res_fit_cust,  self.grid_row+4, 1, 1, 4) 
        self.grid.addWidget(self.cbx_res_ascii_out, self.grid_row+2, 6, 1, 3)
        self.grid.addWidget(self.cbx_res_png_out,   self.grid_row+3, 6, 1, 3) 
        self.grid.addWidget(self.cbx_res_save_log,  self.grid_row+4, 6, 1, 3) 

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.grid)
        self.vbox.addStretch(1)

        self.setLayout(self.vbox)

        self.rad_lld_none.clicked.connect(self.onRadioLLD)
        self.rad_lld_adu.clicked.connect(self.onRadioLLD)
        self.rad_lld_rms.clicked.connect(self.onRadioLLD)

        self.edi_lld_adu.editingFinished.connect(self.onEdit)
        self.edi_lld_rms.editingFinished.connect(self.onEdit)

        self.cbx_res_ascii_out.stateChanged[int].connect(self.onCBox)
        self.cbx_res_fit1.stateChanged[int].connect(self.onCBox)
        self.cbx_res_fit2.stateChanged[int].connect(self.onCBox)
        self.cbx_res_fit_cust.stateChanged[int].connect(self.onCBox)
        self.cbx_res_png_out.stateChanged[int].connect(self.onCBox)
        self.cbx_res_save_log.stateChanged[int].connect(self.onCBox)

        self.rad_mask_none.clicked.connect(self.onMaskRadioGrp)
        self.rad_mask_file.clicked.connect(self.onMaskRadioGrp)
        self.but_mask_poly.clicked.connect(self.onMaskPoly)
        self.but_file.clicked.connect(self.onButFile)

        self.showToolTips()
        self.setStyle()

    #-------------------
    #  Public methods --
    #-------------------

    def showToolTips(self):
        # Tips for buttons and fields:
        msg = 'Edit field'

        msg_rad_mask = 'Use this group of radio buttons\nto select the type of mask'
        self.rad_mask_none.setToolTip(msg_rad_mask)
        self.rad_mask_file.setToolTip(msg_rad_mask)
        self.but_mask_poly.setToolTip('Click on this button\nto use the polygon mask')
        self.but_file  .setToolTip('Click on this button\nto change the mask file.')
        self.edi_mask_file.setToolTip('Click on "Browse"\nto change this field.')



    def setFrame(self):
        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken ) #Box, Panel | Sunken, Raised 
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        #self.frame.setVisible(False)

    def setStyle(self):

        width = 60
        self.                    setFixedWidth(390)
        self.                    setStyleSheet (cp.styleBkgd)

        self.tit_res_sets       .setStyleSheet (cp.styleTitle)     
        self.cbx_res_ascii_out  .setStyleSheet (cp.styleLabel)
        self.cbx_res_fit1       .setStyleSheet (cp.styleLabel)
        self.cbx_res_fit2       .setStyleSheet (cp.styleLabel)
        self.cbx_res_fit_cust   .setStyleSheet (cp.styleLabel)
        self.cbx_res_png_out    .setStyleSheet (cp.styleLabel)
        self.cbx_res_save_log   .setStyleSheet (cp.styleLabel)

        self.edi_lld_adu        .setStyleSheet(cp.styleEdit) 
        self.edi_lld_rms        .setStyleSheet(cp.styleEdit) 

        self.edi_lld_adu        .setFixedWidth(width)
        self.edi_lld_rms        .setFixedWidth(width)

        self.edi_lld_adu        .setAlignment(QtCore.Qt.AlignRight) 
        self.edi_lld_rms        .setAlignment(QtCore.Qt.AlignRight) 

        self.tit_lld            .setStyleSheet (cp.styleTitle)
        self.rad_lld_none       .setStyleSheet (cp.styleLabel)
        self.rad_lld_adu        .setStyleSheet (cp.styleLabel)
        self.rad_lld_rms        .setStyleSheet (cp.styleLabel)

#        self.box_kin_mode       .setStyleSheet(cp.styleBox) 
        #width = 80
        #self.but_mask_poly.setFixedWidth(width)
        #self.but_file  .setFixedWidth(width)

        self.tit_mask_set .setStyleSheet (cp.styleTitle)
        self.rad_mask_none.setStyleSheet (cp.styleLabel)
        self.rad_mask_file.setStyleSheet (cp.styleLabel)

        self.but_mask_poly.setStyleSheet (cp.styleButton)
        self.but_file     .setStyleSheet (cp.styleButton)
        self.edi_mask_file.setStyleSheet (cp.styleEditInfo)
        self.edi_mask_file.setAlignment (QtCore.Qt.AlignRight)

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
        try: # try to delete self object in the cp
            del cp.guianasettingsright # GUIAnaSettingsRight
        except AttributeError:
            pass # silently ignore

        #try :
        #    cp.maskeditor.close()
        #    del cp.maskeditor
        #except :
        #    pass


    def onClose(self):
        logger.debug('onClose', __name__)
        self.close()

    def on(self):
        logger.debug('on click - is not implemented yet', __name__)

    def onCBox(self):

        if self.cbx_res_ascii_out  .hasFocus() :
            self.cbx = self.cbx_res_ascii_out
            self.par = cp.res_ascii_out
            self.tit = 'res_ascii_out' 

        elif self.cbx_res_fit1       .hasFocus() :
            self.cbx = self.cbx_res_fit1
            self.par = cp.res_fit1
            self.tit = 'res_fit1' 

        elif self.cbx_res_fit2       .hasFocus() :
            self.cbx = self.cbx_res_fit2
            self.par = cp.res_fit2
            self.tit = 'res_fit2' 

        elif self.cbx_res_fit_cust   .hasFocus() :
            self.cbx = self.cbx_res_fit_cust
            self.par = cp.res_fit_cust
            self.tit = 'res_fit_cust' 

        elif self.cbx_res_png_out    .hasFocus() :
            self.cbx = self.cbx_res_png_out
            self.par = cp.res_png_out
            self.tit = 'res_png_out' 

        elif self.cbx_res_save_log   .hasFocus() :
            self.cbx = self.cbx_res_save_log
            self.par = cp.res_save_log
            self.tit = 'res_save_log' 

        self.par.setValue( self.cbx.isChecked() )
        msg = 'onCBox - set status of ' + self.tit  + ': ' + str( self.par.value())
        logger.info(msg, __name__ )
    

    def onEdit(self):

        if self.edi_lld_adu.isModified() :            
            self.edi = self.edi_lld_adu 
            self.par = cp.lld_adu
            self.tit = 'lld_adu'

        elif self.edi_lld_rms.isModified() :            
            self.edi = self.edi_lld_rms
            self.par = cp.lld_rms
            self.tit = 'lld_rms'

        else : return # no-modification

        self.edi.setModified(False)
        self.par.setValue( self.edi.displayText() )        
        msg = 'onEdit - set value of ' + self.tit  + ': ' + str( self.par.value())
        logger.info(msg, __name__ )


    def onRadioLLD(self): 
        if self.rad_lld_none.isChecked() : cp.lld_type.setValue( self.list_lld_types[0] )
        if self.rad_lld_adu .isChecked() : cp.lld_type.setValue( self.list_lld_types[1] )
        if self.rad_lld_rms .isChecked() : cp.lld_type.setValue( self.list_lld_types[2] )
        logger.info('onRadioLLD - selected Low Level Discrimination type: ' + cp.lld_type.value(), __name__ )

    def onMaskRadioGrp(self):
        if self.rad_mask_none.isChecked() : cp.ana_mask_type.setValue(self.list_mask_types[0])
        if self.rad_mask_file.isChecked() : cp.ana_mask_type.setValue(self.list_mask_types[1])
        logger.info('onMaskRadioGrp - set cp.ana_mask_type = ' + cp.ana_mask_type.value(), __name__)

    def onMaskPoly(self):
        logger.info('onMaskPoly', __name__)
        try :
            cp.maskeditor.close()
            try    : del cp.maskeditor
            except : pass
            self.but_mask_poly.setStyleSheet(cp.styleButtonBad)

        except :
            img_fname = fnm.path_data_ave()
            logger.info( 'Open Mask Editor for image from file: ' + img_fname, __name__)
            if img_fname is None : return

            #xy_beam0_img = self.xyLabToImg((cp.x_coord_beam0.value(), cp.y_coord_beam0.value()))
            xy_beam0_img = (cp.x_coord_beam0.value(), cp.y_coord_beam0.value())

            cp.maskeditor = MaskEditor(None, ifname=img_fname, xyc=xy_beam0_img, \
                                       ofname=fnm.path_roi_mask_plot(), mfname=fnm.path_roi_mask_prefix()) #, updown=False)
            cp.maskeditor.move(cp.guimain.pos().__add__(QtCore.QPoint(860,20)))
            cp.maskeditor.show()
            self.but_mask_poly.setStyleSheet(cp.styleButtonGood)


    def  xyLabToImg( self, xy ) :
        
        rows       = cp.bat_img_rows.value()
        cols       = cp.bat_img_cols.value()
        size       = cp.bat_img_size.value()
        ccd_orient = cp.ccd_orient.value()

        x, y = xy

        print('Image rows, cols:', rows, cols)
        print('Beam center Lab x, y =', x, y) 

        if   ccd_orient == '0'   : return (x, rows-y)
        elif ccd_orient == '90'  : return (x, y)
        elif ccd_orient == '180' : return (cols-x, y)
        elif ccd_orient == '270' : return (cols-x, rows-y)
        else :
            logger.error('Non-existent CCD orientation: ' + str(sp.ccd_orient), __name__)            

 
    def onButFile(self):
        logger.info('onButFile', __name__)

        path = fnm.path_roi_mask()
        #print 'path_roi_mask()', path

        if path is None : dname, fname = cp.ana_mask_fname.value_def(), cp.ana_mask_dname.value_def()
        else            : dname, fname = os.path.split(path)

        path = str( QtWidgets.QFileDialog.getOpenFileName(self,'Select file',path) )[0]
        dname, fname = os.path.split(path)

        if dname == '' or fname == '' :
            logger.warning('Input directiry name or file name is empty... keep file name unchanged...', __name__)
            return

        self.edi_mask_file.setText(path)
        cp.ana_mask_fname.setValue(fname)
        cp.ana_mask_dname.setValue(dname)
        logger.info('selected file for mask: ' + str(cp.ana_mask_fname.value()), __name__ )

#-----------------------------

if __name__ == "__main__" :

    app = QtWidgets.QApplication(sys.argv)
    widget = GUIAnaSettingsRight ()
    widget.show()
    app.exec_()

#-----------------------------
