# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 19:03:18 2015

@author: lucas
"""
import os
import codecs
from dominio.entidades import Documento


# REVISADO EM 11-09-2015
class ArquivoUtil(object):
    """Documentar
    """
    @staticmethod
    def ler_documentos(documentos_path, categoria):
        """Lê todos os documentos '.txt' localizados no diretório
        'documentos_path' recebido por parâmetro.
        """
        documentos = []  # Documentos lidos

        for nome_documento in os.listdir(documentos_path):
            if nome_documento.endswith('.txt'):
                # Lê todos os novos documentos coletados e monta uma
                # lista com o conteúdo de todos estes documentos.
                with codecs.open(documentos_path + '/' + nome_documento, 'r', 'utf-8') as f:
                    texto = f.read()
                    documentos.append(Documento(texto, categoria, None, nome_documento))

        return documentos

    @staticmethod
    def get_stoplist():
        stoplist_f = "/home/lucas/Documents/mineracao_opiniao/dicionario_palavras/stoplist_portugues.txt"
        
        # Primeiramente lê a stoplist
        with codecs.open(stoplist_f, 'r', 'utf-8') as f:
            stoplist = f.readlines()
            # Remove o '\n' do final de cada palavra
            stoplist_corrigida = [stopword.rstrip("\n") for stopword in stoplist]
        
        return stoplist_corrigida

    @staticmethod
    def gravar_documento_processado(documento, diretorio_destino):
        with codecs.open(diretorio_destino + "/" + documento.nome, 'w', 'utf-8') as f:
            f.write(documento.texto)
        return True
