import sys
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
import cv2
import pika
import numpy as np
import time 
from DL import main

USERNAME='guest'
PASSWORD='guest'

EXCHANGE_NAME='e.R'
QUEUE_NAME='salam'

FRAME_PROCESS_HOP=200
#45-->10

def decoding_size(x):
    return x*8

class Signals(QWidget):
    one_frame = pyqtSignal(np.ndarray)

class Rbmq(QThread):
    def __init__(self,Signal,Channel):
        print("rbmq")
        super(Rbmq, self).__init__()
        self.signal=Signal
        self.channel = Channel
        #=============================================================
        #set perefetch
        #self.channel.basic_qos(prefetch_count=10)
        #=============================================================
        
        result=self.channel.queue_declare(queue=QUEUE_NAME, durable=False, exclusive=True,auto_delete=True)
        self.channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME,routing_key='')
        self.channel.basic_consume(queue=QUEUE_NAME,on_message_callback=
                      lambda ch, method, properties, body:
                          self.dispatch(
                              ch, method, properties, body,self.signal
                              ),
                           auto_ack=True
                        )
    def run(self):
        print("started")
        self.channel.start_consuming()

        
    def dispatch(self, channel, method, properties, body,Signal):
        frames=np.frombuffer(body,dtype=np.dtype('uint8'))
        frames=frames.reshape(decoding_size(frames[0]), decoding_size(frames[1]), 3)
        if not(frames[0][0][2]%FRAME_PROCESS_HOP):
            Signal.one_frame.emit(frames)

    def stop(self):
        self.channel.stop_consuming()
        self.channel.close()

class Process():
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        self.connect_to_server()
        sys.exit(app.exec_())
        
    def connect_to_server(self):
        self.credentials = pika.PlainCredentials(USERNAME, PASSWORD)
        self.parameters  = pika.ConnectionParameters('localhost',
                               5672,
                                '/',
                                self.credentials)
        self.channel=pika.BlockingConnection(self.parameters).channel()
        self.Signal=Signals()
        #init the rabbitmq
        self.rbmq=Rbmq(self.Signal,self.channel)
        self.net=main.init_model()
        self.Signal.one_frame.connect(self.process_the_frame)
        self.rbmq.start()
        
    def process_the_frame(self,frame):
        box , confidence = main.process(frame,self.net)
        print(confidence)
        
    


if __name__ == "__main__":
    Process()