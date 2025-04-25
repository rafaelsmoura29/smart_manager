# Smart Manager

Este projeto permite o controle de LEDs conectados a uma Raspberry Pi utilizando WebSockets e FastAPI. O sistema é composto por diferentes clientes e servidores para suportar tanto comunicação via WebSocket quanto via requisições HTTP convencionais.

## 📂 Estrutura do Projeto

O projeto contém os seguintes arquivos:

- **cliente.py** → Cliente que se comunica via WebSocket e controla 10 LEDs.
- **cliente2bits.py** → Cliente que envia e recebe sequências de 2 bits sem WebSocket, utilizando apenas GET e POST.
- **cliente2bitsws.py** → Cliente que se comunica via WebSocket, mas controla apenas 2 LEDs.
- **servidor.py** → Servidor WebSocket que controla 10 LEDs na Raspberry Pi.
- **serv2bitsws.py** → Servidor WebSocket que controla apenas 2 LEDs na Raspberry Pi.
- **serv2bits.py** → Servidor HTTP convencional que controla apenas 2 LEDs, sem WebSockets.

---
## 📝 Detalhes sobre os Arquivos

- **cliente.py** → Cliente WebSocket para 10 LEDs
Este script permite ao cliente controlar 10 LEDs conectados à Raspberry Pi via WebSocket. Ele estabelece uma comunicação em tempo real com o servidor WebSocket, enviando sequências de LEDs (compostas por 10 bits) e recebendo atualizações do servidor. O código agora permite que o cliente insira dinamicamente o IP da Raspberry Pi antes de se conectar.

- **cliente2bits.py** → Cliente HTTP para 2 LEDs
Neste script, o cliente interage com o servidor HTTP para controlar 2 LEDs. Ele utiliza as requisições HTTP GET e POST para obter e enviar sequências de LEDs. A sequência de LEDs é composta por 2 bits. O cliente agora permite que o usuário insira o IP da Raspberry Pi de maneira interativa, similar ao cliente.py.

- **cliente2bitsws.py** → Cliente WebSocket para 2 LEDs
Este script é uma versão mais simples do cliente.py, mas controlando apenas 2 LEDs. Ele utiliza WebSockets para comunicação com o servidor e permite ao cliente enviar e receber sequências de 2 bits. Assim como o cliente.py, ele permite que o usuário informe o IP da Raspberry Pi de forma interativa.

- **servidor.py** → Servidor WebSocket para 10 LEDs
O servidor WebSocket que gerencia 10 LEDs na Raspberry Pi. Ele aceita conexões de clientes, atualiza os LEDs de acordo com a sequência recebida e envia a sequência de volta para todos os clientes conectados. Agora, o código permite que o usuário insira dinamicamente os pinos GPIO que deseja usar para os LEDs.

- **serv2bits.py** → Servidor HTTP para 2 LEDs
Este servidor HTTP permite controlar 2 LEDs utilizando requisições HTTP. Ele possui rotas GET e POST para ler e alterar a sequência de LEDs. O código foi ajustado para permitir que o usuário insira os pinos GPIO que deseja utilizar.

- **serv2bitsws.py** → Servidor WebSocket para 2 LEDs
Este servidor WebSocket é projetado para controlar 2 LEDs via WebSocket. Ele mantém uma lista de conexões ativas e envia a sequência de LEDs para todos os clientes conectados. O código agora permite que o usuário insira os pinos GPIO para os LEDs dinamicamente, melhorando a flexibilidade.

## 🚀 Como Utilizar

### 1. Controle de 10 LEDs via WebSocket

**Na Raspberry Pi:**

```bash
uvicorn servidor:app --host 0.0.0.0 --port 8000
```

**No PC:**

```bash
python cliente.py
```

### 2. Controle de 2 LEDs sem WebSocket (HTTP)

**Na Raspberry Pi:**

```bash
python3 serv2bits.py
```

**No PC:**

```bash
python cliente2bits.py
```

### 3. Controle de 2 LEDs via WebSocket

**Na Raspberry Pi:**

```bash
uvicorn serv2bitsws:app --host 0.0.0.0 --port 8000
```

**No PC:**

```bash
python cliente2bitsws.py
```

---

## ✅ Requisitos

### 🦍 O que é Python?

Python é uma linguagem de programação de alto nível, fácil de usar e muito utilizada em automações, aplicações web, ciência de dados e controle de dispositivos físicos como o Raspberry Pi.

### 📥 Como instalar o Python

#### No Raspberry Pi:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

Verifique a instalação:

```bash
python3 --version
```

#### No PC (Windows):

1. Acesse: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Baixe e instale a versão recomendada (marque "Add Python to PATH").
3. Confirme no terminal (cmd):

```bash
python --version
```

---

## 📚 Instalação de Bibliotecas

Execute na Raspberry Pi:

```bash
pip3 install fastapi uvicorn websockets RPi.GPIO
```

### 📦 Resumo das Bibliotecas

- **FastAPI**: framework web moderno e assíncrono para criação de APIs rápidas.
- **Uvicorn**: servidor ASGI leve e rápido para rodar aplicações FastAPI.
- **Websockets**: permite comunicação bidirecional em tempo real entre cliente e servidor.
- **RPi.GPIO**: biblioteca usada para controlar os pinos GPIO da Raspberry Pi.

---

## 🖥️ Como utilizar o Terminal

### No PC (Windows):

- Pressione `Win + R`, digite `cmd` e aperte Enter.
- Ou procure por “Prompt de Comando” no menu iniciar.

### No Raspberry Pi ou Linux:

- Pressione `Ctrl + Alt + T` para abrir o terminal.
- Você pode navegar até uma pasta com `cd nome_da_pasta` e listar arquivos com `ls`.

---

## 👨‍💻 Autor

**Rafael Moura**\
Desenvolvido para controle remoto de LEDs via Raspberry Pi e comunicação em tempo real com WebSockets.

