#include "HX711.h"
#include <ArduinoJson.h>

// HX711 circuit wiring
#define LOADCELL_DOUT_PIN_1 2
#define LOADCELL_SCK_PIN_1 3
#define LOADCELL_DOUT_PIN_2 4
#define LOADCELL_SCK_PIN_2 5
#define LOADCELL_DOUT_PIN_3 6
#define LOADCELL_SCK_PIN_3 7
#define LOADCELL_DOUT_PIN_4 8
#define LOADCELL_SCK_PIN_4 9
#define LOADCELL_DOUT_PIN_5 10
#define LOADCELL_SCK_PIN_5 11



long read_1=0;
long read_2=0;
long read_3=0;
long read_4=0;
long read_5=0;
long read_6=0;
long read_7=0;
long read_8=0;
long read_9=0;

HX711 scale_1;
HX711 scale_2;
HX711 scale_3;
HX711 scale_4;
HX711 scale_5;
// HX711 scale_6;
// HX711 scale_7;
// HX711 scale_8;
// HX711 scale_9;

void setup() {
  Serial.begin(115200);
  pinMode(13,OUTPUT);
  digitalWrite(13,LOW);
  scale_1.begin(LOADCELL_DOUT_PIN_1, LOADCELL_SCK_PIN_1);
  scale_2.begin(LOADCELL_DOUT_PIN_2, LOADCELL_SCK_PIN_2);
  scale_3.begin(LOADCELL_DOUT_PIN_3, LOADCELL_SCK_PIN_3);
  scale_4.begin(LOADCELL_DOUT_PIN_4, LOADCELL_SCK_PIN_4);
  scale_5.begin(LOADCELL_DOUT_PIN_5, LOADCELL_SCK_PIN_5);
  // scale_6.begin(LOADCELL_DOUT_PIN_6, LOADCELL_SCK_PIN_6);
  // scale_7.begin(LOADCELL_DOUT_PIN_7, LOADCELL_SCK_PIN_7);
  // scale_8.begin(LOADCELL_DOUT_PIN_8, LOADCELL_SCK_PIN_8);
  // scale_9.begin(LOADCELL_DOUT_PIN_9, LOADCELL_SCK_PIN_9);
}

void loop() {
  // Create a JSON object
  StaticJsonDocument<200> doc;
  read_1 = scale_1.read();
  read_2 = scale_2.read();
  read_3 = scale_3.read();
  read_4 = scale_4.read();
  read_5 = scale_5.read();
  // read_6 = scale_6.read();
  // read_7 = scale_7.read();
  // read_8 = scale_8.read();
  // read_9 = scale_9.read();
  
  doc["celda_1"] = read_1;
  doc["celda_2"] = read_2;
  doc["celda_3"] = read_3;
  doc["celda_4"] = read_4;
  doc["celda_5"] = read_5;
  doc["celda_6"] = read_6;
  doc["celda_7"] = read_7;
  doc["celda_8"] = read_8;
  doc["celda_9"] = read_9;

  // Serialize JSON to Serial
  serializeJson(doc, Serial);
  Serial.println();
}