SSH Honeypot
Honeypot desarrollado en Python que simula un servicio SSH para registrar intentos de acceso no autorizados. El sistema captura credenciales, geolocaliza la IP del atacante, almacena la informacion en una base de datos local y emite alertas en tiempo real mediante Telegram. Esta version incluye un despliegue en la nube utilizando Amazon Web Services.

Arquitectura Cloud en AWS
El proyecto esta desplegado en una instancia EC2 de AWS.
Los reportes de ataques generados en CSV se exportan automaticamente a un bucket de Amazon S3 utilizando boto3.
Una funcion de AWS Lambda monitorea el bucket y procesa eventos de forma automatizada al recibir nuevos archivos.

Caracteristicas principales
Simulacion de servidor SSH utilizando la libreria Paramiko.
Registro de direcciones IP, usuarios y contrasenas probadas.
Geolocalizacion de atacantes consumiendo la api ip-api.
Almacenamiento persistente en base de datos SQLite.
Notificaciones instantaneas a traves de un bot de Telegram.
Script adicional para exportar los datos a formato CSV y subirlos a S3.
Entorno dockerizado para un despliegue seguro y aislado.

Requisitos
Python 3.11 o superior.
Docker opcional para el despliegue en contenedor.
Un bot de Telegram configurado.
Cuenta de AWS configurada con permisos de S3 o rol IAM asignado.

Instalacion y configuracion
Clonar este repositorio.
Crear un archivo .env en la raiz del proyecto e incluir las variables TELEGRAM_TOKEN y TELEGRAM_CHAT_ID con tus datos.
Instalar las dependencias ejecutando pip install -r requirements.txt.

Ejecucion local
Para iniciar el servidor honeypot ejecuta python Honeypot.py. El sistema comenzara a escuchar en el puerto 2222.
Para exportar los registros y subirlos a S3 ejecuta python exportar_csv.py.

Ejecucion con Docker
Para construir la imagen ejecuta:
docker build -t honeypot-ssh .
Para levantar el contenedor en segundo plano ejecuta:
docker run -d -p 2222:2222 honeypot-ssh