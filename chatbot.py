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
from textblob import TextBlob
import pandas as pd
import math
import os
from staticmap import StaticMap, CircleMarker


# ******************************************************************
# GREETINGS
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)



# ******************************************************************
#TREAT THE INPUT

#LEMMATIZATION
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)	#remove punctuation

#funtion to lemmatize a sentance
lemmer = WordNetLemmatizer()	#this is an internal dictionary
def lemmatize(p):
    if p[1][0] in {'N','V'}:
        return lemmer.lemmatize(p[0].lower(), pos=p[1][0].lower())
    return p[0]

#STOPWORDS
def removeStopWords(sentance):
    words = word_tokenize(sentance)
    filtered_words = [word for word in words if word not in stopwords.words('english')]
    return filtered_words

#CORRECCIO
def correccio(text):
    s = TextBlob(text)
    return s.correct()

def extractSintagma (text):
    pairs = pos_tag(text)
    grammar = "NP: {<DT>?<JJ>*<NN>}"
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(pairs)
    return result

def treatInput(sentence):
   # sentence = str(correccio(sentence.lower()))
    sentence = sentence.lower().translate(remove_punct_dict)    #eliminem els punts
    #aux = removeStopWords(sentence)
    words = word_tokenize(sentence)
    pairs = pos_tag(words)
    result = [lemmatize(p) for p in pairs]
  #  result = extractSintagma(result)
    return result

# ******************************************************************

from googletrans import Translator

def tr2english(text,user_data):
    translator = Translator()
    msg_tr = translator.translate(text).text
    if 'language' not in user_data:
        user_data['language'] = translator.detect(text).lang

    return msg_tr

def tr2other(text,language):
    translator = Translator()
    msg_tr = translator.translate(text, dest=str(language)).text
    return msg_tr



# ******************************************************************
#DICTIONARY OF TYPES OF MELANOMA

tipus = [
'Uveal melanoma',
'Diffuse leptomeningeal melanocytosis',
'Familial atypical multiple mole melanoma syndrome',
'Familial melanoma',
'Malignant melanoma of the mucosa',
'Melanoma and neural system tumor syndrome',
'Melanoma of soft tissue',
'Primary melanoma of the central nervous system'
]

sinonims = [
    ['choroidal melanoma' ,'iris melanoma','Intraocular melanoma'],
    ['DLM Leptomeningeal melanomatosis'],
    ['B-K mole syndrome',
    'FAMM-PC syndrome',
    'FAMMM syndrome',
    'Familial Clark nevus syndrome',
    'Familial atypical mole syndrome',
    'Familial atypical multiple mole melanoma-pancreatic carcinoma syndrome',
    'Familial dysplastic nevus syndrome',
    'Melanoma-pancreatic cancer syndrome'],
    ['Dysplastic nevus syndrome hereditary','B-K mole syndrome'],
    [],
    ['Melanoma-astrocytoma syndrome'],
    ['Clear cell sarcoma of the tendons and aponeuroses'],
    ['Malignant melanoma of meninges','Primary melanoma of the CNS']
    ]

dic = {}
types_melanomes = []
for i in range(0,len(sinonims)):
    family = sinonims[i]
    type = tipus[i]
    dic[type.lower()] = type.lower()
    for sin in family:
        dic[sin.lower()] = type.lower()
        types_melanomes.append(sin.lower())

# ******************************************************************

import geocoder

R = 6371000
pi = 3.14159

def radians(c):
    return pi/180 * c

