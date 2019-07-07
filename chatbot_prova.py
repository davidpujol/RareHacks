import nltk
import numpy as np
import random
import string # to process standard python strings
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#READ THE INPUT FILE
f=open('input.txt','r',errors = 'ignore')
raw=f.read()	#open the input file
raw=raw.lower()# converts to lowercase to not distinguish same words


#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only

#Tokenisation into sentences
sent_tokens = nltk.sent_tokenize(raw)

# Preprocessing
lemmer = WordNetLemmatizer()	#this is an internal dictionary
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]	#lemmatization (good,better = good)


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)	#remove punctuation

#Function to lematize text
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# GREETINGS
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)




# Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')	#settings of the tfidf: tokenize the user response into words, delete stop words
    tfidf = TfidfVec.fit_transform(sent_tokens)	#calculate tfidf matrix (how important is every word, using word count and inverse document appearences in every sentence)
    vals = cosine_similarity(tfidf[-1], tfidf)	#calculate the similarity between all the document and the last entry, which is the users response

    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]		#get the one that fits best (not considering the last which was our initial entry)
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


#Main program
flag=True
print("ROBO: My name is Robo. I will answer your queries about Chatbots. If you want to exit, type Bye!")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("ROBO: You are welcome..")
        else:
            if(greeting(user_response)!=None):
                print("ROBO: "+greeting(user_response))
            else:
                print("ROBO: ",end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("ROBO: Bye! take care..")
