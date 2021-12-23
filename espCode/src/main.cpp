
#include "Arduino.h"

constexpr uint8_t pressurePin = A0;

auto led = HIGH;
int count = 0;

constexpr unsigned long frequency = 40;
constexpr unsigned long time_delay = 1000 / frequency;


char writeString[9] = "";

inline void writeToGlobalString(int analog, int val1, int val2)
{
  writeString[4] = ' ';
  writeString[6] = ' ';
  writeString[8] = '\0';

  writeString[0] = '0' + (analog / 1000);
  writeString[1] = '0' + ((analog / 100) % 10);
  writeString[2] = '0' + ((analog / 10) % 10);
  writeString[3] = '0' + (analog % 10);

  writeString[5] = '0' + val1;
  writeString[7] = '0' + val2;
}

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