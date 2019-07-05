from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters

#function to be called
def responde(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text = "Hello World")


#load the access token
TOKEN = open('token.txt').read().strip()

updater = Updater(token= TOKEN)
dispatcher = updater.dispatcher

#handling the call
dispatcher.add_handler(MessageHandler(Filters.text, responde))

#starting the bot
updater.start_polling()