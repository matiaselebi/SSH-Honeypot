import socket
import logging
import paramiko
import threading

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger("paramiko").setLevel(logging.CRITICAL)
HOST_KEY = paramiko.RSAKey.generate(2048)

class ServidorSSH(paramiko.ServerInterface):
    def __init__(self, cliente_ip):
        self.cliente_ip = cliente_ip
        self.evento = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        logging.info(f"Intento de login - IP: {self.cliente_ip} - Usuario: {username} - Contrasena: {password}")
        return paramiko.AUTH_FAILED

def manejar_conexion(cliente, direccion):
    try:
        transporte = paramiko.Transport(cliente)
        transporte.add_server_key(HOST_KEY)
        server = ServidorSSH(direccion[0])
        
        try:
            transporte.start_server(server=server)
        except paramiko.SSHException:
            return
        
        canal = transporte.accept(20)
        if canal is None:
            transporte.close()
            return
        
        server.evento.wait(10)
        canal.close()
    except Exception:
        pass
    finally:
        transporte.close()

def iniciar_honeypot():
    puerto = 2222
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(('0.0.0.0', puerto))
    servidor.listen(100)
    
    logging.info(f"Honeypot SSH escuchando en el puerto {puerto}")

    while True:
        cliente, direccion = servidor.accept()
        hilo = threading.Thread(target=manejar_conexion, args=(cliente, direccion))
        hilo.start()

if __name__ == '__main__':
    iniciar_honeypot()