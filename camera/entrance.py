import time
import cv2
import urllib
import pyupm_grove as grove
import pyupm_ttp223 as ttp223

CAMERA_IP_ADDRESS = '10.43.4.35'
img_retriever = urllib.URLopener()

def read_plate(img):
    return str(img)


def take_photo():
    img_retriever.retrieve('http://' + CAMERA_IP_ADDRESS + ':8080/shot.jpg', 'shot.jpg')
    img = cv2.imread('shot.jpg')
    return img


def get_plate():
    img = take_photo()
    if img is None:
        print "Photo not taken"
    return read_plate(img)


def main():
    button = grove.GroveButton(4)
    while 1:
        if button.value() == 1:
            print "Pressed"
            print get_plate()
            time.sleep(0.5)

if __name__ == '__main__':
    main()
