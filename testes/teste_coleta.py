#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 10:39:52 2015

@author: lucas
"""

from controle.nova_fachada import Fachada

fachada = Fachada()

palavras_chave = raw_input("Palavras-chave: ")
qtde_tweets = raw_input("Quantidade de tweets: ")
dir_destino = raw_input("Diretório destino: ")

palavras_chave = palavras_chave.decode('utf-8')
palavras_chave_ok = [palavra.strip() for palavra in palavras_chave.split(',')]
qtde_tweets = int(qtde_tweets)

if not dir_destino.endswith('/'):
    dir_destino += '/'

fachada.coletar_documentos(palavras_chave=palavras_chave_ok,
                           qtde_tweets=qtde_tweets,
                           dir_destino=dir_destino)
