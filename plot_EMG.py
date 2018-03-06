#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 07:54:13 2018

@author: jerry
"""

#plot EMG data onto two plots (raw and scaled data)


import matplotlib.pyplot as plt

#open EMG_raw_data.txt for reading
with open("EMG_raw_data.txt", 'r') as read_file:
    #read the entirety of read_file
    reading = read_file.read()
    
    #arrays to record time of each sample and sampled raw data
    xValue = []
    yValue = []
    
    #find and record time of each sample and sampled raw data
    while "reading" in reading:
        yValue += [int(reading[reading.find("reading: ") + 9: reading.find("\t")])]
        xValue += [int(reading[reading.find("start: ") + 7: reading.find("microseconds")])]
        
        reading = reading[reading.find("\n") + 1:]
    
    #plot the data, label the title and axes, set axes and show the plot
    plt.plot(xValue, yValue)
    
    plt.title('EMG Raw Data')
    plt.ylabel('Raw Data Bits')
    plt.xlabel('time (microseconds)')
    
    plt.axis([0, 5000000, 0, 1024])
    plt.show()
            
#open EMG_scaled_data.txt for reading
with open("EMG_scaled_data.txt", 'r') as read_file:
    #read the entirety of read_file
    reading = read_file.read()
    
    #arrays to record time of each sample and sampled scaled data
    xValue = []
    yValue = []
    
    #find and record time of each sample and sampled scaled data
    while "reading" in reading:
        yValue += [float(reading[reading.find("reading: ") + 9: reading.find("V")])]
        xValue += [int(reading[reading.find("start: ") + 7: reading.find("microseconds")])]
        
        reading = reading[reading.find("\n") + 1:]
        
    #plot the data, label the title and axes, set axes and show the plot
    plt.plot(xValue, yValue)
    
    plt.title('EMG Scaled Data')
    plt.ylabel('Scaled Data (mV)')
    plt.xlabel('time (microseconds)')
    
    plt.show()