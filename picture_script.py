import cv2

def picture(filename):
    camSet = 'nvarguscamerasrc wbmode=3 tnr-mode=2 tnr-strength=1 ee-mode=2 ee-strength=1 ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method=2 ! video/x-raw, width=1280, height=720, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.5 brightness=0.15 saturation=1.5 ! appsink'
    camera = cv2.VideoCapture(camSet)
    r, img = camera.read()
    if r is not True:
        return 'Failed to read image'
    rw = cv2.imwrite(filename, img)
    if rw is not True:
        return 'Failed to write image'
    return True
