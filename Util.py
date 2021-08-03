from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
import numpy as np
import time

def decoding_size(x):
    return x*8

class Signals(QWidget):
    one_frame = pyqtSignal(np.ndarray)
    one_data  = pyqtSignal(np.ndarray)
    
class Rbmq(QThread):
    def __init__(self,Signal,Channel,EXCHANGE_NAME,Dispatch):
        print("rbmq")
        super(Rbmq, self).__init__()
        self.signal=Signal
        self.channel = Channel
        self.dispatch=Dispatch
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
                              ch, method, properties, body,self.signal,EXCHANGE_NAME
                              ),
                           auto_ack=True
                        )
    def run(self):
        print("started")
        self.channel.start_consuming()

                        

    def stop(self):
        self.channel.stop_consuming()
        self.channel.close()
