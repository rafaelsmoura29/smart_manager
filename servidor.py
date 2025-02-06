from fastapi import FastAPI
from pydantic import BaseModel
import RPi.GPIO as GPIO
import random
import threading
import time

# Definindo os pinos de LED
led_pins = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5]

# Configurações do GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pins, GPIO.OUT)

# Variável global para armazenar a sequência de LEDs
led_sequencia = "0000000000"

# Instância do FastAPI
app = FastAPI()

# Classe para validar a sequência de LEDs
class LEDsequencia(BaseModel):
    sequencia: str

# Função para atualizar os LEDs com a sequência
def atualiza(sequencia):
    global led_sequencia
    led_sequencia = sequencia
    for i, bit in enumerate(sequencia):
        GPIO.output(led_pins[i], GPIO.HIGH if bit == '1' else GPIO.LOW)

# Função para gerar uma sequência aleatória a cada 30 segundos
def aleatorio():
    global led_sequencia
    while True:
        sequencia_ale = ''.join(random.choice("01") for _ in range(10))
        atualiza(sequencia_ale)
        print(f"Nova sequência gerada: {sequencia_ale}")
        time.sleep(30)

# Inicia a thread que gera sequências aleatórias
thread = threading.Thread(target=aleatorio, daemon=True)
thread.start()

# Rota GET para retornar a sequência de LEDs
@app.get("/leds")
async def get_leds():
    return {"sequencia": led_sequencia}

# Rota POST para atualizar a sequência de LEDs
@app.post("/leds")
async def set_leds(sequencia: LEDsequencia):
    atualiza(sequencia.sequencia)
    return {"mensagem": "Sequência de LEDs atualizada!", "sequencia": led_sequencia}
