import serial
import time

arduino = serial.Serial('COM5', 9600)  # Troque pela porta correta
time.sleep(2)  # Aguarda a conexão

while True:
    comando = input("Digite P para Pedra, A para Papel, T para Tesoura ou Q para sair: ").upper()
    
    if comando in ['P', 'A', 'T']:
        arduino.write(comando.encode())  # Envia o comando via serial
        print(f"Comando {comando} enviado para o Arduino.")
    elif comando == 'Q':
        print("Encerrando comunicação.")
        break

arduino.close()
