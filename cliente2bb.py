import websocket
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
        return f"ws://{ip_digitado.strip()}:8000/ws"
    else:
        try:
            # Captura o IP local da máquina como tentativa
            hostname = socket.gethostname()
            ip_local = socket.gethostbyname(hostname)
            print(f"Usando IP local detectado: {ip_local}")
            return f"ws://{ip_local}:8000/ws"
        except Exception as e:
            print("Não foi possível detectar automaticamente. Por favor, tente inserir manualmente.")
            exit(1)

# =========================
# Constante com o endereço
# =========================

raspberry_pi_ip = obter_ip_raspberry()  # Endereço do servidor (WebSocket)

# ====================================
# Função para enviar nova sequência
# ====================================

def enviar_sequencia_leds(ws, sequencia):
    """
    Envia uma nova sequência de 2 bits para o servidor via WebSocket.
    A sequência deve conter apenas os dígitos '0' ou '1'.
    """
    if len(sequencia) == 2 and all(bit in "01" for bit in sequencia):
        ws.send(sequencia)
    else:
        print("Erro: a sequência deve conter exatamente 2 bits (0s e 1s).")

# ====================================
# Função chamada ao receber mensagem
# ====================================

def receber_mensagem(ws, mensagem):
    """
    Mostra no terminal a sequência de LEDs recebida do servidor.
    """
    print("Sequência recebida do servidor:", mensagem)

# ====================================
# Função de tratamento de erros
# ====================================

def ocorre_erro(ws, erro):
    """
    Exibe mensagem de erro do WebSocket.
    """
    print("Erro no WebSocket:", erro)

# ====================================
# Função chamada quando a conexão é encerrada
# ====================================

def fechar_conexao(ws, codigo_status, mensagem_fechamento):
    """
    Informa que a conexão WebSocket foi encerrada.
    """
    print("Conexão WebSocket fechada")

# ====================================
# Função chamada ao abrir a conexão
# ====================================

def abrir_conexao(ws):
    """
    Pergunta ao usuário uma sequência inicial e a envia ao servidor.
    """
    print("Conexão WebSocket estabelecida")
    sequencia = input("Digite a sequência inicial de 2 bits (ex: 10): ")
    enviar_sequencia_leds(ws, sequencia)

# ====================================
# Inicialização da conexão WebSocket
# ====================================

ws = websocket.WebSocketApp(raspberry_pi_ip,
                            on_message=receber_mensagem,
                            on_error=ocorre_erro,
                            on_close=fechar_conexao,
                            on_open=abrir_conexao)

# ====================================
# Execução do cliente WebSocket
# ====================================

ws.run_forever()
