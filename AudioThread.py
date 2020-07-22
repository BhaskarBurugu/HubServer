#!/usr/bin/python

import threading
import pyttsx3

########################################################################################################################
class myAudioThread(threading.Thread):
   def __init__(self, text, Vol_level = 0.8):
       threading.Thread.__init__(self)
       self.text = text
       self.Vol_level = Vol_level

########################################################################################################################
   def run(self):
    #  print ("Starting " + self.name)
    #  print_time(self.name, 5, self.counter)
    #  print("Exiting " + self.name)
    try:
        self.engine = pyttsx3.init()
       # rate = self.engine.getProperty('rate')  # getting details of current speaking rate
        # print (rate)                        #printing current voice rate
        rate = 150
        self.engine.setProperty('rate', rate)  # setting up new voice rate
      #  volume = self.engine.getProperty('volume')  # getting to know current volume level (min=0 and max=1)
        # print (volume)                          #printing current volume level
      #  self.engine.setProperty('volume', self.Vol_level)  # setting up volume level  between 0 and 1
      #  voices = self.engine.getProperty('voices')  # getting details of current voice
       # self.engine.setProperty('voice', voices[0].id)  # changing index, changes voices. o for male
        #   print('i am here')
        self.engine.say(self.text)
        self.engine.runAndWait()
    except AttributeError:
        pass
 #   print('Exit')

########################################################################################################################
#myAudioThread('hai Bhaskar').start()
