from PyQt5.QtCore import QThread
import time
import pika
import numpy as np
from multiprocessing import Queue
from PyQt5 import QtWidgets,QtGui
import sys
from DL import main
import os
import cv2
from ServerUI import Ui_MainWindow
from loginServerUI import Ui_MainWindow as login_Ui_MainWindow
import requests, json

# EXCHANGE_NAME=sys.argv[1]
# FRAME_HOP = int(sys.argv[2])

HOST="localhost"
PORT='15672'

EXCHANGE_NAME='e.R'

FRAME_HOP=200


def decoding_size(x):
    return x*8
def coding_size(x):
    return np.uint8((x[0]/8,x[1]/8))

def call_rabbitmq_api_validation(host, port, user, passwd):
  url = 'http://%s:%s/api/whoami' % (host, port)
  r = requests.get(url, auth=(user,passwd))
  return dict(r.json())

def create_exchange(host,port,user,passwd,exchange_name):
        # defining the api-endpoint
    API_ENDPOINT = f"http://{host}:{port}/api/exchanges/%2f/{exchange_name}"
    # your source code here
    headers = {'content-type': 'application/json'}
    # data to be sent to api
    pdata = {"type":"fanout",'durable': False,"auto_delete":False}
    # sending post request and saving response as response object
    r = requests.put(url = API_ENDPOINT ,auth=(user, passwd),
                      json = pdata,
                      headers=headers)
    try:
        r.json()
        return False
    except :
        return True
class Rbmq(QThread):
    def __init__(self,Channel,Queue,EXCHANGE_NAME,Frame_hop):
        super(Rbmq, self).__init__()
        self.channel = Channel        
        result=self.channel.queue_declare(queue=EXCHANGE_NAME+"_pr-"+str(int(time.time())), durable=False, exclusive=True)
        queue_name = result.method.queue        
        self.channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name,routing_key='')
        self.channel.basic_consume(queue=queue_name,on_message_callback=
                      lambda ch, method, properties, body:
                          self.dispatch(
                              ch, method, properties, body,Queue
                              ),
                           auto_ack=True
                        )
        self.frame_hop=Frame_hop
    def update_frame_hop(self,Frame_Hop):
        self.frame_hop=Frame_Hop
    def run(self):
        print("started")
        self.channel.start_consuming()

    def stop(self):
        self.channel.stop_consuming()
        self.channel.close()

    def dispatch(self, ch, method, properties, body,Queue):
        frames=np.frombuffer(body,dtype=np.dtype('uint8'))
        if not(frames[2]%self.frame_hop):
            frames=frames.reshape(decoding_size(frames[0]), decoding_size(frames[1]), 3)
            Queue.put(frames)
            

class Consumer(QThread):
    def __init__(self,Channel,queue,EXCHANGE_NAME):
        super(Consumer, self).__init__()
        self.channel = Channel       
        self.Queue=queue
        self.exchange_name=EXCHANGE_NAME
        self.net=main.init_model()
        
    def run(self):
        while(1):
            frame=self.Queue.get()
            box , confidence = main.process(frame,self.net)
            if confidence:
                self.channel.basic_publish(
                    exchange=self.exchange_name+'_pr',
                    routing_key='',
                    body=np.array(box).tobytes(),
                    properties=pika.BasicProperties(delivery_mode = 1)
                    )
            else:
                self.channel.basic_publish(
                        exchange=self.exchange_name+'_pr',
                        routing_key='',
                        body=np.array([0,0,0,0]).tobytes(),
                        properties=pika.BasicProperties(delivery_mode = 1)
                        )

