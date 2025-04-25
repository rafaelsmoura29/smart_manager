from fastapi import FastAPI
from pydantic import BaseModel
import RPi.GPIO as GPIO
import random
import threading
import time

# ========================================
# Função para solicitar pinos do usuário
# ========================================

def obter_pinos_uso():
    """
    Pergunta ao usuário quais 2 pinos GPIO serão usados para os LEDs.
    Espera uma entrada separada por vírgula, ex: 23,29
    """
    entrada = input("Digite os 2 pinos GPIO que você usará para os LEDs, separados por vírgula (ex: 23,29): ")
    try:
        pinos = [int(p.strip()) for p in entrada.split(",")]
        if len(pinos) != 2:
            raise ValueError("Você deve informar exatamente 2 pinos.")
        return pinos
    except Exception as e:
        print("Erro na entrada dos pinos:", e)
        exit(1)

# ========================================
# Inicialização dos pinos
# ========================================

pinos_led = obter_pinos_uso()  # Lista com 2 pinos definidos pelo usuário

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinos_led, GPIO.OUT)  # Define os pinos como saída

# ========================================
# Variável global para armazenar a sequência atual
# ========================================

sequencia_led = "00"  # Estado inicial: ambos os LEDs desligados

# ========================================
# Instância do FastAPI
# ========================================

app = FastAPI()

# ========================================
# Modelo para validar dados da requisição
# ========================================

class LEDSequencia(BaseModel):
    sequencia: str

# ========================================
# Função para atualizar os LEDs
# ========================================

def atualizar_leds(sequencia):
    """
    Atualiza o estado dos 2 LEDs com base em uma sequência de 2 bits.
    """
    global sequencia_led
    sequencia_led = sequencia
    for i, bit in enumerate(sequencia):
        GPIO.output(pinos_led[i], GPIO.HIGH if bit == '1' else GPIO.LOW)

# ========================================
# Geração automática de sequência aleatória
# ========================================

def gerar_sequencia_aleatoria():
    """
    Gera uma nova sequência aleatória a cada 30 segundos.
    """
    global sequencia_led
    while True:
        nova = ''.join(random.choice("01") for _ in range(2))
        atualizar_leds(nova)
        print(f"Nova sequência gerada: {nova}")
        time.sleep(30)

# Início da thread que atualiza os LEDs automaticamente
thread = threading.Thread(target=gerar_sequencia_aleatoria, daemon=True)
thread.start()

# ========================================
# Rotas da API
# ========================================

@app.get("/leds")
async def get_leds():
    """
    Retorna a sequência atual dos LEDs.
    """
    return {"sequencia": sequencia_led}

@app.post("/leds")
async def set_leds(sequencia: LEDSequencia):
    """
    Atualiza os LEDs com a sequência enviada via POST.
    """
    if len(sequencia.sequencia) == 2 and all(bit in "01" for bit in sequencia.sequencia):
        atualizar_leds(sequencia.sequencia)
        return {"mensagem": "Sequência de LEDs atualizada!", "sequencia": sequencia_led}
    else:
        return {"erro": "A sequência deve conter exatamente 2 bits (0 ou 1)."}
