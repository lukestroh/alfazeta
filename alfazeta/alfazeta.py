#!/usr/bin/env python3
"""
alfazeta.py - Package for the 7-segment display control from Alfazeta
Author: Luke Strohbehn
Date: 08/27/2023
"""

import time
import datetime
from alfazeta import library
import collections as col
import serial
import python_weather
import asyncio
import sys, os
import warnings
import copy


try:
    import pigpio as gpio
    raspi_mode = True
except ImportError as e:
    print(f"{e}: This computer does not appear to have the Raspberry Pi GPIO library. Shadowing hardware calls with substitute functions.")
    raspi_mode = False
    

START_BYTE = 0x80
END_BYTE = 0x8f
CLEAR_BYTE = 0xff # clears the screen
LOAD_DATA_SHOW = 0x8d
LOAD_DATA_DONT_SHOW = 0x8e
SHOW_LOADED_DATA = 0x82


DEBUG = 0

class AlfaZeta:
    def __init__(
        self,
        port,
        address,
        button_pin,
        BAUDRATE = 57600,
        flipped = False,
        start_byte = START_BYTE,
        end_byte = END_BYTE,
        display_option = LOAD_DATA_SHOW
    ) -> None:
        self.port = port
        self.address = address
        self.button_pin = button_pin
        self.BAUDRATE = BAUDRATE
        self.BYTESIZE = 8
        self.start_byte = start_byte
        self.end_byte = end_byte
        self.display_option = display_option
        self.empty_byte_arr = bytearray([self.start_byte, self.display_option, self.address, 0b0, 0b0, 0b0, 0b0, 0b0, 0b0, 0b0, 0b0, 0b0, 0b0, self.end_byte])
        self.last_data_sent = bytearray([])
        # Load normal or flipped library
        self.flipped = flipped
        if flipped == True:
            self.dictionary = library.flipped()
        else:
            self.dictionary = library.library()
        
        # Connect to Serial
        self._connect_to_serial()
        
        if raspi_mode:
            # Set up GPIO pin to be pulldown
            self.pio = gpio.pi()
            self.pio.set_mode(self.button_pin, gpio.INPUT)
            self.pio.set_pull_up_down(self.button_pin, gpio.PUD_UP)
            self.pio_cb_id = self.pio.callback(self.button_pin, gpio.RISING_EDGE, self.button_callback)

        self._run = True
        return

    def button_callback(self):
        """ Button press callback """
        print("Got a callback!")
        if self.pio_cb_id.tally() % 2 == 0:
            self.startup_sequence()
            self._run = True
        else:
            self.shutdown_sequence()
            self._run = False
        return 

    def _connect_to_serial(self) -> None:
        """ Connect to the Serial to RS232 converter """
        try:
            self.serial = serial.Serial(self.port, baudrate=self.BAUDRATE, bytesize=self.BYTESIZE)
            # print(self.serial)
        except serial.serialutil.SerialException as e:
            if DEBUG:
                print(f"\nCould not connect to the device on port {self.port}. Continuing in DEBUG mode, running shadow functions.")
            else:
                sys.exit(f"\nCould not connect to the device on port {self.port}. Error: {e}\nExiting.")
        return

    def _write_buffer(self, data, raw_data: bool = False) -> bytearray:
        """ Put the data in the correct format """
        data_buf = copy.deepcopy(self.empty_byte_arr)
        if not raw_data:
            byte_data = list(map(lambda x: self.dictionary[x], data))
        else:
            byte_data = data
        data_buf[3:-1] = byte_data[:10]
        self.last_data_sent = byte_data
        return data_buf
            
    def write_to_display(self, data, raw_data: bool = False) -> None:
        """ Send a message to the display"""
        if len(data) > 10:
            warnings.warn(f"Input buffer {data} is longer than 10 characters. The entire message may not be displayed.", UserWarning)
        if self.flipped:
            data.ljust(10)
        else:
            data.rjust(10)
        data_buf = self._write_buffer(data, raw_data=raw_data)
        # if not DEBUG:
        self.serial.write(data_buf)
        return
        
    def clear_display(self) -> None:
        """ Completely clear the display """
        if not DEBUG:
            self.serial.write(self.empty_byte_arr)
        return
    
    def fill_display(self) -> None:
        """ Completely fill the display """
        data_buf = copy.deepcopy(self.empty_byte_arr)
        fill_arr = bytearray([0b01111111]*10)
        print(fill_arr)
        data_buf[3:-1] = fill_arr
        print(data_buf)
        if not DEBUG:
            self.serial.write(data_buf)
        return 
  
    def display_datetime(self, h24: bool = True) -> None:
        """ Display the datetime """
        slow_message_trigger = 0
        cur_time = datetime.datetime.now()
        # Send fewer messages to the controller by syncing our clock up to be within a second using slow_message_trigger.
        if cur_time.strftime('%S') == '00':
            slow_message_trigger = 1
        if h24:
            cur_time = cur_time.strftime(r'%H%M %d%b')
        else:
            cur_time = cur_time.strftime(r'%I%M %d%b')

        # Send time data
        if self.flipped:
            # self.slide(cur_time+" hello world")
            self.write_to_display(cur_time[::-1])
        else:
            self.write_to_display(cur_time)
        
        if slow_message_trigger:
            return 1
        else:
            return 0

    def run_shutdown_sequence(self) -> None:
        """ Run the shutdown sequence """
        self._run = False
        return

    def run_startup_sequence(self) -> None:
        """ Run the startup sequence 
        Better option TODO: make a function that detects whether a horizontal or vertical piece is touching, like tetris. Then
        fill in the spots until the screen is full
        """
        self.clear_display()
        time.sleep(0.5)

        byte_deque = col.deque([
            0b00000001,
            0b00000000,
            0b00000000,
            0b00000000,
            0b00000000,
            0b00000000,
            0b00000000,
            0b00000000,
            0b00000000,
            0b00000000,
        ])

        for _i in range(0,7):
            
            for _j in range(0,10):
                self.write_to_display(bytearray(byte_deque), raw_data = True)
                time.sleep(0.05)
                byte_deque.rotate(1)
                
            byte_deque[0] = byte_deque[0] << 1
        
        self.clear_display()

        # Bit shift open one to next position
        self._run = True
        return   

    def run_program(self) -> None:
        """ Run the main control sequence """
        self.run_startup_sequence()
        while True:
            if self._run:
                slow_message_trigger = self.display_datetime(h24 = True)
                if slow_message_trigger:
                    time.sleep(60)
                else:
                    time.sleep(1)
            # self.clear_display()
            # time.sleep(1)
    # def error_screen(self):
    #     byte_array = self.byte_header.copy()
    #     for letter in "error".rjust(10):
    #         byte_array.append(self.dictionary[letter])
    #     byte_array.append(self.end_byte)
    #     return self.serial.write(byte_array)
    

    # async def _get_weather(self, location, format):
    #     if format.lower() != 'imperial' and format.lower() != 'metric':
    #         raise Exception(f"'{format}' is not a valid weather format. Try 'imperial' or 'metric'\n")
    #     elif format == 'imperial':
    #         client = python_weather.Client(format=python_weather.IMPERIAL)
    #     elif format == 'metric':
    #         client = python_weather.Client(format=python_weather.METRIC)
    #     weather = await client.find(location)
    #     await client.close()
    #     return int(weather.current.temperature), weather.current.sky_text
    

    # def display_weather(self, location, format='imperial'):
    #     loop = asyncio.get_event_loop()
    #     temp, forecast = loop.run_until_complete(self._get_weather(location, format.lower())) # Do I need the lower here?

    #     print(forecast)

    #     byte_array = self.byte_header.copy()
    #     for digit in str(temp):
    #         byte_array.append(self.dictionary[digit])
    #     if format == 'imperial':
    #         byte_array.extend([self.dictionary['*'], self.dictionary['F']])
    #     elif format == 'metric':
    #         byte_array.extend([self.dictionary['*'], self.dictionary['C']])

    #     if len(forecast) <= 6:
    #         for letter in forecast:
    #             byte_array.append(self.dictionary[letter])
    #     # need to account for if length is less than 6, then move letters over

    #     byte_array.append(self.end_byte)
    #     self.serial.write(byte_array)

    #     return

    # def loading_screen(self, stop_trigger):
    #     number_of_frames = 3

    #     byte_list = col.deque([
    #         0b00001000,
    #         0b00001000,
    #         0b00001000,
    #         0b00000000,
    #         0b00000000,
    #         0b00000000,
    #         0b00000000,
    #         0b00000000,
    #         0b00000000,
    #         0b00000000,
    #     ])
    #     # print(translated_list)
    #     # shifted_list = list(translated_list)
    #     # print(shifted_list)

    #     # for frame in number_of_frames:
    #     i = 0
    #     while i < 100:

    #         byte_array = bytearray([self.start_byte, self.display_option, self.address])
    #         for _byte in byte_list:
    #             byte_array.append(_byte)
    #         byte_array.append(self.end_byte)
    #         self.serial.write(byte_array)
    #         time.sleep(.1)
    #         byte_list.rotate(1)
    #         i+=1
    #         # if i == 8:
    #         #     i=0
    #     return

#   def slide(self, data) -> None:
#         """ If the board is flipped, send a message sliding across the digits  """
#         new_str = " ".ljust(10)
#         for iletter in data+"          ":
#             byte_array = self.byte_header.copy()
#             new_str = new_str[1:] + iletter
#             for jletter in new_str[::-1]:
#                 byte_array.append(self.dictionary[jletter.lower()]) # change this when capital letters are added
#             byte_array.append(self.end_byte)
#             self.serial.write(byte_array)
#             time.sleep(.5)
#         return
