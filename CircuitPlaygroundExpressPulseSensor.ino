/***
 * Author: J Newland
 * 2018/07/15
 * 
 * This sketch demonstrates manual, unfiltered,
 * plethysmography versus the amplified and 
 * low-pass filtered signal from the
 * Pulse Sensor Amped.
 * NOTE: The sensor is simply read directly
 *       rather than using the Pulse Sensor
 *       Amped library. This is as close to
 *       the raw signal as possible.
 ***/
#include "Adafruit_CircuitPlayground.h"

// The P.S. Amped should be have the "purple"
// (data) wire on A1.
int pulsePin = 1;  

// Initialize our data variables.
int pulseSignal = 0;
int lightSensor = 0;

void setup() {
  // How fast you read can make a difference.
  // Go as fast as your hardware can handle.
  Serial.begin(115200);
  Serial.println("Circuit Playground Express Pulse Sensor");
  
  // Start the CPX
  CircuitPlayground.begin();

  // Max brightness!
  CircuitPlayground.setBrightness(255); 

  // Green LED light works best for
  // photoplethysmography.
  CircuitPlayground.setPixelColor(1, 0, 255, 0);
  CircuitPlayground.strip.show();
}


void loop() {
  pulseSignal = analogRead(pulsePin);
  lightSensor = (CircuitPlayground.lightSensor())*1024.0/255.0;
  Serial.print(lightSensor);
  Serial.print("\t");
  Serial.println(pulseSignal);
  delay(20); 
}
