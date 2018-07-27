/***
 * Author: J Newland
 * 2018/07/27
 * 
 * Use the Adafruit Circuit Playground Express
 * to detect and display the pulse using an 
 * on-board LED and the on-board light sensor.
 ***/
#include "Adafruit_CircuitPlayground.h"

// Initialize variables.
int lightSensor = 0;
int ppg = 0;

void setup() {
  // How fast you read can make a difference.
  // Go as fast as your hardware can handle.
  Serial.begin(115200);
  Serial.println("Circuit Playground Express PPG");
  
  // Start the CPX
  CircuitPlayground.begin();

  // pick an LED and turn it on
  // You'll need to experiment with color
  <...>
}

void loop() {
  // Read the light sensor signal.
  lightSensor = <...>
  
  // Since this is reflective photoplethysmography,
  // we need to invert the signal to see the true waveform.
  <...> // 1024 is ths max value possible.

  // Print waveform to the serial console and plotter
  <...>
  
  // Delay to allow the sensor to reset.
  delay(20); 
}
