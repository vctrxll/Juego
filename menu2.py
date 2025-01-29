#Archivo para probar con monedero
#Libreria para manejar gráficos, sonido y dibujar gráficos en la ventana
import pygame
#Libreria usada para establecer comunicación con Arduinoy se conecta a través del puerto serie.
from serial import Serial
#Libreria para controlar el tiempo del juego, medir tiempos de respuesta y sincronizar eventos.
import time
#Libreria usada para automatizar tareas.
import subprocess
#Libreria usada para seguimiento de movimientos de la mano y análisis de posturas
import mediapipe as mp
#libreria usada para  trabajar con los datos visuales, procesamiento de imágenes y visión por computadora.
import cv2
#Libreria usada para cálculos matemáticos para trabajar coordenadas
import math


# Inicializar Pygame
pygame.init()
# Dimensiones de la ventana de captura de video (webcam) en pixeles
cap_width = 640
cap_height = 360

# Dimensiones de la ventana de pygame en pixeles
ANCHO = 1300
ALTO = 850

# Colores
BLANCO = (255, 255, 255)#En RGB
NEGRO = (0, 0, 0)
AZUL = (0, 128, 255)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
CAFE = (188, 104, 67)
VERDE = (59, 202, 37)
# Variables
coin = False  #Indica si se ha insertado una moneda
piramide_held = False # Indica si la pirámide está "sostenida"
piramide_released = False # Indica si la pirámide ha sido "soltada"

# Crear ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))  # Crear la ventana de Pygame
pygame.display.set_caption("Menú Principal") # Crea una ventana con el tamaño definido("Menú Principal": Es el Título que tendra la ventana)

# Configuración de la fuente de texto
fuente = pygame.font.Font(None, 40) # Fuente predeterminada, tamaño 40

# Comunicación con Arduino (Comentado para que no dependa de él)
arduino = Serial('COM3', 9600) # Conectar con Arduino en el puerto COM3, a 9600 baudios
time.sleep(2) # Esperar 2 segundos para que la conexión esté lista

# Inicializar Mediapipe para la detección de manos
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)#123456987aqui
# Captura de video desde la webcam
cap = cv2.VideoCapture(0)  # Capturar video desde la cámara predeterminada (índice 0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)  # Establece el ancho del cuadro de video en 640 píxeles.
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)  # Establece la altura del cuadro de video en 360 píxeles.


# Cargar una imagen de fondo
fondo_img = pygame.image.load('fondo/piramidesinicial.jpg') #Cargar la imagen de fondo
fondo_img = pygame.transform.scale(fondo_img, (ANCHO, ALTO)) # Redimensionarla al tamaño de la ventana


# Función para mostrar texto en la pantalla
def mostrar_texto(texto, x, y, color):
    superficie = fuente.render(texto, True, color) # Renderizar el texto con la fuente y color especificados
    pantalla.blit(superficie, (x, y))  # Dibujar el texto en la pantalla

# Función para mostrar texto centrado en el rectángulo
def mostrar_texto_centrado(texto, rectangulo, color):
    superficie = fuente.render(texto, True, color) # Renderizar el texto
    text_rect = superficie.get_rect(center=rectangulo.center) # Obtener el rectángulo centrado
    pantalla.blit(superficie, text_rect) # Dibujar el texto centrado en la pantalla


def detect_finger_down(hand_landmarks):
    print("-----------------------------")
    finger_down = False
    x_base1 = int(hand_landmarks.landmark[0].x * cap_width)
    y_base1 = int(hand_landmarks.landmark[0].y * cap_height)

    x_base2 = int(hand_landmarks.landmark[17].x * cap_width)
    y_base2 = int(hand_landmarks.landmark[17].y * cap_height)

    x_pinky = int(hand_landmarks.landmark[20].x * cap_width)
    y_pinky = int(hand_landmarks.landmark[20].y * cap_height)

    x_anular = int(hand_landmarks.landmark[16].x * cap_width)
    y_anular = int(hand_landmarks.landmark[16].y * cap_height)

    x_medio = int(hand_landmarks.landmark[12].x * cap_width)
    y_medio = int(hand_landmarks.landmark[12].y * cap_height)

    p1 = (x_base1, y_base1)
    p5 = (x_base2, y_base2)
    p2 = (x_pinky, y_pinky)
    p3 = (x_anular, y_anular)
    p4 = (x_medio, y_medio)
    d_base_base = calc_distance(p1, p5)
    d_base_pinky = calc_distance(p1, p2)
    d_base_anular = calc_distance(p1, p3)
    d_base_medio = calc_distance(p1, p4)
    print(d_base_base)
    print("------------------------------------")
    print("Pinky ", d_base_pinky)
    print("Anular ", d_base_anular)
    print("Medio ", d_base_medio)
    if d_base_anular < 20 and d_base_medio < 20 and d_base_pinky < 20:
        finger_down = True
    #print("---------------------")
    return finger_down



