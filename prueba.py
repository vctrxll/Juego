import serial
import time
import cv2
import mediapipe as mp
import os

# Configura la conexión con el Arduino
def conectar_arduino(puerto='COM3', baudrate=9600, timeout=1):
    try:
        arduino = serial.Serial(puerto, baudrate, timeout=timeout)
        time.sleep(2)  # Espera a que el Arduino se inicialice
        print("Conexión con Arduino establecida.")
        return arduino
    except Exception as e:
        print(f"Error al conectar con Arduino: {e}")
        return None

arduino = conectar_arduino()
initialstate = True

#VENTANA OPENCV
# Cargar imagen de fondo desde una ruta relativa
background_path = "pantallaprincipal2.jpg"  # Cambia esto según el nombre de tu imagen
if not os.path.exists(background_path):
    print(f"Error: La imagen de fondo '{background_path}' no se encuentra.")
    exit(1)

background = cv2.imread(background_path)
background = cv2.resize(background, (1920, 1080))

cap = cv2.VideoCapture(0)
cap.set(3, 1920)  # Ancho
cap.set(4, 1080)  # Alto

run = False


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=1) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar el frame")
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)  # Efecto espejo

        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Reemplazar el frame con la imagen de fondo
        output = background.copy()

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(output, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Optimización de la lectura del puerto serie

        # Mostrar la imagen en la ventana de OpenCV
        cv2.imshow("Menu", output)

        if cv2.waitKey(1) & 0xFF == ord(" "):
            break

        if not run:
            if arduino.in_waiting > 0:  # Si hay datos disponibles en el puerto serie
                resultado = arduino.readline().decode('utf-8').strip()  # Leer y decodificar el dato
                if resultado == "COIN":
                    print("Moneda insertada")
                    coin = True  # Cambiar el estado de la moneda a True
                else:
                    print("Moneda no insertada")
                    coin = False  # Cambiar el estado de la moneda a False

cap.release()
cv2.destroyAllWindows()
