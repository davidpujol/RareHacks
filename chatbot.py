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

def tr2english(text):
    translator = Translator()
    msg_tr = translator.translate(text).text
    global language
    language = translator.detect(text).lang
    return msg_tr

def tr2other(text):
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

print(types_melanomes)
print(dic)
# ******************************************************************

#DICTIONARY TYPES OF MEDICIN





# ******************************************************************
import geocoder

R = 6371000
pi = 3.14159

def radians(c):
    return pi/180 * c

#distance in meters
def distancia(hospital, persona):
    print('dist')
    lat1 = radians(float(hospital[0]))
    print('a')
    long1 = radians(float(hospital[1]))
    print('b')
    lat2 = radians(float(persona[0]))
    print('c')
    long2 = radians(float(persona[1]))
    print('d')
    lat = abs(lat2-lat1)
    print('a')
    long = abs(long2 - long1)
    print(type(lat))
    print(type(long))
    a = sin(lat/2)**2 + cos(lat1) * cos(lat2) * sin(long/2) ** 2
    print('c')
    c = 2*atan2(sqrt(a),sqrt(1-a))
    print('c')
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
hospitals = pd.read_csv('Intraocular_melanoma.csv').values

for hospital in hospitals:
    name = hospital[4]
    telefon = hospital[5]
    address = hospital[6]
    lat = hospital[7]
    long = hospital[8]
    if (not pd.isnull(name)) and (not pd.isnull(telefon)) and (not pd.isnull(address)) and (not pd.isnull(lat)) and (not pd.isnull(long)):
        information_hospitals.append([name,telefon,address,lat,long])


# ******************************************************************


#function to be called
def responde(bot, update, user_data):
    user_response = tr2english(update.message.text).lower()
  #  words = word_tokenize(user_response)

 #   if user_response == 'bye' or user_response=='Bye':
 #       bot.send_message(chat_id=update.message.chat_id, text=tr2other("Goodbye!!"))

 #   elif user_response == 'thanks' or user_response == 'thank you':
 #           bot.send_message(chat_id=update.message.chat_id, text=tr2other("You are very welcome"))

 #   elif greeting(user_response) is not None:   #when greetings appear
 #       bot.send_message(chat_id=update.message.chat_id, text=greeting(user_response)+ " " + update.message.chat.first_name)
 #       bot.send_message(chat_id = update.message.chat_id, text=tr2other("It is very important for me to make sure that you have been already diagnosed by a professional. Could you please confirm me so?"))

 #   elif 'diagnosed' not in user_data:
 #       if ('no' in words) or ("n't" in words) or ("not" in words):
 #           bot.send_message(chat_id=update.message.chat_id, text=tr2other("Don't worry. In this case we believe you should first go to a certified center to diagnose the exact type of melanoma that you suffer"))

 #       else:
 #           user_data['diagnosed'] = True
 #           bot.send_message(chat_id = update.message.chat_id, text=tr2other("Then, it would be very helpful for me to know what specific type of Melanoma you are interested in. Do you know its name?"))


 #   elif ('type_disease' not in user_data) and ('diagnosed' in user_data):
 #           if ('no' in words) or ("n't" in words) or ("not" in words):
 #               bot.send_message(chat_id= update.message.chat_id, text=tr2other("Don't worry..."))

 #           else:
 #               print(user_response)
 #               found = False
 #               for type in types_melanomes:
 #                   if type in user_response:
 #                       found = True
 #                       user_data['type_disease'] = dic[type]
 #                       print(user_data['type_disease'])
 #               if found:
 #                  bot.send_message(chat_id=update.message.chat_id, text=tr2other("Perfect"))
 #                   bot.send_message(chat_id = update.message.chat_id, text=tr2other("Now, it is important for me to know what drugs have been prescribed for this disease by your doctor?"))

  #              else:
  #                  bot.send_message(chat_id=update.message.chat_id,text=tr2other("Go ahead and tell me what is its name, please."))


  #  elif 'medicin' not in user_data:
  #      bot.send_message(chat_id=update.message.chat_id, text="klasjdfladf")
  #      user_data['medicin'] = user_response


  #  else:
    words = treatInput(user_response)
    #check if this is a where sentence.
    if 'where' in words:
        bot.send_message(chat_id=update.message.chat_id, text=tr2other("Please send me your location, so I can give you the best option."))

    else:
        bot.send_message(chat_id = update.message.chat_id, text=words)



def findClosestHospital(lat, long):
    print('aadsjflasdf')
    list = []
    for i in range(0, len(information_hospitals)):
        hospital = information_hospitals[i]
        print(hospital)
        lat2 = hospital[3]
        long2 = hospital[4]
        print(lat2)
        print(long2)
        print(lat)
        print(long)
        distance = distancia([lat,long],[lat2,long2])
        print(distance)
        list.append([i,distance])

    list = sorted(list, lambda x: x[1])
    print(len(list))
    return list[-1][0]


def giveClosestHospital(bot, update, user_data):
    try:
        name = "%d.png" % random.randint(1000000, 9999999)
        lat = str(update.message.location.latitude)[1:-1]
        lon = str(update.message.location.longitude)[1:-1]
        print('a')
        index = findClosestHospital(lat,lon)
        #entry = information_hospitals[index]
        #lat = entry[3]
        #lon = entry[4]

        #mapa = StaticMap(500, 500)
        #mapa.add_marker(CircleMarker((lon, lat), 'blue', 10))
        #imatge = mapa.render()
        #imatge.save(name)
        #bot.send_photo(chat_id=update.message.chat_id, photo=open(name, 'rb'))
        #os.remove(name)

    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id,text='Something goes wrong!')






#load the access token
TOKEN = open('token.txt').read().strip()

updater = Updater(token= TOKEN)
dispatcher = updater.dispatcher

#handling the call
dispatcher.add_handler(MessageHandler(Filters.text, responde, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.location, giveClosestHospital, pass_user_data = True)) #telegram api

#starting the bot
updater.start_polling()



