#!/usr/bin/python
# -*- coding: utf-8 -*-

from controle.fachada import Fachada
from dominio.entidades import Documento
from util.classificador_util import ClassificadorUtil
from util.corpus_util import CorpusUtil
import codecs
import os
from random import shuffle
from util.arquivo_util import ArquivoUtil

if __name__ == '__main__':
    texto = raw_input("Resenha: ")
    nova_fachada = Fachada()

    # texto = "Incrível apaixonante emocionante."
    # texto = u"""Imprestável Puro lixo!"""
    # texto = u"livro cansativo, massante."
    # texto = "livro apaixonante, lindo!"
    # texto = u"péssimo horrível desisti enfadonho"
    # texto = u"livro muito chato"

    documento = nova_fachada.analisar_sentimento_documento(texto)

    print "-- sentimento: %s." % documento.categoria

