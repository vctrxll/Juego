import serial
import time

# Configura la conexión con el Arduino
try:
    arduino = serial.Serial('COM3', 9600, timeout=1)  # Cambia 'COM3' al puerto correspondiente
    time.sleep(2)  # Espera a que el Arduino se inicialice
    print("Conexión con Arduino establecida.")
except Exception as e:
    print(f"Error al conectar con Arduino: {e}")
    arduino = None

# Verifica la conexión y solicita el comando al usuario
if arduino is not None:
    while True:
        comando = input("¿Enviar comando 'darobsequio'? Ingresa 'S' para enviar o 'Q' para salir: ").strip().upper()
        
        if comando == "S":
            try:
                mensaje = "darobsequio"  # Mensaje que queremos enviar
                arduino.write(mensaje.encode()) # Envía el comando al Arduino
                print("Señal enviada: darobsequio")
                print("----------------------------")
                resultado = arduino.readline().decode('utf-8').strip() # Leer y decodificar el dato
                print(resultado)
            except Exception as e:
                print(f"Error al enviar datos al Arduino: {e}")
        elif comando == "Q":
            print("Saliendo del programa.")
            break
        else:
            print("Comando no reconocido. Intenta nuevamente.")
else:
    print("No se pudo establecer la conexión con el Arduino.")
