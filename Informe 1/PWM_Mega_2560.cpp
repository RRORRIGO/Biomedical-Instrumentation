
#include <Arduino.h>
#include <math.h>

// Pin DAC del ESP32 clásico
const int dacPin = 25;

// Frecuencia de la señal senoidal
const float frecuencia = 2.0;

// Intervalo de actualización
const unsigned long intervalo = 2;

unsigned long tiempoAnterior = 0;

void setup() {
  // No se necesita pinMode() para dacWrite()
}

void loop() {
  unsigned long tiempoActual = millis();

  if (tiempoActual - tiempoAnterior >= intervalo) {
    tiempoAnterior = tiempoActual;

    // Tiempo en segundos
    float tiempo = tiempoActual / 1000.0;

    // Calcular seno
    float seno = sin(2.0 * PI * frecuencia * tiempo);

    // Convertir seno (-1 a 1) a DAC (0 a 255)
    int valorDAC = (int)(127.5 + 127.5 * seno);

    // Limitar el valor
    valorDAC = constrain(valorDAC, 0, 255);

    // Escribir salida analógica
    dacWrite(dacPin, valorDAC);
  }
}