# Función para ejecutar el juego (dependiendo de la moneda)
def ejecutar_juego():
    global coin, cap

    # Verificar si el usuario ha insertado la moneda
    if coin:  # Si se ha insertado la moneda
        # Liberar la cámara antes de ejecutar el segundo script
        cap.release()
        cv2.destroyAllWindows()  # Destruir ventanas abiertas por OpenCV

        # Cerrar la conexión con Arduino
        arduino.close()
        print("Conexión con Arduino cerrada.")

        # Ejecutar el segundo script (juego.py)
        subprocess.run(['python', '3.py'])

        # Reiniciar la variable coin a False después de ejecutar el juego
        coin = False
        print("Juego finalizado. Coin se ha puesto en False.")

        # Volver a capturar la cámara
        cap.open(0)

        # Reabrir la conexión con Arduino
        arduino.open()
        print("Conexión con Arduino reabierta.")
    else:
        print("No puedes ejecutar el juego, la variable coin debe ser True.")

# Inicialización de la cámara (solo si es necesario en tu caso)
cap = cv2.VideoCapture(0)
# Función para verificar el estado de la moneda desde Arduino
def verificar_moneda():
    global coin
    if arduino.in_waiting > 0: # Si hay datos disponibles en el puerto serie
        resultado = arduino.readline().decode('utf-8').strip() # Leer y decodificar el dato
        if resultado == "COIN":
            print("Moneda insertada")
            coin = True # Cambiar el estado de la moneda a True
        else:
            print("Moneda no insertada")
            coin = False # Cambiar el estado de la moneda a False

# Función para calcular la distancia entre dos puntos (usada para determinar si el puño está cerrado)
def calc_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Función para convertir una imagen de OpenCV a formato Pygame
def cvimage_to_pygame(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Convertir la imagen de BGR (OpenCV) a RGB
    image_surface = pygame.image.frombuffer(image_rgb.tobytes(), image_rgb.shape[1::-1], 'RGB') # Convertir a superficie de Pygame
    return image_surface # Retornar la imagen convertida

# Función principal para mostrar el menú
def mostrar_menu():
    global coin, piramide_held, piramide_released
    corriendo = True # Variable de control del bucle
    game_starting = False # Indica si el juego está a punto de empezar
    while corriendo:
        # Leer la imagen desde la webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Procesar la imagen: voltear y convertir a RGB
        frame = cv2.flip(frame, 1) # Espejar horizontalmente la image
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convertir a RGB
        resultado = hands.process(frame_rgb) # Procesar la imagen para la detección de manos

        # Convertir el frame de OpenCV a un formato que Pygame pueda usar
        frame_surface = cvimage_to_pygame(frame)
        pantalla.blit(frame_surface, (0, 0))# Dibujar el frame en la pantalla

        # Dibujar la imagen de fondo en la pantalla
        pantalla.blit(fondo_img, (0, 0))
        # Si se ha detectado una moneda
        if coin:
           # Mostrar el texto que indica cerrar el puño por 3 segundos
            mostrar_texto("Cierra el puño por 3 segundos", 330, 300, CAFE)

            # Verificar si hay manos detectadas por MediaPipe
            if resultado.multi_hand_landmarks:
                    game_starting = True


        # Si el juego está comenzando, mostrar un mensaje durante 3 segundos
        if game_starting:
            mostrar_texto("HOLA!!!! TE HE DETECTADO", 460, 520, VERDE)
            time.sleep(2)
            # Verificar si han pasado 3 segundos desde que el juego comenzó
            print("si funciono")
            ejecutar_juego()
        # Verificar el estado de la moneda (omitido porque siempre será True)
        verificar_moneda()
        mostrar_texto(f"Moneda: {'Aceptada' if coin else 'Inserte moneda'}", 850, 470, AZUL)

        # Actualizar la pantalla de Pygame
        pygame.display.flip()

        # Manejar eventos de Pygame
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                # Si el usuario cierra la ventana, detener el programa
                corriendo = False
            elif evento.type == pygame.KEYDOWN:
                # Si se presiona la tecla '1', iniciar el juego
                if evento.key == pygame.K_1:
                    ejecutar_juego()
                # Si se presiona la tecla '2', terminar el programa
                elif evento.key == pygame.K_2:
                    corriendo = False

    # Cerrar todo al salir
    pygame.quit()
    cap.release() # Liberar el recurso de captura de video
    cv2.destroyAllWindows() # Cerrar todas las ventanas de OpenCV

# Ejecutar el menú principal si el script se está ejecutando directamente
if __name__ == "__main__":
    try:
        mostrar_menu() # Mostrar el menú del juego
    except KeyboardInterrupt:
         # Si el usuario interrumpe con Ctrl+C, mostrar un mensaje
        print("Interrumpido por el usuario.")
    finally:
        # Cerrar la conexión con Arduino
        arduino.close()  #Cerrar el recurso de Arduino
        hands.close() # Cerrar el recurso de detección de manos