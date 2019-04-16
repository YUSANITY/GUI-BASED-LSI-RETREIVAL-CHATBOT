import pandas as pd
import os
import json
import re
import numpy as np
import random
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import gensim
from gensim import corpora, models, similarities

import warnings
warnings.simplefilter('ignore')


class TextProcessing:
    def __init__(self):

        path = './Data/'

        GREETING_INPUTS = ("hello", "hi", "greetings", "hello i need help", "good day","hey","i need help", "greetings")
        GREETING_RESPONSES = ["Good day, How may i of help?", "Hello, How can i help?", "hello", "I am glad! You are talking to me."]

        data = self.preprocessing_data(path)
        
        questions = data['MESSAGE']

        dictionary = corpora.Dictionary(questions)
        corpus = [dictionary.doc2bow(a) for a in questions]
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=680)
        corpus_lsi = lsi[corpus_tfidf]
        index = similarities.MatrixSimilarity(corpus_lsi)



        # self.flag_query = True
        self.path = path
        self.GREETING_INPUTS = GREETING_INPUTS
        self.GREETING_RESPONSES = GREETING_RESPONSES

        # self.flag_language = True
        self.dictionary = dictionary
        self.tfidf = tfidf
        self.lsi = lsi
        self.index = index
        self.data=data


    # Remove punctuation
    def RemovePunction(self, tokens):
        return[t for t in tokens if t not in string.punctuation]


    # Lemmatiztion
    def lemmatize(self, tokens):
        lemm = []
        for word, tag in nltk.pos_tag(tokens, tagset='universal'):
            if tag.startswith('NN'):
                lemm.append(WNlemma.lemmatize(word.lower(), pos='n'))
            elif tag.startswith('VB'):
                lemm.append(WNlemma.lemmatize(word.lower(), pos='v'))
            elif tag.startswith('JJ'):
                lemm.append(WNlemma.lemmatize(word.lower(), pos='a'))
            elif tag.startswith('R'):
                lemm.append(WNlemma.lemmatize(word.lower(), pos='r'))
            else:
                lemm.append(word.lower())
        return lemm


    def pre_process(self, questions):
        WNlemma = nltk.WordNetLemmatizer()
        SNstemmer = nltk.stem.SnowballStemmer('english')
        stop_words = stopwords.words("english")

        # Remove non english words
        questions = [re.sub('[^a-z(c++)(c#)]', ' ', x.lower()) for x in questions]
        # Tokenlization
        questions_tokens = [nltk.word_tokenize(t) for t in questions]
        # Remove punctuation
        questions_punc = [self.RemovePunction(t) for t in questions_tokens]
        # Lemmatiztion
        questions_lemm = [self.lemmatize(t) for t in questions_punc]
        # Removing Stop Words
        questions_stop = [[t for t in tokens if (t not in stop_words) and (3 < len(t.strip()) < 15)] for tokens in questions_lemm]

        questions_stop = pd.Series(questions_stop)
        return questions_stop


    def preprocessing_data(self, path):
        
        lsi_path = path + 'QAdata_json.json'

        with open(lsi_path) as file:
            reader = json.load(file)

            MESSAGE = []
            RESPONSE = []
            
            for row in reader:
                MESSAGE.append(row['MESSAGE'])
                RESPONSE.append(row['RESPONSE'])

            data_tokens = pd.DataFrame({'MESSAGE':  MESSAGE,
                                        'RESPONSE': RESPONSE
                                                                })

        return data_tokens


    def greeting(self, sentence):
        # Get greeting word randomly
        for word in sentence.split():
            if word.lower() in self.GREETING_INPUTS:
                return random.choice(self.GREETING_RESPONSES)


    def Talk_To_Javris(self, sentence, dictionary, tfidf, lsi, index, data):
        # Tokenisation of user input
        texts = self.pre_process(pd.Series(sentence))   
        
        # Find and Sort Similarity
        vec_bow = dictionary.doc2bow(texts[0])
        vec_tfidf = tfidf[vec_bow]
        vec_lsi = lsi[vec_tfidf]

        # If not in the topic trained
        if not (vec_lsi):
            not_understood = "Apology, I do not understand. Can you rephrase?"
            return not_understood

        else:
            # Sort similarity
            sims = index[vec_lsi]
            sims = sorted(enumerate(sims), key=lambda item: -item[1])

            index_s =[]
            score_s = []
            for i in range(len(sims)):
                x = sims[i][1]
                # If similarity is less than 0.5 ask user to rephrase.
                if x <=0.55: # Threshold B
                    not_understood = "Apology, I do not understand. Can you rephrase?"
                    return not_understood, 999  
                else: 
                    index_s.append(str(sims[i][0]))
                    score_s.append(str(sims[i][1]))

                    reply_indexes = pd.DataFrame({'index': index_s, 'score': score_s})
                    # Find Top Questions and Score
                    r_index = int(reply_indexes['index'].iloc[0])
                    r_score = float(reply_indexes['score'].iloc[0])

                    reply = str(data.iloc[:,1][r_index])

                    return reply

    def Main(self, input):

        if input.lower() != 'bye':
            print("successfully")

            if(self.greeting(input.lower()) != None):
                return self.greeting(input.lower())
            else:
                reply= self.Talk_To_Javris(str(input), self.dictionary, self.tfidf, self.lsi, self.index, self.data)
                return reply

        else:
            return "Bye! Hope that i am of help."
