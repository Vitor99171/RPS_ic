import cv2
import mediapipe as mp
import math
import serial  # Biblioteca PySerial
import time

# Configuração do MediaPipe para a detecção de mãos
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Função para calcular a distância entre dois pontos
def calcular_distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Função para identificar o gesto da mão com base em landmarks
def identificar_gesto(pontos):
    def dedo_levantado(tip, pip):
        return pontos[tip][1] < pontos[pip][1]  # Verifica se a ponta está acima da articulação proximal (PIP)

    polegar_levantado = pontos[4][0] > pontos[3][0]
    indicador_levantado = dedo_levantado(8, 6)
    medio_levantado = dedo_levantado(12, 10)
    anelar_levantado = dedo_levantado(16, 14)
    mindinho_levantado = dedo_levantado(20, 18)

    if not polegar_levantado and not indicador_levantado and not medio_levantado and not anelar_levantado and not mindinho_levantado:
        return "Pedra"
    elif polegar_levantado and indicador_levantado and medio_levantado and anelar_levantado and mindinho_levantado:
        return "Papel"
    elif indicador_levantado and medio_levantado and not anelar_levantado and not mindinho_levantado:
        return "Tesoura"
    
    return None

# Função para retornar o gesto de resposta baseado no gesto do usuário
def responder_gesto(gesto):
    if gesto == "Pedra":
        return "Papel"
    elif gesto == "Papel":
        return "Tesoura"
    elif gesto == "Tesoura":
        return "Pedra"
    return None

# Configurando a comunicação Serial com o Arduino via USB
arduino = serial.Serial('COM5', 9600)  # Troque 'COM3' pela porta correta do Arduino
time.sleep(2)  # Espera para garantir a conexão

# Captura de vídeo da câmera
url = 0  # Webcam local
video = cv2.VideoCapture(url)

while True:
    ret, frame = video.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            pontos = [(int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])) for lm in hand_landmarks.landmark]
            gesto = identificar_gesto(pontos)

            if gesto:
                resposta = responder_gesto(gesto)
                cv2.putText(frame, f"Seu Gesto: {gesto}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Resposta: {resposta}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # Enviar o gesto via Serial para o Arduino
                if resposta == "Pedra":
                    arduino.write(b'P!')  # Envia 'P' para Pedra
                elif resposta == "Papel":
                    arduino.write(b'A!')  # Envia 'A' para Papel
                elif resposta == "Tesoura":
                    arduino.write(b'T!')  # Envia 'T' para Tesoura

    cv2.imshow("Pedra, Papel ou Tesoura", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
arduino.close()
