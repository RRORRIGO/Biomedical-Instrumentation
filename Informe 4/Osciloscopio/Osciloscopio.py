
import os
import csv
import time
from bisect import bisect_left, bisect_right
from datetime import datetime

import numpy as np
import serial
import matplotlib.pyplot as plt

from matplotlib.widgets import Button, Slider, CheckButtons
from matplotlib.ticker import MultipleLocator

# =====================================================
# CONFIGURACION GENERAL
# =====================================================

PORT = "COM10"             # Cambiar si es necesario
BAUD = 230400

WINDOW_INITIAL = 50       # Ventana inicial
WINDOW_MIN = 10           # Minimo 10 segundos
WINDOW_MAX = 180          # Maximo 180 segundos

VOLTAGE_MIN = 0.0
VOLTAGE_MAX = 3.3

UPDATE_INTERVAL = 0.05    # Refresco de pantalla

# =====================================================
# CONEXION SERIAL
# =====================================================

print("Conectando al ESP32-S3...")

try:
    ser = serial.Serial(
        PORT,
        BAUD,
        timeout=0
    )

except serial.SerialException as e:
    print("Error de conexion:", e)
    raise SystemExit

time.sleep(2)
ser.reset_input_buffer()

print("ESP32 conectado correctamente.")

# =====================================================
# ALMACENAMIENTO
# =====================================================

times = []
ch1_values = []
ch2_values = []

serial_buffer = b""
first_timestamp = None

# Carpeta de resultados
OUTPUT_DIR = "capturas"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =====================================================
# ESTADO DEL OSCILOSCOPIO
# =====================================================

window_seconds = float(WINDOW_INITIAL)

show_ch1 = True
show_ch2 = True

# Cursores verticales: posicion relativa 0 - 1
cursor_x = [0.25, 0.75]

# Cursores horizontales: voltios
cursor_y = [1.0, 2.0]

current_window_start = 0.0

active_cursor = None

# =====================================================
# CREAR VENTANA
# =====================================================

plt.ion()

fig = plt.figure(figsize=(15, 8))

fig.suptitle(
    "OSCILOSCOPIO DC - ESP32-S3 | CH1 / CH2",
    fontsize=14,
    fontweight="bold"
)

# Grafica principal
ax = fig.add_axes([0.08, 0.26, 0.64, 0.63])

# Panel lateral de estadisticas
ax_stats = fig.add_axes([0.75, 0.27, 0.23, 0.60])
ax_stats.axis("off")

ax_stats.set_title(
    "MEDICIONES",
    fontsize=11,
    fontweight="bold",
    loc="left"
)

# =====================================================
# SEÑALES
# =====================================================

line_ch1, = ax.plot(
    [], [],
    color="blue",
    linewidth=1.2,
    label="CH1"
)

line_ch2, = ax.plot(
    [], [],
    color="darkorange",
    linewidth=1.2,
    label="CH2"
)

ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Voltaje (V)")

ax.set_xlim(0, window_seconds)
ax.set_ylim(VOLTAGE_MIN, VOLTAGE_MAX)

ax.set_autoscale_on(False)

ax.grid(
    True,
    linestyle="--",
    alpha=0.45
)

ax.legend(loc="upper right")

# =====================================================
# CURSORES
# =====================================================

vertical_lines = []

for fraction in cursor_x:

    line = ax.axvline(
        fraction * window_seconds,
        color="red",
        linestyle="--",
        linewidth=1.4
    )

    vertical_lines.append(line)

horizontal_lines = []

for voltage in cursor_y:

    line = ax.axhline(
        voltage,
        color="green",
        linestyle="--",
        linewidth=1.4
    )

    horizontal_lines.append(line)

# =====================================================
# PANEL DE MEDICIONES
# =====================================================

stats_text = ax_stats.text(
    0.0,
    0.98,
    "Esperando datos...",
    transform=ax_stats.transAxes,
    va="top",
    ha="left",
    fontsize=8.5,
    family="monospace"
)

