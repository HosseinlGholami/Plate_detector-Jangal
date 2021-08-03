import sys
from ClientUI import Ui_MainWindow
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

EXCHANGE_NAME='e.R'
fps_sender_limit=f'{1/5}'
USERNAME='guest'
PASSWORD='guest'
DEFAULT_FRAME_PROCESS_HOP='100'

def Perspective_Transformation(img,pts1,x,y):
    pts2 = np.float32([[0,0],[x,0],[0,y],[x,y]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    return cv2.warpPerspective(img,M,(x,y))

class RunDesignerGUI():
    def __init__(self):
        self.process=list()
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        
        self.widget_action()
        self.start_sending_data_to_server()   
        self.control_server_and_signals()
        self.update_widgets()

        self.MainWindow.show()
        sys.exit(app.exec_())

 
    def widget_action(self):
        pass
    
    def control_server_and_signals(self):
        self.credentials = pika.PlainCredentials(USERNAME, PASSWORD)
        self.parameters  = pika.ConnectionParameters('localhost',
                                       5672,
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
        
        
    def start_sending_data_to_server(self):
        self.Send_process=QProcess()
        self.Send_process.finished.connect(self.finish_process_sender)
        self.Send_process.start("python",["VideoSenderToServerFromFile.py",EXCHANGE_NAME,fps_sender_limit])
        self.process_process=QProcess()
        self.process_process.finished.connect(self.finish_process_processor)
        self.process_process.start("python",["proccesor.py",EXCHANGE_NAME,DEFAULT_FRAME_PROCESS_HOP])
    
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

if __name__ == "__main__":
    RunDesignerGUI()    