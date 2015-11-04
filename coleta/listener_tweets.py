# -*- coding: utf-8 -*-


from tweepy.streaming import StreamListener
import json
import codecs
from datetime import datetime
import re


class CustomListener(StreamListener):
    
    def __init__(self, qtde_tweets,
                 dir_destino="/home/lucas/Documents/mineracao_opiniao/tweets_politica/sem_processamento/"):
        """Documentar
        """
        self.qtde_tweets = qtde_tweets
        self.numero_tweet = 0  # contador de tweets coletados
        self.dir_destino = dir_destino
        self.porcentagem_coletada = 0
        
    
    def on_data(self, data):        
        # Se completou a coleta de tweets
        if self.numero_tweet == self.qtde_tweets:
            print '\nUm total de %d tweets foram coletados.\n' % (self.qtde_tweets)
            print 'Saindo...\n'
            return False
        
        tweet = json.loads(data)
        
        # Se não for um retweet
        if not tweet['text'].startswith('RT'):
            tempo_agora = str(datetime.now())
            tempo_agora = re.sub(ur'\:|\s', '.', tempo_agora)  # Substitui ':' por '.'
            
            nome_arquivo = 'tweet_%s.txt' % (tempo_agora)
            tweet_formatado = "@%s: %s" % (tweet['user']['screen_name'], tweet['text'])
            # tweet_formatado = tweet_formatado.encode('utf-8')
            # tweet_formatado = tweet_formatado.decode('utf-8')
            # tweet_formatado = tweet_formatado
            
            # Abre o arquivo de texto para escrever o tweet
            with codecs.open(self.dir_destino + nome_arquivo, 'w', 'utf-8') as f:
                f.write(tweet_formatado)
            
            self.numero_tweet += 1  # Incrementa o contador de tweets coletados

            porcentagem_corrente = (self.numero_tweet * 100 / self.qtde_tweets)
            
            if porcentagem_corrente != self.porcentagem_coletada:
                self.porcentagem_coletada = porcentagem_corrente
                print "%s%% dos tweets foram coletados." % str(self.porcentagem_coletada)
        
        return True
        
    
    def on_status(self, status):
        print status
        
    
    def on_error(self, status_code):
        print status_code
