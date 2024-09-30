import cv2
import mediapipe as mp
import math
import serial
import time

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Inicializar comunicação serial com o Arduino (ajuste a porta conforme necessário)
arduino = serial.Serial('COM3', 9600)  # Ajuste 'COM3' para a sua porta

# Função para desenhar texto com fundo transparente
def desenhar_texto_estilizado(frame, text, pos, font_scale=1, font_thickness=2, font=cv2.FONT_HERSHEY_SIMPLEX, text_color=(255, 255, 255), bg_color=(0, 0, 0, 0.5)):
    # Desenhar fundo para o texto
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    x, y = pos
    bg_color_bgr = bg_color[:3]  # A cor do fundo (sem o alpha)
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y - text_height - 10), (x + text_width + 10, y + 10), bg_color_bgr, -1)
    
    # Adicionar o texto sobre o fundo
    cv2.putText(overlay, text, (x + 5, y), font, font_scale, text_color, font_thickness)

    # Aplicar o efeito de transparência
    alpha = bg_color[3]  # Transparência
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

# Função para identificar o gesto baseado nos pontos da mão
def identificar_gesto(pontos):
    # Lógica para identificar o gesto baseado nos landmarks
    # Pode ser a lógica que você já implementou
    # Exemplo: se o mindinho e anelar estiverem levantados, retorno "tesoura"
    # Adicione sua lógica completa aqui
    if pontos[8][1] < pontos[6][1] and pontos[12][1] < pontos[10][1] and pontos[16][1] > pontos[14][1] and pontos[20][1] > pontos[18][1]:
        return "Papel"
    elif pontos[8][1] > pontos[6][1] and pontos[12][1] > pontos[10][1] and pontos[16][1] > pontos[14][1] and pontos[20][1] > pontos[18][1]:
        return "Pedra"
    elif pontos[8][1] < pontos[6][1] and pontos[12][1] < pontos[10][1] and pontos[16][1] > pontos[14][1] and pontos[20][1] < pontos[18][1]:
        return "Tesoura"
    return None

# Função para responder ao gesto do usuário
def responder_gesto(gesto):
    if gesto == "Pedra":
        return "Papel"
    elif gesto == "Papel":
        return "Tesoura"
    elif gesto == "Tesoura":
        return "Pedra"
    return None

# Função para enviar comando serial ao Arduino
def enviar_comando_serial(comando):
    if comando:
        arduino.write(comando.encode())
        time.sleep(0.1)

# Inicializar captura de vídeo
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Coletar pontos dos landmarks
            pontos = [(int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])) for lm in hand_landmarks.landmark]
            gesto = identificar_gesto(pontos)

            if gesto:
                resposta = responder_gesto(gesto)

                # Exibir o gesto detectado e a resposta com estilo
                desenhar_texto_estilizado(frame, f"Seu Gesto: {gesto}", (10, 50), font_scale=1.5, text_color=(255, 255, 255), bg_color=(50, 50, 50, 0.7))
                desenhar_texto_estilizado(frame, f"Resposta: {resposta}", (10, 120), font_scale=1.5, text_color=(255, 255, 255), bg_color=(200, 0, 0, 0.7))
                
                # Enviar o comando ao Arduino baseado na resposta
                enviar_comando_serial(resposta)

    cv2.imshow("Pedra, Papel ou Tesoura", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

# Fechar a conexão serial com o Arduino
arduino.close()
