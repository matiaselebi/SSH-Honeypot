import sqlite3
import csv

def exportar_datos():
    try:
        conexion = sqlite3.connect('registros.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM intentos")
        filas = cursor.fetchall()
        
        with open('reporte_honeypot.csv', 'w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(['ID', 'Fecha', 'IP', 'Pais', 'Ciudad', 'Usuario', 'Contrasena'])
            escritor.writerows(filas)
        
        conexion.close()
        print("Datos exportados exitosamente a reporte_honeypot.csv")
    except Exception as e:
        print(f"Error al exportar los datos: {e}")

if __name__ == '__main__':
    exportar_datos()