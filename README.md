# Biomedical-Instrumentation
 This repository contains the formal reports and documentation developed during the Biomedical Instrumentation course.

## Amplificador de Instrumentación Biomédico - Fuente y armado



### Resumen
En la presente experiencia se implementó y caracterizó una etapa de acondicionamiento analógico basada en un amplificador de instrumentación discreto de tres amplificadores operacionales (TL084N) alimentado por una fuente dual de  9V. Mediante la selección y apareo manual de resistencias se redujo la dispersión a 0.08 k, logrando un offset de salida de 0.000mV a -0.001mV con las entradas en corto. Para validar el funcionamiento, se sintetizó una bioseñal mediante un ESP32 (PWM filtrado a 2Hz y atenuado), obteniendo exitosamente una onda senoidal suave de 7.68mVpp, dentro del rango objetivo (5-15 mVpp) sin saturar la salida. 


## Amplificador de Instrumentación Biomédico — Caracterización y visualización

### Resumen
Se rearmó el amplificador de instrumentación de tres operacionales con TL084N y se midió su ganancia diferencial para cuatro valores de Rg (10007, 5023, 2520 y 2,4 Ω), comparándola con la teórica. Con las entradas unidas se midió la ganancia en modo común y se estimó el CMRR. Se incorporó una referencia de tierra virtual bufferizada con LM324N y un nodo sumador para adaptar la salida al ADC; esta etapa se simuló en Proteus con un Arduino Mega 2560. La ganancia aumentó al disminuir Rg, aunque siempre quedó por debajo de la teórica (con saturación en Rg = 2,4 Ω), y el CMRR estimado fue de unos 114 dB. La referencia entregó 2,5 V y la señal acondicionada se mantuvo dentro del rango del ADC.



