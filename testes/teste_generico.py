# -*- coding: utf-8 -*-

from dominio.entidades import Documento
from util.corpus_util import CorpusUtil

# documento = Documento("meu texto", "minha categoria", "meu corpus", "meu nome")
CORPUS_RAIZ = "/home/lucas/Documents/tweets_pos_neg"

documentos = train_set = CorpusUtil(CORPUS_RAIZ).get_documentos()
print " -- texto: %s" % documentos[0].texto
print " -- categoria: %s" % documentos[0].categoria
print " -- type(corpus_pertencente): ", type(documentos[0].corpus_pertencente)

palavras_frequentes = documentos[0].corpus_pertencente.get_palavras_frequentes()

print " ++ len(palavras_frequentes): %d" % len(palavras_frequentes)
print " ++ palavras_frequentes: %s" % palavras_frequentes
