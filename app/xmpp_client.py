import slixmpp

class XMPPClient(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("auth_failed", self.auth_failed)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.disconnect()  # Desconectar después de obtener el roster para la prueba

    def auth_failed(self, event):
        print("Authentication failed")
