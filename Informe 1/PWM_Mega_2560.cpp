#include <Arduino.h>
#include <math.h>

// Pin PWM seleccionado
const int pwmPin = 25;

// Frecuencia de variación de la señal (Hz)
const float frecuencia = 2.0;

// Intervalo de actualización del PWM (ms)
const unsigned long intervalo = 5;

unsigned long tiempoAnterior = 0;

void setup() {
  pinMode(pwmPin, OUTPUT);
}

void loop() {
  unsigned long tiempoActual = millis();

  // Actualizar PWM cada 5 ms
  if (tiempoActual - tiempoAnterior >= intervalo) {
    tiempoAnterior = tiempoActual;

    // Tiempo transcurrido en segundos
    float tiempo = tiempoActual / 1000.0;

    // Calcular fase de la función seno
    float fase = 2.0 * PI * frecuencia * tiempo;

    // Función seno: rango -1 a 1
    float seno = sin(fase);

    // Convertir a rango 0-255
    int duty = (int)(127.5 + 127.5 * seno);

    // Asegurar que el valor esté dentro del rango permitido
    duty = constrain(duty, 0, 255);

    // Aplicar ciclo de trabajo PWM
    analogWrite(pwmPin, duty);
  }
}