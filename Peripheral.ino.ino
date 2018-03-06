/*
 * Copyright (c) 2016 Intel Corporation.  All rights reserved.
 * See the bottom of this file for the license terms.
 */

/*
 * Sketch: led.ino
 *
 * Description:
 *   This is a Peripheral sketch that works with a connected Central.
 *   It allows the Central to write a value and set/reset the led
 *   accordingly.
 */

#include <CurieBLE.h>

#include "CurieTimerOne.h"
#include "CurieIMU.h"

BLEService dataService("19C10000-E8F2-537E-4F6C-D104768A1214"); // BLE DataWrite Service

int notifyLength = 50; // maximum length of the notify string!
BLECharacteristic notifyCharacteristic("19C10001-E8F2-537E-4F6C-234235123113", BLERead | BLEWrite, notifyLength);

int startTime;
float ax, ay, az, gx, gy, gz;
float pinVal1, pinVal2;
bool newRead;
char printString[50];

//When triggered sample from the accelerometer, gyroscope, and analogPins and indicate newly read data
void samplingISR() {
  CurieIMU.readAccelerometerScaled(ax, ay, az);
  CurieIMU.readGyroScaled(gx, gy, gz);
  pinVal1 = analogRead(0);
  pinVal2 = analogRead(1);
  newRead = true;
}

//Setup
void setup() {
  Serial.begin(9600);
  CurieIMU.begin();
  CurieIMU.setGyroRange(250);
  CurieIMU.setAccelerometerRange(5);

  while(!Serial){};
  
  // begin initialization
  BLE.begin();

  // set advertised local name and service UUID:
  BLE.setAdvertisedServiceUuid(dataService.uuid());

  // add the characteristic to the service
  dataService.addCharacteristic(notifyCharacteristic);

  // add service
  BLE.addService(dataService);

  // no sampling has been done yet
  newRead = false;

  // start the timer to begin sampling
  CurieTimerOne.start(5000, &samplingISR);

  // starting time of sampling
  startTime = millis();

  // start advertising
  BLE.advertise();
}

void loop() {
  // listen for BLE peripherals to connect:
  BLEDevice central = BLE.central();

  // if a central is connected to peripheral:
  if (central) {
    Serial.print("Connected to central: ");
    // print the central's MAC address:
    Serial.println(central.address());

    // while the central is still connected to peripheral:
    while(central.connected()) {
      if(newRead) {
        sprintf(printString, "EMG 1(mv)=%.2f, EMG 2(mv)=%.2f\n", pinVal1, pinVal2);
        notifyCharacteristic.writeString(printString);
        sprintf(printString, "ax=%.2f, ay=%.2f, az=%.2f\n", ax, ay, az);
        notifyCharacteristic.writeString(printString);
        sprintf(printString, "gx=%.2f, gy=%.2f, gz=%.2f\n", gx, gy, gz);
        notifyCharacteristic.writeString(printString);
        newRead = false;
      }
    }

    // when the central disconnects, print it out:
    Serial.print(F("Disconnected from central: "));
    Serial.println(central.address());
  }
}

