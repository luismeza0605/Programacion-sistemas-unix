import socket
import struct
import os

def send_file_size(sock, filesize):
    sock.sendall(struct.pack("<Q", filesize))

def send_file(sock, filename):
    filesize = os.path.getsize(filename)
    send_file_size(sock, filesize)
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            sock.sendall(chunk)

# Dirección IP y puerto del servidor
server_ip = "localhost"  # Dirección IP del servidor
server_port = 6190

# Creación del socket del cliente manualmente usando la biblioteca socket
client_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_fd.connect((server_ip, server_port))

print("Conectado al servidor.")
print("Enviando archivo...")
send_file(client_fd, "file_to_send.txt")  # Cambiar nombre del archivo si es necesario
print("Enviado.")

client_fd.close()
print("Conexión cerrada.")
