import socket
import struct
import os

def send_file_size(sock, filesize):
    # Enviar el tamaño del archivo al servidor
    sock.sendall(struct.pack("<Q", filesize))

def send_file(sock, filename):
    # Obtener el tamaño del archivo
    filesize = os.path.getsize(filename)
    # Enviar el tamaño del archivo al servidor
    send_file_size(sock, filesize)
    # Abrir el archivo en modo lectura binaria
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(1024)  # Leer el archivo en trozos de 1024 bytes
            if not chunk:  # Si no hay datos, salir del bucle
                break
            sock.sendall(chunk)  # Enviar el trozo al servidor

# Dirección IP y puerto del servidor
server_ip = "localhost"  # Dirección IP del servidor
server_port = 6190

# Creación del socket del cliente
client_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conexión al servidor
client_fd.connect((server_ip, server_port))

print("Conectado al servidor.")
print("Enviando archivo...")
# Enviar el archivo al servidor
send_file(client_fd, "archivo.txt")  # Cambiar nombre del archivo si es necesario
print("Enviado.")

client_fd.close()  # Cerrar el socket del cliente
print("Conexión cerrada.")

