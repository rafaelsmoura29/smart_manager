import requests
import socket

# ====================================
# Função para obter IP do servidor
# ====================================

def obter_ip_raspberry():
    """
    Pergunta ao usuário o IP da Raspberry Pi ou tenta detectar automaticamente.
    """
    print("Digite o IP da Raspberry Pi (ou pressione Enter para tentar detectar automaticamente):")
    ip_digitado = input("IP: ")

    if ip_digitado.strip():
        return f"http://{ip_digitado.strip()}:8000"
    else:
        try:
            # Captura o IP local da máquina como tentativa
            hostname = socket.gethostname()
            ip_local = socket.gethostbyname(hostname)
            print(f"Usando IP local detectado: {ip_local}")
            return f"http://{ip_local}:8000"
        except Exception as e:
            print("Não foi possível detectar automaticamente. Por favor, tente inserir manualmente.")
            exit(1)

# =========================
# Constante com o endereço
# =========================

raspberry_pi_ip = obter_ip_raspberry()  # Endereço do servidor (Raspberry Pi)

# ====================================
# Função para receber sequência atual
# ====================================

def receber_mensagem():
    """
    Faz uma requisição GET ao servidor para obter a sequência atual dos LEDs.
    """
    try:
        resposta = requests.get(f"{raspberry_pi_ip}/leds")
        if resposta.status_code == 200:
            dados = resposta.json()
            print("Sequência atual:", dados["sequencia"])
        else:
            print("Erro ao obter a sequência: código", resposta.status_code)
    except Exception as e:
        print("Erro na comunicação com o servidor:", e)

# ====================================
# Função para enviar nova sequência
# ====================================

def enviar_sequencia_leds(sequencia):
    """
    Envia uma nova sequência de 2 bits para os LEDs via POST.
    A sequência deve conter apenas os dígitos '0' ou '1'.
    """
    if len(sequencia) == 2 and all(bit in "01" for bit in sequencia):
        try:
            payload = {"sequencia": sequencia}
            resposta = requests.post(f"{raspberry_pi_ip}/leds", json=payload)
            print("Resposta do servidor:", resposta.json())
        except Exception as e:
            print("Erro ao enviar a sequência:", e)
    else:
        print("Erro: a sequência deve conter exatamente 2 bits (0s e 1s).")

# ====================================
# Execução do cliente
# ====================================

if __name__ == "__main__":
    while True:
        print("\n1 - Receber sequência atual")
        print("2 - Enviar nova sequência")
        print("3 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            receber_mensagem()
        elif escolha == "2":
            nova_sequencia = input("Digite a nova sequência de 2 bits (ex: 01): ")
            enviar_sequencia_leds(nova_sequencia)
        elif escolha == "3":
            print("Encerrando o cliente.")
            break
        else:
            print("Opção inválida.")
