import socket
import requests
import json

#git pull

def enviar_datos_al_flask(datos):
    # Formatear los datos en un diccionario
    latitud, longitud, altitud, timestamp = [line.split(': ')[1] for line in datos.split('\n') if line]
    datos_formateados = {
        'latitud': float(latitud),
        'longitud': float(longitud),
        'altitud': float(altitud),
        'timestamp': timestamp
    }

    # Convertir a JSON y enviar
    url = 'http://127.0.0.1:5000/recibir_udp'
    headers = {'Content-Type': 'application/json'}
    response_post = requests.post(url, json=datos_formateados, headers=headers)
    print("Respuesta POST:", response_post.text)

def main():
    host = ''
    puerto = 9999

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor:
        servidor.bind((host, puerto))
        print(f"Servidor UDP escuchando en el puerto {puerto}...")

        while True:
            datos_recibidos, direccion_cliente = servidor.recvfrom(1024)
            datos_decodificados = datos_recibidos.decode('utf-8')
            print("Datos recibidos:", datos_decodificados)

            # Enviar los datos al servidor Flask
            enviar_datos_al_flask(datos_decodificados)

if __name__ == "__main__":
    main()
