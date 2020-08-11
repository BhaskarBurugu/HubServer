#!/usr/bin/python

import threading
from IPCamera import *

exitFlag = 0

class myCameraThread(threading.Thread):
   def __init__(self, CameraIP, timeout, VidAnal,preset):
      threading.Thread.__init__(self)
      self.CameraIP = CameraIP
      self.timeout = timeout
      self.VidAnal = VidAnal
      self.preset = preset

   def run(self):
       try:
            VideoStreamWidget(self.CameraIP,self.timeout,self.VidAnal,self.preset)
            print('Exit from Video play')
       except AttributeError:
           pass

def mainprog():
    # Create new threads
    i = 0
    #stream_link ='rtsp://admin:admin@192.168.1.23:554/cam/realmonitor?channel=1&subtype=0'
    while (i<2):
        if i == 1 :
            myCameraThread('0', 20, 1,'1').start()
            #thread1.start()
        else :
            myCameraThread('192.168.1.23', 40, 2,'1').start()
            #thread2.start()
    # thread2 = myThread(2, "Thread-2", 2)
        i = i + 1

#mainprog()