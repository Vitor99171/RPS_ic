# Pedra, Papel ou Tesoura com Detecção de Gestos

Este projeto implementa o clássico jogo de **Pedra, Papel ou Tesoura** utilizando visão computacional para detectar os gestos das mãos em tempo real. A detecção de gestos é realizada com a biblioteca **MediaPipe**, enquanto a interface de captura e exibição do vídeo é gerenciada pelo **OpenCV**.

---

## :sparkles: **Funcionalidades**

- **Detecção de Gestos em Tempo Real**: Detecta automaticamente os gestos "Pedra", "Papel" e "Tesoura" com base na posição dos dedos da mão.
- **Resposta Automatizada**: O sistema responde ao gesto do jogador de acordo com as regras clássicas do jogo:
    - Se o jogador fizer **Pedra**, o sistema responde com **Papel**.
    - Se o jogador fizer **Papel**, o sistema responde com **Tesoura**.
    - Se o jogador fizer **Tesoura**, o sistema responde com **Pedra**.
- **Exibição Estilizada**: O texto que indica o gesto do jogador e a resposta do sistema é exibido com fundo semi-transparente, tornando a interface mais limpa e fácil de ler.

---

## :computer: **Tecnologias Utilizadas**

- **Python 3.7+**
- **OpenCV**: Para captura de vídeo em tempo real e renderização na tela.
- **MediaPipe**: Para a detecção de landmarks da mão e identificação dos gestos.
- **Math**: Para cálculos simples, como a distância entre dois pontos.

---

## :gear: **Pré-requisitos**

Certifique-se de ter o **Python 3.7+** instalado em seu sistema, além das seguintes bibliotecas:

- `opencv-python`
- `mediapipe`

### :package: Instalação de Dependências

Utilize o **pip** para instalar as dependências do projeto:

```bash
pip install opencv-python mediapipe

```
## :rocket: **Como Executar**

O projeto utiliza a biblioteca **MediaPipe** para detectar landmarks nas mãos do jogador. Esses landmarks são processados para identificar se os dedos estão levantados ou abaixados, determinando qual gesto está sendo feito (**Pedra**, **Papel** ou **Tesoura**).

### :raised_hand: **Detecção dos Gestos**

- **Pedra**: Todos os dedos estão fechados.
- **Papel**: Todos os dedos estão esticados.
- **Tesoura**: Somente o dedo indicador e o dedo médio estão esticados.

### :game_die: **Resposta do Sistema**

Após o gesto ser detectado, o sistema automaticamente escolhe a jogada que venceria o gesto do jogador, garantindo uma resposta lógica.

---

## :wrench: **Personalizações**

### :camera: **Câmera**

Para utilizar uma câmera IP, altere o valor da variável `url` no código para a URL da sua câmera.

### :art: **Aparência**

A função `desenhar_texto_estilizado` pode ser ajustada para modificar cores, tamanhos de fonte, e o nível de transparência do fundo dos textos exibidos na tela.

---

## :video_game: **Exemplo de Uso**

1. O jogador faz o gesto de "Pedra" na frente da câmera.
2. O sistema reconhece o gesto como **Pedra** e exibe na tela.
3. O sistema responde com **Papel** (já que o papel ganha da pedra) e exibe a resposta na tela.

---
