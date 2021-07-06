import cv2 as cv

def init_model():
    # Load names of classes
    with open("./model/classes.names", 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')
    
    # Give the configuration and weight files for the model and load the network using them.
    net = cv.dnn.readNetFromDarknet("./model/darknet-yolov3.cfg", "./model/model.weights")
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

    return (net,classes)