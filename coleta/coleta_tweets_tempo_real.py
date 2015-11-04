#!/usr/bin/python
# -*- coding: utf-8 -*-

from tweepy import OAuthHandler
from tweepy import Stream
from listener_tweets import CustomListener

class ColetaTempoReal(object):
    
    def __init__(self, palavras_chave=['dilma', 'lula'],
                 idiomas=['pt'], qtde_tweets=50,
                 dir_destino=""):
        """Recebe uma list com as palavras-chave, que são o nome
        dos políticos."""
        self.palavras_chave = palavras_chave
        self.idiomas = idiomas
        self.qtde_tweets = qtde_tweets
        self.dir_destino = dir_destino
        
        # Variáveis com as minhas credenciais de acesso a API do Twitter
        self._CONSUMER_KEY = "XOpeznyFiqxHNFKMOCllsYn5C"
        self._CONSUMER_SECRET = "0EYmidRYdeUI9bF5AGLj7Wy9GWA9gu9OwKmP5ZRtBi7V9NhGdd"
        self._ACCESS_TOKEN = "3130786373-0ljRrQ9Qs63CA5GybOEwrgk3Wgfs5xfRFewBzA4"
        self._ACCESS_TOKEN_SECRET = "QPFUggwKhWJXrg5261jX3uCEYZvRMQB4xofI9UY3m8wHY"
        
    
    def coletar_tweets(self):
        
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = CustomListener(self.qtde_tweets, self.dir_destino)
        auth = OAuthHandler(self._CONSUMER_KEY, self._CONSUMER_SECRET)
        auth.set_access_token(self._ACCESS_TOKEN, self._ACCESS_TOKEN_SECRET)
        stream = Stream(auth, listener)
        
        # This line filter Twitter Streams to capture data by the keywords: 'dilma'
        stream.filter(track=self.palavras_chave, languages=self.idiomas)
