#include <Servo.h>

Servo servoThumb;   // Servo do polegar
Servo servoIndex;   // Servo do indicador
Servo servoMiddle;  // Servo do dedo médio
Servo servoRing;    // Servo do anelar
Servo servoPinky;   // Servo do mindinho

void setup() {
  Serial.begin(9600);     // Inicializa a comunicação serial
  servoThumb.attach(8);   // Conecta o servo do polegar ao pino 8
  servoIndex.attach(7);   // Conecta o servo do indicador ao pino 7
  servoMiddle.attach(6);  // Conecta o servo do dedo médio ao pino 6
  servoRing.attach(10);   // Conecta o servo do anelar ao pino 10
  servoPinky.attach(9);   // Conecta o servo do mindinho ao pino 9

  // Coloca todos os dedos na posição inicial (abaixados)
  servoThumb.write(0);
  servoIndex.write(180);
  servoMiddle.write(180);
  servoRing.write(180);
  servoPinky.write(180);
}

void loop() {
  if (Serial.available() > 0) {                     // Verifica se há dados disponíveis na serial
    String comando = Serial.readStringUntil('!');  // Lê o comando até o caractere de nova linha

    if (comando == "P") {
      // Configuração para "Pedra" (todos os dedos abaixados)
      servoThumb.write(0);
      servoIndex.write(180);
      servoMiddle.write(180);
      servoRing.write(180);
      servoPinky.write(180);
    } else if (comando == "A") {
      // Configuração para "Papel" (todos os dedos levantados)
      servoThumb.write(180);
      servoIndex.write(0);
      servoMiddle.write(0);
      servoRing.write(0);
      servoPinky.write(0);
    } else if (comando == "T") {
      // Configuração para "Tesoura" (somente o indicador e o médio levantados)
      servoThumb.write(0);    // Polegar abaixado
      servoIndex.write(0);    // Indicador levantado
      servoMiddle.write(0);   // Médio levantado
      servoRing.write(180);   // Anelar abaixado
      servoPinky.write(180);  // Mindinho abaixado
    }

    delay(10);  // Adiciona um delay de 1 segundo após o comando antes de ler o próximo
  }
}
