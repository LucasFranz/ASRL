# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 20:02:03 2015

@author: lucas
"""

import pickle
'''
with open('/home/lucas/Desktop/teste.pickle', 'wb') as f:
    pickle.dump(classificador, f)
'''
f = open('/home/lucas/Documents/mineracao_opiniao/classificadores_treinados/classificadores_tweets_politica/classificador_naive_bayes.pickle', 'rb')
classificador = pickle.load(f)
f.close()

print classificador.show_most_informative_features(15)