# =====================================================
# SLIDER: VENTANA DE TIEMPO
# =====================================================

ax_slider = fig.add_axes([
    0.18, 0.155, 0.52, 0.035
])

slider_window = Slider(
    ax=ax_slider,
    label="Ventana (s)",
    valmin=WINDOW_MIN,
    valmax=WINDOW_MAX,
    valinit=WINDOW_INITIAL,
    valstep=1,
    color="steelblue"
)

def change_window(value):

    global window_seconds

    window_seconds = float(value)

slider_window.on_changed(change_window)

# =====================================================
# CASILLAS: MOSTRAR / OCULTAR CANALES
# =====================================================

ax_checks = fig.add_axes([
    0.78, 0.08, 0.16, 0.13
])

checks = CheckButtons(
    ax_checks,
    ["CH1", "CH2"],
    [True, True]
)

def toggle_channel(label):

    global show_ch1, show_ch2

    if label == "CH1":
        show_ch1 = not show_ch1
        line_ch1.set_visible(show_ch1)

    elif label == "CH2":
        show_ch2 = not show_ch2
        line_ch2.set_visible(show_ch2)

    fig.canvas.draw_idle()

checks.on_clicked(toggle_channel)

# =====================================================
# BOTONES DE EXPORTACION
# =====================================================

ax_png = fig.add_axes([
    0.13, 0.055, 0.17, 0.06
])

ax_csv = fig.add_axes([
    0.34, 0.055, 0.17, 0.06
])

button_png = Button(
    ax_png,
    "Guardar PNG",
    color="lightblue",
    hovercolor="skyblue"
)

button_csv = Button(
    ax_csv,
    "Guardar CSV",
    color="lightgreen",
    hovercolor="palegreen"
)

# =====================================================
# GUARDAR PNG
# =====================================================

def save_png(event):

    filename = os.path.join(
        OUTPUT_DIR,
        "Osciloscopio_" +
        datetime.now().strftime("%Y%m%d_%H%M%S") +
        ".png"
    )

    fig.savefig(
        filename,
        dpi=200,
        facecolor="white"
    )

    print("PNG guardado:", os.path.abspath(filename))

button_png.on_clicked(save_png)

# =====================================================
# GUARDAR CSV
# =====================================================

def save_csv(event):

    filename = os.path.join(
        OUTPUT_DIR,
        "Datos_" +
        datetime.now().strftime("%Y%m%d_%H%M%S") +
        ".csv"
    )

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Tiempo_s",
            "CH1_V",
            "CH2_V"
        ])

        writer.writerows(
            zip(times, ch1_values, ch2_values)
        )

    print("CSV guardado:", os.path.abspath(filename))

button_csv.on_clicked(save_csv)

# =====================================================
# FUNCIONES DE MEDICION
# =====================================================

def get_stats(values):

    if len(values) == 0:
        return None

    vmax = float(np.max(values))
    vmin = float(np.min(values))
    vmean = float(np.mean(values))
    vpp = vmax - vmin

    return vmax, vmin, vpp, vmean


def format_stats(values):

    result = get_stats(values)

    if result is None:
        return " Sin datos\n"

    vmax, vmin, vpp, vmean = result

    return (
        f" Max:  {vmax:.3f} V\n"
        f" Min:  {vmin:.3f} V\n"
        f" Vpp:  {vpp:.3f} V\n"
        f" Prom: {vmean:.3f} V\n"
        f" N:    {len(values)}\n"
    )


