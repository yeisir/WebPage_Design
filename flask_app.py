from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO
import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime

# Variable de entorno
load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app)

# Configuración de la base de datos MySQL
db = mysql.connector.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME")
)

# Función para obtener coordenadas históricas desde la base de datos en un rango de fechas
def obtener_coordenadas_historicas(inicio, fin):
    cursor = db.cursor()
    select_query = "SELECT latitud, longitud, altitud FROM coordenadas WHERE timestamp BETWEEN %s AND %s"
    cursor.execute(select_query, (inicio, fin))
    coordenadas_historicas = [{'latitud': latitud, 'longitud': longitud, 'altitud': altitud} for (latitud, longitud, altitud) in cursor.fetchall()]
    cursor.close()
    return coordenadas_historicas



@app.route('/tiempo_real', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('pag1.html')
    else:
        return render_template('pag1.html')

@app.route('/recibir_udp', methods=['POST'])
def recibir_udp():
    data = request.json
    print("Datos recibidos en la solicitud POST:", data)

    # Extraer los valores de latitud, longitud, altitud y timestamp
    latitud = data.get('latitud')
    longitud = data.get('longitud')
    altitud = data.get('altitud')
    timestamp = data.get('timestamp')

    # Insertar los datos en la base de datos MySQL
    cursor = db.cursor()
    insert_query = "INSERT INTO coordenadas (latitud, longitud, altitud, timestamp) VALUES (%s, %s, %s, %s)"
    data_tuple = (latitud, longitud, altitud, timestamp)
    cursor.execute(insert_query, data_tuple)
    db.commit()
    cursor.close()

    # Emitir los datos al cliente WebSocket
    socketio.emit('update_coords', {'latitud': latitud, 'longitud': longitud, 'altitud': altitud, 'timestamp': timestamp})
    print("Datos enviados al cliente WebSocket:", {'latitud': latitud, 'longitud': longitud, 'altitud': altitud, 'timestamp': timestamp})
    return 'Datos recibidos y procesados correctamente'

@app.route('/consulta_historica', methods=['POST'])
def consulta_historica():
    inicio = request.form.get('inicio')
    fin = request.form.get('fin')
    
    if inicio and fin:
        coordenadas_historicas = obtener_coordenadas_historicas(inicio, fin)
        print("Coordenadas históricas enviadas al cliente:", coordenadas_historicas)  # Imprimir los datos en el servidor
        return jsonify({'coordenadas': coordenadas_historicas})  # Devuelve las coordenadas como JSON
    else:
        print("Error: No se proporcionaron valores de inicio y fin.")  # Imprimir el error en el servidor
        return render_template('pag2.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)




