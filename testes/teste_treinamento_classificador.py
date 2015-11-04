#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 22:34:21 2015

@author: lucas
"""

from controle.fachada import Fachada
from util.classificador_util import ClassificadorUtil

CORPUS_RAIZ = "/home/lucas/Documents/mineracao_opiniao/corpus_resenhas_livros_processadas_c"

DIRETORIO_DESTINO = "/home/lucas/Documents/mineracao_opiniao/classificadores_treinados"

nova_fachada = Fachada()
classificador = nova_fachada.treinar_classificador(CORPUS_RAIZ)

resultado = ClassificadorUtil().salvar_classificador_treinado(classificador,
                                                              "3860_resenhas_negacao",
                                                              DIRETORIO_DESTINO)

if resultado:
    print "-- Classificador salvo com sucesso."
