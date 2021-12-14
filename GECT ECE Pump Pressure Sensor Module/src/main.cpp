
#include "Arduino.h"

constexpr uint8_t pressurePin = A0;

bool led = true;
int count = 0;

void setup()
{
  Serial.begin(9600);
  pinMode(BUILTIN_LED, OUTPUT);
}

void loop()
{
  digitalWrite(BUILTIN_LED, (led ? HIGH : LOW));
  Serial.println(analogRead(pressurePin));
  led = ((count % 40) > 28 ? true : false);
  ++count;
  delay(25);
  
}