import subprocess
import urllib
import time

import pyupm_i2clcd as lcd
LCD = lcd.Jhd1313m1(0, 0x3E, 0x62)

CAMERA_IP_ADDRESS = '10.43.4.35'
img_retriever = urllib.URLopener()


def main():
    img_retriever.retrieve('http://' + CAMERA_IP_ADDRESS + ':8080/shot.jpg', 'shot.jpg')
    output = subprocess.check_output(['alpr', 'shot.jpg'])
    splitted = output.split("\n")
    if len(splitted) > 2:
        plate = splitted[1].split("\t")
        plate = plate[0].strip().split(' ')[1]
        LCD.setCursor(0, 0)
        LCD.write(('Plate: ' + plate).encode('utf-8'))
    else:
        LCD.setCursor(0, 0)
        LCD.write('Could not identify')

    time.sleep(5.0)


if __name__ == '__main__':
    main()
