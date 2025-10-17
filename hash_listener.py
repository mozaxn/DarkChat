import socket

HOST = "0.0.0.0"  # listen on all interfaces
PORT = 7887       # same port as client

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

conn, addr = server.accept()
print(f"Connection established from {addr}")

data = conn.recv(1024)
print("Received message:", data.decode('utf-8'))

conn.close()
server.close()
