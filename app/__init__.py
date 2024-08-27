from flask import Flask
from flask_socketio import SocketIO
import os

app = Flask(__name__, template_folder=os.path.join(os.pardir, 'templates'))
socketio = SocketIO(app)

def create_app():
    with app.app_context():
        from . import routes  # Importa las rutas aquí para que estén disponibles

    return app, socketio  # Devuelve tanto `app` como `socketio`
