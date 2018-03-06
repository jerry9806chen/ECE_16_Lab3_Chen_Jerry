#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 15:44:25 2018

@author: jerry
"""

#plot the signal passed through multiple filters on multiple plots


import scipy.signal as signal
import matplotlib.pyplot as plt

#function to simplify plotting each set of data
def plot_signal(x_value, y_value, title, x_label = 'time (microseconds)', y_label = 'Scaled Data (mV)'):
    
    plt.plot(x_value, y_value)
    
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    #plt.axis([0, 5000000, 0, 4])
    plt.show()

with open("EMG_scaled_data.txt", 'r') as read_file:
    #read the entirety of the file
    reading = read_file.read()
    
    #arrays for recording the time of each sample and each sample
    time = []
    orig_signal = []
    
    #Find and record the time for and each sample
    while "reading" in reading:
        orig_signal += [float(reading[reading.find("reading: ") + 9: reading.find("V")])]
        time += [int(reading[reading.find("start: ") + 7: reading.find("microseconds")])]
        
        reading = reading[reading.find("\n") + 1:]
    
    #plot original data
    plot_signal(time, orig_signal, 'Original EMG Scaled Data')

    #calculate and plot data after going through high pass filter
    b_high, a_high = signal.butter(3, 0.1, 'highpass', analog=False)
    high_pass_signal = signal.lfilter(b_high, a_high, orig_signal)
    plot_signal(time, high_pass_signal, 'High Pass EMG Data')
    
    #calculate and plot data after going through low pass filter
    b_low, a_low = signal.butter(3, .5, 'lowpass', analog=False)
    low_pass_signal = signal.lfilter(b_low, a_low, orig_signal)
    plot_signal(time, low_pass_signal, 'Low Pass EMG Data')
    
    #calculate and plot data after going through high and low pass filters
    hilo_pass_signal = signal.lfilter(b_low, a_low, high_pass_signal)
    plot_signal(time, hilo_pass_signal, 'High-Low Pass EMG Data')
    
    #rectify the hi-lo pass signal and plot the rectified signal
    rectified_signal = abs(hilo_pass_signal)
    plot_signal(time, rectified_signal, 'Rectified EMG Data')
    
    #put the data through a boxcar filter to smooth the EMG data
    box = signal.boxcar(100)
    smoothed_signal = signal.lfilter(box, 1, rectified_signal)
    plot_signal(time, smoothed_signal, 'Smoothed EMG Data')
    
    #calculate and plot the power spectral density.
    frequency, power = signal.welch(hilo_pass_signal, 200)
    plot_signal(frequency, power, 'Power Spectral Density', 'Frequency(Hz)', 'log(Power/Hz)')
