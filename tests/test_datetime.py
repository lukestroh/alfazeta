#!/usr/bin/env python3

from alfazeta import alfazeta
import time

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
    # flip_digit.display_time(h24=True)

    # try:
    #     while 1:
    #         slow_message_trigger = flip_digit.display_time(h24=True)

    #         if slow_message_trigger:
    #             time.sleep(30)
    #             flip_digit.display_weather('berkeley ca')
    #             time.sleep(30)
    #         else:
    #             time.sleep(60)
    # except KeyboardInterrupt:
    #     sys.exit()


if __name__ == "__main__":
    main()