import websocket
import socket

# ================================
# Função para obter IP do servidor
# ================================

def obter_ip_raspberry():
    """Pergunta ao usuário o IP da Raspberry ou tenta detectar automaticamente."""
    print("Digite o IP da Raspberry Pi (ou pressione Enter para tentar detectar automaticamente):")
    ip_digitado = input("IP: ")

    if ip_digitado.strip():
        return f"ws://{ip_digitado.strip()}:8000/ws"
    else:
        try:
            # Captura o IP local da máquina como tentativa (funciona se Raspberry for o gateway)
            hostname = socket.gethostname()
            ip_local = socket.gethostbyname(hostname)
            print(f"Usando IP local detectado: {ip_local}")
            return f"ws://{ip_local}:8000/ws"
        except Exception as e:
            print("Não foi possível detectar automaticamente. Por favor, tente inserir manualmente.")
            exit(1)

# ==================================
# Constante com o endereço do servidor
# ==================================
raspberry_pi_ip = obter_ip_raspberry()  # IP da Raspberry Pi fornecido ou detectado

# ==================================
# Função para enviar dados ao servidor
# ==================================
def enviar_sequencia_leds(ws, sequencia):
    """
    Envia uma sequência de 10 bits para o servidor via WebSocket.
    A sequência deve ser composta apenas por 0s e 1s.
    """
    if len(sequencia) == 10 and all(bit in "01" for bit in sequencia):
        ws.send(sequencia)
    else:
        print("Erro: A sequência deve ter exatamente 10 bits (0s e 1s).")

# ==================================
# Função chamada ao receber mensagem do servidor
# ==================================
def receber_mensagem(ws, mensagem):
    """
    Mostra no terminal a sequência de LEDs recebida do servidor.
    """
    print("Sequência recebida do servidor:", mensagem)

# ==================================
# Função de tratamento de erros
# ==================================
def ocorre_erro(ws, erro):
    """
    Exibe mensagem de erro do WebSocket.
    """
    print("Erro no WebSocket:", erro)

# ==================================
# Função chamada quando a conexão é encerrada
# ==================================
def fechar_conexao(ws, codigo_status, mensagem_fechamento):
    """
    Informa que a conexão WebSocket foi encerrada.
    """
    print("Conexão WebSocket fechada")

# ==================================
# Função chamada quando a conexão é aberta
# ==================================
def abrir_conexao(ws):
    """
    Envia uma sequência inicial de LEDs assim que a conexão é aberta.
    """
    print("Conexão WebSocket estabelecida")
    enviar_sequencia_leds(ws, "1110000000")  # Exemplo de sequência inicial

# ==================================
# Inicialização da conexão WebSocket
# ==================================
ws = websocket.WebSocketApp(raspberry_pi_ip,
                            on_message=receber_mensagem,
                            on_error=ocorre_erro,
                            on_close=fechar_conexao,
                            on_open=abrir_conexao)

# ==================================
# Execução do cliente WebSocket
# ==================================
ws.run_forever()
