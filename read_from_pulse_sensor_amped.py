amped_comport = '/dev/tty.usbmodem1411'
amped_baudrate = 115200
amped_serial_timeout = 1

import serial
import time
from datetime import datetime
from time import sleep

now = datetime.now()
        
print('reading from serial port %s...' % amped_comport)
ser = serial.Serial(amped_comport, amped_baudrate, timeout=amped_serial_timeout)    # open serial port


def get_data_amped():
    bpm = -1
    ibi = -1
    signal = -1
    serialRead = ser.readline()
    single_record = {}
    #print(serialRead)
    read_time = datetime.now()    
    arduino_input = serialRead.strip()
    #print(arduino_input)

    if arduino_input.count(",") == 2:
        bpm,ibi,signal = arduino_input.split(',')
        elapsed = (read_time - now).total_seconds()
        #if len(bpm) > 0 and len(signal) > 0:
        single_record['pulseRate'] = int(bpm)
        single_record['pulseWaveform'] = int(signal)
        single_record['time'] = elapsed
        return single_record
    else:
        return {"pulseRate":0,"pulseWaveform":0,"time":0}
sleep(5)                   
while True:
    read_amped = get_data_amped()
    
    print(read_amped)