#distance in meters
def distancia(hospital, persona):
    lat1 = radians(float(hospital[0]))
    long1 = radians(float(hospital[1]))
    lat2 = radians(float(persona[0]))
    long2 = radians(float(persona[1]))
    lat = abs(lat2-lat1)
    long = abs(long2 - long1)
    a = math.sin(lat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(long/2) **2
    c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
    return R*c


def getLatLong (address):
    g = geocoder.mapquest(address, key='SBCjXsQ99VWjbfwSFYh1UDv3QhzYfyGj')
    lat = g.lat
    lon = g.lng
    return [lat,lon]

def computeLatsAndLongs(hospitals_information):
    for i in range(0,len(hospitals_information)):
        list = getLatLong(hospitals_information[i][2])
        hospitals_information[i][3] = list[0]
        hospitals_information[i][4] = list[1]




# *********************************************************************
#WE WILL USE THIS TO READ THE INFORMATION OF THE DISEASE WE HAVE FOUND


global information_hospitals
information_hospitals = []
#medicins = []
#side_effects = []
rows = pd.read_csv('Intraocular_melanoma.csv').values

for row in rows:
    name = row[4]
    telefon = row[5]
    address = row[6]
    lat = row[7]
    long = row[8]
    if (not pd.isnull(name)) and (not pd.isnull(telefon)) and (not pd.isnull(address)) and (not pd.isnull(lat)) and (not pd.isnull(long)):
        information_hospitals.append([name,telefon,address,lat,long])

# ******************************************************************


#function to be called
def responde(bot, update, user_data):
    user_response = tr2english(update.message.text, user_data).lower()
    words = word_tokenize(user_response)
    if user_response == 'bye' or user_response=='Bye':
        bot.send_message(chat_id=update.message.chat_id, text=tr2other("Goodbye!!",user_data['language']))

    elif user_response == 'thanks' or user_response == 'thank you':
            bot.send_message(chat_id=update.message.chat_id, text=tr2other("You are very welcome",user_data['language']))

    elif greeting(user_response) is not None:   #when greetings appear
        text = greeting(user_response)+ " " + update.message.chat.first_name + "\nIt is very important for me to make sure that you have been already diagnosed by a professional. Could you please confirm me so?"
        bot.send_message(chat_id=update.message.chat_id, text=tr2other(text, user_data['language']))

    elif 'diagnosed' not in user_data:
        if ('no' in words) or ("n't" in words) or ("not" in words):
            bot.send_message(chat_id=update.message.chat_id, text=tr2other("Don't worry. In this case we believe you should first go to a certified center to diagnose the exact type of melanoma that you suffer",user_data['language']))

        else:
            user_data['diagnosed'] = True
            bot.send_message(chat_id = update.message.chat_id, text=tr2other("Then, it would be very helpful for me to know what specific type of Melanoma you are interested in. Do you know its name?",user_data['language']))


    elif ('type_disease' not in user_data) and ('diagnosed' in user_data):
            if ('no' in words) or ("n't" in words) or ("not" in words):
                bot.send_message(chat_id= update.message.chat_id, text=tr2other("Don't worry...",user_data['language']))

            else:
                found = False
                for type in types_melanomes:
                    if type in user_response:
                        found = True
                        user_data['type_disease'] = dic[type]
                if found:
                    bot.send_message(chat_id=update.message.chat_id, text=tr2other("Perfect",user_data['language']))
                    bot.send_message(chat_id = update.message.chat_id, text=tr2other("Now, it is important for me to know what drugs have been prescribed for this disease by your doctor?",user_data['language']))

                else:
                    bot.send_message(chat_id=update.message.chat_id,text=tr2other("Go ahead and tell me what is its name, please.",user_data['language']))


    elif 'medicin' not in user_data:
        bot.send_message(chat_id=update.message.chat_id, text="Thank you. This will be very helpful for me to know you a little better. Is there anything I can help you with?")
        user_data['medicin'] = user_response


    else:
        words = treatInput(user_response)
        #here we have to make a prediction of what will be the answer

        if

        if 'where' in words:
            bot.send_message(chat_id=update.message.chat_id, text=tr2other("Please send me your location, so I can give you the best option.", user_data['language']))

        else:
            bot.send_message(chat_id = update.message.chat_id, text=words)



def findClosestHospital(lat, long):
    list = []
    for i in range(0, len(information_hospitals)):
        hospital = information_hospitals[i]
        lat2 = hospital[3]
        long2 = hospital[4]
        distance = distancia([lat,long],[lat2,long2])

        list.append([distance,i])

    list = sorted(list, key=lambda x: x[0])
    return list[0][1]


def giveClosestHospital(bot, update, user_data):
    try:
        name = "%d.png" % random.randint(1000000, 9999999)
        lat = str(update.message.location.latitude)
        lon = str(update.message.location.longitude)
        index = findClosestHospital(lat,lon)
        entry = information_hospitals[index]
        nom = entry[0]
        telefon = entry[1]
        address = entry[2]
        lat = entry[3]
        lon = entry[4]

        mapa = StaticMap(500, 500)
        mapa.add_marker(CircleMarker((lon, lat), 'blue', 10))
        imatge = mapa.render()
        imatge.save(name)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(name, 'rb'))

        text = "This is the location of the nearest hospital in which your type of disease can be treated.\nThis hospital is called " + nom + " and its address is " + address + "\n" + "I would recommend you to contact it through the telefon " + telefon + " so you can book a meet with an specialist."
        bot.send_message(chat_id=update.message.chat_id, text=tr2other(text,user_data['language']))
        os.remove(name)

    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id,text='Something went wrong! Please try it again later.')






#load the access token
TOKEN = open('token.txt').read().strip()

updater = Updater(token= TOKEN)
dispatcher = updater.dispatcher

#handling the call
dispatcher.add_handler(MessageHandler(Filters.text, responde, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.location, giveClosestHospital, pass_user_data = True)) #telegram api

#starting the bot
updater.start_polling()



