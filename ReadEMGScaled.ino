/*
 * Read EMG Raw data every 5000 microseconds (200Hz) convert
 * to scaled data and print to Serial
 */
#include "CurieTimerOne.h"

//startTime and analogPin, which are defined in setup
int startTime;
int analogPin;

/*last raw reading of analogPin retrieved by sample, 
 *time of each sampling relative to startTime
 *and flag for when a new reading has been retrieved
 */
int lastRawReading;
int timeSinceStart;
boolean newRead;

//Sampling ISR to be triggered by CurieTimerOne.
void sample() {
  lastRawReading = analogRead(analogPin);
  timeSinceStart = micros() - startTime;
  newRead = true;
}

//Sets up Serial, the sampling pin, startTime, newRead, and the timer.
void setup() {
  Serial.begin(115200);
  analogPin = 0;
  pinMode(0, INPUT);
  while(!Serial);
  newRead = false;
  CurieTimerOne.start(5000, &sample);
  startTime = micros();
}

//Prints out every sampled data value and the time of each sampling.
void loop() {
  if(newRead) {
    Serial.print("Last voltage reading: ");
    Serial.print(((lastRawReading * 3.3) / 1024.0 - 1.5) / 3600);
    Serial.print("V\tTime since start: ");
    Serial.print(timeSinceStart);
    Serial.println("microseconds");
    newRead = false;
  }
}
