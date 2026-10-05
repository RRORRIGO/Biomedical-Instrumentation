#include <Arduino.h>
#include <math.h>
// Generación de señal
const int pinPWM = 9;
const float frecuencia = 2.0;
// Adquisición ADC
const int pinADC = A0;
// Temporización
unsigned long tiempoAnterior = 0;
const unsigned long intervalo = 5;
void setup() {
  pinMode(pinPWM, OUTPUT);
  Serial.begin(9600);
}
void loop() {

unsigned long ahora = millis();
if (ahora - tiempoAnterior >= intervalo)
{
    tiempoAnterior = ahora;
   // Generar PWM con envolvente senoidal de 2 Hz
    float t = ahora / 1000.0;
    float seno = sin(2.0 * PI * frecuencia * t);
    int valorPWM = 127.5 + 127.5 * seno;
    analogWrite(pinPWM, valorPWM);
    // Leer la señal acondicionada
    int lectura = analogRead(pinADC);
    // Conversión de ADC a voltios
    float voltaje = lectura * 5.0 / 1023.0;
    // Enviar el voltaje por comunicación serial
    Serial.println(voltaje, 3); 
}
}
