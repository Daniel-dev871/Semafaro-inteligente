# 🚦 Semáforo Inteligente com Visão Computacional (OpenCV Puro + Arduino)

Este projeto implementa um sistema de semáforo inteligente urbano baseado em engenharia de tráfego dinâmica. Utilizando visão computacional nativa para monitorar a presença de pedestres na calçada através de uma webcam, o sistema alterna o tempo de abertura e fechamento das vias de forma eficiente, otimizando o fluxo de veículos e garantindo a segurança na travessia.

---

## 🧠 Lógica de Funcionamento (Máquina de Estados)

O sistema opera alternando entre dois ciclos principais de tráfego, priorizando a fluidez dos veículos quando a via está vazia e compensando o fluxo após uma travessia:

* **Ciclo Curto (15 segundos de Cooldown):** O semáforo dos carros abre e garante um tempo mínimo obrigatório de 15 segundos para o trânsito fluir. 
    * **Com Pedestre:** Se a IA detetar um pedestre, o sinal aguarda o fim do cooldown (15s) e fecha imediatamente por **10 segundos** para a travessia. Ao reabrir, avança para o **Ciclo Longo** para compensar os carros.
    * **Sem Pedestre:** Se nenhum pedestre for detetado até aos 15 segundos, o sinal **não fecha**. Ele continua aberto monitorizando a rua. Se atingir o limite máximo de **60 segundos** sem ninguém aparecer, o sinal fecha por tempo padrão (15 segundos) e, ao reabrir, **mantém-se no Ciclo Curto**.
* **Ciclo Longo (60 segundos de Compensação):** Ativado apenas após o sinal ter sido forçado a fechar por um pedestre. Mantém o sinal verde para os carros por **60 segundos obrigatórios**, garantindo que a avenida escoe o trânsito acumulado. Ao fim deste tempo, fecha no modo padrão por **15 segundos** e retorna ao Ciclo Curto.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagens:** Python 3.13+ & C++ (Arduino IDE)
* **Visão Computacional:** OpenCV Nativo (Algoritmo Haar Cascade `haarcascade_frontalface_default.xml`)
* **Comunicação:** PySerial (Protocolo de comunicação serial a 9600 bps)
* **Hardware:** Arduino Uno/Mega, 3 LEDs para o semáforo dos carros (Verde, Amarelo, Vermelho) e 2 LEDs para o semáforo dos pedestres (Verde, Vermelho).

---

## 🔌 Esquema de Ligação do Hardware

Conecte os LEDs nos pinos digitais do Arduino utilizando resistores adequados (ex: 220Ω):

| Componente | Pino Digital Arduino |
| :--- | :--- |
| 🔴 LED Vermelho (Carro) | `Pin 13` |
| 🟡 LED Amarelo (Carro) | `Pin 12` |
| 🟢 LED Verde (Carro) | `Pin 11` |
| 🔴 LED Vermelho (Pedestre) | `Pin 10` |
| 🟢 LED Verde (Pedestre) | `Pin 9` |

---

## 🚀 Como Executar o Projeto

### 1. Configuração do Arduino
1. Abra o arquivo `.ino` localizado na pasta do projeto utilizando a **Arduino IDE**.
2. Certifique-se de selecionar a placa correta e a porta correspondente (ex: `COM4`).
3. Faça o **Upload** do código para a placa.
4. **Importante:** Feche a Arduino IDE após o upload para liberar a porta serial para o Python.

### 2. Configuração do Ambiente Python
Certifique-se de estar com o ambiente virtual (`venv`) ativo no seu terminal e instale as dependências necessárias:

```bash
# Ativar ambiente virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Atualizar o gerenciador de pacotes
python -m pip install --upgrade pip

# Instalar as dependências compatíveis com Python 3.13+
pip install opencv-python pyserial