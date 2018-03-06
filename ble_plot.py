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
fig1 = plt.figure(1)
fig2 = plt.figure(2)
fig3 = plt.figure(3)

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

#Label title and axes of figure
def label_plot(fig, title, x_label, y_label):
    fig.title(title)
    fig.xlabel(x_label)
    fig.ylabel(y_label)

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
        fig1.clear()
        fig1.axis([time[len(time)] - 5000, time[len(time)], -0.8, 0.8])
        fig1.plot(time, EMG1)
        fig1.plot(time, EMG2)
        label_plot(fig1, "EMG Scaled Data", 'time (milliseconds)', "Scaled Data (mV)")
        
        fig2.clear()
        fig2.axis([time[len(time)] - 5000, time[len(time)], -5, 5])
        fig2.plot(time, ax)
        fig2.plot(time, ay)
        fig2.plot(time, az)
        label_plot(fig1, "Accelerometer Data", 'time (milliseconds)', "acceleration (m/s^2)")

        fig3.clear()
        fig3.axis([time[len(time)] - 5000, time[len(time)], -250, 250])
        fig3.plot(time, gx)
        fig3.plot(time, gy)
        fig3.plot(time, gz)
        label_plot(fig1, "Gyroscope Data", 'time (milliseconds)', "ang. accel. (deg/s^2)")
        
ani = animation.FuncAnimation(plt, plotting, interval=1000)
plt.show()