def update_statistics(window_start):

    # Posiciones temporales de los cursores
    x1 = window_start + cursor_x[0] * window_seconds
    x2 = window_start + cursor_x[1] * window_seconds

    t1 = min(x1, x2)
    t2 = max(x1, x2)

    y1 = min(cursor_y)
    y2 = max(cursor_y)

    delta_t = abs(x2 - x1)
    delta_v = abs(cursor_y[1] - cursor_y[0])

    # Buscar indices dentro de X1 y X2
    i0 = bisect_left(times, t1)
    i1 = bisect_right(times, t2)

    ch1 = np.asarray(ch1_values[i0:i1])
    ch2 = np.asarray(ch2_values[i0:i1])

    # Datos dentro del rectangulo X-Y
    rect_ch1 = ch1[
        (ch1 >= y1) &
        (ch1 <= y2)
    ]

    rect_ch2 = ch2[
        (ch2 >= y1) &
        (ch2 <= y2)
    ]

    text = (
        "CURSORES\n"
        "----------------------\n"
        f"X1: {x1:.2f} s\n"
        f"X2: {x2:.2f} s\n"
        f"dT: {delta_t:.2f} s\n"
        f"Y1: {cursor_y[0]:.3f} V\n"
        f"Y2: {cursor_y[1]:.3f} V\n"
        f"dV: {delta_v:.3f} V\n\n"
    )

    text += "CH1 - ENTRE X1 Y X2\n"
    text += format_stats(ch1)

    text += "\nCH2 - ENTRE X1 Y X2\n"
    text += format_stats(ch2)

    text += "\nCH1 - RECTANGULO XY\n"
    text += format_stats(rect_ch1)

    text += "\nCH2 - RECTANGULO XY\n"
    text += format_stats(rect_ch2)

    stats_text.set_text(text)

# =====================================================
# CURSORES ARRASTRABLES CON EL MOUSE
# =====================================================

def on_mouse_press(event):

    global active_cursor

    if event.inaxes != ax or event.button != 1:
        return

    # Detectar cursor mas cercano en pixeles
    candidates = []

    for i, line in enumerate(vertical_lines):

        x = line.get_xdata()[0]
        xp = ax.transData.transform((x, 0))[0]

        distance = abs(event.x - xp)

        if distance <= 10:
            candidates.append((distance, "x", i))

    for i, line in enumerate(horizontal_lines):

        y = line.get_ydata()[0]
        yp = ax.transData.transform((0, y))[1]

        distance = abs(event.y - yp)

        if distance <= 10:
            candidates.append((distance, "y", i))

    if candidates:

        candidates.sort(key=lambda item: item[0])

        _, cursor_type, index = candidates[0]

        active_cursor = (cursor_type, index)


def on_mouse_move(event):

    if active_cursor is None:
        return

    if event.inaxes != ax:
        return

    if event.xdata is None or event.ydata is None:
        return

    cursor_type, index = active_cursor

    if cursor_type == "x":

        # Posicion proporcional a ventana actual
        relative = (
            event.xdata - current_window_start
        ) / window_seconds

        cursor_x[index] = float(
            np.clip(relative, 0, 1)
        )

    elif cursor_type == "y":

        cursor_y[index] = float(
            np.clip(
                event.ydata,
                VOLTAGE_MIN,
                VOLTAGE_MAX
            )
        )


def on_mouse_release(event):

    global active_cursor

    active_cursor = None


fig.canvas.mpl_connect(
    "button_press_event",
    on_mouse_press
)

fig.canvas.mpl_connect(
    "motion_notify_event",
    on_mouse_move
)

fig.canvas.mpl_connect(
    "button_release_event",
    on_mouse_release
)

# =====================================================
# CONFIGURACION DINAMICA DEL EJE X
# =====================================================

def update_x_axis(window_start, window_end):

    ax.set_xlim(window_start, window_end)

    # Ajustar distancia entre divisiones
    target_step = window_seconds / 8.0

    possible_steps = [
        1, 2, 5, 10, 15, 20, 30, 60
    ]

    step = possible_steps[-1]

    for candidate in possible_steps:

        if candidate >= target_step:
            step = candidate
            break

    ax.xaxis.set_major_locator(
        MultipleLocator(step)
    )

    # Evitar zoom automatico
    ax.set_ylim(VOLTAGE_MIN, VOLTAGE_MAX)

# =====================================================
# LEER DATOS DEL ESP32
# =====================================================

