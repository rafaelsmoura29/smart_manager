import requests

# Defina o IP da Raspberry Pi (substitua pelo IP correto)
ip_raspberry_pi = "http://10.102.78.7:8000"

# Função para obter a sequência atual dos LEDs
def obter_sequencia_leds():
    resposta = requests.get(f"{ip_raspberry_pi}/leds")  # Faz uma requisição GET para o servidor da Raspberry Pi no endpoint /leds.
    try:
        dados = resposta.json() # Se a resposta não for um JSON válido, o programa entrará no bloco except.
        print("Resposta completa do servidor:", dados)  # Exibe a resposta antes de acessar os dados
        if "sequencia" in dados:
            print("Sequência atual:", dados["sequencia"]) # Imprime a sequência de LEDs atual.
        else:
            print("Erro: resposta inesperada do servidor!")
    except Exception as e:
        print("Erro ao processar a resposta do servidor:", e)

# Função para enviar uma nova sequência de LEDs
def enviar_sequencia_leds(sequencia):
    dados_envio = {"sequencia": sequencia}
    resposta = requests.post(f"{ip_raspberry_pi}/leds", json=dados_envio)
    print("Resposta do servidor:", resposta.json())

# Exemplo de uso
obter_sequencia_leds()  # Obtém a sequência atual dos LEDs
enviar_sequencia_leds("1010101011")  # Envia uma nova sequência personalizada
