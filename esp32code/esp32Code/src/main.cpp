
#include "Arduino.h"

constexpr uint8_t pressurePin = 34u;

constexpr uint8_t rawInputPin = 25u;
constexpr uint8_t firstOrderPin = 26u;
constexpr uint8_t secondOrderPin = 33u;
constexpr uint8_t thirdOrderPin = 32u;
constexpr uint8_t risePulse = 35u;
constexpr uint8_t fallPulse = 34u;

uint8_t tapCount = 1;
bool lastFallValue = false;
bool lastRiseValue = false;

auto led = HIGH;
unsigned int count = 0;

constexpr unsigned long frequency = 20;
constexpr unsigned long time_period = 1000 / frequency;
constexpr unsigned LED_BUILTIN = 2;

void setup()
{
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(risePulse, INPUT);
  pinMode(fallPulse, INPUT);
}

char line[30] = "";

void fill(long long value, char* ptrBuffer, std::size_t len)
{
  for(int i = 0; i < len; ++i)
  {
    ptrBuffer[len - i - 1] = '0' + (value % 10);
    value = value / 10;
  }
}

void loop()
{
  auto first = millis();
  digitalWrite(LED_BUILTIN, led);

  fill(analogRead(rawInputPin), line, 4);
  line[4] = ' ';

  fill(analogRead(firstOrderPin), line + 5, 4);
  line[9] = ' ';

  fill(analogRead(secondOrderPin), line + 10, 4);
  line[14] = ' ';

  fill(analogRead(thirdOrderPin), line + 15, 4);
  line[19] = ' ';

  auto fl = digitalRead(fallPulse);
  auto rs = digitalRead(risePulse);

  line[20] = '0' + fl;
  line[21] = ' ';

  line[22] = '0' + rs;
  line[23] = ' ';

  bool fallVal = (fl != 0)? true : false;
  bool riseVal = (rs != 0)? true : false;

  if((!lastFallValue) && fallVal)
  {
    tapCount += 1;
  }

  if((!lastRiseValue) && riseVal)
  {
    tapCount -= 1;
  }
  lastFallValue = fallVal;
  lastRiseValue = riseVal;


  fill(tapCount, line + 24, 3);
  line[27] = ' ';
  line[28] = ' ';
  line[29] = '\0';

  Serial.println(line);

  led = ((count % 40) > 28 ? HIGH : LOW);
  ++count;
  auto time_delay = time_period + first - millis();
  
  delay(time_delay);  
}