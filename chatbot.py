#telegram api
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters

#nltk
import nltk
import numpy as np
import random
import string # to process standard python strings
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# GREETINGS
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


#LEMMATIZATION
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)	#remove punctuation

#funtion to lemmatize a sentance
lemmer = WordNetLemmatizer()	#this is an internal dictionary
def lemmatize(p):
    print(p)
    if p[1][0] in {'N','V'}:
        return lemmer.lemmatize(p[0].lower(), pos=p[1][0].lower())
    return p[0]


def removeStopWords(sentance):
    words = word_tokenize(sentance)
    filtered_words = [word for word in words if word not in stopwords.words('english')]
    print(filtered_words)
    return filtered_words

def treatInput(sentence):
    sentence = sentence.lower().translate(remove_punct_dict)    #eliminem els punts
    sentence_without_stop = removeStopWords(sentence)
    pairs = pos_tag(sentence_without_stop)
    result = lemmatize(pairs)

    print(result)



#function to be called
def responde(bot, update):
    user_response = update.message.text

    if (user_response != 'bye' or user_response != 'Bye'):
            if (user_response == 'thanks' or user_response == 'thank you'):
                bot.send_message(chat_id=update.message.chat_id, text="You are very welcome")

            else:
                if (greeting(user_response) != None):
                    bot.send_message(chat_id=update.message.chat_id, text=greeting(user_response))
                else:
                    treatInput(user_response)
                    bot.send_message(chat_id = update.message.chat_id, text="OTHER")
    else:
            bot.send_message(chat_id = update.message.chat_id, text="Goodbye!!")






#
#load the access token
TOKEN = open('token.txt').read().strip()

updater = Updater(token= TOKEN)
dispatcher = updater.dispatcher

#handling the call
dispatcher.add_handler(MessageHandler(Filters.text, responde))

#starting the bot
updater.start_polling()