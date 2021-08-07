import sys
from ClientUI import Ui_MainWindow
from loginClientUI import Ui_MainWindow as login_Ui_MainWindow
import requests, json
from PyQt5.QtCore import QProcess
import pika
import Util
from Util import decoding_size
import cv2
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import numpy as np
import time

EXCHANGE_NAME='e.R'
fps_sender_limit=f'{1/5}'
USERNAME='guest'
PASSWORD='guest'
DEFAULT_FRAME_PROCESS_HOP='20'

def call_rabbitmq_api_validation(host, port, user, passwd):
  url = 'http://%s:%s/api/whoami' % (host, port)
  r = requests.get(url, auth=(user,passwd))
  return dict(r.json())
def get_active_exchange(host,port,user,passwd):    
    GET_VHOST = f"http://{host}:{port}/api/definitions"
    r = requests.get(url = GET_VHOST ,auth=(user, passwd),)
    return [ex['name'] for ex in dict(r.json())['exchanges']]

def Perspective_Transformation(img,pts1,x,y):
    pts2 = np.float32([[0,0],[x,0],[0,y],[x,y]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    return cv2.warpPerspective(img,M,(x,y))

class RunDesignerGUI():
    def __init__(self):
        self.process=list()
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.LoginWindow = QtWidgets.QMainWindow()
        #clientUI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        #LoginUI
        self.login_ui = login_Ui_MainWindow()
        self.login_ui.setupUi(self.LoginWindow)
        
        self.widget_action()
        
        # self.start_sending_data_to_server()   

        self.update_widgets()
        self.LoginWindow.show()
        self.MainWindow.hide()
        sys.exit(app.exec_())

 
    def widget_action(self):
        self.login_ui.login_Button.clicked.connect(self.login_Button)
        self.ui.disconButton.clicked.connect(self.disconnect_func)
    
    def login_Button(self):
        Serverip=self.login_ui.Serverip_lineEdit.text()
        Serverport=self.login_ui.Serverport_lineEdit.text()
        username=self.login_ui.Username_lineEdit.text()
        password=self.login_ui.Password_lineEdit.text()
    
        try:
            rabbit_authorization=call_rabbitmq_api_validation(Serverip,Serverport,username,password)
        except:
            self.send_log("rabbit is offline")
            rabbit_authorization={'error':'offline'}        
        if 'name' in rabbit_authorization:
            self.send_log("connection to server is ok")
            exchange_list=get_active_exchange(Serverip,Serverport,username,password)
            if EXCHANGE_NAME in exchange_list:
                self.send_log("client can connect to server")
                self.MainWindow.show()
                self.LoginWindow.hide()
                self.control_server_and_signals()
            else:
                self.send_log("client cant connect to server since server application does no runs")
            
        else:
            self.send_log(f"rabbit_authorization failed: error --> {rabbit_authorization['error']}")
        del rabbit_authorization

            
    def disconnect_func(self):
        self.MainWindow.hide()
        self.LoginWindow.show()
        
        
    def control_server_and_signals(self):
        Serverip=self.login_ui.Serverip_lineEdit.text()
        Serverport=self.login_ui.Serverport_lineEdit.text()
        username=self.login_ui.Username_lineEdit.text()
        password=self.login_ui.Password_lineEdit.text()
        
        self.credentials = pika.PlainCredentials(username, password)
        self.parameters  = pika.ConnectionParameters(Serverip,
                                       Serverport[1:],
                                        '/',
                                        self.credentials)
        
        self.channel1=pika.BlockingConnection(self.parameters).channel()
        self.channel2=pika.BlockingConnection(self.parameters).channel()
        self.Signal= Util.Signals()
        self.rbmq1= Util.Rbmq(self.Signal,self.channel1,EXCHANGE_NAME,self.dispatch1)
        self.rbmq2= Util.Rbmq(self.Signal,self.channel2,EXCHANGE_NAME+'_pr',self.dispatch2)
        self.Signal.one_frame.connect(self.update_image)
        self.Signal.one_data.connect(self.update_plate)
        self.rbmq1.start()
        self.rbmq2.start()
        
    def dispatch1(self, channel, method, properties, body,Signal,exchange_name):
        frames=np.frombuffer(body,dtype=np.dtype('uint8'))
        frames=frames.reshape(decoding_size(frames[0]), decoding_size(frames[1]), 3)
        Signal.one_frame.emit(frames)
    def dispatch2(self, channel, method, properties, body,Signal,exchange_name):
        position=np.frombuffer(body,dtype=np.dtype('uint32'))
        Signal.one_data.emit(position)
        
        
    # def start_sending_data_to_server(self):
    #     self.Send_process=QProcess()
    #     self.Send_process.finished.connect(self.finish_process_sender)
    #     self.Send_process.start("python",["VideoSenderToServerFromFile.py",EXCHANGE_NAME,fps_sender_limit])
    #     self.process_process=QProcess()
    #     self.process_process.finished.connect(self.finish_process_processor)
    #     self.process_process.start("python",["proccesor.py",EXCHANGE_NAME,DEFAULT_FRAME_PROCESS_HOP])
    
    def finish_process_sender(self,  exitCode,  exitStatus):
        print('Sender Application has die')
        del self.Send_process
    def finish_process_processor(self,  exitCode,  exitStatus):
        print('process Application has die')
        del self.process_process
        
    def close_GUI(self):
        self.MainWindow.close()
    def update_widgets(self):
        self.MainWindow.setWindowTitle("JANGAL-Plate detector")

    def update_plate(self, position):
        left, top, width, height=position
        pts1 = np.float32([[left,top],[left+width,top],[left,top+height],[left+width,top+height]])
        plate_box=Perspective_Transformation(self.CV_img, pts1=pts1, x=self.ui.PlateLabel.width(),y=self.ui.PlateLabel.height())
        qt_img = self.convert_cv_qt(plate_box,self.ui.PlateLabel)
        self.ui.PlateLabel.setPixmap(qt_img)
        
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        self.CV_img=cv_img
        qt_img = self.convert_cv_qt(self.CV_img,self.ui.Video_label)
        self.ui.Video_label.setPixmap(qt_img)
        
        
    def convert_cv_qt(self, cv_img,label_obj):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(label_obj.width(), label_obj.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    def send_log(self,txt):
        pre_txt=self.login_ui.LogtextBrowser.toPlainText()
        if (pre_txt==''):
            self.login_ui.LogtextBrowser.setText(txt)
        else:
            self.login_ui.LogtextBrowser.setText(pre_txt+'\n'+txt)
if __name__ == "__main__":
    RunDesignerGUI()    