from fastapi import FastAPI
from pydantic import BaseModel
import RPi.GPIO as GPIO
import random
import threading
import time

# Definindo os pinos de LED (10 pinos)
led_pins = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# Configurações do GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pins, GPIO.OUT)

# Variável global para armazenar a sequência de LEDs
led_sequencia = "0000000000"  # Sequência inicial para 10 LEDs

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
        sequencia_ale = ''.join(random.choice("01") for _ in range(10))  # Gerando sequência de 10 bits
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
    if len(sequencia.sequencia) == 10 and all(bit in "01" for bit in sequencia.sequencia):
        atualiza(sequencia.sequencia)
        return {"mensagem": "Sequência de LEDs atualizada!", "sequencia": led_sequencia}
    else:
        return {"erro": "A sequência deve ter exatamente 10 bits contendo apenas 0s e 1s."}
