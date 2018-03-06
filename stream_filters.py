#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 22:23:16 2018

@author: jerry
"""

#plot live streaming data through five signals


import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.signal as signal

# this port address is for the serial Arduino port
SERIAL_PORT = '/dev/cu.usbmodem1421'
#the same rate used on the Arduino
SERIAL_RATE = 115200

#the figures for original, hilo pass, rectified, and smooth signals and power spectral density.
fig1 = plt.figure(1)
fig2 = plt.figure(2)
fig3 = plt.figure(3)
fig4 = plt.figure(4)
fig5 = plt.figure(5)

#timing of each signal sample and original signal samples
time = []
orig_signal = []

# connect to serial and retrieve the first line
ser = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=1)

#custom IIR filter function
def my_filter(b, a, orig_signal):
    new_signal = [orig_signal[0], orig_signal[1], orig_signal[2]]
    
    for x in range(3, len(orig_signal)):
        new_signal += [-a[1] * new_signal[x - 1] - a[2] * new_signal[x - 2] - a[3] * new_signal[x - 3] + b[0] * orig_signal[x] + b[1] * orig_signal[x - 1] + b[2] * orig_signal[x - 2] + b[3] * orig_signal[x - 3]]
        
    return new_signal

#plot x_value and signal onto a subplot
def plot_signal(fig, x_value, y_value, title, x_label = 'time (milliseconds)', y_label = 'Scaled Data (mV)'):
    fig.clear()
    fig.plot(x_value, y_value)
    fig.axis([time[len(time)] - 5000, time[len(time)], -0.8, 0.8])
    fig.title(title)
    fig.xlabel(x_label)
    fig.ylabel(y_label)

#main function for plotting data signals.
def main(i):
    #globalize the current reading and previous data.
    global time
    global orig_signal
    
    reading = str(ser.readline().decode('utf-8'))
    #calculate and plot original EMG scaled signal
    if "\n" in reading:
        orig_signal += [float(reading[reading.find("g:") + 3:reading.find("V")])]
        time += [int(reading[reading.find("t:") + 3:reading.find("micro")])]
    plot_signal(fig1, time, orig_signal, 'Original EMG Scaled Data')
    
    #calculate and plot hi-low pass signal
    b_high, a_high = signal.butter(3, 0.1, 'highpass', analog=False)
    high_pass_signal = my_filter(b_high, a_high, orig_signal)    
    b_low, a_low = signal.butter(3, .5, 'lowpass', analog=False)    
    hilo_pass_signal = my_filter(b_low, a_low, high_pass_signal)
    plot_signal(fig2, time, hilo_pass_signal, 'High-Low Pass EMG Scaled Data')

    #calculate and plot rectified signal
    rectified_signal = []
    for x in hilo_pass_signal:
        rectified_signal += [abs(x)]
    plot_signal(fig3, time, rectified_signal, 'Rectified EMG Scaled Data')
    
    #calculate and plot smoothed signal
    box = signal.boxcar(100)
    smoothed_signal = signal.lfilter(box, 1, rectified_signal)
    plot_signal(fig4, time, smoothed_signal, 'Smoothed EMG Scaled Data')
   
    #calculate and plot the power spectral density
    frequency, power = signal.welch(hilo_pass_signal, 200)
    plot_signal(fig5, frequency, power, 'Power Spectral Density', 'Frequency(Hz)', 'log(Power/Hz)')
    
# animate and show the plot
ani = animation.FuncAnimation(plt, main, interval=1000)
plt.show()