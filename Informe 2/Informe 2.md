
<center>
### **UNIVERSIDAD NACIONAL MAYOR DE SAN MARCOS** 

##### **FACULTAD DE INGENIERÍA ELECTRÓNICA Y ELÉCTRICA** 

##### **ESCUELA PROFESIONAL DE INGENIERÍA BIOMÉDICA** 

**INSTRUMENTACIÓN BIOMÉDICA I** 

# **INFORME DE LABORATORIO N.° 2** 

_Amplificador de Instrumentación Biomédico — Caracterización y visualización_ 

#### **Integrantes** 

|**N.°**|**Apellidos y nombres**|**Código**|
|---|---|---|
|1|Leal Yopla Carlos Rodrigo|24190292|
|2|Mamani Chavez Lizbeth Rocio|24190105|
|3|Gironzini Córdova, Enrico Salvatore|23190373|



**Grupo / horario:** Grupo A: 8 - 10 pm 

**Fecha:** 14 de septiembre de 2026 

**Docente:** Maria Elisia Armas Alvarado 

</center>



## **1. Resumen** 

Se rearmó el amplificador de instrumentación de tres operacionales con TL084N y se midió su ganancia diferencial para cuatro valores de Rg (10007, 5023, 2520 y 2,4 Ω), comparándola con la teórica. Con las entradas unidas se midió la ganancia en modo común y se estimó el CMRR. Se incorporó una referencia de tierra virtual bufferizada con LM324N y un nodo sumador para adaptar la salida al ADC; esta etapa se simuló en Proteus con un Arduino Mega 2560. La ganancia aumentó al disminuir Rg, aunque siempre quedó por debajo de la teórica (con saturación en Rg = 2,4 Ω), y el CMRR estimado fue de unos 114 dB. La referencia entregó 2,5 V y la señal acondicionada se mantuvo dentro del rango del ADC. 

## **2. Objetivos** 

- Rearmar el amplificador de instrumentación verificado en el Laboratorio N.° 1. 

- Medir la ganancia diferencial del AI para al menos cuatro valores de Rg y contrastarla con el valor teórico. 

- Estimar el CMRR del AI a partir de la ganancia diferencial máxima y la ganancia en modo común medidas. 

- Acondicionar la salida del AI mediante una referencia de tierra virtual bufferizada con el LM324N. 

- Visualizar en tiempo real la señal acondicionada mediante el Serial Plotter del microcontrolador. 

## **3. Marco teórico y contexto de aplicación** 

En la experiencia anterior se implementó un amplificador de instrumentación de tres amplificadores operacionales con el TL084N. El presente laboratorio permite caracterizar su ganancia y su capacidad de rechazo al modo común, además de incorporar una referencia de tierra virtual bufferizada para adaptar la señal amplificada al rango de entrada del convertidor analógico-digital (ADC). 

**_(a) Ganancia diferencial y rechazo al modo común (CMRR)_** 

La ganancia diferencial expresa la capacidad del amplificador de incrementar la diferencia de potencial existente entre sus dos entradas, mientras que la ganancia en modo común representa la amplificación no deseada de las señales presentes simultáneamente en ambas entradas. La relación de rechazo al modo común (CMRR) cuantifica la capacidad del circuito para discriminar entre ambas componentes y se expresa en decibelios mediante: 



Donde 𝐴𝑑 es la ganancia diferencial y 𝐴𝑐𝑚 es la ganancia en modo común. 

Este parámetro es especialmente importante en la adquisición de bioseñales, debido al acoplamiento electromagnético de la red eléctrica a 50/60 Hz, que puede introducir interferencias de amplitud considerablemente superior a la señal fisiológica de interés. Un CMRR elevado permite atenuar esta componente común y evitar que comprometa la medición o provoque la saturación de etapas posteriores. Según Texas Instruments, el apareamiento de los componentes externos también influye en el rechazo efectivo al modo común del circuito. 

En el amplificador implementado, la ganancia diferencial se modifica mediante la resistencia 𝑅𝑔, de acuerdo con la expresión: 



Por ello, la caracterización experimental considera diferentes valores de 𝑅𝑔 y compara la ganancia teórica con la obtenida a partir de las amplitudes pico a pico de entrada y salida. Posteriormente, la medición de la ganancia en modo común permite estimar el CMRR del amplificador construido. 





##### **_(b) Referencia de tierra virtual bufferizada y adaptación al ADC_** 

El amplificador de instrumentación alimentado con una fuente dual de ±9 V puede entregar una señal bipolar, con valores positivos y negativos respecto a tierra. Sin embargo, el ADC de los microcontroladores utilizados en la experiencia admite únicamente tensiones positivas dentro de su rango de operación. Por este motivo, es necesario acondicionar la señal mediante un desplazamiento de nivel de continua (DC level shifting), que permita digitalizarla sin perder su componente negativa. Este procedimiento se utiliza en circuitos de adquisición con alimentación unipolar, como describe Texas Instruments en su diseño de referencia TIPD154. 

En el laboratorio se utiliza el LM324N para implementar una referencia de tierra virtual mediante un divisor resistivo de 10 kΩ y un amplificador operacional configurado como seguidor de tensión. El divisor proporciona una tensión intermedia de aproximadamente 1,65 V para ESP32. El seguidor actúa como buffer, proporcionando una elevada impedancia de entrada y una baja impedancia de salida, con el propósito de mantener estable la referencia frente a las cargas conectadas. 

