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

db_config = {
    'host': os.environ.get("DB_HOST"),
    'user': os.environ.get("DB_USER"),
    'password': os.environ.get("DB_PASSWORD"),
    'database': os.environ.get("DB_NAME")
}



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
def consultar_historial():
    inicio = request.form.get('inicio')
    fin = request.form.get('fin')
    
    # Verifica si hay valores para inicio y fin
    if inicio is not None and fin is not None:
        # Realiza la conexión con la base de datos y ejecuta la consulta SQL
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()
        consulta = ("SELECT Latitud, Longitud FROM coordenadas "
                    "WHERE timestamp >= %s AND timestamp <= %s")
        cursor.execute(consulta, (inicio, fin))
        coordenadas = cursor.fetchall()
        conexion.close()
        
        # Prepara las coordenadas para enviarlas al frontend
        coordenadas_json = [{'latitud': str(lat), 'longitud': str(lon)} for lat, lon in coordenadas]
        
        print("Coordenadas consultadas:", coordenadas_json)
        # Emitir las coordenadas al cliente WebSocket
        socketio.emit('update_historical_coords', {'coordenadas': coordenadas_json})

    
    # Si no hay valores para inicio y fin, solo muestra la página pag2.html
    return render_template('pag2.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)




