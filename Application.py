import sys
from ClientUI import Ui_MainWindow
import requests, json
from PyQt5.QtCore import QProcess
import pika
import Util
import cv2
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

EXCHANGE_NAME='e.R'
fps_sender_limit='0.03'
USERNAME='guest'
PASSWORD='guest'
DEFAULT_FRAME_PROCESS_HOP=200

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
        self.connection=pika.BlockingConnection(self.parameters)
        self.channel=self.connection.channel()
        self.Signal= Util.Signals()
        self.rbmq= Util.Rbmq(self.Signal,self.channel,EXCHANGE_NAME,DEFAULT_FRAME_PROCESS_HOP)
        self.Signal.one_frame.connect(self.update_image)
        self.rbmq.start()
    
    def start_sending_data_to_server(self):
        self.Send_process=QProcess()
        self.Send_process.finished.connect(self.finish_process)
        self.Send_process.start("python",["VideoSenderToServerFromFile.py",EXCHANGE_NAME,fps_sender_limit])
    def finish_process(self,  exitCode,  exitStatus):
        print('Sender Application has die')

    def close_GUI(self):
        self.MainWindow.close()
    def update_widgets(self):
        self.MainWindow.setWindowTitle("JANGAL-Plate detector")

    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.Video_label.setPixmap(qt_img)
        
        
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.ui.Video_label.width(), self.ui.Video_label.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

if __name__ == "__main__":
    RunDesignerGUI()    