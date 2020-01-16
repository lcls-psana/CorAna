
#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIDark...
#
#------------------------------------------------------------------------

"""GUI works with dark run"""
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
import random
#import numpy as np

from PyQt5 import QtCore
#import time   # for sleep(sec)
#from BatchJobCorAna import bjcora
from ConfigParametersCorAna import confpars as cp

#---------------------
#  Class definition --
#---------------------

class ThreadWorker (QtCore.QThread) :
    update = QtCore.pyqtSignal('QString')

    def __init__ ( self, parent=None ) :
        QtCore.QThread.__init__(self, parent)        
        self.thread_id = random.random()
        #self.thread_id    = self.currentThreadId()
        #self.thread_count = self.idealThreadCount()

        cp.thread1 = self
        self.counter = 0

        #self.connect( self, QtCore.SIGNAL('update(QString)'), self.testConnection )


    def testConnection(self, text) :
        print('ThreadWorker: Signal is recieved ' + str(text))


    def run( self ) :
        while True :
            self.counter += 1
            #print '\nThread id, i:', self.thread_id, self.counter
            self.emitCheckStatusSignal()
            self.sleep(5)
            #time.sleep(1)


    def emitCheckStatusSignal( self ) :
        #bstatus, bstatus_str = bjcora.status_batch_job_for_cora_split()
        #fstatus, fstatus_str = bjcora.status_for_cora_split_files()
        #status_str = bstatus_str + '   ' + fstatus_str
        #status_str = bstatus_str
        if not QtCore is None :
            self.update.emit(\
                       'from work thread ' + str(self.thread_id) +\
                       '  check counter: ' + str(self.counter))
        #print status_str


#---------------------
