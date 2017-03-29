import logging
from sleekxmpp import ClientXMPP
import subprocess

class RadioBot(ClientXMPP):

    def __init__(self, jid, password, channel, nick, whitelist):

        self.whitelist = whitelist
        self.channel = channel
        self.nick = nick

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
            send_from = msg['from']
            send_name = send_from.resource.lower()
            if not self.whitelist or send_name in self.whitelist:
                body = msg['body']
                if self.nick in body:
                    if "play radio" in body:
                        self.handle_play_radio(body)
                    if "stop" in body:
                        self.handle_stop(body)
                    if "play file" in body:
                        self.handle_play_file(body)


    def handle_play_radio(self, command):
        station = command.split()[-1]
        cmd = "mplayer -playlist " + station +" &"
        self.run_command(cmd)

    def handle_stop(self, command):
        cmd = "pkill -f mplayer"
        self.run_command(cmd)

    def handle_play_file(self, command):
        file = command.split()[-1]
        cmd = "mplayer " + file + " &"
        self.run_command(cmd)

    def run_command(self, command):
        print("execute: " + command)
        subprocess.Popen(command, shell=True)