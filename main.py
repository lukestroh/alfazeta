from alfazeta import alfazeta
import serial
import time
import sys, os

COM_PORT = 'com19'
BAUDRATE = 57600
BYTESIZE = 8
DISPLAY_ADDRESS = 0x1f # The address of my flip disc display (set with dip switches)

def main():
    try:
        ser = serial.Serial(COM_PORT, baudrate=BAUDRATE, bytesize=BYTESIZE)
        print(ser)
    except (serial.serialutil.SerialException, KeyboardInterrupt) as e:
        sys.exit(f"\nCould not connect to the device. Error: {e}\n")

    flip_digit = alfazeta.AlfaZeta(ser, address=DISPLAY_ADDRESS, flipped=False)

    time.sleep(.5)
    flip_digit.clear_screen()


    try:
        while 1:
            slow_message_trigger = flip_digit.display_time(h24=True)

            if slow_message_trigger:
                time.sleep(30)
                flip_digit.display_weather('berkeley ca')
                time.sleep(30)
            else:
                time.sleep(60)
    except KeyboardInterrupt:
        sys.exit()
    return

if __name__ == '__main__':
    main()
