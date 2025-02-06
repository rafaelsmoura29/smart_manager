import requests

# Defina o IP da Raspberry Pi (substitua pelo IP correto)
raspberry_pi_ip = "http://10.102.78.7:8000"

# Função para obter a sequência de LEDs atual
def get_led_sequence():
    response = requests.get(f"{raspberry_pi_ip}/leds")
    try:
        data = response.json()
        print("Resposta completa do servidor:", data)  # Ver resposta antes de acessar
        if "sequencia" in data:
            print("Sequência atual:", data["sequencia"])
        else:
            print("Erro: resposta inesperada do servidor!")
    except Exception as e:
        print("Erro ao processar resposta do servidor:", e)

# Função para enviar uma nova sequência
def send_led_sequence(sequencia):
    payload = {"sequencia": sequencia}
    response = requests.post(f"{raspberry_pi_ip}/leds", json=payload)
    print("Resposta do servidor:", response.json())

# Exemplo de uso
get_led_sequence()  # Obtém a sequência atual
send_led_sequence("1010101011")  # Envia uma nova sequência personalizada

