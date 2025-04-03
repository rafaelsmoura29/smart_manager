# smart_manager
# Smart Manager

Este projeto permite o controle de LEDs conectados a uma Raspberry Pi utilizando WebSockets e FastAPI. O sistema é composto por diferentes clientes e servidores para suportar tanto comunicação via WebSocket quanto via requisições HTTP convencionais.

## Estrutura do Projeto

O projeto contém os seguintes arquivos:

- **cliente.py** → Cliente que se comunica via WebSocket e controla 10 LEDs.
- **cliente2bits.py** → Cliente que envia e recebe sequências de 2 bits sem WebSocket, utilizando apenas GET e POST.
- **cliente2bitsws.py** → Cliente que se comunica via WebSocket, mas controla apenas 2 LEDs.
- **servidor.py** → Servidor WebSocket que controla 10 LEDs na Raspberry Pi.
- **serv2bitsws.py** → Servidor WebSocket que controla apenas 2 LEDs na Raspberry Pi.
- **serv2bits.py** → Servidor HTTP convencional que controla apenas 2 LEDs, sem WebSockets.

## Como Utilizar

### 1. Controle de 10 LEDs via WebSocket

- Execute **servidor.py** na Raspberry Pi.
- Execute **cliente.py** no seu PC.

### 2. Controle de 2 LEDs sem WebSocket

- Execute **serv2bits.py** na Raspberry Pi.
- Execute **cliente2bits.py** no seu PC.

### 3. Controle de 2 LEDs via WebSocket

- Execute **serv2bitsws.py** na Raspberry Pi.
- Execute **cliente2bitsws.py** no seu PC.

## Requisitos

- Raspberry Pi com GPIO configurado.
- Python 3 instalado.
- Bibliotecas necessárias:
  ```sh
  pip install fastapi pydantic websockets RPi.GPIO
  ```
- Para rodar o servidor FastAPI, utilize:
  ```sh
  uvicorn servidor:app --host 0.0.0.0 --port 8000 --reload
  ```

## Autor
Desenvolvido para controle remoto de LEDs via Raspberry Pi e comunicação em tempo real com WebSockets.

