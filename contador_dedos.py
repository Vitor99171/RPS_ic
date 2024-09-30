import cv2 
import mediapipe as mp
import serial

# Inicialize a conexão serial
# ser = serial.Serial('COMX', 9600)  # Substitua 'COMX' pela porta serial do seu Arduino

video = cv2.VideoCapture(0)

hand = mp.solutions.hands 
Hand = hand.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

while True:
    check,img = video.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_RGB2HSV_FULL)
    results = Hand.process(imgRGB)
    handsPoints = results.multi_hand_landmarks
    h,w,_ = img.shape
    pontos= []
    if handsPoints:
        for points in handsPoints:
            mpDraw.draw_landmarks(img,points,hand.HAND_CONNECTIONS)
            for id, cord in enumerate(points.landmark):
                cx, cy = int(cord.x*w), int(cord.y*h)
                pontos.append((cx,cy))
        dedos = [8,12,16,20]
        contador = 0 
        if points:
            if pontos[4][0] < pontos [2][0]:
                contador +=1
            for x in dedos:
                if pontos[x][1] < pontos [x-2][1]:
                    contador +=1
        if contador == 2:
            cv2.putText(img,str("Tesoura"),(100,100),cv2.FONT_HERSHEY_SIMPLEX,4,(255,0,0),5)
            # ser.write(b'T')  # Envia 'T' para o Arduino
        elif contador == 5:
            cv2.putText(img,str("Papel"),(100,100),cv2.FONT_HERSHEY_SIMPLEX,4,(255,0,0),5)
            # ser.write(b'P')  # Envia 'P' para o Arduino
        elif contador == 0:
            cv2.putText(img,str("Pedra"),(100,100),cv2.FONT_HERSHEY_SIMPLEX,4,(255,0,0),5)
            # ser.write(b'R')  # Envia 'R' para o Arduino

    cv2.imshow("imagem",img)
    cv2.waitKey(1)  

