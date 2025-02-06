from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import random
import time
import threading
import asyncio
import RPi.GPIO as GPIO

app = FastAPI()
active_connections = []  # Lista para armazenar os clientes conectados

# Defina os pinos de LED
led_pins = [5, 11]

# Configura o GPIO da Raspberry Pi
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pins, GPIO.OUT)

led_sequencia = "00"  # Sequência inicial

# Função para atualizar os LEDs na Raspberry Pi
def atualiza_leds(sequencia):
    global led_sequencia
    led_sequencia = sequencia
    for i, bit in enumerate(sequencia):
        GPIO.output(led_pins[i], GPIO.HIGH if bit == '1' else GPIO.LOW)
    print(f"Sequência de LEDs atualizada: {sequencia}")

# Função para enviar a sequência de LEDs para todos os clientes conectados
async def env_led_sequencia():
    for connection in active_connections:
        await connection.send_text(f"Nova sequência de LEDs: {led_sequencia}")

# Função que gera uma nova sequência aleatória a cada 30 segundos
def aleatorio():
    global led_sequencia
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        led_sequencia = ''.join(random.choice("01") for _ in range(2))  # Sequência de 2 LEDs
        print(f"Nova sequência gerada: {led_sequencia}")
        atualiza_leds(led_sequencia)  # Atualiza a sequência de LEDs
        loop.run_until_complete(env_led_sequencia())  # Envia para os clientes
        time.sleep(30)

# Inicia a thread que gera a sequência aleatória
thread = threading.Thread(target=aleatorio, daemon=True)
thread.start()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Mensagem recebida do cliente: {data}")
            # Atualiza a sequência de LEDs com a mensagem recebida
            atualiza_leds(data)
            # Envia a nova sequência de LEDs para todos os clientes
            await env_led_sequencia()
    except WebSocketDisconnect:
        active_connections.remove(websocket)



