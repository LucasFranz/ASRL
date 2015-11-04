#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 18:50:55 2015

@author: lucas
"""
import os
import codecs

dir_tweets = raw_input("Diretório com tweets: ")
if not dir_tweets.endswith('/'):
    dir_tweets += '/'

arqs_tweets_nao_classificados = [dir_tweets + t for t in os.listdir(dir_tweets) if t.endswith('.txt')]
tweets_nao_classificados = []

# Lê os tweets não classificados e anexa todos na lista 'tweets_nao_classificados'
print '-- lendo tweets.'
for t in arqs_tweets_nao_classificados:
    with codecs.open(t, 'r', 'utf-8') as f:
        tweets_nao_classificados.append(f.read())

tweets_qtde_restante = len(tweets_nao_classificados)

# arquivo com palavras positivas
arq_pos_w = "/home/lucas/Documents/mineracao_opiniao/dicionario_palavras/pos_words_pt-br.txt"

# arquivo com palavras negativas
arq_neg_w = "/home/lucas/Documents/mineracao_opiniao/dicionario_palavras/neg_words_pt-br.txt"

# Lê palavras positivas
print '-- lendo lista de palavras positivas'
with codecs.open(arq_pos_w, 'r', 'utf-8') as f:
    temp_pos_w = f.readlines()

# Lê palavras negativas
print '-- lendo lista de palavras negativas'
with codecs.open(arq_neg_w, 'r', 'utf-8') as f:
    temp_neg_w = f.readlines()

# Elimina '\n' do final das palavras
pos_w = [w.strip('\n')for w in temp_pos_w]
neg_w = [w.strip('\n') for w in temp_neg_w]
    
tweets_rotulados = []
qtde_pos = 0
qtde_neg = 0

# Para cada um dos tweets não classificados
for tweet in tweets_nao_classificados:
    cont = 0  # contador
    tweets_pos = []  # tweets positivos
    pos_words_tweet = []  # palavras positivas do tweet
    tweets_neg = []  # tweets negativos
    neg_words_tweet = []  # palavras negativas do tweet
    
    for palavra in tweet.split():
        if palavra in pos_w:
            cont += 1
            pos_words_tweet.append(palavra)
        elif palavra in neg_w:
            cont -= 1
            neg_words_tweet.append(palavra)
    if cont > 2:  # Opinião positiva
        tweets_pos.append({'tweet_texto': tweet, 'palavras': pos_words_tweet})
        print tweet, '\n'
        qtde_pos += 1
    """else:  # Opinião negativa
        tweets_neg.append({'tweet_texto': tweet, 'palavras': neg_words_tweet})
        qtde_neg += 1"""

for tweet in tweets_pos:
    print '\n'
    for key in tweet.iterkeys():
        print key, '    --> ', tweet[key]

print 'positivos = %d' % qtde_pos
# print 'negativos = %d' % qtde_neg
