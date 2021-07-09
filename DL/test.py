import cv2 as cv


X='A.jpg'
cap = cv.VideoCapture(X)

_,frame1 = cap.read()

# if frame1 == frame2:
#     print("salam")