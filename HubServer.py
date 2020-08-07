#######################################################################################################################
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,QTextEdit
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QRect
from PyQt5.QtCore import QThread, pyqtSignal
#import time
import socket
import selectors
import types
import json
import pandas as pd
from CameraThread import *
from AudioThread import *
#import math
#######################################################################################################################
HEADER_INDEX  = 0
CHANNEL_INDEX = 1
IPADDR_INDEX  = 2
RTID_INDEX    = 6
VIBFRQ_INDEX  = 8
VIBMAG_INDEX  = 10
TEMP_INDEX    = 14
MAGN_INDEX    = 17
#######################################################################################################################
#try :
#    pd_HubConfig = pd.read_csv('HubConfigInfo.csv')
#except :
#    print('HubConfigInfo.csv file missing')
#    exit(1)
try:
    pd_SensConfig = pd.read_csv('SensorConfigInfo.csv')
    pd_SensConfig['HUB ID'] = pd_SensConfig['HUB ID'].fillna('NO IP')
    pd_SensConfig['Camera IP'] = pd_SensConfig['Camera IP'].fillna('NO IP')
    pd_SensConfig['Channel'] = pd_SensConfig['Channel'].fillna(0)
    pd_SensConfig['RT No'] = pd_SensConfig['RT No'].fillna(0)
    pd_SensConfig['Preset'] = pd_SensConfig['Preset'].fillna(0)
except :
    print('SensorConfigInfo.csv file missing')
    exit(1)
try :
    with open('HubCat.JSON') as f:
        data = json.load(f)
    # Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
    #print(type(data))
    print(data)
    Hubcategory = data["HubCat"]
    #pd_SensConfig = pd.read_csv('SensorConfigInfo.csv')
except :
    print('HubCat.JSON file missing')
    exit(1)
#######################################################################################################################
def ExtractJSONData(data):
    #print(data)
    Event = json.loads(data)
    print(Event)
    try :
        print(Event["sensorid"])
    except :
        return 1
    Event_Validity = True
    try:
        CameraIP = pd_SensConfig.loc[(pd_SensConfig['Channel'] == int(Event["channel"])) &
                                 (pd_SensConfig['RT No'] == int(Event["sensorid"])) & (
                                         pd_SensConfig['HUB ID'] == Event["hubip"]), 'Camera IP'].values[0]
        print(CameraIP)
    except:
        CameraIP = 'NAN'
        Event_Validity = False
        #print('Except', CameraIP)
    # print(pd_SensConfig)
    if(Event_Validity == False):
        myAudioThread('Invalid Event').start()
        return
    if (Event["events"]["temperature"] >= '60'):  # 229 equivalent to 60Deg
        myAudioThread(Event["events"]["type"] + 'event detected').start()
        if (CameraIP != 'NO IP'):
            print('Call Camera popup here', CameraIP)
            myCameraThread(CameraIP=CameraIP, timeout=40, VidAnal=1).start()
        else:
            print('Not Valid IP')

    elif (Event["events"]["type"] == "MAGNETIC"):
        myAudioThread(Event["events"]["type"] + 'event detected').start()

    elif (Event["events"]["vibrationcount"] > '5') :
        myAudioThread(Event["events"]["type"] + 'event detected').start()
        if (CameraIP != 'NO IP'):
            print('Call Camera popup here', CameraIP)
            myCameraThread(CameraIP=CameraIP, timeout=40, VidAnal='Normal').start()
        else:
            print('Not Valid IP')
    return 5
