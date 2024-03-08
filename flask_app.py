from flask import Flask, render_template, request
from flask_socketio import SocketIO
import mysql.connector

app = Flask(__name__)
socketio = SocketIO(app)

# Base de datos 
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="10122022",
    database="web_ser"
)

#hola

@app.route('/')
def index():
    return render_template('pag1.html')

@app.route('/recibir_udp', methods=['GET', 'POST'])
def recibir_udp():
    if request.method == 'GET':
        # GET, obtener los datos de la consulta
        latitud = request.args.get('latitud')
        longitud = request.args.get('longitud')
        altitud = request.args.get('altitud')
        timestamp = request.args.get('timestamp')
    elif request.method == 'POST':
        # OST, obtener los datos del cuerpo JSON
        data = request.json
        print("Datos recibidos en la solicitud POST:", data)

        # datos
        latitud = data.get('latitud')
        longitud = data.get('longitud')
        altitud = data.get('altitud')
        timestamp = data.get('timestamp')
    else:
        #Mostrar en consola
        return 'Método no permitido'

    # Insertar en MySQL
    cursor = db.cursor()
    insert_query = "INSERT INTO coordenadas (latitud, longitud, altitud, timestamp) VALUES (%s, %s, %s, %s)"
    data_tuple = (latitud, longitud, altitud, timestamp)
    cursor.execute(insert_query, data_tuple)
    db.commit()
    cursor.close()

    # Mostrarlos en el html
    socketio.emit('update_coords', {'latitud': latitud, 'longitud': longitud, 'altitud': altitud, 'timestamp': timestamp})
    print("Datos enviados al cliente WebSocket:", {'latitud': latitud, 'longitud': longitud, 'altitud': altitud, 'timestamp':timestamp})
    return 'Datos recibidos y procesados correctamente'

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)

