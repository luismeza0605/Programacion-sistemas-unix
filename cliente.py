# client.py
import socket
import struct
import os

def send_file_size(sock, filesize):
    sock.sendall(struct.pack("<Q", filesize))

def send_file(sock, filename):
    filesize = os.path.getsize(filename)
    send_file_size(sock, filesize)
    with open(filename, "rb") as f:  # Cambia a modo binario
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            sock.sendall(chunk)

# Creación del socket del cliente manualmente usando la biblioteca socket
client_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_fd.connect(("localhost", 6190))

print("Conectado al servidor.")
print("Enviando archivo...")
send_file(client_fd, "archivo.txt")  # Cambia el nombre del archivo
print("Enviado.")

client_fd.close()
print("Conexión cerrada.")
