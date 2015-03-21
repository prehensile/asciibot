#!/usr/bin/env python

from botkit import botkit
import asciibot

# instantiate botkit
bot = botkit.BotKit( "asciibot" )

# instantiate asciibot
ascii = asciibot.AsciiBot()

# go!
bot.run( ascii )
