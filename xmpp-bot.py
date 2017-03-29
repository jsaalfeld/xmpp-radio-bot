from RadioBot import RadioBot
import RadioBotConfig

xmpp = RadioBot(RadioBotConfig.user, RadioBotConfig.password, RadioBotConfig.channel, RadioBotConfig.nick)
xmpp.connect()
xmpp.process(block=True)