class DataSender(QThread):
    def __init__(self,Channel,Exchange_name,FpsLimit):
        super(DataSender, self).__init__()
        self.channel=Channel
        self.exchange_name=Exchange_name
        self.fpsLimit=FpsLimit
    def update_fps_limit(self,new_fps):
        self.fpsLimit=new_fps
    def Send_data_to_server(self,file_name):
        startTime = time.time()
        cap = cv2.VideoCapture(f'./video/{file_name}')
        sequence_number=0
        
        while (cap.isOpened()):
            nowTime = time.time()
            if (nowTime - startTime) > self.fpsLimit:
                # do other cv2 stuff....
                startTime = time.time() # reset time
                # Capture frame-by-frame
                ret, frame = cap.read()
                if not ret:
                    print(f"Can't receive frame (stream end?). Exiting .{file_name}..")
                    break    
                else:
                    #set the dimention of each frame for converting inside reciever
                    frame[0][0][0],frame[0][0][1]=size_of_frame=coding_size(frame.shape).tobytes()
                    #set the packet numer of each frame for parsing inside reciever
                    frame[0][0][2]=sequence_number
                                
                    #send frame to rabbit mq to transmit it to client
                    self.channel.basic_publish(
                    exchange=self.exchange_name,
                    routing_key='',
                    body=frame.tobytes(),
                    properties=pika.BasicProperties(delivery_mode = 1)
                    )
                    #implements 
                    sequence_number+=1
                    if sequence_number==255:
                        sequence_number=0
            
        
         #close the channel of rabbitmq      
        cap.release()
        
    def run(self):
        while True:
            for item in os.listdir('./Video'):
                self.Send_data_to_server(item)



class RunDesignerGUI():
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.LoginWindow = QtWidgets.QMainWindow()
        #clientUI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        #LoginUI
        self.login_ui = login_Ui_MainWindow()
        self.login_ui.setupUi(self.LoginWindow)
        
        self.exchange_name=EXCHANGE_NAME
        self.fps_limit=1/self.ui.read_spinBox.value()
        self.frame_process_hop=self.ui.process_spinBox.value()
        self.widget_action()
        
        
        self.LoginWindow.show()
        self.MainWindow.hide()
        sys.exit(app.exec_())

    def widget_action(self):
        self.login_ui.login_Button.clicked.connect(self.loging_Button)
        self.ui.read_spinBox.valueChanged.connect(self.read_spinBox_update)
        self.ui.process_spinBox.valueChanged.connect(self.process_spinBox_update)
    def process_spinBox_update(self):
        newframehop=self.ui.process_spinBox.value()
        self.rbmq.update_frame_hop(newframehop)
    def read_spinBox_update(self):
        newfps=self.ui.read_spinBox.value()
        self.dataSender.update_fps_limit(1/newfps)

    def loging_Button(self):
        username=self.login_ui.Username_lineEdit.text()
        password=self.login_ui.Password_lineEdit.text()
        try:
            rabbit_authorization=call_rabbitmq_api_validation(HOST,PORT,username,password)
        except:
            self.send_log("rabbit is offline")
            rabbit_authorization={'error':'offline'}  
            
        if 'name' in rabbit_authorization:
            self.send_log("connection to server is ok")
            create_exchange(HOST,PORT,username,password,self.exchange_name)
            create_exchange(HOST,PORT,username,password,self.exchange_name+'_pr')
            self.MainWindow.show()
            self.LoginWindow.hide()
            self.prepare_conf()
        else:
            self.send_log(f"rabbit_authorization failed: error --> {rabbit_authorization['error']}")
        del rabbit_authorization

    def prepare_conf(self):
        username=self.login_ui.Username_lineEdit.text()
        password=self.login_ui.Password_lineEdit.text()
        
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(HOST,
                                           PORT[1:],
                                            '/',
                                            credentials)
        self.Channel_r=pika.BlockingConnection(parameters).channel()
        self.Channel_s=pika.BlockingConnection(parameters).channel()
        self.Channel_sender=pika.BlockingConnection(parameters).channel()
        
        self.dataSender=DataSender(self.Channel_sender,self.exchange_name,self.fps_limit)
        self.dataSender.start()
        
        self.Queue=Queue()
        self.rbmq=Rbmq(self.Channel_r,self.Queue,self.exchange_name,self.frame_process_hop)
        self.counsumer=Consumer(self.Channel_s,self.Queue,self.exchange_name)
        self.counsumer.start()
        self.rbmq.start()
    def send_log(self,txt):
        pre_txt=self.login_ui.LogtextBrowser.toPlainText()
        if (pre_txt==''):
            self.login_ui.LogtextBrowser.setText(txt)
        else:
            self.login_ui.LogtextBrowser.setText(pre_txt+'\n'+txt)


if __name__ == "__main__":
    RunDesignerGUI()   