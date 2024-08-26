from flask import render_template, request, redirect, url_for
import slixmpp
import asyncio
import multiprocessing
from app.xmpp_client import XMPPClient
from app import app

class RegisterXMPPClient(slixmpp.ClientXMPP):
    def __init__(self, username, password):
        super().__init__(username + '@alumchat.lol', password)
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
        username = request.form['username']
        password = request.form['password']

        # Run the XMPP client in a separate process
        process = multiprocessing.Process(target=run_xmpp_client, args=(username, password))
        process.start()
        process.join()

        message = "Registration successful"

        return render_template('login.html', message=message)

    return render_template('register.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Aquí implementas la lógica de autenticación de usuario
        username = request.form['username']
        password = request.form['password']
        
        # Placeholder: Redirecciona al home si las credenciales son correctas
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/home')
def home():
    return "Página principal después de iniciar sesión."
