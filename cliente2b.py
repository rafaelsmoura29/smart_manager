import requests

# Defina o IP da Raspberry Pi (substitua pelo IP correto)
raspberry_pi_ip = "http://10.102.78.7:8000"  # Alterar para o IP correto da sua Raspberry Pi

# Função para obter a sequência de LEDs atual
def get_led_sequence():
    response = requests.get(f"{raspberry_pi_ip}/leds")
    print("Sequência atual:", response.json()["sequencia"])
    print("Resposta do servidor:", response.json())

# Função para enviar uma nova sequência
def send_led_sequence(sequencia):
    payload = {"sequencia": sequencia}
    response = requests.post(f"{raspberry_pi_ip}/leds", json=payload)
    print("Resposta do servidor:", response.json())

# Exemplo de uso
get_led_sequence()  # Obtém a sequência atual
send_led_sequence("10")  # Envia uma nova sequência personalizada para os 2 LEDs
