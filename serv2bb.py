from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import random
import time
import threading
import asyncio
import RPi.GPIO as GPIO

# ========================================
# Função para solicitar pinos do usuário
# ========================================
def obter_pinos_gpio():
    """
    Solicita ao usuário que informe 2 pinos GPIO separados por vírgula.
    """
    entrada = input("Digite os 2 pinos GPIO que você usará para os LEDs, separados por vírgula (ex: 5,11): ")
    try:
        pinos = [int(p.strip()) for p in entrada.split(",")]
        if len(pinos) != 2:
            raise ValueError("Você deve informar exatamente 2 pinos.")
        return pinos
    except Exception as e:
        print("Erro na entrada dos pinos:", e)
        exit(1)

# ========================================
# Inicialização
# ========================================
app = FastAPI()
conexoes_ativas = []  # Lista de conexões WebSocket ativas

pinos_led = obter_pinos_gpio()  # Obtém os pinos definidos pelo usuário

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinos_led, GPIO.OUT)

sequencia_led = "00"  # Estado inicial dos LEDs

# ========================================
# Função para atualizar os LEDs
# ========================================
def atualizar_leds(sequencia):
    """
    Atualiza os dois LEDs com base na sequência fornecida.
    """
    global sequencia_led
    sequencia_led = sequencia
    for i, bit in enumerate(sequencia):
        GPIO.output(pinos_led[i], GPIO.HIGH if bit == '1' else GPIO.LOW)
    print(f"Sequência de LEDs atualizada: {sequencia}")

# ========================================
# Enviar sequência para todos os clientes
# ========================================
async def enviar_sequencia_para_clientes():
    """
    Envia a sequência atual para todos os clientes conectados via WebSocket.
    """
    for conexao in conexoes_ativas:
        await conexao.send_text(f"Nova sequência de LEDs: {sequencia_led}")

# ========================================
# Geração de sequência aleatória
# ========================================
def gerar_sequencia_aleatoria():
    """
    Gera uma nova sequência de 2 bits aleatoriamente a cada 30 segundos
    e envia para os clientes conectados.
    """
    global sequencia_led
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        nova_sequencia = ''.join(random.choice("01") for _ in range(2))
        atualizar_leds(nova_sequencia)
        loop.run_until_complete(enviar_sequencia_para_clientes())
        time.sleep(30)

# Inicia thread de geração aleatória
thread = threading.Thread(target=gerar_sequencia_aleatoria, daemon=True)
thread.start()

# ========================================
# WebSocket Endpoint
# ========================================
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Lida com a conexão WebSocket do cliente, recebendo comandos e enviando atualizações.
    """
    await websocket.accept()
    conexoes_ativas.append(websocket)
    try:
        while True:
            mensagem = await websocket.receive_text()
            print(f"Mensagem recebida do cliente: {mensagem}")
            atualizar_leds(mensagem)
            await enviar_sequencia_para_clientes()
    except WebSocketDisconnect:
        conexoes_ativas.remove(websocket)
