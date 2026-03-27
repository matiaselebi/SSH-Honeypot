SSH Honeypot
Honeypot desarrollado en Python que simula un servicio SSH para registrar intentos de acceso no autorizados. El sistema captura credenciales, geolocaliza la IP del atacante, almacena la informacion en una base de datos local y emite alertas en tiempo real mediante Telegram.

Caracteristicas principales
Simulacion de servidor SSH utilizando la libreria Paramiko.
Registro de direcciones IP, usuarios y contrasenas probadas.
Geolocalizacion de atacantes consumiendo la api ip-api.
Almacenamiento persistente en base de datos SQLite.
Notificaciones instantaneas a traves de un bot de Telegram.
Script adicional para exportar los datos de la base a formato CSV.
Entorno dockerizado para un despliegue seguro y aislado.

Requisitos
Python 3.11 o superior.
Docker opcional para el despliegue en contenedor.
Un bot de Telegram configurado.

Instalacion y configuracion
Clonar este repositorio.

Crear un archivo .env en la raiz del proyecto e incluir las variables TELEGRAM_TOKEN y TELEGRAM_CHAT_ID con tus datos.

Instalar las dependencias ejecutando pip install -r requirements.txt.

Ejecucion local
Para iniciar el servidor honeypot ejecuta python Honeypot.py. El sistema comenzara a escuchar en el puerto 2222.
Para exportar los registros guardados ejecuta python exportar_csv.py y se generara un archivo reporte_honeypot.csv.

Ejecucion con Docker
Para construir la imagen ejecuta:
docker build -t honeypot-ssh.

Para levantar el contenedor en segundo plano ejecuta:
docker run -d -p 2222:2222 honeypot-ssh