#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 19:46:15 2018

@author: jerry
"""

import serial

# this port address is for the serial Arduino port
SERIAL_PORT = '/dev/cu.usbmodem1411'
# the same rate used on the Arduino
SERIAL_RATE = 115200
# the number of times a set of samples has been printed
printCount = 0

# connect to serial and send user input to request data collection from either one of the three sources.
ser = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=1)

# reads the first line
reading = str(ser.readline().decode('utf-8'))

# select a file to write to depending on data value type.
if "raw" in reading:
    fileName = "EMG_raw_data.txt"
elif "voltage" in reading:
    fileName = "EMG_scaled_data.txt"
    
printCount = 1

# opens the selected file for writing
fo = open(fileName, "w")

# reads and prints every samples (at 200Hz) for 5 seconds and writes it to the selected file. Increments printCount for every printed line up to 1000.
while printCount < 200 * 5:
    if "\n" not in reading:
        reading += str(ser.readline().decode('utf-8'))
    else:
        endIndex = reading.index("\n")
        writeString = reading[0:endIndex]
        print(writeString)
        fo.write(writeString + "\n")
        reading = reading[endIndex + 1:]
        printCount += 1
        
# Close the serial and file connections
ser.close()
fo.close()