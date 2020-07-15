from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,QTextEdit
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QRect
from PyQt5.QtCore import QThread, pyqtSignal
#import time
import socket
import selectors
import types


class MyThread(QThread):
    # Create a counter thread
    change_value = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.StopFlag = False

    def run(self):
        GUI_CONNECT = b'I am GUI'
        GUI_Client_Conn_Status = False
        GUI_IPAddr = ('127.0.0.1',5410) # dummy Values
        GUI_Port = 5410                 # Dummy Values

        sel = selectors.DefaultSelector()
        #host = '192.168.1.150'  # Standard loopback interface address (localhost)
        host = 'localhost'  # Standard loopback interface address (localhost)
        port = 6666  # Port to listen on (non-privileged ports are > 1023)
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((host, port))
        lsock.listen()
        self.change_value.emit('listening on : (' + str(host) + ' , '+ str(port) +')')
       # print('listening on', (host, port))
        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ, data=None)

        def accept_wrapper(sock):
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
          events = sel.select(timeout=1)
          #print(events)
          for key, mask in events:
              if key.data is None:
                  conn, addr1 = accept_wrapper(key.fileobj)
              else:
                  sock = key.fileobj
                  data = key.data
                  # data = service_connection(key, mask)
                  if mask & selectors.EVENT_READ:
                      recv_data = sock.recv(1024)  # Should be ready to read
                      if recv_data:
                          data.inb = recv_data
                          #print('type of recv_data is', data.inb)
                          self.change_value.emit('Received Data :'+ str(recv_data) +'\nData in Hex Format : '+ str(recv_data.hex()))
                          if(GUI_Client_Conn_Status == True) and (recv_data != GUI_CONNECT):
                              GUI_sock.send(recv_data)
                              self.change_value.emit('#####   Data Sent to GUI  ######\n')
                          else :
                              self.change_value.emit('######  GUI Link Down  #######\n')
                         # print(recv_data.hex())
                        #  self.change_value.emit('Received Data :'+ str(recv_data) +'\nData in Hex Format : '+ str(recv_data.hex()))
                          if (recv_data == GUI_CONNECT ):
                              if ((GUI_Client_Conn_Status == False) or (data.addr == GUI_IPAddr)):
                                  self.change_value.emit('Connected to GUI :' + str(data.addr))
                                  GUI_Client_Conn_Status = True
                                  GUI_IPAddr = data.addr
                                  GUI_sock = sock
                                 # GUI_Port = data.addr[1]
                                 # print(data.addr,GUI_IPAddr,GUI_Port)
                              else :
                                  self.change_value.emit('GUI Client Already Connected.\n Rejecting Connection Request from :' + str(data.addr))
                                  sel.unregister(sock)
                                  sock.close()
                          elif (recv_data[0] == 0xfa):
                              self.change_value.emit('Event Data')

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
       # lsock.shutdown()

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
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(iconName))
        self.setGeometry(left,  top, width, height)
        self.UiComponents()
        self.show()
      #  self.Text.append("Server Started")
        self.Server_Start()

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

    def Server_Start(self):
        self.Text.append("Server Started")
        self.button.setEnabled(False)
        self.button1.setEnabled(True)
       # self.Text.append("Server Started")
        self.thread = MyThread()
        self.thread.change_value.connect(self.setProgressVal)
        self.thread.StopFlag = False
        self.thread.start()

    def Server_Stop(self):
        self.thread.StopFlag = True
        self.button.setEnabled(True)
        self.button1.setEnabled(False)
        self.Text.append("Server Disconnected")
        #self.thread.exit()
       #self.ServerStopFlag = True

    def setProgressVal(self, val):
        self.Text.append(val)
       # print(val)

    def Clear(self):
        self.Text.clear()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())