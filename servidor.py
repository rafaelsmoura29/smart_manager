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
    Pergunta ao usuário quais pinos da Raspberry Pi serão utilizados.
    Espera uma entrada separada por vírgula, ex: 2,3,4,5,6,7,8,9,10,11
    """
    entrada = input("Digite os 10 pinos GPIO que você usará para os LEDs, separados por vírgula (ex: 2,3,4,...): ")
    try:
        pinos = [int(p.strip()) for p in entrada.split(",")]
        if len(pinos) != 10:
            raise ValueError("Você deve informar exatamente 10 pinos.")
        return pinos
    except Exception as e:
        print("Erro na entrada dos pinos:", e)
        exit(1)

# ========================================
# Inicialização dos pinos
# ========================================

pinos_led = obter_pinos_uso()  # Lista dos pinos definidos pelo usuário

# Configuração do modo de operação do GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinos_led, GPIO.OUT)  # Define os pinos como saída

# ========================================
# Variável global com a sequência de LEDs
# ========================================

sequencia_led = "0000000000"  # Estado inicial: todos os LEDs desligados

# ========================================
# Instância da aplicação FastAPI
# ========================================

app = FastAPI()

# ========================================
# Classe para validação dos dados recebidos
# ========================================

class LEDSequencia(BaseModel):
    sequencia: str

# ========================================
# Função para atualizar o estado dos LEDs
# ========================================

def atualizar_leds(sequencia):
    """
    Atualiza o estado dos LEDs com base em uma sequência de 10 bits.
    """
    global sequencia_led
    sequencia_led = sequencia
    for i, bit in enumerate(sequencia):
        GPIO.output(pinos_led[i], GPIO.HIGH if bit == '1' else GPIO.LOW)

# ========================================
# Função para gerar sequência aleatória
# ========================================

def gerar_sequencia_aleatoria():
    """
    Gera uma nova sequência de 10 bits aleatoriamente a cada 30 segundos
    e atualiza os LEDs com essa nova sequência.
    """
    global sequencia_led
    while True:
        nova_sequencia = ''.join(random.choice("01") for _ in range(10))
        atualizar_leds(nova_sequencia)
        print(f"Nova sequência gerada: {nova_sequencia}")
        time.sleep(30)

# Início da thread para alternar as sequências automaticamente
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
    Atualiza a sequência de LEDs a partir da string enviada.
    A string deve conter exatamente 10 bits (apenas '0' ou '1').
    """
    if len(sequencia.sequencia) == 10 and all(bit in "01" for bit in sequencia.sequencia):
        atualizar_leds(sequencia.sequencia)
        return {"mensagem": "Sequência de LEDs atualizada!", "sequencia": sequencia_led}
    else:
        return {"erro": "A sequência deve ter exatamente 10 bits contendo apenas 0s e 1s."}
