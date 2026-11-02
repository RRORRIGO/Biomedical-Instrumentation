#include "semg.h"

// Pin DAC del ESP32
const int DAC_PIN = 25;

// Periodo de muestreo en microsegundos
// 1 / 2048 Hz = 488.28125 us
const uint32_t PERIODO_US = 1000000UL / FS_SEMG;

// Índice de la muestra actual
uint32_t i = 0;

// Instante programado para la siguiente muestra
uint32_t siguienteTiempo = 0;

void setup() {

  // Inicializamos el instante de referencia
  siguienteTiempo = micros();
}

void loop() {

  uint32_t ahora = micros();

  // Verificamos si ya llegó el momento
  // de enviar la siguiente muestra
  if ((int32_t)(ahora - siguienteTiempo) >= 0) {

    // Enviar muestra al DAC del ESP32
    dacWrite(DAC_PIN, SEMG[i]);

    // Pasar a la siguiente muestra
    i++;

    // Si llegamos al final,
    // regresamos al inicio
    if (i >= N_SEMG) {
      i = 0;
    }

    // Programamos el siguiente instante
    siguienteTiempo += PERIODO_US;
  }
}
