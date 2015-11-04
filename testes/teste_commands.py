# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 09:05:00 2015

@author: lucas
"""

import codecs
from controle.fachada import Fachada
from dominio.entidades import Documento

DIRETORIO_ARQUIVO = "/home/lucas/Desktop"
# NOME_ARQUIVO = "a_arte_de_fazer_acontecer_resenha18920039_-_5_estrelas.txt"
# NOME_ARQUIVO = "teste_negacao.txt"
NOME_ARQUIVO = "dez_leis.txt"
documento = Documento('', "sem_categoria", None, "")

with codecs.open(DIRETORIO_ARQUIVO + "/" + NOME_ARQUIVO, "r", "utf-8") as f:
    documento.texto = f.read()

print documento.texto

nova_fachada = Fachada()
documento = nova_fachada.processar_documento(documento)
