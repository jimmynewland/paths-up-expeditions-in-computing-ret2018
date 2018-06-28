# This Python file uses the following encoding: utf-8
import serial
import time
import array
from datetime import datetime
import csv
import io

def cms_serial(portstr,csv=True,csvStr=None):
    # Below is the sequence of messages that the SpO2 monitoring app sends to the CMS50D+.
    controlData = []

    port = serial.Serial(port=portstr, baudrate=115200, timeout=0, stopbits=1, parity=serial.PARITY_NONE, bytesize=8)
    port.write(([0x7D, 0x81, 0xA2, 0x80,0x80, 0x80, 0x80,0x80, 0x80, 0x7D, 0x81, 0xA7,0x80,0x80, 0x80, 0x80,0x80, 0x80,0x7D, 0x81, 0xA8, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80,0x7D, 0x81, 0xA8, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x7D, 0x81, 0xA9, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80,0x7D, 0x81, 0xAA, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80,0x7D, 0x81, 0xB0, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80]))
    time.sleep(0.05)
    controlData.append(([0x7D, 0x81, 0xA1, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80]))
        
    #initialize the CMS50D+ and start it sending output
    for c in controlData:
        port.write(c)
        time.sleep(0.02) 
        data = port.read(128)
    start_time = datetime.now()
    csvFileName = ''
    if csv:
        csvFileName = setup_csv(csvStr)
    output = {'port':port,'data':data,'start_time':start_time,'csvFileName':csvFileName}

    return output
    
def get_buffer(port,data):
    numSymbols = 9
    buf = array.array('B')
    while port.in_waiting != 9:
        time.sleep(0.005)

    buf.fromstring(port.read(128))
    temp = buf.tolist()

    if len(temp) % numSymbols != 0:
        print('error in data')
       
    parsedData = [temp[i:i + numSymbols] for i in range(0, len(temp), numSymbols)]

    outputData = []
        
    # There are 9 bytes in each data sample. 
    # Bytes 0 and 1 are a header equal to 0x01, 0xe0.
    # Bytes 7 and 8 are a footer equal to 0xff, 0xff.
    for data in parsedData:
        pulseWaveform = data[3]

        pulseRate = (data[4] & 0x40) << 1
        pulseRate |= data[5] & 0x7f

        now = str(datetime.now())
      
        output = {}
        output['pulseWaveform'] = pulseWaveform
        output['pulseRate'] = pulseRate
        output['time'] = now
        outputData.append(output)

    return outputData

def get_cms_data(init):
    port = init['port']
    buf = init['data']
    start_time = init['start_time']
    # Here the cmsInterface object queries the device for a data object.
    data = get_buffer(port,buf) 
    
    # Keep calling get_data on cmsInterface until it is not blank.
    while data is None or len(data) == 0:
        data = get_buffer(port,buf) 

    single_record = {}

    for entry in data:
        values = entry.values()

        # The pulse rate is stored in the 2nd element of the dictionary object as an int.
        single_record['pulseRate'] = values[0]
            
        # The signal is stored in the 3rd element of the dictionary object as an in.
        single_record['pulseWaveform'] = values[2]
            
        # The time is stored in the 5th element of the dictionary object as a 
        # datetime object.            
        # The time as a string is converted into a datetime object
        read_time = datetime.strptime(values[1], '%Y-%m-%d %H:%M:%S.%f')
            
        # The elapsed time since we started reading data and this reading.
        # The total_seconds method returned 
        single_record['time'] = (read_time-start_time).total_seconds()
        if not init['csvFileName'] == '':
            save_to_csv(init['csvFileName'],single_record)
    return single_record

def setup_csv(csvStr=None):
    now = datetime.now()
    if csvStr is None:
        csvFileName = 'cmsd50plus_'+now.strftime("%Y-%m-%d_%I_%M_%S")
    else:
        csvFileName = csvStr+'_'+now.strftime("%Y-%m-%d_%I_%M_%S")
    headers = unicode(u'pulseWaveform'+','+u'pulseRate'+','+u'time')
    with io.open(csvFileName + '.csv', 'w', newline='') as f:
        f.write(headers)
        f.write(u'\n')
    return csvFileName

def save_to_csv(csvFileName, cmsData):
    with io.open(csvFileName + '.csv', 'a', newline='') as f:
        row = unicode(unicode(cmsData['pulseWaveform'])+','+unicode(cmsData['pulseRate'])+','+unicode(cmsData['time']))
        f.write(row)
        f.write(u'\n')  

