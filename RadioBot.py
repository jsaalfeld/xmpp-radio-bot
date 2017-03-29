import logging
from sleekxmpp import ClientXMPP
from subprocess import call

class RadioBot(ClientXMPP):

    def __init__(self, jid, password, channel, nick):

        self.channel = channel;
        self.nick = nick;

        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("groupchat_message", self.handle_group_message)

    def session_start(self, event):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)-8s %(message)s')
        self.send_presence()
        self.register_plugin('xep_0045')
        self.get_roster()
        self.plugin['xep_0045'].joinMUC(self.channel,
                                        self.nick,
                                        wait=True)

    def handle_group_message(self, msg):
        if msg['type'] in ('groupchat', 'normal'):
            body = msg['body']
            if self.nick in body:
                if "command" in body:
                    self.handle_message_command(body.split())
            print(msg['body'])

    def handle_message_command(self, command):
        call(command)