########################################################################################################################
#######################################################################################################################
def Extract_Engg_Values(data):
    Event = {
        "sensorid": "5",
        "hubip": "192.168.1.100",
        "channel": "0",
        "events":
            {
                "type": "VIBRATION",
                "vibrationcount": "10",
                "temperature": "60"
            }
    }

    EventStatus = False
    if (len(data) >= 22):
        EventStatus = True
        HubIP = str(data[IPADDR_INDEX]) + '.' + str(data[IPADDR_INDEX + 1]) + '.' + str(
            data[IPADDR_INDEX + 2]) + '.' + str(data[IPADDR_INDEX + 3])
        RT_ID = ((data[RTID_INDEX] & 0x0f) << 4) + (data[RTID_INDEX + 1] & 0x0f)
        VibFreq = ((data[VIBFRQ_INDEX] & 0x0f) << 4) + (data[VIBFRQ_INDEX + 1] & 0x0f)
        VibMag = ((data[VIBMAG_INDEX] & 0x0f) << 12) + ((data[VIBMAG_INDEX + 1] & 0x0f) << 8) + (
                    (data[VIBMAG_INDEX + 2] & 0x0f) << 4) + (data[VIBMAG_INDEX + 3] & 0x0f)
        Temp = ((data[TEMP_INDEX] & 0x0f) << 8) + ((data[TEMP_INDEX + 1] & 0x0f) << 4) + (data[TEMP_INDEX + 2] & 0x0f)
        Magn = True if (data[MAGN_INDEX] & 0x0f) == 0x0f else False
        #  RT_ID      = int(4)
        # print(HubIP)
        # print(type(HubIP))
        Event['hubip'] = HubIP
        Event["channel"] = str(data[1])
        Event["sensorid"] = str(RT_ID)

        try:
            CameraIP = pd_SensConfig.loc[(pd_SensConfig['Channel'] == int(Event["channel"])) &
                                         (pd_SensConfig['RT No'] == int(RT_ID)) & (
                                                     pd_SensConfig['HUB ID'] == HubIP), 'Camera IP'].values[0]
        except:
            CameraIP = float('nan')
        # print(pd_SensConfig)

        if (Temp < 229):  # 229 equivalent to 60Deg
            Event["events"]["type"] = "TEMPERATURE"
            Event["events"]["vibrationcount"] = str(VibFreq)
            Event["events"]["temperature"] = str(Temp)
            myAudioThread(Event["events"]["type"] + 'event detected').start()
            if (CameraIP != 'NO IP'):
                print('Call Camera popup here', CameraIP)
                myCameraThread(CameraIP=CameraIP, timeout=40, VidAnal=1).start()
            else:
                print('Not Valid IP')

        elif (Magn == True):
            Event["events"]["type"] = "MAGNETIC"
            myAudioThread(Event["events"]["type"] + 'event detected').start()

        elif (VibFreq > 3) and (VibMag > 5000):
            Event["events"]["type"] = "VIBRATION"
            Event["events"]["vibrationcount"] = str(VibFreq)
            Event["events"]["temperature"] = '30'#str(Temp)
            myAudioThread(Event["events"]["type"] + 'event detected').start()
            if (CameraIP != 'NO IP'):
                print('Call Camera popup here', CameraIP)
                myCameraThread(CameraIP=CameraIP,timeout=40,VidAnal='Normal').start()
            else:
                print('Not Valid IP')
        else:
            EventStatus = False

        EventJSON = json.dumps(Event)

    return EventStatus, EventJSON
########################################################################################################################
#######################################################################################################################
#Received Data :b'{"sensorid":"5","hubip":"192.168.1.100","channel":"0","events":{"type":"VIBRATION","vibrationcount":"10","temperature":"60"}}'
#Received Data :b'{"sensorid":"15","hubip":"192.168.1.100","channel":"0","events":{"type":"MAGNETIC","vibrationcount":"10","temperature":"60"}}'

