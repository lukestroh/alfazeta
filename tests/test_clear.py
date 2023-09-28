#!/usr/bin/env python3

from alfazeta import alfazeta
import time
import sys


COM_PORT = 'com22'
DISPLAY_ADDRESS = 0x1f # The address of my flip disc display (set with dip switches)
BUTTON_PIN = 26

def main():
    
    flip_digit = alfazeta.AlfaZeta(
        port=COM_PORT,
        address=DISPLAY_ADDRESS,
        button_pin=BUTTON_PIN,
        flipped=False
    )

    time.sleep(.5)
    flip_digit.clear_display()

    
    return

if __name__ == '__main__':
    main()
