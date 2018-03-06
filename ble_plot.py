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
# the number of times a set of samples has been printed
printCount = 0

# connect to serial and send user input to request data collection from either one of the three sources.
ser = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=1)

fig = plt.figure()
sub1 = fig.add_subplot(2,2,1)
sub2 = fig.add_subplot(2,2,2)
sub3 = fig.add_subplot(2,2,3)

EMG1 = []
EMG2 = []
ax = []
ay = []
az = []
gx = []
gy = []
gz = []
time = []

reading = str(ser.readline().decode('utf-8'))

#plot x_value and signal onto a subplot
def plot_signal(sub, x_value, signal, title, x_label = 'time (milliseconds)', y_label = 'Scaled Data (mV)'):
    sub.clear()
    sub.plot(x_value, signal)
    #ax.title(title)
    #ax.xlabel(x_label)
    #ax.ylabel(y_label)

def main(i):
    global reading
    reading += str(ser.readline().decode('utf-8'))
    global EMG1, EMG2, ax, ay, az, gx, gy, gz, time
    if "(mv)" in reading:
        EMG1 += []
        EMG2 += []
        sub1.clear()
        sub1.plot(time, EMG1)
        sub1.plot(time, EMG2)
    elif "ax=" in reading:
        ax += []
        ay += []
        az += []
        sub2.clear()
        sub2.plot(time, ax)
        sub2.plot(time, ay)
        sub2.plot(time, az)
    elif "gx=" in reading:
        gx += []
        gy += []
        gz += []
        sub3.clear()
        sub3.plot(time, gx)
        sub3.plot(time, gy)
        sub3.plot(time, gz)
        
ani = animation.FuncAnimation(fig, main, interval=1000)
plt.show()