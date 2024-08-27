from flask import render_template, request, redirect, url_for
import slixmpp
import asyncio
from flask_socketio import emit
from app.xmpp_client import XMPPClient
from app import app, socketio
import re
import concurrent.futures

class RegisterXMPPClient(slixmpp.ClientXMPP):
    def __init__(self, username, password):
        jid = f'{username}@alumchat.lol'
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.disconnect()

    async def async_connect_and_run(self):
        self.connect()
        await self.process(forever=False)

def run_xmpp_client(username, password):
    xmpp_client = RegisterXMPPClient(username, password)
    asyncio.run(xmpp_client.async_connect_and_run())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()  # Eliminar espacios en blanco
        password = request.form['password']

        # Ejecuta el cliente XMPP para registrar al usuario
        run_xmpp_client(username, password)

        message = "Registration successful"
        return render_template('login.html', message=message)

    return render_template('register.html')

def is_valid_jid(jid):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+$', jid))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        jid = f'{username}@alumchat.lol'
        if not is_valid_jid(jid):
            return render_template('login.html', message="Invalid JID format")

        async def authenticate_user():
            client = XMPPClient(jid, password)
            try:
                client.connect()  # Conexión sin await
                client.process(forever=False)
                return True
            except Exception as e:
                print(f'Authentication failed: {e}')
                return False

        # Ejecuta la función async en un hilo separado
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        executor = concurrent.futures.ThreadPoolExecutor()
        is_authenticated = loop.run_until_complete(loop.run_in_executor(executor, authenticate_user))

        if is_authenticated:
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message="Authentication failed")

    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@socketio.on('message')
def handle_message(data):
    print('Received message: ' + data)
    emit('response', {'data': 'Message received'})
