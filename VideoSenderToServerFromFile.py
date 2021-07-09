import cv2
import pika
import numpy as np
import os
import time

EXCHANGE_NAME='e.R'

def coding_size(x):
    return np.uint8((x[0]/8,x[1]/8))

def Send_data_to_server(file_name):
    fpsLimit = 0.03333 # throttle limit
    startTime = time.time()
    cap = cv2.VideoCapture(f'./video/{file_name}')
    #Connect to Server
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost',
                                           5672,
                                            '/',
                                            credentials)
    channel=pika.BlockingConnection(parameters).channel()
    
    sequence_number=0
    # Check if camera opened successfully
    if (cap.isOpened()== False):
      print("Error opening video stream or file")
     
    # Read until video is completed
    while (cap.isOpened()):
        nowTime = time.time()
        if (nowTime - startTime) > fpsLimit:
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
                channel.basic_publish(
                exchange=EXCHANGE_NAME,
                routing_key='',
                body=frame.tobytes(),
                properties=pika.BasicProperties(delivery_mode = 1)
                )
                #implements 
                sequence_number+=1
                if sequence_number==255:
                    sequence_number=0
        
    #TODO:
    channel.close()
    #close the channel of rabbitmq      
    cap.release()
    cv2.destroyAllWindows()


while True:
    for item in os.listdir('./Video'):
        Send_data_to_server(item)