def read_serial_data():

    global serial_buffer
    global first_timestamp

    # Leer datos que ya llegaron por USB
    waiting = ser.in_waiting

    if waiting <= 0:
        return

    chunk = ser.read(min(waiting, 65536))

    serial_buffer += chunk

    # Conservar ultima linea incompleta
    lines = serial_buffer.split(b"\n")
    serial_buffer = lines.pop()

    # Formato esperado:
    # tiempo_us,CH1,CH2
    for raw in lines:

        try:

            parts = raw.decode(
                "ascii",
                errors="ignore"
            ).strip().split(",")

            if len(parts) != 3:
                continue

            timestamp_us = int(parts[0])
            voltage1 = float(parts[1])
            voltage2 = float(parts[2])

            if not (
                np.isfinite(voltage1) and
                np.isfinite(voltage2)
            ):
                continue

            if first_timestamp is None:
                first_timestamp = timestamp_us

            elapsed = (
                timestamp_us - first_timestamp
            ) / 1_000_000.0

            if elapsed < 0:
                continue

            # Mantener tiempo creciente
            if times and elapsed <= times[-1]:
                continue

            times.append(elapsed)
            ch1_values.append(voltage1)
            ch2_values.append(voltage2)

        except (ValueError, IndexError):
            continue


# =====================================================
# ACTUALIZAR OSCILOSCOPIO
# =====================================================

def update_oscilloscope():

    global current_window_start

    if not times:
        return

    elapsed = times[-1]

    # Ventana visible de longitud variable
    window_start = max(
        0.0,
        elapsed - window_seconds
    )

    window_end = (
        window_start + window_seconds
    )

    current_window_start = window_start

    # Seleccionar solo muestras visibles
    i0 = bisect_left(times, window_start)
    i1 = bisect_right(times, window_end)

    t_visible = times[i0:i1]

    ch1_visible = ch1_values[i0:i1]
    ch2_visible = ch2_values[i0:i1]

    # Actualizar CH1 y CH2
    line_ch1.set_data(
        t_visible,
        ch1_visible
    )

    line_ch2.set_data(
        t_visible,
        ch2_visible
    )

    # Respetar visibilidad
    line_ch1.set_visible(show_ch1)
    line_ch2.set_visible(show_ch2)

    # Actualizar eje X
    update_x_axis(
        window_start,
        window_end
    )

    # Reubicar cursores verticales
    for i in range(2):

        x = (
            window_start +
            cursor_x[i] * window_seconds
        )

        vertical_lines[i].set_xdata([x, x])

    # Reubicar cursores horizontales
    for i in range(2):

        y = cursor_y[i]

        horizontal_lines[i].set_ydata([y, y])

    # Estadisticas de ambos canales
    update_statistics(window_start)

    # Mostrar tiempo total transcurrido
    ax.set_title(
        f"Tiempo: {elapsed:.1f} s   |   "
        f"Ventana: {window_seconds:.0f} s   |   "
        f"Muestras: {len(times)}",
        fontsize=10
    )

    fig.canvas.draw_idle()

# =====================================================
# INICIAR ADQUISICION CONTINUA
# =====================================================

print("--------------------------------------")
print("OSCILOSCOPIO DC - DOS CANALES")
print("--------------------------------------")
print("CH1: GPIO 4")
print("CH2: GPIO 5")
print("Ventana variable: 10 a 180 segundos")
print("Frecuencia objetivo: 500 Hz")
print("Presiona Ctrl+C para detener")
print("--------------------------------------")

try:

    while plt.fignum_exists(fig.number):

        read_serial_data()

        update_oscilloscope()

        plt.pause(UPDATE_INTERVAL)

except KeyboardInterrupt:

    print("Adquisicion detenida.")

except serial.SerialException as e:

    print("Error de comunicacion:", e)

finally:

    ser.close()

    print("Puerto serial cerrado.")
    print("Muestras adquiridas:", len(times))

    plt.ioff()

    if plt.fignum_exists(fig.number):
        plt.show()
