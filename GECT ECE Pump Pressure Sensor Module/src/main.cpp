
#include "Arduino.h"

constexpr uint8_t pressurePin = A0;

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  Serial.println(analogRead(pressurePin));
  delay(100);
  
}