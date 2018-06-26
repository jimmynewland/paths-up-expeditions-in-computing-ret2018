
import cmsd50plus as cms
import serial
import time
from datetime import datetime
import csv
import io

def list_ports():
    import serial.tools.list_ports
    print([comport.device for comport in serial.tools.list_ports.comports()])

cms_port = '/dev/tty.SLAB_USBtoUART'
amped_port = '/dev/tty.usbmodem1411'
ports = [cms_port, amped_port]

cmsSerial = cms.cms_serial(cms_port)
#ampedSerial = serial.Serial(amped_port, 115200, timeout=0, stopbits=1, parity=serial.PARITY_NONE, bytesize=8)
now = datetime.now()

def setup_csv():
    csvFileName = now.strftime("%Y-%m-%d_%I_%M_%S")
    headers = unicode(u'cms_pulseWaveform'+','+u'cms_pulseRate'+','+u'cms_time'+','
                     +u'amped_pulseWaveform'+','+u'amped_pulseRate'+','+u'amped_time'+','+u'amped_ibi')
    with io.open(csvFileName + '.csv', 'w', newline='') as f:
        f.write(headers)
        f.write(u'\n')
    return csvFileName


def get_cms_data(cmsSerial):
    # Here the cmsInterface object queries the device for a data object.
    port, data = cms.get_data(cmsSerial) 
    
    # Keep calling get_data on cmsInterface until it is not blank.
    while data is None or len(data) == 0:
        data = cms.get_data(cmsSerial) 

    single_record = {}

    for entry in data:
        values = entry.values()

        # The pulse rate is stored in the 2nd element of the dictionary object as an int.
        single_record['pulseRate'] = values[1]
            
        # The signal is stored in the 3rd element of the dictionary object as an in.
        single_record['pulseWaveform'] = values[2]
            
        # The time is stored in the 5th element of the dictionary object as a 
        # datetime object.            
        # The time as a string is converted into a datetime object
        read_time = datetime.strptime(values[4], '%Y-%m-%d %H:%M:%S.%f')
            
        # The elapsed time since we started reading data and this reading.
        # The total_seconds method returned 
        single_record['time'] = (read_time-now).total_seconds()
    return single_record

def get_amped_data(amped_port):
    bpm = -1
    ibi = -1
    signal = -1
    
    serialRead = ampedSerial.readline()
    
    single_record = {"pulseRate":0,"pulseWaveform":0,"time":0,"ibi":0}
    read_time = datetime.now()    
    arduino_input = serialRead.strip()

    if arduino_input.count(",") == 2:
        bpm,ibi,signal = arduino_input.split(',')
        if signal is not '' and bpm is not '' and ibi is not '':
            elapsed = (read_time - now).total_seconds()
            single_record['pulseRate'] = int(bpm)
            single_record['pulseWaveform'] = int(signal)
            single_record['time'] = elapsed
            single_record['ibi'] = int(ibi)    
    time.sleep(0.02)
    return single_record

def save_to_csv(csvFileName, cmsData, ampedData):
    with io.open(csvFileName + '.csv', 'a', newline='') as f:
        row = unicode(unicode(cmsData['pulseWaveform'])+','+unicode(cmsData['pulseRate'])+','+unicode(cmsData['time'])+','+
                      unicode(ampedData['pulseWaveform'])+','+unicode(ampedData['pulseRate'])+','+unicode(ampedData['time'])+','+unicode(ampedData['ibi']))
        f.write(row)
        f.write(u'\n')    

# main() function
def main():
    #csvFileName = setup_csv()
    print("Press CTRL-C or disconnect the device to terminate data collection.")
    
    while True:
        cmsData = get_cms_data(cmsSerial)
        #ampedData = get_amped_data(amped_port)
        #scaled = int(ampedData['pulseWaveform']*255/1024.0)
        #print("B:C{}\tA{}\tS:C{}\tA{}\tT:C{}\tA{}".format(cmsData['pulseRate'],     ampedData['pulseRate'],
        #                                          cmsData['pulseWaveform'], scaled,
        #                                          cmsData['time'],          ampedData['time']))
        print("B:{}\tS:{}\tT:{}".format(cmsData['pulseRate'],cmsData['pulseWaveform'], cmsData['time']))
        #
        #save_to_csv(csvFileName,cmsData,ampedData) 

# call main
if __name__ == '__main__':
    main()