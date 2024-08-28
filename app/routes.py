from flask import render_template, request, redirect, url_for, jsonify
import slixmpp
import asyncio
from flask_socketio import emit, join_room, leave_room
from app.xmpp_client import XMPPClient, fetch_roster
from app import app, socketio
import re
import concurrent.futures

class RegisterXMPPClient(slixmpp.ClientXMPP):
    def __init__(self, username, password):
        jid = f'{username}@alumchat.lol'
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.start)
        self.rooms = {}  # Track rooms for chats

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

@app.route('/roster', methods=['GET'])
def get_roster():
    jid = 'your_username@alumchat.lol'  # Usa el JID correcto
    password = 'your_password'  # Usa la contraseña correcta

    async def fetch_and_return_roster():
        roster = await fetch_roster(jid, password)
        return roster

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    executor = concurrent.futures.ThreadPoolExecutor()
    roster = loop.run_until_complete(loop.run_in_executor(executor, fetch_and_return_roster))
    
    return jsonify(roster)

async def check_user_exists(jid):
    class PresenceClient(slixmpp.ClientXMPP):
        def __init__(self, jid, password):
            super().__init__(jid, password)
            self.add_event_handler("session_start", self.start)
            self.online = False

        async def start(self, event):
            self.send_presence()
            await self.get_roster()
            self.online = True
            self.disconnect()

        async def check_user_presence(self, user_jid):
            if self.online:
                roster = self.client_roster
                return user_jid in roster
            return False

    client = PresenceClient('your_username@alumchat.lol', 'your_password')  # Use valid credentials
    client.connect()
    await client.process(forever=False)
    return await client.check_user_presence(jid)

import logging

# Configura el logging
logging.basicConfig(level=logging.DEBUG)

@socketio.on('new_chat')
async def handle_new_chat(data):
    username = data['username']
    jid = f'{username}@alumchat.lol'

    user_exists = await check_user_exists(jid)
    if user_exists:
        logging.debug("User exists, starting new chat")
        emit('new_chat_started', {'username': username}, broadcast=True)
    else:
        logging.debug("User does not exist")
        emit('error', {'message': 'User does not exist'})
