import socket
import requests
import json

def enviar_datos_al_flask(datos):
    url = 'http://127.0.0.1:5000/recibir_udp'
    
    # solicitud POST
    headers = {'Content-Type': 'application/json'}
    response_post = requests.post(url, json=json.loads(datos), headers=headers)
    print("Respuesta POST:", response_post.text)

    # solicitud GET
    response_get = requests.get(url, params=json.loads(datos))
    print("Respuesta GET:", response_get.text)

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
