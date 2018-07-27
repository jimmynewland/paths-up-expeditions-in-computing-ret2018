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

  // Max brightness helps the signal strength.
  CircuitPlayground.setBrightness(255); 

  // Green LED light works best for photoplethysmography
  // and LED 1 (not 0) is closest to the on-board light sensor.
  CircuitPlayground.setPixelColor(1, 0, 255, 0);
  CircuitPlayground.strip.show();
}

void loop() {
  // Read the light sensor signal.
  lightSensor = CircuitPlayground.lightSensor();

  // Since this is reflective photoplethysmography,
  // we need to invert the signal to see the true waveform.
  ppg = 1024 - lightSensor; // 1024 is ths max value possible.

  // Print waveform to the serial console and plotter
  Serial.println(ppg);
  
  // Delay to allow the sensor to reset.
  delay(20); 
}
