
#include "Arduino.h"

constexpr uint8_t pressurePin = A0;

auto led = HIGH;
int count = 0;

constexpr unsigned long frequency = 40;
constexpr unsigned long time_delay = 1000 / frequency;


void setup()
{
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
  digitalWrite(LED_BUILTIN, led);

  Serial.println(analogRead(pressurePin));

  led = ((count % 40) > 28 ? HIGH : LOW);
  ++count;
  
  delay(time_delay);  
}