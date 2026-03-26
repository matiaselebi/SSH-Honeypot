import os
import socket
import logging
import paramiko
import threading
import sqlite3
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger("paramiko").setLevel(logging.CRITICAL)

def cargar_o_generar_clave():
    archivo_clave = 'honeypot_rsa.key'
    if os.path.exists(archivo_clave):
        return paramiko.RSAKey.from_private_key_file(archivo_clave)
    else:
        clave = paramiko.RSAKey.generate(2048)
        clave.write_private_key_file(archivo_clave)
        return clave

HOST_KEY = cargar_o_generar_clave()

def inicializar_db():
    conexion = sqlite3.connect('registros.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS intentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            ip TEXT,
            pais TEXT,
            ciudad TEXT,
            usuario TEXT,
            contrasena TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

def obtener_ubicacion(ip):
    if ip == '127.0.0.1' or ip.startswith('192.168.'):
        return "Local", "Red Interna"
    try:
        respuesta = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if respuesta.get('status') == 'success':
            return respuesta.get('country', 'Desconocido'), respuesta.get('city', 'Desconocida')
    except Exception:
        pass
    return "Desconocido", "Desconocida"

def enviar_alerta_telegram(ip, pais, ciudad, usuario, contrasena):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    
    mensaje = f"Alerta Honeypot SSH\nIP: {ip} ({ciudad}, {pais})\nUsuario: {usuario}\nClave: {contrasena}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    datos = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    
    try:
        requests.post(url, data=datos, timeout=5)
    except Exception:
        pass

def registrar_intento(ip, usuario, contrasena):
    pais, ciudad = obtener_ubicacion(ip)
    conexion = sqlite3.connect('registros.db')
    cursor = conexion.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO intentos (fecha, ip, pais, ciudad, usuario, contrasena) VALUES (?, ?, ?, ?, ?, ?)", 
                   (fecha_actual, ip, pais, ciudad, usuario, contrasena))
    conexion.commit()
    conexion.close()
    return pais, ciudad

class ServidorSSH(paramiko.ServerInterface):
    def __init__(self, cliente_ip):
        self.cliente_ip = cliente_ip
        self.evento = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        pais, ciudad = registrar_intento(self.cliente_ip, username, password)
        logging.info(f"Login - IP: {self.cliente_ip} ({ciudad}, {pais}) - User: {username} - Pass: {password}")
        enviar_alerta_telegram(self.cliente_ip, pais, ciudad, username, password)
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
    inicializar_db()
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