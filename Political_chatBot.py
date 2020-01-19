import nltk
import numpy as np
import random
import string

f = open('chatbox.txt', 'r', errors = 'ignore')

raw = f.read()

raw = raw.lower()

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lemmer = nltk.stem.WordNetLemmatizer() #WordNet is semantically oriented dictionary in NLTK.

def LemTokens(tokens):
    return[lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

greeting_f = open('greetings.txt' 'r', errors = 'ignore')
GREETING_INPUTS = tuple(f.read().split(", "))
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):

    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
           return random.choice(GREETING_RESPONSES)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def response(user_response):
    poli_chatbox_response = ''
    sent_tokens.append(user_response)

    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if(req_tfidf == 0):
        poli_chatbox_response = poli_chatbox_response + "I'm sorry! didnt get that"

        return poli_chatbox_response
    else:
        poli_chatbox_response = poli_chatbox_response + sent_tokens[idx]
        return poli_chatbox_response

flag=True
print("POLLY: Hello! My name is Polly. I am a political chatbox created by Sooraj. I will answer your queries about all things political and more. If you want to exit, type Bye!")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("POLLY: You are welcome..")
        else:
            if(greeting(user_response)!=None):
                print("POLLY: "+greeting(user_response))
            else:
                print("POLLY: ",end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("POLLY: Bye! take care..")
