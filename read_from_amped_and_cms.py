import serial
import time
from datetime import datetime
from time import sleep
import cms50dplus as cms

# For saving data to a CSV
import csv
import io

amped_comport = '/dev/tty.usbmodem1421'
amped_baudrate = 115200
amped_serial_timeout = 1

now = datetime.now()

# A simple helper function to print the serial ports available on the system
def print_serial_ports():
    import serial.tools.list_ports
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    for port in ports:
        print port

# Setup the file: note start time, open file, create filename, return the filename
def setup_csv(csvStr=None):
    now = datetime.now()
    if csvStr is None:
        csvFileName = now.strftime("%Y-%m-%d_%I_%M_%S")
    else:
        csvFileName = csvStr+'_'+now.strftime("%Y-%m-%d_%I_%M_%S")
    headers = unicode(u'pulseWaveform1'+','+u'pulseRate1'+','+u'time1'+','+u'pulseWaveform2'+','+u'pulseRate2'+','+u'time2')
    with io.open(csvFileName + '.csv', 'w', newline='') as f:
        f.write(headers)
        f.write(u'\n')
    return csvFileName

def save_to_csv(csvFileName, allData):
    ampedData = allData[0]
    cmsData = allData[1]
    with io.open(csvFileName + '.csv', 'a', newline='') as f:
        row = unicode(unicode(ampedData['pulseWaveform'])+','+unicode(ampedData['pulseRate'])+','+unicode(ampedData['time'])+','+unicode(cmsData['pulseWaveform'])+','+unicode(cmsData['pulseRate'])+','+unicode(cmsData['time']))
        f.write(row)
        f.write(u'\n')  

#print('reading from serial port %s...' % amped_comport)
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
        single_record['ibi'] = int(ibi)
        single_record['time'] = elapsed
        return single_record
    else:
        return {"pulseRate":0,"pulseWaveform":0,"time":0}

csvFilename = setup_csv('amped_and_cms50dplus')

port = '/dev/tty.SLAB_USBtoUART'
cms_init = cms.cms_serial(port,False,csvStr='amped_and_cms_')

#time.sleep(5)    

while True:
    cmsData = cms.get_cms_data(cms_init)
    read_amped = get_data_amped()
    allData = read_amped,cmsData

    print("PR1:{}\tSig1:{}\tT1:{}\tPR2:{}\tSig2:{}\tT2:{}".format(
          read_amped['pulseRate'],read_amped['pulseWaveform'], read_amped['time'],
          cmsData['pulseRate'],cmsData['pulseWaveform'], cmsData['time']
         ))
    save_to_csv(csvFilename, allData)
    time.sleep(0.02)