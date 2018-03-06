#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 17:37:42 2018

@author: jerry
"""

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

#custom IIR filter function
def my_filter(b, a, orig_signal):
    new_signal = [orig_signal[0], orig_signal[1], orig_signal[2]]
    
    for x in range(3, len(orig_signal)):
        new_signal += [-a[1] * new_signal[x - 1] - a[2] * new_signal[x - 2] - a[3] * new_signal[x - 3] + b[0] * orig_signal[x] + b[1] * orig_signal[x - 1] + b[2] * orig_signal[x - 2] + b[3] * orig_signal[x - 3]]
        
    return new_signal

#open EMG_scaled_data.txt for read EMG scaled data
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
    
    #calculate and plot data after going through custom high pass filter
    b_high, a_high = signal.butter(3, 0.1, 'highpass', analog=False)
    #high_pass_signal = signal.lfilter(b_high, a_high, orig_signal)
    high_pass_signal = my_filter(b_high, a_high, orig_signal)
    plot_signal(time, high_pass_signal, 'High Pass EMG Data')
    
    #calculate and plot data after going through custom low pass filter
    b_low, a_low = signal.butter(3, .5, 'lowpass', analog=False)
    #low_pass_signal = signal.lfilter(b_low, a_low, orig_signal)
    low_pass_signal = my_filter(b_low, a_low, orig_signal)
    plot_signal(time, low_pass_signal, 'Low Pass EMG Data')