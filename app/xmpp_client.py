import slixmpp
from slixmpp.exceptions import IqError, IqTimeout

class XMPPClient(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        # Handle session start
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

        # You can now add logic here for what to do after login, like joining a room or sending a message
        print("Logged in as:", self.boundjid.full)

        # Disconnect after completing the action
        self.disconnect()

