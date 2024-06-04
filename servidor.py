import socket
import struct

def receive_file_size(conn):
    fmt = "<Q"
    expected_bytes = struct.calcsize(fmt)
    received_bytes = 0
    stream = b''
    while received_bytes < expected_bytes:
        chunk = conn.recv(expected_bytes - received_bytes)
        stream += chunk
        received_bytes += len(chunk)
    filesize = struct.unpack(fmt, stream)[0]
    return filesize

def receive_file(conn, filename):
    filesize = receive_file_size(conn)
    with open(filename, "wb") as f:
        received_bytes = 0
        while received_bytes < filesize:
            chunk = conn.recv(1024)
            if not chunk:
                break
            f.write(chunk)
            received_bytes += len(chunk)

# Dirección IP y puerto en el que el servidor escucha
server_ip = "localhost"  # Escucha en todas las interfaces
server_port = 6190

# Imprime la dirección IP del servidor
print("Dirección IP del servidor:", server_ip)

# Creación del socket del servidor
server_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_fd.bind((server_ip, server_port))
server_fd.listen(1)

print("Esperando al cliente...")
conn, address = server_fd.accept()
print(f"{address[0]}:{address[1]} conectado.")
print("Recibiendo archivo...")
receive_file(conn, "received_file.txt")  # Cambiar nombre del archivo si es necesario
print("Archivo recibido.")

conn.close()
server_fd.close()
print("Conexión cerrada.")

