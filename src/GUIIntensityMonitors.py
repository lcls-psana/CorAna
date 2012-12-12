#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIIntensityMonitors...
#
#------------------------------------------------------------------------

"""GUI sets parameters for intensity monitors"""

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
from FileNameManager        import fnm
from PlotArray              import *
import GlobalUtils          as     gu
#---------------------
#  Class definition --
#---------------------
class GUIIntensityMonitors ( QtGui.QWidget ) :
    """GUI sets parameters for intensity monitors"""

    def __init__ ( self, parent=None ) :
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(100, 200, 850,300)
        self.setWindowTitle('GUI for Intensity Monitors')
        self.setFrame()

        self.list_of_dicts   = []

        self.grid = QtGui.QGridLayout()
        self.grid_row = 0
        self.setTitleBar()

        self.rad_nonorm = QtGui.QRadioButton('No norm.')
        self.rad_sele_grp = QtGui.QButtonGroup()
        self.rad_sele_grp.addButton(self.rad_nonorm)
        self.connect(self.rad_nonorm, QtCore.SIGNAL('clicked()'), self.onRadio)

        for i, (name, ch1, ch2, ch3, ch4, norm, sele, sele_min, sele_max) in enumerate(cp.imon_pars_list) :
            #print i, name.value(), ch1.value(), ch2.value(), ch3.value(), ch4.value()
            self.guiSection(name, ch1, ch2, ch3, ch4, norm, sele, sele_min, sele_max) 

        self.grid.addWidget(self.rad_nonorm, self.grid_row, 6, 1, 3)

        self.setLayout(self.grid)

        self.showToolTips()
        self.setStyle()

        self.initRadio()
        self.setStyleEdiFields()

    #-------------------
    #  Public methods --
    #-------------------

    def showToolTips(self):
        msg = 'Use this GUI to set partitions.'
        self.setToolTip(msg)

    def setFrame(self):
        self.frame = QtGui.QFrame(self)
        self.frame.setFrameStyle( QtGui.QFrame.Box | QtGui.QFrame.Sunken ) #Box, Panel | Sunken, Raised 
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        self.frame.setVisible(False)

    def setStyle(self):
        self.setMinimumSize(600,300)
        #self.setMinimumWidth(380)
        #self.setMinimumHeight(300)
        self.setStyleSheet(cp.styleBkgd)


    def setTitleBar(self) :
        self.list_of_titles = ['Intensity Monitor', 'Ch.1', 'Ch.2', 'Ch.3', 'Ch.4',
                               'Plot', 'Norm', 'Select', 'Imin', 'Imax']
        for i,t in enumerate(self.list_of_titles) : 
            label = QtGui.QLabel(t)
            label.setStyleSheet(cp.styleLabel)
            label.setFixedHeight(10)
            if i==5 : label.setFixedWidth(80)
            if i==6 : label.setFixedWidth(50)
            if i==7 : label.setFixedWidth(50)
            self.grid.addWidget(label, self.grid_row, i)
        self.grid_row += 1


    def guiSection(self, name, cbch1=None, cbch2=None, cbch3=None, cbch4=None,
                   norm=None, sele=None, sele_min=None, sele_max=None) :
        edi      = QtGui.QLineEdit( str(name.value()) )        
        but      = QtGui.QPushButton('Browse')
        #box      = QtGui.QComboBox( self ) 
        #box.addItems(self.list_of_methods)
        #box.setCurrentIndex( self.list_of_methods.index(method.value()) )
        cb1 = QtGui.QCheckBox('   +', self)
        cb2 = QtGui.QCheckBox('   +', self)
        cb3 = QtGui.QCheckBox('   +', self)
        cb4 = QtGui.QCheckBox('   =', self)

        rad = QtGui.QRadioButton('    ')
        if norm.value() : rad.setChecked(True)

        self.rad_sele_grp.addButton(rad)

        cbs = QtGui.QCheckBox('', self)
        mis = QtGui.QLineEdit( str(sele_min.value()) )        
        mas = QtGui.QLineEdit( str(sele_max.value()) )        

        sec_dict = { 0:(edi,name),
                     1:(cb1,cbch1),
                     2:(cb2,cbch2),
                     3:(cb3,cbch3),
                     4:(cb4,cbch4),
                     5:(but,None),
                     6:(rad,norm),
                     7:(cbs,sele),
                     8:(mis,sele_min),
                     9:(mas,sele_max)
                     }

        self.list_of_dicts.append( sec_dict )

        for col,(fld, par) in sec_dict.iteritems() :
            self.grid.addWidget(fld, self.grid_row, col)
            if col>0 and col<5 or col==7 :
                fld.setChecked( par.value() )
                self.connect(fld, QtCore.SIGNAL('stateChanged(int)'), self.onCBox )

        self.grid_row += 1
        self.connect(rad, QtCore.SIGNAL('clicked()'), self.onRadio)


        edi.setReadOnly( True )  
        edi.setToolTip('Edit number in this field\nor click on "Browse"\nto select the file.')
        but.setToolTip('Click on this button\nand select the file.')
        #box.setToolTip('Click on this box\nand select the partitioning method.')

        edi    .setStyleSheet (cp.styleEditInfo) # cp.styleEdit
        #box    .setStyleSheet (cp.styleButton) 
        but    .setStyleSheet (cp.styleButton) 
        edi    .setAlignment (QtCore.Qt.AlignLeft)
        mis    .setStyleSheet (cp.styleEdit) # cp.styleEditInfo
        mas    .setStyleSheet (cp.styleEdit) # cp.styleEditInfo

        #mas.setObjectName('mas')
        #mas.setStyleSheet('QLineEdit#mas          {color: blue; background-color: yellow;}' +
        #                  'QLineEdit#mas[readOnly="true"] {color: black; background-color: green;}' )



        #cbs    .setStyleSheet (cp.styleCBox)
        #cbs    .initStyleOption (QtGui.QStyleOptionButton.CE_CheckBox)
        #cbs    .setPalette(QtGui.QPalette(QtGui.QColor(255, 255, 255)))

        width = 60
        but    .setFixedWidth(width)
        edi    .setFixedWidth(230)
        mis    .setFixedWidth(width)
        mas    .setFixedWidth(width)

        self.connect(but, QtCore.SIGNAL('clicked()'),         self.onBut  )
        self.connect(mis, QtCore.SIGNAL('editingFinished()'), self.onEdit )
        self.connect(mas, QtCore.SIGNAL('editingFinished()'), self.onEdit )


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
        try    : del cp.guiintensitymonitors # GUIIntensityMonitors
        except : pass # silently ignore

    def onClose(self):
        logger.debug('onClose', __name__)
        self.close()

    def onApply(self):
        logger.debug('onApply - is already applied...', __name__)

    def onShow(self):
        logger.debug('onShow - is not implemented yet...', __name__)


    def onCBox(self) :
        for row0, sec_dict in enumerate(self.list_of_dicts) :                        
            for col in [1,2,3,4,7] :
                cbx, par = sec_dict[col]
                if cbx.hasFocus() : 
                    cbx_status = cbx.isChecked()
                    msg = 'onCBox - set status %s of checkbox in row:%s col:%s' % (cbx_status, row0+1, col)
                    par.setValue( cbx_status )
                    logger.info(msg, __name__ )

                    if col == 7 :
                        self.setStyleEdiFieldsForRow(row0)

                    elif cp.plotarray_is_on :
                        self.redrawArray(row0)                        
                    return




    def setStyleEdiFields(self):
        for row0, sec_dict in enumerate(self.list_of_dicts) :                        
            self.setStyleEdiFieldsForRow(row0)


    def setStyleEdiFieldsForRow(self, row):
        sec_dict = self.list_of_dicts[row]
        rad, par_rad = sec_dict[6]
        cbx, par_cbx = sec_dict[7]
        for col in [8,9] :
            edi, par = sec_dict[col]
            is_selected = cbx.isChecked() or rad.isChecked()
            edi.setReadOnly(not is_selected)
            if is_selected :
                edi.setStyleSheet (cp.styleEdit)
                self.checkEdiLimits(row)

            else :
                edi.setStyleSheet (cp.styleEditInfo)



    def checkEdiLimits(self, row):
        sec_dict = self.list_of_dicts[row]
        mis, par_mis = sec_dict[8]
        mas, par_mas = sec_dict[9]
        if par_mis.value() >= par_mas.value() :
            mis.setStyleSheet (cp.styleEditBad)
            mas.setStyleSheet (cp.styleEditBad)


    def initRadio(self): 
        for row0, sec_dict in enumerate(self.list_of_dicts) :                        
            rad, par = sec_dict[6]
            if par.value :
                rad.setChecked(True)
                return
        self.rad_nonorm.setChecked(True)


    def onRadio(self):
        isOn = False
        for row0, sec_dict in enumerate(self.list_of_dicts) :                        
            rad, par = sec_dict[6]
            if rad.isChecked() :
                par.setValue(True)
                isOn = True
                logger.info('onRadio in row:' + str(row0), __name__)
            else               :
                par.setValue(False)

        if not isOn : logger.info('onRadio - Normalization is OFF', __name__)

        self.setStyleEdiFields()


