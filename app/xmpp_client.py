import ssl
import slixmpp

class XMPPClient(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("auth_failed", self.auth_failed)

        # Configurar el cliente para no verificar los certificados del servidor
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.disconnect()  # Desconectar después de obtener el roster para la prueba

    def auth_failed(self, event):
        print("Authentication failed")

class RosterClient(XMPPClient):
    async def get_roster(self):
        self.send_presence()
        await self.get_roster()
        roster = self.client_roster
        return {jid: roster[jid] for jid in roster}

async def fetch_roster(jid, password):
    client = RosterClient(jid, password)
    client.connect()
    await client.process(forever=False)
    return await client.get_roster()
