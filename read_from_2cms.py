''' Read data from CMS D50+ Pulse Oximeter (firmware ver 4.6)
Author: J Newland 
        newton@jayfox.net https://github.com/jimmynewland https://jimmynewland.com

Version 1.0.0 2018/06/27

Project: Rice University PATHS-UP/Expeditions in Computing 
         Scalable Health Research Experience for Teachers (RET)
Attribution: Many elements of this code were modified from https://github.com/atbrask/CMS50Dplus

Usage: This script pulls live data from 2 Contech CMS D50+ Pulse Oximeters.
       You must also have the cmsd50plus library in the same location as this script.

       These data could be used to find the pulse transit time with proper processing.

       Serial port: You must know the serial port for both devices. See the function below
       for printing a list of available serial ports.

#Reference: Newland, J, PATHS-UP/Expeditions in Computing RET at Rice University, Summer 2018,
                https://www.rstem.rice.edu/paths-up-ret

'''
import cmsd50plus as cms

# For saving data to a CSV
import csv
import io

# Allows use of Time objects and ime deltas
import time
from datetime import datetime

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
        csvFileName = 'cmsd50plus_'+now.strftime("%Y-%m-%d_%I_%M_%S")
    else:
        csvFileName = csvStr+'_'+now.strftime("%Y-%m-%d_%I_%M_%S")
    headers = unicode(u'pulseWaveform1'+','+u'pulseRate1'+','+u'time1'+','+u'pulseWaveform2'+','+u'pulseRate2'+','+u'time2')
    with io.open(csvFileName + '.csv', 'w', newline='') as f:
        f.write(headers)
        f.write(u'\n')
    return csvFileName

def save_to_csv(csvFileName, allData):
    cmsData1 = allData[0]
    cmsData2 = allData[1]
    with io.open(csvFileName + '.csv', 'a', newline='') as f:
        row = unicode(unicode(cmsData1['pulseWaveform'])+','+unicode(cmsData1['pulseRate'])+','+unicode(cmsData1['time'])+','+unicode(cmsData2['pulseWaveform'])+','+unicode(cmsData2['pulseRate'])+','+unicode(cmsData2['time']))
        f.write(row)
        f.write(u'\n')  

# main() function
def main():
    # Print serial ports
    print_serial_ports()

    # This string should match the serial port to which the CMS D50+ is connected.
    # On Mac OS 10.13.5 the port was /dev/tty.SLAB_USBtoUART
    # Alternately, the serial ports can be listed from the OS X command line:
    # ls /dev/tty.*
    port1 = '/dev/tty.SLAB_USBtoUART'
    port2 = '/dev/tty.SLAB_USBtoUART10'
    
    csvFilename = setup_csv('two_cms50dplus')

    print("Press CTRL-C or disconnect the device to terminate data collection.")
    
    # Sends the correct serial port as s string and opens the serial connection. 
    # Optionally, the save-to-csv flag can be set to false here.
    # e.g. cms_init = cms.cms_serial(port, False) would initialize the serial connection.
    # but would not save live data to a file.
    cms_init1 = cms.cms_serial(port1, False)
    cms_init2 = cms.cms_serial(port2, False)

    # This script will read live data until interrupted by CTRL-C or the device is unplugged.
    while True:
        # Take a reading from both CMS D50+. Data is returned as a dictionary object:
        # { 
        #   pulseRate (integer 0 - ~220), 
        #   pulseWaveform (integer 0 - 255 at 255 the light sensor is saturated), 
        #   time (seconds since data collection started as a float)
        # }
        cmsData1 = cms.get_cms_data(cms_init1)
        cmsData2 = cms.get_cms_data(cms_init2)
        
        # A tuple with both datasets
        allData = cmsData1,cmsData2

        # By default, a call to get_cms_data also save to a CSV file.
        # The filename will be cmsd50_YYYY-MM-DD_HH_MM_SS.csv
        print("PR1:{}\tSig1:{}\tT1:{}\tPR2:{}\tSig2:{}\tT2:{}".format(
            cmsData1['pulseRate'],cmsData1['pulseWaveform'], cmsData1['time'],
            cmsData2['pulseRate'],cmsData2['pulseWaveform'], cmsData2['time']
            ))
        save_to_csv(csvFilename, allData)
        
# call main
if __name__ == '__main__':
    main()
