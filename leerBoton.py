# leerBoton.py
"""
Módulo para leer botones desde RedBearLab Blend Micro v1 conectado por USB.
El microcontrolador envía por serial el nombre del botón presionado (UP, DOWN, LEFT, RIGHT, A, B, MENU) seguido de '\n'.
"""
import serial
import time

# Configuración del puerto serial (ajusta según tu sistema, p.ej. '/dev/ttyACM0' o '/dev/ttyUSB0')
SERIAL_PORT = '/dev/ttyACM0'
BAUDRATE = 9600

# Inicializa conexión serial
try:
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=0.1)
    time.sleep(2)  # espera inicial para estabilizar conexión
except serial.SerialException as e:
    raise RuntimeError(f"No se pudo abrir el puerto serial {SERIAL_PORT}: {e}")


def leer_boton():
    """
    Lee una línea del serial. Si el microcontrolador envía un nombre de botón,
    retorna ese string; en caso contrario retorna None.
    """
    try:
        raw = ser.readline()
        if not raw:
            return None
        btn = raw.decode('utf-8', errors='ignore').strip()
        return btn if btn in {'UP','DOWN','LEFT','RIGHT','A','B','MENU'} else None
    except Exception:
        return None


def cleanup():
    """
    Cierra el puerto serial. Llamar al terminar el programa.
    """
    try:
        ser.close()
    except Exception:
        pass
