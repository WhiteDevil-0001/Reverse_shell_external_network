# Reverse_shell_external_network (Educational Use)

## Overview
This project demonstrates a simple client-server architecture in Python that enables:
- Remote command execution
- File upload (server → client)
- File download (client → server)

It is designed for **educational purposes**, such as understanding:
- Socket programming
- Custom binary protocols (length-prefixed messaging)
- File transfer over TCP
- Process execution with Python

## ⚠️ Legal & Ethical Use
This software must only be used:
- On systems you **own**, or
- On systems where you have **explicit permission**

Unauthorized access, control, or data transfer is illegal in many jurisdictions.

By using this code, you agree that you are solely responsible for your actions.

## Features
- Persistent TCP connection between client and server
- Length-prefixed message protocol using `struct`
- Remote command execution (`exec`)
- File upload and download support
- Cross-platform compatibility (Windows/Linux/macOS)

## Project Structure

├── client.py

├── server.py

├── README.md


## Requirements
- Python 3.x

Install dependencies:
```bash
pip install -r requirements.txt
```

## How It Works

Communication Protocol
Messages are sent with a 4-byte big-endian length prefix
Ensures reliable transmission of commands and file data

## Commands
### 1. Execute Command
```bash
exec <command>
```
Runs a system command on the client and returns output.

### 2. Download File (Client → Server)
```bash
download <remote_path> <local_path>
```
Retrieves file from client machine
Saves it on server machine

### 3. Upload File (Server → Client)
```bash
upload <local_path> <remote_path>
```
Sends file from server to client
Saves it on client machine

### 4. Exit
```bash
exit
```
Closes the connection

## Usage
1. Start Server
python server.py
2. Configure Client

Edit in client.py:

SERVER_IP = "YOUR_SERVER_IP"
PORT = 4444
3. Run Client
python client.py
4. Interact

Use commands in the server terminal:

>> exec whoami
>> upload test.txt /tmp/test.txt
>> download /tmp/test.txt downloaded.txt
⚠️ Security Limitations

This project is intentionally minimal and not secure:

No authentication
No encryption
No input validation
Full command execution capability

Do NOT use this in production or exposed environments.

Learning Outcomes
TCP socket programming
Handling binary data with struct
Building simple communication protocols
Understanding risks of unrestricted remote execution
