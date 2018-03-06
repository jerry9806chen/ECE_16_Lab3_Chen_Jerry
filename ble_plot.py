#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 16:44:14 2018

@author: jerry
"""


import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# this port address is for the serial Arduino port
SERIAL_PORT = '/dev/cu.usbmodem1411'
# the same rate used on the Arduino
SERIAL_RATE = 115200

# connect to serial and send user input to request data collection from either one of the three sources.
ser = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=1)

# define the figure and its subplots
fig = plt.figure()
sub1 = fig.add_subplot(2,2,1)
sub2 = fig.add_subplot(2,2,2)
sub3 = fig.add_subplot(2,2,3)

# arrays for EMG, accelerometer, gyroscope, and sampling times
EMG1 = []
EMG2 = []
ax = []
ay = []
az = []
gx = []
gy = []
gz = []
time = []

#plot x_value and signal onto a subplot
def plot_signal(sub, x_value, signal, title, x_label = 'time (milliseconds)', y_label = 'Scaled Data (mV)'):
    sub.clear()
    sub.plot(x_value, signal)
    #ax.title(title)
    #ax.xlabel(x_label)
    #ax.ylabel(y_label)

#plotting function. Gather data from each line and update the subplots only when the arrays have the same number of entries(time is being update).
def plotting(i):
    reading = str(ser.readline().decode('utf-8'))
    global EMG1, EMG2, ax, ay, az, gx, gy, gz, time
    if "(mv)" in reading:
        EMG1 += [float(reading[reading.find("1(mv)") + 6:reading.find(", EMG 2")])]
        EMG2 += [float(reading[reading.find("2(mv)") + 6:reading.find("\n")])]
    elif "ax=" in reading:
        ax += [float(reading[reading.find("ax=") + 3:reading.find(", ay=")])]
        ay += [float(reading[reading.find("ay=") + 3:reading.find(", az=")])]
        az += [float(reading[reading.find("az=") + 3:reading.find("\n")])]
    elif "gx=" in reading:
        gx += [float(reading[reading.find("gx=") + 3:reading.find(", gy=")])]
        gy += [float(reading[reading.find("gy=") + 3:reading.find(", gz=")])]
        gz += [float(reading[reading.find("gz=") + 3:reading.find("\n")])]
    elif "time" in reading:
        time += [int(reading[reading.find("start: ") + 7:reading.find(" ms")])]
        sub1.clear()
        sub1.axis([time[len(time)] - 5000, time[len(time)], -0.8, 0.8])
        sub1.plot(time, EMG1)
        sub1.plot(time, EMG2)
        sub2.clear()
        sub2.axis([time[len(time)] - 5000, time[len(time)], -5, 5])
        sub2.plot(time, ax)
        sub2.plot(time, ay)
        sub2.plot(time, az)
        sub3.clear()
        sub3.axis([time[len(time)] - 5000, time[len(time)], -250, 250])
        sub3.plot(time, gx)
        sub3.plot(time, gy)
        sub3.plot(time, gz)
        
ani = animation.FuncAnimation(fig, plotting, interval=1000)
plt.show()