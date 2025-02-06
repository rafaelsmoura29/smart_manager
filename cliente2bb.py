import websocket

# IP da Raspberry Pi (servidor)
raspberry_pi_ip = "ws://10.102.78.7:8000/ws"

# Função para enviar a sequência de LEDs para o servidor via WebSocket
def enviar_sequencia_leds(ws, sequencia):
    ws.send(sequencia)  # Envia a nova sequência para o servidor

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
    # Aqui podemos enviar uma nova sequência caso o cliente deseje
    enviar_sequencia_leds(ws, "11")  # Exemplo: envia "11" para acender os dois LEDs

# Cria a conexão WebSocket
ws = websocket.WebSocketApp(raspberry_pi_ip,
                            on_message=receber_mensagem,
                            on_error=ocorre_erro,
                            on_close=fechar_conexao,
                            on_open=abrir_conexao)

# Rodando o WebSocket
ws.run_forever()