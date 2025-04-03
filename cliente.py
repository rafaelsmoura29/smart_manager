import websocket

# IP da Raspberry Pi (servidor)
raspberry_pi_ip = "ws://10.102.78.7:8000/ws"

# Função para enviar a sequência de LEDs para o servidor via WebSocket
def enviar_sequencia_leds(ws, sequencia):
    if len(sequencia) == 10 and all(bit in "01" for bit in sequencia):
        ws.send(sequencia)  # Envia a nova sequência para o servidor
    else:
        print("Erro: A sequência deve ter exatamente 10 bits (0s e 1s).")

# Função para receber as atualizações de LEDs via WebSocket
def receber_mensagem(ws, mensagem):
    print("Sequência recebida do servidor:", mensagem)

# Função que lida com erros
def ocorre_erro(ws, erro):
    print("Erro no WebSocket:", erro)

# Função para quando o WebSocket for fechado
def fechar_conexao(ws, codigo_status, mensagem_fechamento):
    print("Conexão WebSocket fechada")

# Função para quando a conexão WebSocket for estabelecida
def abrir_conexao(ws):
    print("Conexão WebSocket estabelecida")
    # Enviar uma sequência inicial de LEDs (exemplo: acender os 3 primeiros LEDs)
    enviar_sequencia_leds(ws, "1110000000")

# Cria a conexão WebSocket
ws = websocket.WebSocketApp(raspberry_pi_ip,
                            on_message=receber_mensagem,
                            on_error=ocorre_erro,
                            on_close=fechar_conexao,
                            on_open=abrir_conexao)

# Rodando o WebSocket
ws.run_forever()