La salida del amplificador de instrumentación se combina con esta referencia mediante una red resistiva, de modo que la señal resultante permanezca dentro del intervalo admitido por el ADC. Así, es posible digitalizarla y visualizarla en tiempo real mediante el Serial Plotter del Arduino IDE, comparando su comportamiento con la forma de onda observada en el osciloscopio. 

## **4. Desarrollo experimental** 

### **Diagrama de bloques** 



_Figura 1. Diagrama de bloques_ 

La señal sinusoidal generada por el ESP32 pasa primero por un filtro RC y un divisor atenuador para reducir su amplitud. Luego, la señal es amplificada mediante el amplificador de instrumentación y acondicionada en el nodo sumador utilizando una referencia de tierra virtual. Finalmente, la señal resultante ingresa al ADC del microcontrolador para su digitalización y posterior visualización. 



**Esquemático del montaje** 





_Figura 2: Circuito amplificador de instrumentación simulado en Proteus._ 



_Figura 3. Circuito amplificador de instrumentación y nodo sumador simulado en Proteus._ 

### **Fotografía del montaje** 





_Figura 4. Vista general del montaje experimental del amplificador de instrumentación._ 

En la Figura 4 se muestra el montaje experimental, el cual comprende un amplificador de instrumentación de tres etapas basado en el TL084N, implementado en el Laboratorio N.º 1 y reconstruido para su caracterización eléctrica. El circuito se alimentó mediante una fuente de banco de ±9 V y recibió una señal de prueba generada por el microcontrolador, filtrada y atenuada para simular una bioseñal de baja amplitud. 

Para evaluar su funcionamiento, se emplearon un osciloscopio y un multímetro, que permitieron medir las amplitudes de entrada y salida, ajustar la resistencia de ganancia (Rg) y determinar el rechazo al modo común. Posteriormente, se incorporó el LM324N para generar una referencia de tierra virtual bufferizada y acondicionar la señal de salida antes de su adquisición y visualización mediante el Serial Plotter. 

### **Etapa A — Rearmado del circuito e incorporación del LM324N** 

Para el rearmado primero, se configuró la fuente de banco en modo dual ( _tracking_ ) para obtener una alimentación de ±9 V, estableciendo inicialmente un límite de corriente bajo para proteger los componentes frente a posibles errores de conexión. Antes de energizar el circuito, se verificaron con el multímetro las tensiones de +9 V y −9 V respecto a la tierra común (GND). 

Posteriormente, se rearmó el amplificador de instrumentación de tres amplificadores operacionales basado en el TL084N, conservando la configuración del Laboratorio N.º 1 y las se seleccionaron nuevas resistencias apareadas. Se conectaron ambas entradas, V1 y V2, a GND para comprobar que la tensión de salida, medida en el pin 8, permaneciera cercana a 0 V, considerando que pueden presentarse pequeñas desviaciones debido al voltaje de offset de los amplificadores operacionales. 

Asimismo, se reconstruyó el generador de señal de prueba mediante el microcontrolador ESP32, programado para producir una señal PWM con envolvente senoidal de 2 Hz. Esta señal se acondicionó mediante un filtro RC de 1 kΩ y 10 µF, seguido de un divisor resistivo de 1 kΩ y 10 Ω, con el propósito de obtener una señal de baja amplitud que simulara una bioseñal. 

Finalmente, se incorporó el LM324N, conectando su pin 4 a +9 V y su pin 11 a −9 V. Se añadieron dos capacitores cerámicos de 100 nF para el desacople de su alimentación, con el fin de reducir perturbaciones eléctricas y favorecer la estabilidad del circuito. De esta manera, se preparó el montaje para las posteriores etapas de caracterización y acondicionamiento de la señal. 





Figura 5. Valores reales de las resistencias apareadas. 







_Figura 6: Medición de voltaje  +9V - GND_ 

_Figura 7: Medición de voltaje -9 V - GND_ 

### **Etapa B — Caracterización de la ganancia** 

Se identificaron los terminales del amplificador de instrumentación TL084N, utilizando el pin 3 como entrada no inversora (V1), el pin 5 como segunda entrada (V2) y el pin 8 como salida (Vout). Se conectó la señal de prueba atenuada a V1 y se mantuvo V2 conectada a GND. 

Para caracterizar la ganancia diferencial, se seleccionaron cuatro posiciones del potenciómetro Rg, incluyendo sus extremos y dos posiciones intermedias, con el propósito de evaluar la variación de la ganancia en función de la resistencia. Se registraron los valores ajustados y las lecturas obtenidas con el circuito desenergizado. Para el cálculo de la ganancia se consideró la ecuación II el valor promedio de R1 y R1’ siendo este igual a 9.82k Ω . 

**Tabla 1. Caracterización de la ganancia diferencial del AI.** 

