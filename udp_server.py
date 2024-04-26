import socket
import requests
import json


def enviar_datos_al_flask(datos, ruta):
    # Dividir los datos en líneas y extraer las claves y valores
    datos_lineas = datos.split('\n')
    datos_formateados = {}
    for linea in datos_lineas:
        key, value = linea.split(': ')
        datos_formateados[key] = float(value) if key != 'timestamp' else value

    # Si los datos incluyen RPM, agregarlos al diccionario
    if 'rpm' in datos_formateados:
        datos_formateados['rpm'] = float(datos_formateados['rpm'])

    # Convertir a JSON y enviar a la ruta especificada
    url = f'http://127.0.0.1:5000/{ruta}'
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

            # Determinar la ruta a la que enviar los datos
            ruta = 'recibir_coordenadas'
            if 'rpm' in datos_decodificados:
                ruta = 'recibir_coordenadas_rpm'

            # Enviar los datos al servidor Flask con la ruta correspondiente
            enviar_datos_al_flask(datos_decodificados, ruta)

if __name__ == "__main__":
    main()