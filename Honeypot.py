import socket
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def iniciar_honeypot():
    puerto = 2222
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', puerto))
    servidor.listen(5)
    
    logging.info(f"Honeypot escuchando en el puerto {puerto}")

    while True:
        cliente, direccion = servidor.accept()
        logging.info(f"Conexion detectada desde la IP: {direccion[0]}")
        cliente.send(b"Connection refused\n")
        cliente.close()

if __name__ == '__main__':
    iniciar_honeypot()