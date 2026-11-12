#include <Arduino.h>
#include "esp_timer.h"

// ==========================================
// OSCILOSCOPIO DC - ESP32-S3 N16R8
// DOS CANALES: CH1 Y CH2
// ==========================================

#define CH1_PIN 4
#define CH2_PIN 5

#define BAUD_RATE 230400

// 500 muestras por segundo
const uint32_t SAMPLE_PERIOD_US = 2000;

// Factor de correccion del divisor
// 1.0 = conexion directa
// 1.5 = divisor 10k / 20k en cada canal
const float FACTOR_CH1 = 1.0;
const float FACTOR_CH2 = 1.0;

int64_t nextSample = 0;

void setup() {

  Serial.begin(BAUD_RATE);

  analogReadResolution(12);

  analogSetPinAttenuation(CH1_PIN, ADC_11db);
  analogSetPinAttenuation(CH2_PIN, ADC_11db);

  delay(1500);

  nextSample = esp_timer_get_time();
}

void loop() {

  int64_t now = esp_timer_get_time();

  if (now >= nextSample) {

    nextSample += SAMPLE_PERIOD_US;

    // Evitar acumulacion de retrasos
    if (now - nextSample > SAMPLE_PERIOD_US) {
      nextSample = now + SAMPLE_PERIOD_US;
    }

    // Lecturas ADC calibradas
    uint32_t adc1 = analogReadMilliVolts(CH1_PIN);
    uint32_t adc2 = analogReadMilliVolts(CH2_PIN);

    float voltage1 = (adc1 / 1000.0) * FACTOR_CH1;
    float voltage2 = (adc2 / 1000.0) * FACTOR_CH2;

    // Marca temporal en microsegundos
    uint64_t timestamp = (uint64_t)esp_timer_get_time();

    // Formato: tiempo_us,CH1,CH2
    Serial.printf(
      "%llu,%.4f,%.4f\n",
      (unsigned long long)timestamp,
      voltage1,
      voltage2
    );
  }
}