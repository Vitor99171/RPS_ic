import cv2
import mediapipe as mp
import math

# Configuração do MediaPipe para a detecção de mãos
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Função para calcular a distância entre dois pontos
def calcular_distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Função para identificar o gesto da mão com base em landmarks
def identificar_gesto(pontos):
    # Verificação dedo por dedo se está levantado ou não
    def dedo_levantado(tip, pip):
        return pontos[tip][1] < pontos[pip][1]  # Verifica se a ponta está acima da articulação proximal (PIP)

    # Verifica cada dedo individualmente
    polegar_levantado = pontos[4][0] > pontos[3][0]  # Verifica se o polegar está esticado (no eixo X)
    indicador_levantado = dedo_levantado(8, 6)  # Verifica se o indicador está levantado
    medio_levantado = dedo_levantado(12, 10)  # Verifica se o médio está levantado
    anelar_levantado = dedo_levantado(16, 14)  # Verifica se o anelar está levantado
    mindinho_levantado = dedo_levantado(20, 18)  # Verifica se o mindinho está levantado

    # Definição dos gestos com base nos dedos levantados
    # Pedra: Todos os dedos abaixados
    if not polegar_levantado and not indicador_levantado and not medio_levantado and not anelar_levantado and not mindinho_levantado:
        return "Pedra"
    # Papel: Todos os dedos levantados
    elif polegar_levantado and indicador_levantado and medio_levantado and anelar_levantado and mindinho_levantado:
        return "Papel"
    # Tesoura: Somente o indicador e o médio levantados
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

# Função para desenhar texto com fundo transparente estilizado
def desenhar_texto_estilizado(frame, text, pos, font_scale=1, font_thickness=2, font=cv2.FONT_HERSHEY_SIMPLEX, text_color=(255, 0, 255), bg_color=(0, 0, 0, 0.5)):
    # Desenhar fundo para o texto
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    x, y = pos
    bg_color_bgr = bg_color[:]  
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y - text_height - 10), (x + text_width + 10, y + 10), bg_color_bgr, -1)
    cv2.putText(overlay, text, (x + 5, y), font, font_scale, text_color, font_thickness)

    alpha = bg_color[3]
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

# Captura de vídeo da câmera IP ou webcam local
url = 0  # Substitua pela URL correta ou use '0' para webcam local
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

            # Coletar pontos dos landmarks
            pontos = [(int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])) for lm in hand_landmarks.landmark]
            gesto = identificar_gesto(pontos)

            if gesto:
                resposta = responder_gesto(gesto)
                
                # Exibir o gesto detectado e a resposta estilizada
                desenhar_texto_estilizado(frame, f"Seu Gesto: {gesto}", (10, 50), font_scale=1.5, text_color=(255, 0, 255), bg_color=(50, 50, 50, 0.7))
                desenhar_texto_estilizado(frame, f"Resposta: {resposta}", (10, 120), font_scale=1.5, text_color=(255, 0, 255), bg_color=(200, 0, 0, 0.7))

    cv2.imshow("Pedra, Papel ou Tesoura", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
