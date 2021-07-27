from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
import numpy as np
import time

def decoding_size(x):
    return x*8

class Signals(QWidget):
    one_frame = pyqtSignal(np.ndarray)

class Rbmq(QThread):
    def __init__(self,Signal,Channel,EXCHANGE_NAME,FRAME_PROCESS_HOP):
        print("rbmq")
        super(Rbmq, self).__init__()
        self.signal=Signal
        self.channel = Channel
        #=============================================================
        #set perefetch
        #self.channel.basic_qos(prefetch_count=10)
        #=============================================================
        result=self.channel.queue_declare(queue=EXCHANGE_NAME+str(int(time.time())), durable=False, exclusive=True)
        queue_name = result.method.queue
        
        self.channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name,routing_key='')
        self.channel.basic_consume(queue=queue_name,on_message_callback=
                      lambda ch, method, properties, body:
                          self.dispatch(
                              ch, method, properties, body,self.signal,FRAME_PROCESS_HOP,EXCHANGE_NAME
                              ),
                           auto_ack=True
                        )
    def run(self):
        print("started")
        self.channel.start_consuming()

        
    def dispatch(self, channel, method, properties, body,Signal,frame_process_hop,exchange_name):
        frames=np.frombuffer(body,dtype=np.dtype('uint8'))
        frames=frames.reshape(decoding_size(frames[0]), decoding_size(frames[1]), 3)
        Signal.one_frame.emit(frames)
        if not(frames[0][0][2]%frame_process_hop):
            channel.basic_publish(
                exchange=exchange_name+'_pr',
                routing_key='',
                body=body,
                properties=pika.BasicProperties(delivery_mode = 1)
                )
                

    def stop(self):
        self.channel.stop_consuming()
        self.channel.close()