class MyThread(QThread):
    # Create a counter thread
    change_value = pyqtSignal(str)
    ####################################################################################################################
    ####################################################################################################################
    def __init__(self):
        super().__init__()
        self.StopFlag = False
    ####################################################################################################################
    ####################################################################################################################
    def run(self):
        GUI_CONNECT = b'I am GUI'
        GUI_Client_Conn_Status = False
        GUI_IPAddr = ('127.0.0.1',5410) # dummy Values
        GUI_Port = 5410                 # Dummy Values

        sel = selectors.DefaultSelector()
        host = '192.168.1.150'  # Standard loopback interface address (localhost)
        #host = 'DESKTOP-E9LCLCN'  # Standard loopback interface address (localhost)
        port = 5555  # Port to listen on (non-privileged ports are > 1023)
       # host = socket.gethostname()
        #IPAddr = socket.gethostbyname(host)
        IPAddr = "192.168.1.150"
        self.change_value.emit("Your Computer Name is:" + host)
        self.change_value.emit("Your Computer IP Address is:" + IPAddr)

        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.settimeout(1)
        lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        lsock.bind((IPAddr, port))
        lsock.listen()
        self.change_value.emit('listening on : (' + str(IPAddr) + ' , '+ str(port) +')')
       # print('listening on', (host, port))
        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ | selectors.EVENT_WRITE, data=None)

        ################################################################################################################
        ################################################################################################################
        def accept_wrapper(sock):
           # print('trying for connection')
            conn, addr = sock.accept()  # Should be ready to read
            self.change_value.emit('accepted connection from :'+ str(addr))
            #print('accepted connection from', addr)
            conn.setblocking(False)
            data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            sel.register(conn, events, data=data)
            return conn, addr

        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        cnt = 0
        #while cnt < 100:
        while self.StopFlag == False :
          #  cnt+=1
          #  time.sleep(1)
           # self.change_value.emit(cnt)
          try :
            print(cnt)
            events = sel.select(timeout=1)
            print(cnt)
            cnt = (cnt + 1) % 99999
          except :
              print("error")
          #print(events)
          print(cnt)
          for key, mask in events:
              if key.data is None:
                  #print(key.fileobj)
                  conn, addr1 = accept_wrapper(key.fileobj)
              #    print(conn,addr1)
              else:
                  sock = key.fileobj
                  data = key.data
                  # data = service_connection(key, mask)
                  if mask & selectors.EVENT_READ:
                      recv_data = sock.recv(1024)  # Should be ready to read
                      if recv_data:
                          data.inb = recv_data
                          if (GUI_Client_Conn_Status == True) and (recv_data != GUI_CONNECT):
                              if(Hubcategory == 'SBC'):
                                  GUI_sock.send(recv_data)
                                  ExtractJSONData(recv_data)
                                  self.change_value.emit('#####  JSON String is  ######\n' + str(recv_data))
                                  #self.change_value.emit(recv_data)
                              elif(Hubcategory == 'FPGA'):
                                if (recv_data[0] == 0xfa):
                                  EventStatus, Event = Extract_Engg_Values(recv_data)
                                  if EventStatus == True :
                                     # GUI_sock.send(recv_data)
                                     GUI_sock.send(bytes(Event,encoding="utf-8"))
                                     self.change_value.emit('#####  JSON String is  ######\n'+ Event)
                                  else :
                                      self.change_value.emit('#####   Invalid Event  ######\n')
                          else:
                              self.change_value.emit('######  GUI Link Down  #######\n')
                          # print(recv_data.hex())
                        #  self.change_value.emit('Received Data :'+ str(recv_data) +'\nData in Hex Format : '+ str(recv_data.hex()))
                          if (recv_data == GUI_CONNECT ):
                              if ((GUI_Client_Conn_Status == False) or (data.addr == GUI_IPAddr)):
                                  self.change_value.emit('Connected to GUI :' + str(data.addr))
                                  self.change_value.emit('######  GUI Link Up  #######\n')
                                  GUI_Client_Conn_Status = True
                                  GUI_IPAddr = data.addr
                                  GUI_sock = sock
                                 # GUI_Port = data.addr[1]
                                 # print(data.addr,GUI_IPAddr,GUI_Port)
                              else :
                                  self.change_value.emit('GUI Client Already Connected.\nRejecting Connection Request from :' + str(data.addr))
                                  sel.unregister(sock)
                                  sock.close()
                      else:
                          self.change_value.emit('closing connection to :' + str(data.addr))
                         # print('GUI',GUI_IPAddr,GUI_Port)
                          #print('closing connection to', data.addr)
                          if (data.addr == GUI_IPAddr) :
                              GUI_Client_Conn_Status = False
                              self.change_value.emit('GUI_Client Closed' )
                          sel.unregister(sock)
                          sock.close()
        #('closing Socket')
        sel.unregister(lsock)
        lsock.close()
########################################################################################################################
########################################################################################################################
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        title = "Multi-Vibration Sensor Server"
        left = 500
        top = 300
        width = 800
        height = 600
        iconName = "icon.png"
        self.ServerStopFlag = False
        self.ClearDispCount = 0
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(iconName))
        self.setGeometry(left,  top, width, height)
        self.UiComponents()
        self.show()
      #  self.Text.append("Server Started")
        self.Server_Start()
    ###################################################################################################################
    def UiComponents(self):
        self.Text = QTextEdit(self)
        self.Text.move(0, 0)
        self.Text.resize(800, 500)
        self.button = QPushButton("Start Server", self)
        self.button.move(150,150)
        self.button.setGeometry(QRect(50,525,200,40))
        self.button1 = QPushButton("Stop Server",self)
        self.button1.move(40,40)
        self.button1.setGeometry(QRect(280,525,200,40))
        self.button2 = QPushButton("Clear",self)
        self.button2.move(50,50)
        self.button2.setGeometry(QRect(510,525,200,40))
        self.button.clicked.connect(self.Server_Start)
        self.button1.clicked.connect(self.Server_Stop)
        self.button2.clicked.connect(self.Clear)
        self.button.setEnabled(False)
    ###################################################################################################################
    def Server_Start(self):
        self.Text.append("Server Started")
        self.button.setEnabled(False)
        self.button1.setEnabled(True)
       # self.Text.append("Server Started")
        self.thread = MyThread()
        self.thread.change_value.connect(self.setProgressVal)
        self.thread.StopFlag = False
        self.thread.start()
    ###################################################################################################################
    def Server_Stop(self):
        self.thread.StopFlag = True
        self.button.setEnabled(True)
        self.button1.setEnabled(False)
        self.Text.append("Server Disconnected")
        #self.thread.exit()
       #self.ServerStopFlag = True
    ###################################################################################################################
    def setProgressVal(self, val):
        if(self.ClearDispCount >10):
            self.ClearDispCount = 0
            self.Text.clear()
            self.Text.setText(val)
        else:
            self.Text.append(val)
        self.ClearDispCount = self.ClearDispCount + 1
        #self.Text.setText(val)
       # print(val)
    ###################################################################################################################
    def Clear(self):
        self.Text.clear()

#######################################################################################################################
#######################################################################################################################
if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    try:
        sys.exit(App.exec())
    except:
        print("ERRRRR")