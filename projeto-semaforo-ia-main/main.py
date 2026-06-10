import cv2
import serial
import time

# --- CONFIGURAÇÃO SERIAL ---
try:
    arduino = serial.Serial('COM4', 9600, timeout=1)
    time.sleep(2) 
    print("Conectado ao Arduino com sucesso!")
except:
    print("Erro: Não foi possível conectar ao Arduino. Verifique a porta COM.")
    exit()

# --- CONFIGURAÇÃO DA IA (OPENCV NATIVO) ---
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

# Configura a resolução da câmera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# --- VARIÁVEIS DE CONTROLE DOS CICLOS ---
MODO_ATUAL = "CURTO" 
SINAL_ABERTO = True  

inicio_do_verde = time.time()
tempo_bloqueado_ate = 0
pedestre_detectado = False
ultimo_segundo_printado = -1
frames_com_rosto = 0
FRAMES_NECESSARIOS = 3 

print("🚦 [CICLO CURTO] Sinal Verde. Aguardando 15s de cooldown...")

while cap.isOpened():
    success, image = cap.read()
    if not success: break

    tempo_atual = time.time()

    if not SINAL_ABERTO:
        if tempo_atual >= tempo_bloqueado_ate:
            SINAL_ABERTO = True
            inicio_do_verde = time.time() 
            ultimo_segundo_printado = -1
            pedestre_detectado = False
            print(f"\n🔄 Sinal Verde reiniciado! Modo Atual: {MODO_ATUAL}")
    else:
        tempo_decorrido = int(tempo_atual - inicio_do_verde)

        # 1. DETECÇÃO DO PEDESTRE COM OPENCV
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            frames_com_rosto += 1
            if frames_com_rosto >= FRAMES_NECESSARIOS and not pedestre_detectado:
                # Se estiver no Ciclo Curto, só valida o pedestre após o cooldown de 15s
                if MODO_ATUAL == "CURTO" and tempo_decorrido >= 15:
                    print("\n👤 Pedestre detectado após o cooldown! Fechando sinal...")
                    pedestre_detectado = True
                # Se estiver no Ciclo Longo, o pedestre pode ser detectado a qualquer momento (mas o sinal só fecha em 60s)
                elif MODO_ATUAL == "LONGO":
                    pedestre_detectado = True
            
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        else:
            frames_com_rosto = 0

        # 2. EXIBIÇÃO DO TEMPO NO TERMINAL
        # Agora o limite visível no terminal para ambos os ciclos passa a ser 60s se ninguém aparecer
        tempo_limite = 60
        if tempo_decorrido != ultimo_segundo_printado and tempo_decorrido <= tempo_limite:
            print(f"🚗 Verde ({MODO_ATUAL}): {tempo_decorrido}s / {tempo_limite}s", end="\r")
            ultimo_segundo_printado = tempo_decorrido

        # 3. LÓGICA DE DECISÃO DOS CICLOS REVISADA
        if MODO_ATUAL == "CURTO":
            # Condição A: Pedestre detectado (apenas após os 15s de cooldown)
            if pedestre_detectado:
                print("\n🚨 [CICLO CURTO] Fechando por pedestre! Avançando para Ciclo Longo. (Espera: 10s)")
                arduino.write(b'P') 
                tempo_bloqueado_ate = tempo_atual + 3 + 10 
                SINAL_ABERTO = False
                MODO_ATUAL = "LONGO" # Vai para o ciclo longo compensar os carros na volta
            
            # Condição B: Chegou no limite de 60s sem nenhum pedestre aparecer
            elif tempo_decorrido >= 60:
                print("\n⏰ [CICLO CURTO] 60s atingidos sem pedestre. Fechando padrão e MANTENDO Ciclo Curto! (Espera: 15s)")
                arduino.write(b'N') 
                tempo_bloqueado_ate = tempo_atual + 3 + 15 
                SINAL_ABERTO = False
                MODO_ATUAL = "CURTO" # MANTÉM no ciclo curto para a próxima abertura

        elif MODO_ATUAL == "LONGO":
            # No ciclo longo, ele obrigatoriamente espera os 60s inteiros passarem
            if tempo_decorrido >= 60:
                print("\n⏰ [CICLO LONGO] 60s atingidos de compensação. Fechando padrão! (Espera: 15s)")
                arduino.write(b'N') 
                tempo_bloqueado_ate = tempo_atual + 3 + 15 
                SINAL_ABERTO = False
                MODO_ATUAL = "CURTO" # Sempre retorna para o modo curto para monitorar a rua

    cv2.imshow('Detector de Pedestres', image)
    if cv2.waitKey(5) & 0xFF == 27: break 

cap.release()
cv2.destroyAllWindows()
arduino.close()