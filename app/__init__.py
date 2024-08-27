from flask import Flask
from flask_socketio import SocketIO
import os

app = Flask(__name__, template_folder=os.path.join(os.pardir, 'templates'), static_folder=os.path.join(os.pardir, 'static'))
socketio = SocketIO(app)

def create_app():
    with app.app_context():
        from . import routes

    return app, socketio
