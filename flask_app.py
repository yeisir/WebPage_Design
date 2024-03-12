from flask import Flask, render_template, request
from flask_socketio import SocketIO
import mysql.connector

app = Flask(__name__)
socketio = SocketIO(app)

# Base de datos 
db = mysql.connector.connect(
    host="database-1.c50sa4y2g28z.us-east-2.rds.amazonaws.com",
    user="admin",
    password="10122022",
    database="data"
)

#hola

@app.route('/')
def index():
    return render_template('pag1.html')

@app.route('/recibir_udp', methods=['GET', 'POST'])
def recibir_udp():
    if request.method == 'GET':
        # Si la solicitud es GET, obtener los datos de la consulta
        latitud = request.args.get('latitud')
        longitud = request.args.get('longitud')
        altitud = request.args.get('altitud')
        timestamp = request.args.get('timestamp')
    elif request.method == 'POST':
        # Si la solicitud es POST, obtener los datos del cuerpo JSON
        data = request.json
        print("Datos recibidos en la solicitud POST:", data)

        # Extraer los valores de latitud, longitud, altitud y timestamp
        latitud = data.get('latitud')
        longitud = data.get('longitud')
        altitud = data.get('altitud')
        timestamp = data.get('timestamp')
    else:
        # Si la solicitud no es ni GET ni POST, retornar un mensaje de error
        return 'Método no permitido'

    # Insertar los datos en la base de datos MySQL
    cursor = db.cursor()
    insert_query = "INSERT INTO coordenadas (latitud, longitud, altitud, timestamp) VALUES (%s, %s, %s, %s)"
    data_tuple = (latitud, longitud, altitud, timestamp)
    cursor.execute(insert_query, data_tuple)
    db.commit()
    cursor.close()

    # Emitir los datos al cliente WebSocket
    socketio.emit('update_coords', {'latitud': latitud, 'longitud': longitud, 'altitud': altitud, 'timestamp': timestamp})
    print("Datos enviados al cliente WebSocket:", {'latitud': latitud, 'longitud': longitud, 'altitud': altitud, 'timestamp':timestamp})
    return 'Datos recibidos y procesados correctamente'

if __name__ == '__main__':
    socketio.run(app, debug=True, host= '0.0.0.0', port='80')

