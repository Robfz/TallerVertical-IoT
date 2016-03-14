#!/usr/bin/python

import matplotlib.colors as colors
import pyupm_i2clcd as lcd
from colour import Color

class xLcdRgb(object):

    def __init__(self):
        self.lcdrgb = lcd.Jhd1313m1(1, 0x3E, 0x62)

    def __del__(self):
        pass

    def hexToRgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return list(tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)))

    def clear(self):
        self.lcdrgb.clear()

    def setCursor(self, x, y):
        self.lcdrgb.setCursor(x,y)

    def setColor(self, color):
        color = Color(color)
        colordecimal = self.hexToRgb(colors.rgb2hex(color.rgb))
        self.lcdrgb.setColor(colordecimal[0], colordecimal[1], colordecimal[2])

    def setText(self, text):
        self.lcdrgb.write(text)

if __name__ == "__main__":

    idLcdRgb = xLcdRgb()
    while True:
        idLcdRgb.setCursor(0,0)
        idLcdRgb.setText("Hello Lcd Rgb!") 
        idLcdRgb.setColor("Red")

# End of Text
