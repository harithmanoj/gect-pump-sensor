/*
 * Blink
 * Turns on an LED on for one second,
 * then off for one second, repeatedly.
 */

#include "Arduino.h"

static const uint8_t pressurePin = A0;

void setup()
{
  
  Serial.begin(9600);
}

void loop()
{
  Serial.println(analogRead(pressurePin));
  delay(1000);
}

