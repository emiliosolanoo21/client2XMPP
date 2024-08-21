from flask import Flask, render_template, request, redirect, url_for
from app import app
from app.xmpp_client import XMPPClient

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        jid = request.form['jid']
        password = request.form['password']

        xmpp = XMPPClient(jid, password)
        xmpp.connect()
        xmpp.process(forever=False)

        return redirect(url_for('index'))

    return render_template('login.html')
