import serial
import time
import datetime
import library

display_address = 0x1f # The address of my flip disc display (set with dip switches)
end_byte = 0x8f

start_byte = 0x80
load_data_dont_show = 0x8e
load_data_show = 0x8d
show_loaded_data = 0x82
# clear_byte = 0xff # clears the screen
empty_display = [0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000]

class AlfaZeta:
    def __init__(self, serial, start_byte, display_option, address, end_byte):
        self.serial = serial
        self.start_byte = start_byte
        self.display_option = display_option
        self.address = address
        self.end_byte = end_byte

    # def display_string(self,serial,start,display_option,address,data,end):
    #     byte_array = bytearray([start, display_option, address])
    #     for item in data:
    #         byte_array.append(item)
    #     byte_array.append(end)
    #     serial.write(byte_array)
    #
    # def display_number(serial,display_option,address,number,end):
    #     byte_array = bytearray([start, display_option, address])
    #     for digit in str(number).zfill(10):
    #         byte_array.append(int(digit))
    #     byte_array.append(end)
    #     serial.write(byte_array)

    def clear_screen(self, data):# (serial,start,display_option,address,clear_bytes,end):
        byte_array = bytearray([self.start_byte, self.display_option, self.address])
        for byte in clear_bytes:
            byte_array.append(byte)
        byte_array.append(end)
        serial.write(byte_array)

    def display_time(serial,start,display_option,address,end, dictionary, h24=True):
        # This will pad the date with 0, must be reconfigured for no pad
        cur_time = datetime.datetime.now()
        if h24:
            cur_time = cur_time.strftime('%H%M %d%b')
        else:
            cur_time = cur_time.strftime('%I%M %d%b')
        byte_array = bytearray([start, display_option, address])
        for letter in cur_time:
            byte_array.append(dictionary[letter.lower()]) # change this when capital letters are added
        byte_array.append(end)
        serial.write(byte_array)
        return


def main():
    dictionary = library.create_library()

    ser = serial.Serial('com4', baudrate=57600, bytesize=8)
    print(ser)

    flip_digit = AlfaZeta(ser, start_byte, load_data_show, display_address, end_byte)

    time.sleep(.5)
    flip_digit.clear_screen(ser, start_byte, load_data_show, display_address, empty_display, end_byte)

    while 1:
        flip_digit.display_time(ser, start_byte, load_data_show, display_address, end_byte, dictionary, h24=True)
        time.sleep(1)

    # while 1:
    #     myinput = input('Enter a 10-char string: ').lower()
    #     my_data=bytearray([])
    #     for letter in myinput:
    #         if len(my_data) >= 10:
    #             break
    #         else:
    #             try:
    #                 my_data.append(dictionary[letter])
    #             except KeyError as e:
    #                 print("Unsupported character: ",e, ". Please try again")
    #                 continue
    #     display_string(ser, start_byte, load_data_show, display_address, my_data, end_byte)

if __name__ == '__main__':
    main()
