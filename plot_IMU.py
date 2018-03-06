#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 14:09:04 2018

@author: jerry
"""
#plot IMU data onto two plots with 3 subplots each (one for each axis)


import matplotlib.pyplot as plt

#open gyro_output.txt for reading
with open("gyro_output.txt", 'r') as read_file:  
    #read the entirety of gyro_output      
    reading = read_file.read()
    
    #arrays to record time of each sample and sampled angular acceleration along each axis
    times = []
    xValue = []
    yValue = []
    zValue = []
    
    #find and record time of each sample and sampled angular acceleration along each axis
    while "Time" in reading:
        times += [int(reading[reading.find("start: ") + 7: reading.find("ms")])]
        xValue += [float(reading[reading.find("gx=") + 3: reading.find(",")])]
        reading = reading[reading.find(",") + 1:]
        yValue += [float(reading[reading.find("gy=") + 3: reading.find(",")])]
        reading = reading[reading.find(",") + 1:]
        zValue += [float(reading[reading.find("gz=") + 3: reading.find("\n")])]
        reading = reading[reading.find("\n") + 1:]
    
    #plot each data set into a subplot
    plt.subplot(2,2,1)
    plt.title('X gyro Data')
    plt.xlabel('time (ms)')
    plt.ylabel('ang. accel. (deg/s^2)')
    plt.plot(times, xValue)
    
    plt.subplot(2,2,2)
    plt.title('Y gyro Data')
    plt.xlabel('time (ms)')
    plt.ylabel('ang. accel. (deg/s^2)')
    plt.plot(times, yValue)
    
    plt.subplot(2,2,3)
    plt.title('Z gyro Data')
    plt.xlabel('time (ms)')
    plt.ylabel('ang. accel. (deg/s^2)')
    plt.plot(times, zValue)
    
    plt.show()

#open accel_output.txt for reading            
with open("accel_output.txt", 'r') as read_file:  
    #read the entirety of gyro_output     
    reading = read_file.read()

    #arrays to record time of each sample and sampled acceleration along each axis
    times = []
    xValue = []
    yValue = []
    zValue = []
    
    #find and record time of each sample and sampled angular acceleration along each axis
    while "Time" in reading:
        times += [int(reading[reading.find("start: ") + 7: reading.find("ms")])]
        xValue += [float(reading[reading.find("ax=") + 3: reading.find(",")])]
        reading = reading[reading.find(",") + 1:]
        yValue += [float(reading[reading.find("ay=") + 3: reading.find(",")])]
        reading = reading[reading.find(",") + 1:]
        zValue += [float(reading[reading.find("az=") + 3: reading.find("\n")])]
        reading = reading[reading.find("\n") + 1:]
    
    #plot each data set into a subplot
    plt.subplot(2,2,1)
    plt.title('X accel Data')
    plt.xlabel('time (ms)')
    plt.ylabel('lin. accel. (m/s^2)')
    plt.plot(times, xValue)
    
    plt.subplot(2,2,2)
    plt.title('Y accel Data')
    plt.ylabel('lin. accel. (m/s^2)')
    plt.xlabel('time (ms)')
    plt.plot(times, yValue)
    
    plt.subplot(2,2,3)
    plt.title('Z accel Data')
    plt.ylabel('lin. accel. (m/s^2)')
    plt.xlabel('time (ms)')
    plt.plot(times, zValue)
    
    plt.show()