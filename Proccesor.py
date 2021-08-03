from PyQt5.QtCore import QThread
import time
import pika
import numpy as np
from multiprocessing import Queue
from PyQt5 import QtWidgets,QtGui
import sys
from DL import main

EXCHANGE_NAME=sys.argv[1]
FRAME_HOP = int(sys.argv[2])

# EXCHANGE_NAME='e.R'
# FRAME_HOP=200

def decoding_size(x):
    return x*8

class Rbmq(QThread):
    def __init__(self,Channel,Queue,EXCHANGE_NAME,frame_hop):
        super(Rbmq, self).__init__()
        self.channel = Channel        
        result=self.channel.queue_declare(queue=EXCHANGE_NAME+"_pr-"+str(int(time.time())), durable=False, exclusive=True)
        queue_name = result.method.queue        
        self.channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name,routing_key='')
        self.channel.basic_consume(queue=queue_name,on_message_callback=
                      lambda ch, method, properties, body:
                          self.dispatch(
                              ch, method, properties, body,frame_hop,Queue
                              ),
                           auto_ack=True
                        )
    def run(self):
        print("started")
        self.channel.start_consuming()

    def stop(self):
        self.channel.stop_consuming()
        self.channel.close()

    def dispatch(self, ch, method, properties, body,frame_hop,Queue):
        frames=np.frombuffer(body,dtype=np.dtype('uint8'))
        if not(frames[2]%frame_hop):
            frames=frames.reshape(decoding_size(frames[0]), decoding_size(frames[1]), 3)
            print('*')
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
                if confidence>0.85:
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



class RunDesignerGUI():
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        self.prepare_conf()
        sys.exit(app.exec_())

    def prepare_conf(self):
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('localhost',
                                           5672,
                                            '/',
                                            credentials)
        self.Channel_r=pika.BlockingConnection(parameters).channel()
        self.Channel_s=pika.BlockingConnection(parameters).channel()
        self.Queue=Queue()
        self.rbmq=Rbmq(self.Channel_r,self.Queue,EXCHANGE_NAME,FRAME_HOP)
        self.counsumer=Consumer(self.Channel_s,self.Queue,EXCHANGE_NAME)
        self.counsumer.start()
        self.rbmq.start()


if __name__ == "__main__":
    RunDesignerGUI()   