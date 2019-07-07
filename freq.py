import nltk
import numpy as np
import random
import string # to process standard python strings
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

f = open("sentences.txt","r")
s = f.read()
f.close()
sent_tokens = nltk.sent_tokenize(s)

#print(sent_tokens)

lemmer = WordNetLemmatizer()	#this is an internal dictionary
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]	#lemmatization (good,better = good)


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)	#remove punctuation

#Function to lematize text
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))



def predictAnswer(input):
    f = open("sentences.txt", "r")
    s = f.read()
    f.close()
    sent_tokens = nltk.sent_tokenize(s)
    sent_tokens.append(str(input))
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize)  # settings of the tfidf: tokenize the user response into words, delete stop words
    tfidf = TfidfVec.fit_transform(sent_tokens)  # calculate tfidf matrix (how important is every word, using word count and inverse document appearences in every sentence)
    vals = cosine_similarity(tfidf[-1],tfidf)  # calculate the similarity between all the document and the last entry, which is the users response

    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    return sent_tokens[idx]