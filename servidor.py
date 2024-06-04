import socket
import struct

def receive_file_size(conn):
    # Formato de la estructura para recibir el tamaño del archivo
    fmt = "<Q"  # "<" indica little-endian, "Q" indica un unsigned long long (8 bytes)
    expected_bytes = struct.calcsize(fmt)
    received_bytes = 0
    stream = b''
    # Recibir datos hasta que se reciba la cantidad esperada de bytes
    while received_bytes < expected_bytes:
        chunk = conn.recv(expected_bytes - received_bytes)
        stream += chunk
        received_bytes += len(chunk)
    # Desempaquetar los datos recibidos para obtener el tamaño del archivo
    filesize = struct.unpack(fmt, stream)[0]
    return filesize

def receive_file(conn, filename):
    # Recibir el tamaño del archivo
    filesize = receive_file_size(conn)
    # Abrir el archivo en modo escritura binaria
    with open(filename, "wb") as f:
        received_bytes = 0
        # Recibir el archivo en trozos de 1024 bytes hasta que se haya recibido todo
        while received_bytes < filesize:
            chunk = conn.recv(1024)
            if not chunk:  # Si no hay datos, salir del bucle
                break
            f.write(chunk)  # Escribir el trozo en el archivo
            received_bytes += len(chunk)  # Actualizar la cantidad de bytes recibidos

# Dirección IP y puerto en el que el servidor escucha
server_ip = "localhost"  # Escucha en todas las interfaces
server_port = 6190

# Imprime la dirección IP del servidor
print("Dirección IP del servidor:", server_ip)

# Creación del socket del servidor
server_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_fd.bind((server_ip, server_port))
server_fd.listen(1)  # Escuchar una conexión entrante

print("Esperando al cliente...")
# Aceptar la conexión entrante y obtener el socket de conexión y la dirección del cliente
conn, address = server_fd.accept()
print(f"{address[0]}:{address[1]} conectado.")
print("Recibiendo archivo...")
# Recibir el archivo enviado por el cliente
receive_file(conn, "received_file.txt")  # Cambiar nombre del archivo si es necesario
print("Archivo recibido.")

conn.close()  # Cerrar el socket de conexión
server_fd.close()  # Cerrar el socket del servidor
print("Conexión cerrada.")