|**Rg real**<br>**(Ω)**|**Vin(pp)**<br>**(mV)**|**Vout(pp)**<br>**(mV)**|**Ganancia**<br>**experimental**|**Ganancia**<br>**teórica**|**Observaciones**|
|---|---|---|---|---|---|
|10007|31.2|51.2|1.64|2.962|Ganancia mínima medida; salida inferior a la esperada.|
|5023|26|84|3.23|4.91|Amplificación observable, con ganancia inferior a la teórica.|
|2520|28|149|5.32|8.793|Aumento de la ganancia al disminuir Rg; resultado inferior al<br>teórico.|
|2.4|32|17400|543.75|8184.333|Probable saturación por la elevada ganancia; salida próxima al<br>límite de alimentación.|





Cuando 𝑅𝑔 = 10 007Ω 





_Figura 8. Medición en el osciloscopio de los voltaje pico-pico de Vin y Vout para Rg = 10007 Ohm_ 

- Cuando 𝑅𝑔 = 5023Ω 



_Figura 9. Medición en el osciloscopio de los voltaje pico-pico de Vin y Vout para Rg = 5023 Ohm_ 





- Cuando 𝑅𝑔 = 2520Ω 



_Figura 10. Medición en el osciloscopio de los voltaje pico-pico de Vin y Vout para Rg = 2520 Ohm_ 

- Cuando 𝑅𝑔 = 2, 4Ω 



_Figura 11. Medición en el osciloscopio de los voltaje pico-pico de Vin y Vout para Rg = 2.4 Ohm_ 





**Etapa C — Prueba de rechazo en modo común (CMRR)** Para evaluar la capacidad de rechazo al modo común del amplificador de instrumentación, se ajustó la resistencia 𝑅𝑔 a 2,4 Ω, correspondiente a la configuración de mayor ganancia utilizada en la etapa B. Posteriormente, se desconectó la señal diferencial y se unieron las entradas V1 (pin 3) y V2 (pin 5) del TL084N, aplicando a ambas la misma señal procedente del filtro RC, antes del divisor atenuador. 

Se utilizó el osciloscopio para medir el voltaje pico a pico de la señal de entrada común y el voltaje residual en la salida del amplificador (pin 8). 

La ganancia en modo común se determinó mediante la relación: 



Posteriormente, se calculó la relación de rechazo al modo común (CMRR), expresada en decibelios mediante la ecuación I. 

**Tabla 2. Ganancia en modo común y cálculo de CMRR.** 

|**Medición**|**Valor**|**Observaciones**|
|---|---|---|
|Ganancia diferencial máxima|543.75|Obtenida con Rg = 2,4 Ω; posible saturación.|
|(Tabla 1, Rg mínimo)|||
|Vin(pp)modo común|4.5 V|Señal aplicada simultáneamente a ambas entradas.|
|Vout(pp)modo común|4.86 mV|Señal residual de baja amplitud.|
|Ganancia en modo común|0.00108|Atenuación considerable de la señal común.|
|CMRR (dB)|114,039|Valor calculado, condicionado por la posible saturación en la<br>medición diferencial.|





_Figura 12. Medición en el osciloscopio de los voltaje pico-pico de Vin y Vout para Rg = 2.4 Ohm, configuración modo común (pin 3 y pin 5)_ 





### **Etapa D — Acondicionamiento final y visualización en PC** 

Debido a que esta etapa no pudo completarse durante la sesión presencial con el ESP32, se realizó una simulación complementaria en Proteus utilizando un Arduino Mega 2560, alternativa contemplada en la guía de laboratorio. Se conservó la configuración del amplificador de instrumentación basado en el TL084N y se incorporó el LM324N para acondicionar la señal antes de su adquisición digital. 

Inicialmente, se implementó una referencia de tierra virtual mediante un divisor resistivo de dos resistencias de 10 kΩ conectadas entre los 5 V del Arduino Mega y GND. El punto medio del divisor, con una tensión nominal de 2,5 V, se conectó a un amplificador operacional del LM324N configurado como seguidor de tensión, con el propósito de obtener una referencia bufferizada de baja impedancia. 

Posteriormente, se construyó el nodo sumador mediante dos resistencias adicionales de 10 kΩ: una conectada a la salida del TL084N (pin 8) y otra a la referencia bufferizada del LM324N (pin 1). El punto de unión de ambas resistencias se conectó a la entrada analógica A0 del Arduino Mega, compartiendo la tierra común del circuito. Esta configuración permite desplazar la señal bipolar hacia valores positivos y reducir su amplitud para adaptarla al rango de entrada del ADC. 

Se empleó el osciloscopio virtual para observar la forma de onda acondicionada y comprobar que permaneciera dentro del intervalo de 0 a 5 V, sin recortes. Finalmente, se programó el Arduino Mega para generar una señal PWM con envolvente senoidal de 2 Hz mediante el pin digital 9 y adquirir simultáneamente la señal acondicionada a través de A0. Las lecturas se convirtieron a voltios y se transmitieron por comunicación serial a 9600 baudios, utilizando el Virtual Terminal de Proteus para comprobar la adquisición digital. 

Código del Arduino Mega: 

