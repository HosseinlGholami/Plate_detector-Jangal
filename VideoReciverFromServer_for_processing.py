import sys
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
import cv2
import pika
import numpy as np
import time 


USERNAME='guest'
PASSWORD='guest'

def decoding_size(x):
    return x*8

class Rbmq(QThread):
    def __init__(self,Channel):
        super(Rbmq, self).__init__()
        self.channel = Channel
        #=============================================================
        #set perefetch
        #self.channel.basic_qos(prefetch_count=10)
        #=============================================================
        
        result=self.channel.queue_declare(queue='salam', durable=False, exclusive=True,auto_delete=True)
        self.channel.queue_bind(exchange='e.R', queue='salam',routing_key='')
        self.channel.basic_consume(queue='salam',
                      on_message_callback=
                      lambda ch, method, properties, body:
                          self.dispatch(
                              ch, method, properties, body,None
                              ),
                          consumer_tag="ct_test",
                           auto_ack=True
                        )
        self.channel.start_consuming()
        print('Waiting for message')
        
    def dispatch(self, channel, method, properties, body,Signal):
        frames=np.frombuffer(body,dtype=np.dtype('uint8'))
        frames=frames.reshape(decoding_size(frames[0]), decoding_size(frames[1]), 3)
        print(frames[0][0][2])
        # channel.basic_ack(delivery_tag = method.delivery_tag)

    def stop(self):
        channel.stop_consuming("ct_test")


credentials = pika.PlainCredentials(USERNAME, PASSWORD)
parameters  = pika.ConnectionParameters('localhost',
                               5672,
                                '/',
                                credentials)
connection=pika.BlockingConnection(parameters)
channel=connection.channel()



#init the rabbitmq
rbmq=Rbmq(channel)


