from flask import Flask
import os

app = Flask(__name__, template_folder=os.path.join(os.pardir, 'templates'))

def create_app():
    with app.app_context():
        from . import routes  # Importa las rutas aquí para que estén disponibles

    return app