|#include <Arduino.h>|unsigned long ahora = millis();|
|---|---|
|#include <math.h>|if (ahora - tiempoAnterior >= intervalo)|
|// Generación de señal|{|
|const int pinPWM = 9;|tiempoAnterior = ahora;|
|const float frecuencia = 2.0;|// Generar PWM con envolvente senoidal de 2 Hz|
|// Adquisición ADC|float t = ahora / 1000.0;|
|const int pinADC = A0;|float seno = sin(2.0 * PI * frecuencia * t);|
|// Temporización|int valorPWM = 127.5 + 127.5 * seno;|
|unsigned long tiempoAnterior = 0;|analogWrite(pinPWM, valorPWM);|
|const unsigned long intervalo = 5;|// Leer la señal acondicionada|
|void setup() {|int lectura = analogRead(pinADC);|
|pinMode(pinPWM, OUTPUT);|// Conversión de ADC a voltios|
|Serial.begin(9600);|float voltaje = lectura * 5.0 / 1023.0;|
|}|// Enviar el voltaje por comunicación serial|
|void loop() {|Serial.println(voltaje, 3);<br>}}|





**Tabla 3. Verificación de la referencia bufferizada y del nodo sumador.** 



|**Medición**|**Valor esperado **|**Valor medido**|**Observaciones**|
|---|---|---|---|
|Salida del buffer respecto<br>a GND|<br>2.5V|2.5V|Coincide con el valor teórico, lo que verifica el<br>funcionamiento de la referencia bufferizada.|
|Rango del nodo sumador<br>(verificado con<br>osciloscopio, sin recorte)|0-5V|0-1.251 V|La tensión máxima se encuentra dentro del rango<br>permitido por el ADC del Arduino Mega.|





_Figura 13. Simulación de la salida del nodo sumador en osciloscopio virtual en Proteus._ 



_Figura 14. Simulación del Serial Plotter del Arduino Mega en Proteus._ 





## **5. Resultados y discusión** 