#-----------------------------

    def onEdit(self):
        logger.debug('onEdit', __name__)
        for row0, sec_dict in enumerate(self.list_of_dicts) :                        

            for col in [8,9] :
                edi, par = sec_dict[col]

                if edi.isModified() :            
                    edi.setModified(False)
                    par.setValue( str(edi.displayText()) )
                    msg = 'row:' + str(row0) + ' set ' + \
                          self.list_of_titles[col] + ' = ' + str(par.value())
                    logger.info(msg, __name__ )

                    self.setStyleEdiFieldsForRow(row0)

#-----------------------------

    def onBut(self):
        logger.debug('onBut', __name__)
        for row0, sec_dict in enumerate(self.list_of_dicts) :                        
            edi, name = sec_dict[0]
            but, empt = sec_dict[5]
            if but.hasFocus() : 
                msg = 'onBut - click on button %s in row %s, plot for %s' % (str(but.text()), row0+1, name.value())
                logger.info(msg, __name__ )
                self.plotIMon(row0)
                return


    def plotIMon(self,imon):
        logger.debug('plotIMon', __name__)
        arr = self.getArray(imon)
        try :
            cp.plotarray.close()
        except :
            if arr == None : return
            cp.plotarray = PlotArray(None, arr,
                                     ofname=fnm.path_data_mons_plot(),
                                     title=self.titleForIMon(imon))
            cp.plotarray.move(self.parentWidget().pos().__add__(QtCore.QPoint(700,300)))
            cp.plotarray.show()


    def titleForIMon(self,imon):
        return cp.imon_name_list[imon].value() + \
               ':  sum of channels: ' + \
               self.strMaskForIMonChannels(imon) 
        

    def redrawArray(self,imon):
        logger.debug('plotIMon', __name__)
        arr = self.getArray(imon)
        if arr == None : return
        try :
            cp.plotarray.set_array(arr, title=self.titleForIMon(imon))
        except :
            pass


    def boolMaskForIMonChannels(self,imon):
        return [cp.imon_ch1_list[imon].value(),
                cp.imon_ch2_list[imon].value(),
                cp.imon_ch3_list[imon].value(),
                cp.imon_ch4_list[imon].value()]


    def npIntMaskForIMonChannels(self,imon):
        return np.array(self.boolMaskForIMonChannels(imon),dtype=int)


    def strMaskForIMonChannels(self,imon):
        mask = self.boolMaskForIMonChannels(imon)
        str = ''
        for i,v in enumerate(mask) :
            if v : str += '%s+' % (i+1)
        return str.rstrip('+')


    def getArray(self,imon):
        logger.debug('getArray for imon: '+str(imon), __name__)
        arr_all = gu.get_array_from_file(fnm.path_data_scan_monitors_data())
        if arr_all == None : return None
        logger.debug('Array shape: ' + str(arr_all.shape), __name__)

        ibase    = 1+imon*4
        arr_imon = arr_all[:,ibase:ibase+4]
        #print 'arr_imon:\n', arr_imon
        #print 'arr_imon.shape:', arr_imon.shape

        #mask = self.maskForIMonChannels(imon)
        #npmask = np.array(mask,dtype=float)
        npmask = self.npIntMaskForIMonChannels(imon)

        size   = arr_imon.shape[0]
        npcol1 = np.ones(size)

        X,Y = np.meshgrid(npmask,npcol1)
        arr_prod = (arr_imon * X)        
        arr_sum  = arr_prod.sum(1) 
        
        #print 'npmask=', npmask
        #print 'size=', size
        #print X
        #print X.shape
        #print arr_imon
        #print arr_imon.shape
        #print arr_prod
        #print arr_prod.shape
        return arr_sum

#-----------------------------
#    def onBox(self):
#        for fields in self.sect_fields :
#            box = fields[3]
#            if box.hasFocus() :
#                tit    = fields[0]
#                method = fields[6]
#                method_selected = box.currentText()
#                method.setValue( method_selected ) 
#                logger.info('onBox for ' + str(tit.text()) + ' - selected method: ' + method_selected, __name__)
#
#-----------------------------

if __name__ == "__main__" :

    app = QtGui.QApplication(sys.argv)

    widget = GUIIntensityMonitors ()
    widget.show()

    #app.setStyleSheet('QLineEdit {color:  blue; background-color: yellow;}' +
    #                  'QLineEdit:[readOnly="true"] {color: black; background-color: green;}' )

    app.exec_()

#-----------------------------