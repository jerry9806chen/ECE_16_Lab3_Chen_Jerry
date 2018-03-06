/*
 * Copyright (c) 2016 Intel Corporation.  All rights reserved.
 * See the bottom of this file for the license terms.
 */

/*
 * Sketch: LedControl.ino
 *
 * Description:
 *   This is a Central sketch that looks for a particular Sevice with a
 *   certain Characteristic from a Peripheral.  Upon succesful discovery,
 *   it reads the state of a button and write that value to the
 *   Peripheral Characteristic.
 *
 * Notes:
 *
 *  - Expected Peripheral Service: 19c10000-e8f2-537e-4f6c-d104768a1214
 *  - Expected Peripheral Characteristic: 19c10001-e8f2-537e-4f6c-d104768a1214
 *  - Expected Peripheral sketch:
 *
 */

#include <CurieBLE.h>

void setup() {
  Serial.begin(9600);
  while(!Serial){};
  Serial.println("BLE Central - Data Plotting");

  // initialize the BLE hardware
  BLE.begin();
  
  // start scanning for peripherals
  BLE.scanForUuid("19C10000-E8F2-537E-4F6C-D104768A1214");
}

void loop() {
  // check if a peripheral has been discovered
  BLEDevice peripheral = BLE.available();

  if (peripheral) {
    // discovered a peripheral, print out address, local name, and advertised service
    Serial.print("Found ");
    Serial.print(peripheral.address());
    Serial.print(" '");
    Serial.print(peripheral.localName());
    Serial.print("' ");
    Serial.print(peripheral.advertisedServiceUuid());
    Serial.println();

    // stop scanning
    BLE.stopScan();

    print_data(peripheral);

    // peripheral disconnected, start scanning again
    BLE.scanForUuid("19c10000-e8f2-537e-4f6c-d104768a1214");
  }
}

void print_data(BLEDevice peripheral) {
  // connect to the peripheral
  Serial.println("Connecting ...");

  if (peripheral.connect()) {
    Serial.println("Connected");
  } else {
    Serial.println("Failed to connect!");
    return;
  }

  // discover peripheral attributes
  Serial.println("Discovering attributes ...");
  if (peripheral.discoverAttributes()) {
    Serial.println("Attributes discovered");
  } else {
    Serial.println("Attribute discovery failed!");
    peripheral.disconnect();
    return;
  }

  // retrieve the Data transmission characteristic
  BLECharacteristic notifyCharacteristic = peripheral.characteristic("19C10001-E8F2-537E-4F6C-234235123113");

  if (!notifyCharacteristic) {
    Serial.println("Peripheral does not have Notify characteristic!");
    peripheral.disconnect();
    return;
  }
  
  while (peripheral.connected()) {
    // while the peripheral is connection
    if (notifyCharacteristic.canRead())
      notifyCharacteristic.read();
    Serial.println(notifyCharacteristic.stringValue());
  }

  Serial.println("Peripheral disconnected");
}