- A partir de la Tabla 1, comparar la ganancia experimental con la ganancia teórica (G = 1 + 2·R1/Rg) para cada valor de Rg y discutir a qué se atribuyen las diferencias observadas (tolerancia de R1/R1', offset del TL084N, impedancia de entrada del osciloscopio, resolución de la medición de Rg, entre otros). 

A partir de los resultados obtenidos en la Tabla 1, se observa que la ganancia experimental aumentó a medida que se disminuyó el valor de la resistencia 𝑅𝑔, lo cual coincide con el comportamiento 

esperado según la expresión: 



considerando un valor promedio de 𝑅1 y 𝑅1' de aproximadamente 9.82 kΩ. Sin embargo, los valores experimentales resultaron menores que los valores teóricos en las cuatro mediciones realizadas. 

Para 𝑅𝑔 = 10007Ω , se obtuvo una ganancia experimental de 1.64 frente a una ganancia teórica de 2.962. Esto representa una diferencia aproximada de 44.6 %. Para 𝑅𝑔 = 5023Ω , la ganancia experimental fue de 3.23 y la teórica de 4.91, obteniéndose una diferencia aproximada de 34.2 %. En el caso de 𝑅𝑔 = 2520Ω , se obtuvo experimentalmente una ganancia de 5.32 mientras que el valor teórico fue de 8.793, con una diferencia de aproximadamente 39.5 %. 

La mayor diferencia ocurrió cuando 𝑅𝑔 = 2. 4Ω . En este caso la ganancia teórica calculada fue aproximadamente 8184.33, mientras que experimentalmente se obtuvo solamente 543.75. Esta diferencia no significa necesariamente que el circuito estuviera funcionando incorrectamente, sino que para una ganancia tan elevada la salida quedó limitada por la tensión de alimentación de ±9 V. Es decir, el amplificador entró en saturación y ya no podía seguir amplificando proporcionalmente la señal de entrada. Esto también se observa en la Figura 11, donde la señal de salida presenta deformación y recorte. Laboratorio 2 

Las diferencias entre los valores teóricos y experimentales pueden atribuirse a varios factores. En primer lugar, las resistencias reales no tienen exactamente su valor nominal, por lo que incluso después de aparearlas existe un pequeño desajuste entre ellas. Además, el TL084N presenta una tensión de offset de entrada y características no ideales que pueden afectar el comportamiento del circuito. También influyen la precisión del osciloscopio al medir amplitudes pequeñas, la resolución del multímetro utilizado para medir 𝑅𝑔, las resistencias internas y contactos de la protoboard, y posibles variaciones de la señal de entrada. 

Por lo tanto, aunque experimentalmente no se alcanzaron exactamente los valores teóricos, sí se comprobó la tendencia principal del amplificador: cuando disminuye 𝑅𝑔, aumenta la ganancia diferencial. 

- Describir las dificultades experimentales encontradas al medir y mantener estable el valor de Rg durante las cuatro mediciones (por ejemplo, desajuste del potenciómetro al manipularlo) y explicar cómo esto pudo afectar la comparación entre la ganancia experimental y la ganancia teórica registrada en la Tabla 1. 

Una de las principales dificultades experimentales fue ajustar y mantener estable el valor de la resistencia 𝑅𝑔, especialmente porque se utilizó un potenciómetro. Al manipularlo para medir su resistencia con el multímetro o volver a conectarlo al circuito, era posible modificar ligeramente su posición. 





Este problema se vuelve especialmente importante para valores pequeños de 𝑅𝑔. Debido a que la ganancia depende inversamente de esta resistencia, una variación aparentemente pequeña puede generar un cambio considerable en la ganancia teórica. Por ejemplo, cuando 𝑅𝑔 se encuentra alrededor de algunos ohmios, una variación de solo uno o dos ohmios representa porcentualmente un cambio muy grande. 

Además, para realizar la medición correcta de 𝑅𝑔 era necesario desenergizar el circuito, medir la resistencia y posteriormente volver a conectarlo. Durante ese proceso podían aparecer cambios en las conexiones de la protoboard o en la posición del potenciómetro. El propio informe indica que las mediciones de 𝑅𝑔 se realizaron con el circuito desenergizado. Laboratorio 2 

Por esta razón, es posible que el valor real de 𝑅𝑔 durante la medición de la señal no fuera exactamente igual al valor registrado previamente con el multímetro. Esto contribuiría a explicar parte de la diferencia entre la ganancia experimental y la ganancia teórica. 

Una mejora para futuros experimentos sería reemplazar el potenciómetro por resistencias fijas medidas previamente, o utilizar un potenciómetro multivuelta que permita realizar ajustes más precisos y estables. 

- A partir de la Tabla 2, indicar el valor de CMRR obtenido y discutir si es consistente con lo esperable para un amplificador discreto de resistencias apareadas manualmente frente a un CMRR típico de un IA integrado. 

En la prueba de rechazo en modo común se obtuvo una señal de entrada común de 4.5 Vpp y una señal residual de salida de aproximadamente 4.86 mVpp. A partir de estos valores se calculó: 



Utilizando la ganancia diferencial máxima experimental de 543.75 se obtuvo: 



Este es el valor reportado en la Tabla 2. 

A primera vista, un CMRR de aproximadamente 114 dB representa una capacidad de rechazo al modo común bastante alta. Sin embargo, debe interpretarse con precaución. El valor de ganancia diferencial utilizado para calcularlo corresponde a la configuración con 𝑅𝑔 = 2. 4Ω , donde ya existían evidencias de saturación de la salida. Por lo tanto, la ganancia diferencial utilizada no representa completamente una región lineal de funcionamiento. 

También debe considerarse que el amplificador fue construido de manera discreta utilizando resistencias apareadas manualmente. En este tipo de circuito el CMRR real depende mucho de qué tan iguales sean las relaciones entre las resistencias de la etapa diferencial. Incluso diferencias pequeñas pueden reducir de forma importante el rechazo al modo común. 

Un amplificador de instrumentación integrado normalmente puede obtener un CMRR elevado de manera más consistente debido a que las resistencias internas son fabricadas y ajustadas con tolerancias mucho menores que las que podemos conseguir manualmente en una protoboard. 

Por esta razón, aunque el valor calculado de 114 dB es favorable, no sería correcto asumir que el 





circuito discreto presenta realmente ese CMRR en todas las condiciones de operación. Se trata principalmente de una estimación experimental condicionada por las mediciones realizadas. 

- Explicar qué ocurriría con una bioseñal real si el CMRR del amplificador fuera insuficiente frente a una interferencia de red de 50/60 Hz, considerando que dicha interferencia suele ser mucho mayor que la señal diferencial útil. 

En la adquisición de bioseñales, como ECG o EMG, la señal diferencial que se desea medir puede presentar amplitudes bastante pequeñas, mientras que las interferencias externas pueden tener amplitudes mucho mayores. 

Una de las interferencias más comunes es la señal de la red eléctrica de 50 o 60 Hz. Esta interferencia puede acoplarse al cuerpo humano, los electrodos y los cables de medición. El propio informe menciona que este fenómeno constituye una de las principales razones por las cuales se requiere un CMRR elevado en instrumentación biomédica.     Laboratorio 2 

Si el amplificador tuviera un CMRR insuficiente, parte importante de esa señal común aparecería amplificada en la salida. Como consecuencia, podrían ocurrir varios problemas. 

La primera consecuencia sería observar una componente sinusoidal de 50/60 Hz superpuesta a la bioseñal. En un ECG, por ejemplo, esta interferencia podría dificultar la identificación correcta de las ondas P, QRS y T. 

Además, si la señal de modo común es suficientemente grande, la salida del amplificador puede saturarse incluso antes de amplificar correctamente la bioseñal de interés. En ese caso se perdería información y posteriormente ya no sería posible recuperarla solamente mediante procesamiento digital. 

Por esto, el CMRR constituye una característica crítica en un sistema biomédico. No solamente mejora la calidad visual de la señal, sino que ayuda a evitar que las interferencias ambientales oculten una señal fisiológica que puede encontrarse en el orden de microvoltios o milivoltios. 

- A partir de la Tabla 3, comparar el valor medido de la referencia bufferizada con el valor esperado y explicar qué ocurriría con la señal digitalizada si esta referencia no estuviera bien centrada o no estuviera bufferizada. 

La función de esta referencia es desplazar la señal bipolar proveniente del amplificador de instrumentación hacia una región positiva compatible con el ADC. Como el Arduino Mega solamente puede digitalizar tensiones aproximadamente comprendidas entre 0 y 5 V, una señal con valores negativos no podría aplicarse directamente. 

Si la referencia no estuviera correctamente centrada, la señal podría desplazarse demasiado hacia 0 V o demasiado hacia 5 V. Como consecuencia, una parte de la forma de onda podría superar los límites del ADC y producir recorte. 

Por ejemplo, si la referencia fuese demasiado pequeña, los semiciclos negativos podrían quedar por debajo de 0 V. Si fuese demasiado elevada, los valores positivos podrían acercarse o superar los 5 V. 

Por otro lado, si se utilizara directamente el divisor resistivo sin buffer, su tensión podría cambiar al conectarle una carga. Esto ocurre porque el divisor presenta una impedancia de salida distinta de cero. Al conectar el nodo sumador, aparecería un nuevo camino de corriente que modificaría el valor del divisor. 

El seguidor con LM324N evita este problema porque presenta una impedancia de entrada elevada y una impedancia de salida relativamente baja. De esta manera, la referencia puede mantenerse mucho más estable frente a las etapas posteriores. 

- Comparar la forma de onda observada en el osciloscopio con la señal digitalizada en el Serial Plotter: describir diferencias en resolución temporal y de amplitud, y su relación con la tasa de muestreo empleada en el código. 

La forma de onda observada en el osciloscopio presenta una representación más continua y detallada que la obtenida mediante la adquisición digital. El osciloscopio posee una frecuencia de muestreo considerablemente mayor y está diseñado específicamente para visualizar señales 





eléctricas con alta resolución temporal. 

En cambio, en el programa utilizado para el Arduino Mega se realiza una lectura cada 5 ms: 



por lo que la frecuencia máxima programada de adquisición es aproximadamente: 



El código efectivamente establece un intervalo de 5 ms entre adquisiciones. Laboratorio 2 

Por lo tanto, el Serial Plotter recibe como máximo aproximadamente 200 muestras por segundo, aunque en la práctica esta frecuencia puede ser ligeramente menor debido al tiempo necesario para realizar analogRead(), convertir el dato y transmitirlo por comunicación serial. 

En el aspecto de amplitud también existen diferencias. El Arduino Mega utiliza un ADC de 10 bits, por lo que dispone de: 



Si la referencia utilizada es 5 V, la resolución teórica es aproximadamente: 



por cada nivel del ADC. 

Por lo tanto, pequeñas variaciones inferiores a unos pocos milivoltios pueden no ser distinguibles digitalmente. En cambio, el osciloscopio puede presentar una resolución y sensibilidad vertical mucho mayor dependiendo de la escala seleccionada. 

En este laboratorio la señal simulada era solamente de 2 Hz, por lo que 200 muestras/s son más que suficientes para representar su forma general. Sin embargo, para bioseñales de mayor contenido frecuencial, como el EMG, esta velocidad podría resultar insuficiente. 

- Discutir las posibles fuentes de variabilidad del montaje propio (tolerancia real de los componentes, ancho de banda del TL084N y del LM324N, precisión del osciloscopio y del multímetro empleados, calidad de las conexiones en la protoboard, entre otros), e indicar a qué se atribuyen las diferencias frente a otro grupo que ejecutó el mismo procedimiento. 

Una de las principales es la tolerancia de las resistencias. Aunque se seleccionaron resistencias apareadas, estas no presentan valores exactamente iguales. En una etapa diferencial, pequeños errores en las relaciones entre resistencias pueden modificar tanto la ganancia como el CMRR. 

También influyen las características propias de los amplificadores operacionales utilizados. Dos TL084N del mismo modelo pueden presentar pequeñas diferencias en tensión de offset, corriente de polarización, ganancia de lazo abierto y ancho de banda. 

Otra fuente importante corresponde a la protoboard. Las conexiones generan resistencias y capacitancias parásitas y algunos cables pueden realizar contactos imperfectos. Además, usar cables demasiado largos puede aumentar la captación de ruido electromagnético. 

También existe incertidumbre en los equipos de medición. Tanto el multímetro como el osciloscopio presentan una precisión limitada. Cuando se trabaja con señales pequeñas, incluso una diferencia de algunos milivoltios puede representar un porcentaje considerable del valor medido. 

Finalmente, también existen diferencias introducidas por el procedimiento experimental. Por 





ejemplo, otro grupo podría ajustar un 𝑅𝑔 ligeramente diferente, configurar otra escala en el osciloscopio o medir amplitudes utilizando cursores en lugar de la función automática del equipo. 

Por estas razones no se espera que todos los grupos obtengan exactamente los mismos resultados, aunque sí debería mantenerse la misma tendencia general del circuito. 

## **6. Cuestionario y preguntas de ampliación** 

_Responder justificando con referencias bibliográficas cuando corresponda._ 

- ¿Por qué el CMRR de un amplificador de instrumentación depende principalmente del apareo de las resistencias de la etapa diferencial (R2, R2', R3, R3') y no de la ganancia establecida por Rg? 

En un amplificador de instrumentación de 3 amplificadores, Rg se utiliza para controlar la ganancia diferencial de la primera etapa. Es decir, modifica la amplitud de la diferencia que existe entre las entradas. Sin embargo, el rechazo de modo común depende que las resistencias R2, R2', R3, R3' cumplan con: 



Para que ambas ramas tengan la misma ganancia y una señal de modo común pueda cancelarse al realizar la resta. 

Si estas relaciones no son exactamente iguales, una parte de la señal que está presente simultáneamente en ambas entradas deja de cancelarse y aparece en la salida. 

Por ejemplo, idealmente si: 



entonces: 



y la salida producida por esa señal común debería ser cero. 

Sin embargo, si existe un desbalance entre las resistencias, la etapa diferencial puede producir: 



aunque las dos entradas tengan exactamente la misma tensión. 

Por eso el CMRR depende fuertemente del apareamiento de las resistencias de la etapa diferencial. En el propio marco teórico del informe se indica que el apareamiento de los componentes externos influye directamente en el rechazo efectivo al modo común.     Laboratorio 2 

𝑅𝑔, en cambio, modifica principalmente la ganancia diferencial. Puede afectar indirectamente el valor calculado del CMRR porque este utiliza 𝐴𝑑, pero no es el elemento que determina principalmente cuánto de la señal común consigue cancelarse. 

- ¿Cómo varía el CMRR con la frecuencia de la señal de modo común, y qué relación tiene esto con el ancho de banda del op-amp utilizado? 





En general, el CMRR disminuye cuando aumenta la frecuencia de la señal de modo común. Esto ocurre porque los amplificadores operacionales tienen un ancho de banda limitado y su comportamiento deja de ser ideal a frecuencias mayores. 

También influyen las capacitancias parásitas de la protoboard, resistencias y cables. Por ello, un amplificador puede rechazar muy bien una señal común a bajas frecuencias, pero presentar menor rechazo cuando aumenta la frecuencia. 

- ¿Por qué debe bufferizarse la referencia de tierra virtual con un op-amp seguidor en lugar de conectar directamente el divisor resistivo 10 kΩ/10 kΩ al nodo sumador? 

El divisor formado por dos resistencias de 10 kΩ genera idealmente la mitad de la tensión de alimentación. Para una alimentación de 5 V: 



Sin embargo, esa expresión es válida cuando el punto medio prácticamente no entrega corriente. El op-amp configurado como seguidor resuelve este problema. Su entrada consume una corriente muy pequeña, por lo cual prácticamente no carga el divisor. Al mismo tiempo, su salida posee una impedancia mucho menor y puede entregar corriente al nodo sumador manteniendo prácticamente constante la tensión de referencia. 

- Investigar el ancho de banda y el slew rate del LM324N y compararlos con los del TL084N: ¿por qué conviene usar el LM324N para la etapa de referencia y suma en lugar de reutilizar un op-amp del TL084N? 

LM324-N presenta aproximadamente: 

- ➢ Gain Bandwidth Product: 1 MHz 

- ➢ Slew Rate típico: 0.5 V/µs 

TL084 utilizado en la etapa principal presenta aproximadamente: 

- ➢ Gain Bandwidth Product: 3 MHz 

- ➢ Slew Rate típico: 13 V/µs 

Aunque el TL084 es más rápido, en la etapa de referencia no se necesita una gran velocidad porque se trabaja principalmente con una tensión continua. Además, el LM324N funciona adecuadamente cerca del riel negativo con alimentación unipolar, por lo que resulta conveniente para generar y bufferizar la referencia utilizada antes del ADC. 

- ¿Qué limitaciones tiene el Serial Plotter del Arduino IDE frente a un osciloscopio para visualizar una señal biomédica en tiempo real, en términos de tasa de muestreo, resolución y análisis en frecuencia? 

El Serial Plotter tiene una menor tasa de muestreo y depende de la velocidad del ADC y de la comunicación serial. En nuestro código se toma una muestra cada 5 ms, lo que corresponde aproximadamente a: 



Además, el Arduino Mega utiliza un ADC de 10 bits, por lo que tiene una resolución menor que un equipo de medición dedicado. 





Un osciloscopio, en cambio, permite observar señales con mucha mayor resolución temporal y ofrece herramientas como cursores, trigger, medición de frecuencia y análisis espectral. Por ello, el Serial Plotter es útil para visualizar la señal, pero no reemplaza a un osciloscopio. 

- A partir de lo investigado, indicar qué modificaciones requeriría este montaje (ancho de banda, resolución del ADC, filtrado adicional) para digitalizar una señal biológica real (ECG o EMG) en lugar de la señal de prueba simulada. 

Para trabajar con ECG o EMG se necesitaría agregar filtros analógicos para eliminar ruido y evitar aliasing, aumentar la frecuencia de muestreo y utilizar un ADC de mayor resolución. 

Para ECG podría utilizarse una frecuencia de muestreo de aproximadamente 500 Hz o mayor, mientras que para EMG sería recomendable trabajar alrededor de 1 kHz o más, debido a su mayor contenido en frecuencia. 

También sería importante mejorar el rechazo al ruido de 50/60 Hz y considerar aislamiento y protección eléctrica antes de conectar el circuito a una persona. 

## **7. Conclusiones** 

- Ganancia diferencial. Se comprobó la tendencia esperada: al disminuir Rg aumenta la ganancia. Las ganancias experimentales (1,64; 3,23; 5,32 y 543,75) fueron menores que las teóricas (2,962; 4,91; 8,793 y 8184,33), con diferencias de entre 34 % y 45 % en las tres primeras mediciones. Estas diferencias se atribuyen a la tolerancia de las resistencias, al offset del TL084N, a la precisión de los instrumentos y a la inestabilidad del potenciómetro al usarlo como Rg. 

- Saturación. Con Rg = 2,4 Ω la salida (≈17,4 Vpp) quedó limitada por la alimentación de ±9 V, de modo que la ganancia medida no representa la operación lineal del circuito. Esto se observa en la deformación y el recorte de la Figura 11. 

- CMRR. Con una ganancia en modo común de 0,00108 se estimó un CMRR de aproximadamente 114 dB. Este valor debe tomarse con cautela, porque se calculó con una ganancia diferencial obtenida en saturación. Además, en un amplificador discreto el rechazo al modo común depende del apareamiento de R2, R2', R3 y R3' (Texas Instruments, hoja de datos del TL084), por lo que no es comparable de forma directa con el de un amplificador integrado, cuyas resistencias internas se fabrican con tolerancias mucho menores. 

- Acondicionamiento y visualización. (modificada) Se aplicó un desplazamiento de nivel de continua con una referencia de tierra virtual bufferizada con LM324N, técnica propia de los circuitos de adquisición con alimentación unipolar (Texas Instruments, diseño de referencia TIPD154). La referencia entregó 2,5 V, igual al valor teórico, y el nodo sumador mantuvo la señal dentro del rango del ADC (0–1,251 V, sin recorte). La adquisición digital se verificó en simulación con el Arduino Mega, con una frecuencia de muestreo de 200 Hz y una resolución de ≈4,89 mV por nivel. Es suficiente para la señal de 2 Hz, pero limitada para bioseñales como el EMG. 

- Alcance. La etapa D no pudo completarse con el ESP32 en el laboratorio y se resolvió con la alternativa de simulación de la guía. Para una aplicación real con ECG o EMG harían falta filtrado analógico anti-aliasing, mayor frecuencia de muestreo, mayor resolución del ADC y mejor rechazo al ruido de 50/60 Hz. 





## **8. Materiales y código** 

**Tabla 4. Lista de materiales y componentes utilizados.** 

|**Componente (materiales y equipos)**|**Cantidad utilizada**|**Marca / modelo u observación**|
|---|---|---|
|TL084N (amplificador operacional cuádruple JFET)|1|Genérica|
|LM324N (amplificador operacional cuádruple)|1|Genérica|
|Resistencia 10 kΩ, tolerancia estándar|10|Genérica|
|Resistencia 1 kΩ (5%, filtro RC de la señal de prueba)|1|Genérica|
|Resistencia 1 kΩ y 10 Ω (5%, divisor atenuador a nivel de<br>mV)|1|Genérica|
|Capacitor electrolítico 10 µF (filtro RC de la señal de prueba)|1|Genérica|
|Capacitor cerámico 100 nF (desacople de alimentación: 1 por<br>cada pin V+ y V− de cada IC)|6|Genérica|
|Arduino Mega|1|Genérica|
|ESP32 DEVKIT V1|1|Genérica|
|Protoboard|1|Genérica|
|Cables jumper macho-macho|Varios|Genérica|
|Cables jumper macho-hembra|Varios|Genérica|
|Cable USB (programación / lectura del microcontrolador)|1|Genérica|
|Multímetro|1|FLUKEs|
|Fuente de alimentación|1|Genérica|
|Cables banana-coco|2||
|Osciloscopio|1||
|Puntas de osciloscopio|2||



**Tabla 5. Código fuente y enlace de repositorio.** 

|**Archivo / módulo**<br>**de código**|**Descripción breve**|**Plataforma**|**Enlace al repositorio**|
|---|---|---|---|
|ESP32|Señal sinusoidal para la parte<br>experimental|GITHUB|https://github.com/RRORRIGO/Biome<br>dical-Instrumentation/blob/master/Infor<br>me%202/Code_ESp32_sinoidal.cpp|
|Arduino Mega|Señal sinusoidal para la parte de<br>simulación|GITHUB|https://github.com/RRORRIGO/Biome<br>dical-Instrumentation/blob/master/Infor<br>me%202/Code_Mega_2560.cpp|







## **9. Referencias bibliográficas** 

- Aston, R. (1990). _Principles of biomedical instrumentation and measurement_ . Merrill Publishing Company. 

Arduino. (s. f.). _Arduino Mega 2560 Rev3: Technical documentation_ . Arduino. 

- Cromwell, L., Weibell, F. J., & Pfeiffer, E. A. (1980). _Biomedical instrumentation and measurements_ (2nd ed.). Prentice-Hall. 

- Khandpur, R. S. (2014). _Handbook of biomedical instrumentation_ (3rd ed.). McGraw Hill Education. 

- Pickett, M. (2013). _What you need to know about CMRR: The instrumentation amplifier, part 2_ . Texas Instruments. 

- Sedra, A. S., & Smith, K. C. (2020). _Microelectronic circuits_ (8th ed.). Oxford University Press. 

Texas Instruments. (s. f.-a). _LM324 low-power, quad-operational amplifiers_ [Data sheet]. 

- Texas Instruments. (s. f.-b). _TL084 JFET-input operational amplifiers_ [Data sheet]. 

- Texas Instruments. (2024). _Common-mode rejection ratio in difference amplifier circuits_ . Texas Instruments. 

- Webster, J. G., & Nimunkar, A. J. (2020). _Medical instrumentation: Application and design_ (5th ed.). John Wiley & Sons. 



