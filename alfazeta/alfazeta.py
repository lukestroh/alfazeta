import time
import datetime
from alfazeta import library
import collections as col
import python_weather
import asyncio

START_BYTE = 0x80
END_BYTE = 0x8f
load_data_dont_show = 0x8e
LOAD_DATA_SHOW = 0x8d
show_loaded_data = 0x82
# clear_byte = 0xff # clears the screen

class AlfaZeta:
    def __init__(
        self,
        serial,
        address,
        start_byte=START_BYTE,
        display_option=LOAD_DATA_SHOW,
        end_byte=END_BYTE,
        flipped=False
    ):
        self.serial = serial
        self.start_byte = start_byte
        self.display_option = display_option
        self.address = address
        self.byte_header = bytearray([self.start_byte, self.display_option, self.address])
        self.end_byte = end_byte
        self.flipped = flipped
        if flipped == True:
            self.dictionary = library.flipped()
        else:
            self.dictionary = library.library()


    def clear_screen(self):
        byte_array = self.byte_header.copy()
        empty_display = [0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000]
        for byte in empty_display:
            byte_array.append(byte)
        byte_array.append(self.end_byte)
        return self.serial.write(byte_array)

    def slide(self, data):
        new_str = " ".ljust(10)
        for iletter in data+"          ":
            byte_array = self.byte_header.copy()
            new_str = new_str[1:] + iletter
            for jletter in new_str[::-1]:
                byte_array.append(self.dictionary[jletter.lower()]) # change this when capital letters are added
            byte_array.append(self.end_byte)
            self.serial.write(byte_array)
            time.sleep(.5)
        return

    def display_time(self, h24=True):
        slow_message_trigger = 0
        cur_time = datetime.datetime.now()
        # Send fewer messages to the controller by syncing our clock up to be within a second using slow_message_trigger.
        if cur_time.strftime('%S')=='00':
            slow_message_trigger = 1
        if h24:
            cur_time = cur_time.strftime('%H%M %d%b')
        else:
            cur_time = cur_time.strftime('%I%M %d%b')

        byte_array = self.byte_header.copy()
        if self.flipped:
            # self.slide(cur_time+" hello world")
            self.slide("Welcome to the noisiest clock you've ever had")
            for letter in cur_time[::-1]: # reverse the string
                byte_array.append(self.dictionary[letter.lower()]) # change this when capital letters are added
        else:
            for letter in cur_time:
                byte_array.append(self.dictionary[letter.lower()]) # change this when capital letters are added
        byte_array.append(self.end_byte)
        self.serial.write(byte_array)
        if slow_message_trigger:
            return 1
        else:
            return 0

    def error_screen(self):
        byte_array = self.byte_header.copy()
        for letter in "error".rjust(10):
            byte_array.append(self.dictionary[letter])
        byte_array.append(self.end_byte)
        return self.serial.write(byte_array)

    async def _get_weather(self, location, format):
        if format.lower() != 'imperial' and format.lower() != 'metric':
            raise Exception(f"'{format}' is not a valid weather format. Try 'imperial' or 'metric'\n")
        elif format == 'imperial':
            client = python_weather.Client(format=python_weather.IMPERIAL)
        elif format == 'metric':
            client = python_weather.Client(format=python_weather.METRIC)
        weather = await client.find(location)
        await client.close()
        return int(weather.current.temperature), weather.current.sky_text

    def display_weather(self, location, format='imperial'):
        loop = asyncio.get_event_loop()
        temp, forecast = loop.run_until_complete(self._get_weather(location, format.lower())) # Do I need the lower here?

        print(forecast)

        byte_array = self.byte_header.copy()
        for digit in str(temp):
            byte_array.append(self.dictionary[digit])
        if format == 'imperial':
            byte_array.extend([self.dictionary['*'], self.dictionary['F']])
        elif format == 'metric':
            byte_array.extend([self.dictionary['*'], self.dictionary['C']])

        if len(forecast) <= 6:
            for letter in forecast:
                byte_array.append(self.dictionary[letter])
        # need to account for if length is less than 6, then move letters over

        byte_array.append(self.end_byte)
        self.serial.write(byte_array)

        return

    def loading_screen(self, stop_trigger):
        number_of_frames = 3

        byte_list = col.deque([
            0b00001000,
            0b00001000,
            0b00001000,
            0b00000000,
            0b00000000,
            0b00000000,
            0b00000000,
            0b00000000,
            0b00000000,
            0b00000000,
        ])
        # print(translated_list)
        # shifted_list = list(translated_list)
        # print(shifted_list)

        # for frame in number_of_frames:
        i = 0
        while i < 100:

            byte_array = bytearray([self.start_byte, self.display_option, self.address])
            for _byte in byte_list:
                byte_array.append(_byte)
            byte_array.append(self.end_byte)
            self.serial.write(byte_array)
            time.sleep(.1)
            byte_list.rotate(1)
            i+=1
            # if i == 8:
            #     i=0
        return
