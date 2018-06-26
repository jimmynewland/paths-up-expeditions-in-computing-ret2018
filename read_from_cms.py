''' Read data from CMS D50+ Pulse Oximeter (firmware ver 4.6)
Author: J Newland 
        newton@jayfox.net https://github.com/jimmynewland https://jimmynewland.com

Version 1.0.0 2018/06/26

Project: Rice University PATHS-UP/Expeditions in Computing 
         Scalable Health Research Experience for Teachers (RET)
Attribution: Many elements of this code were modified from https://github.com/atbrask/CMS50Dplus

Usage: This script pulls live data from the Contech CMS D50+ Pulse Oximeter.
       You must also have the cmsd50plus library in the same location as this script.

       Serial port: You must know the serial port

#Reference: Newland, J, PATHS-UP/Expeditions in Computing RET at Rice University, Summer 2018,
                https://www.rstem.rice.edu/paths-up-ret

'''
import cmsd50plus as cms

# main() function
def main():
    # Print serial ports
    print_serial_ports()

    # This string should match the serial port to which the CMS D50+ is connected.
    # On Mac OS 10.13.5 the port was /dev/tty.SLAB_USBtoUART
    # Alternately, the serial ports can be listed from the OS X command line:
    # ls /dev/tty.*
    port = '/dev/tty.SLAB_USBtoUART'
    
    print("Press CTRL-C or disconnect the device to terminate data collection.")
    
    # Sends the correct serial port as s string and opens the serial connection. 
    # Optionally, the save-to-csv flag can be set to false here.
    # e.g. cms_init = cms.cms_serial(port, False) would initialize the serial connection.
    # but would not save live data to a file.
    cms_init = cms.cms_serial(port)

    # This script will read live data until interrupted by CTRL-C or the device is unplugged.
    while True:
        # Take a reading from the CMS D50+. Data is returned as a dictionary object:
        # { 
        #   pulseRate (integer 0 - ~220), 
        #   pulseWaveform (integer 0 - 255 at 255 the light sensor is saturated), 
        #   time (seconds since data collection started as a float)
        # }
        cmsData = cms.get_cms_data(cms_init)
        # By default, a call to get_cms_data also save to a CSV file.
        # The filename will be cmsd50_YYYY-MM-DD_HH_MM_SS.csv
        print("Pulse Rate:{}\tSignal:{}\tTime:{}".format(cmsData['pulseRate'],cmsData['pulseWaveform'], cmsData['time']))
        
# call main
if __name__ == '__main__':
    main()

# A simple helper function to print the serial ports available on the system.
def print_serial_ports():
    import serial.tools.list_ports
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    for port in ports:
        print port