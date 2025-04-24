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
1. Acesse: https://www.python.org/downloads/
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

**Rafael Moura**  
Desenvolvido para controle remoto de LEDs via Raspberry Pi e comunicação em tempo real com WebSockets.

