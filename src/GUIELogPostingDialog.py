#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIELogPostingDialog...
#
#------------------------------------------------------------------------

"""Send message to ELog"""
from __future__ import print_function
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
from CorAna.Logger import logger
from .ConfigParametersCorAna import confpars as cp
from .GUIELogPostingFields import *

#---------------------
#  Class definition --
#---------------------


class GUIELogPostingDialog(QtWidgets.QDialog) :
    def __init__(self, parent=None, fname=None):
        QtWidgets.QDialog.__init__(self,parent)
        #self.setGeometry(20, 40, 500, 200)
        self.setWindowTitle('Send message to ELog')
        self.setFrame()
        cp.setIcons()

        #self.setModal(True)
        self.widg_pars = GUIELogPostingFields(parent=self,att_fname=fname)
        self.cbx_cntl  = QtWidgets.QCheckBox('&Lock control') 
        self.but_canc  = QtWidgets.QPushButton('&Cancel') 
        self.but_send  = QtWidgets.QPushButton('&Send to ELog') 
        #self.but_canc.setIcon(cp.icon_button_cancel)
        #self.but_send.setIcon(cp.icon_mail_forward)
        #self.setWindowIcon(cp.icon_mail_forward)

        self.cbx_cntl.setCheckState(QtCore.Qt.Checked)
        self.but_canc.setIcon(cp.icon_button_cancel)
        self.but_send.setIcon(cp.icon_mail_forward)
        self.setWindowIcon   (cp.icon_mail_forward)
        
        self.cbx_cntl.stateChanged[int].connect(self.onCBox)
        self.but_canc.clicked.connect(self.onCancel)
        self.but_send.clicked.connect(self.onSend)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.cbx_cntl)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.but_canc)
        self.hbox.addWidget(self.but_send)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.widg_pars)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

        self.but_canc.setFocusPolicy(QtCore.Qt.NoFocus)
        #self.but_send.setFocusPolicy(QtCore.Qt.NoFocus)
        #self.but_send.setFocus()

        self.setStyle()
        self.showToolTips()

#-----------------------------  

    def showToolTips(self):
        self.but_send.setToolTip('Mouse click on this button or Alt-S \nor "Enter" submits message to ELog')
        self.but_canc.setToolTip('Mouse click on this button \nor Alt-C cancels submission...')
        self.cbx_cntl.setToolTip('Lock/unlock top row \nof control buttons')
        
    def setFrame(self):
        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken ) #Box, Panel | Sunken, Raised 
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        #self.frame.setVisible(False)

    def setStyle(self):
        self.setFixedWidth(500)
        self.setStyleSheet(cp.styleBkgd)
        self.but_canc.setStyleSheet(cp.styleButton)
        self.but_send.setStyleSheet(cp.styleButton)
 
    def resizeEvent(self, e):
        #logger.debug('resizeEvent', __name__) 
        self.frame.setGeometry(self.rect())

    def moveEvent(self, e):
        pass

    def closeEvent(self, event):
        logger.debug('closeEvent', __name__)
        #print 'closeEvent'
        try    : self.widg_pars.close()
        except : pass

    def onCBox(self):
        logger.info('onCBox: control lock state: ' + str(self.cbx_cntl.checkState()), __name__) # cbx_cntl.isChecked()
        self.widg_pars.setControlLock(self.cbx_cntl.isChecked())

    def onCancel(self):
        logger.debug('onCancel', __name__)
        self.reject()
        #self.close()

    def onSend(self):
        logger.debug('onSend', __name__)
        self.widg_pars.updateConfigPars()
        list_of_fields = self.widg_pars.getListOfFields()

        logger.debug('Send to ELod the massege with parameters:', __name__)        
        for [label, edi, par, loc_par] in list_of_fields :
            msg = str(label.text()) + ' ' + loc_par.value()
            logger.debug(msg, __name__)        

        ins = self.widg_pars.ins.value()
        exp = self.widg_pars.exp.value()
        run = self.widg_pars.run.value()
        tag = self.widg_pars.tag.value()
        res = self.widg_pars.res.value()
        msg = self.widg_pars.msg.value()
        att = self.widg_pars.att.value()
        #msg = '"' + msg + '"'

        #msg_id = gu.send_msg_with_att_to_elog(ins, exp, run, tag, msg, fname_att=att, resp=res)
        logger.warning('Sorry, but sending post to ELog is unavailable in this app', __name__)  
        #logger.info('Sending post to ELog, msg_id: \n' + str(msg_id), __name__)  

        self.accept()
        #self.close()
 
#-----------------------------

if __name__ == "__main__" :

    app = QtWidgets.QApplication(sys.argv)
    w = GUIELogPostingDialog ()
    #w.show()
    resp=w.exec_()
    print('resp=',resp)
    print('QtWidgets.QDialog.Rejected: ', QtWidgets.QDialog.Rejected)
    print('QtWidgets.QDialog.Accepted: ', QtWidgets.QDialog.Accepted)

    #app.exec_()

#-----------------------------
