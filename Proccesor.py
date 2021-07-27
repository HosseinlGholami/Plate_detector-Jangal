import concurrent.futures
import logging
import queue
import threading
import time
import pika
import numpy as np

EXCHANGE_NAME='e.R'
FRAME_PROCESS_HOP=200

def dispatch(channel, method, properties, body,frame_process_hop,queue):
        frames=np.frombuffer(body,dtype=np.dtype('uint8'))
        frames=frames.reshape(decoding_size(frames[0]), decoding_size(frames[1]), 3)
        if not(frames[0][0][2]%200):
            print('salam')
            queue.put(frames)
            
def producer(queue,channel):
    result=channel.queue_declare(queue=EXCHANGE_NAME+str(int(time.time())), durable=False, exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name,routing_key='')
    channel.basic_consume(queue=queue_name,on_message_callback=
                  lambda ch, method, properties, body:
                      dispatch(
                          ch, method, properties, body,FRAME_PROCESS_HOP,queue
                          ),
                       auto_ack=True
                    )
    channel.start_consuming()
    
def consumer(queue,channel):
    while(1):
        if not queue.empty():
            print('salam')
            message = queue.get()
            #send to processor
            frame=message
            #send procced data to server again
            channel.basic_publish(
                        exchange=EXCHANGE_NAME+'_pr',
                        routing_key='',
                        body=frame.tobytes(),
                        properties=pika.BasicProperties(delivery_mode = 1)
                        )
        
if __name__ == "__main__":
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost',
                                           5672,
                                            '/',
                                            credentials)
    channel=pika.BlockingConnection(parameters).channel()
    pipeline = queue.Queue(maxsize=10)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, channel)
        executor.submit(consumer, pipeline, channel)
