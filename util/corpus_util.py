# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 14:38:34 2015

@author: lucas
"""
from nltk.corpus import CategorizedPlaintextCorpusReader
from dominio.entidades import Documento
from nltk import FreqDist
from nltk.classify import apply_features
import sys
from random import shuffle
import pickle
from datetime import datetime
import re
from nltk.util import LazyMap

# REVISADO - 11-09-2015


class CorpusUtil(object):
    """Documentar
    """
    def __init__(self, raiz_corpus):
        """Cria um objeto do tipo 'CategorizedPlaintextCorpusReader',
        utilizando o diretório raiz do corpus, onde os documentos
        estão localizados, dispostos em seus respectivos subdiretórios,
        de acordo com sua categoria, sejam eles/elas quais for
        
        -->     raiz_corpus/{pos,neg,neu,...}.
        """
        reload(sys)
        sys.setdefaultencoding("utf-8")
        
        self._raiz_corpus = raiz_corpus
        self._corpus = CategorizedPlaintextCorpusReader(raiz_corpus, r'.+\.txt', cat_pattern=r'(\w+)/*',
                                                        encoding='utf-8')
        self._documentos = None
        self._palavras_frequentes = None
        self._todas_palavras = None
        self._featuresets = None
        self._train_set = None
        self._test_set = None

    def get_documentos(self):
        """Construimos uma lista de documentos, rotulados com as
        categorias apropriadas. Cada documento é representado por
        uma tupla na estrutura abaixo:
        
        (conteudo_do_documento, categoria)
        
        Retorna essa lista com todos os documentos do corpus.
        """
        """
        documentos = [(self.corpus.words(fileid), categoria)
                       for categoria in self.corpus.categories()
                       for fileid in self.corpus.fileids(categoria)]
        """
        print "-- Recuperando documentos do corpus."

        if self._documentos is None:            
            self._documentos = [Documento(" ".join(self._corpus.words(fileid)), categoria, self, fileid)
                                for categoria in self._corpus.categories()
                                for fileid in self._corpus.fileids(categoria)]

        # Embaralha documentos
        for i in range(0, 10):
            shuffle(self._documentos)

        return self._documentos

    def get_palavras_frequentes(self):
        """Documentar.
        """
        if self._palavras_frequentes is None:

            print "-- Verificando as palavras mais frequentes do corpus."

            # Teste - retorna apenas as 2000 palavras mais frequentes do corpus
            todas_palavras = [word.lower() for word in self._corpus.words()]
            freq_dist_palavras = FreqDist(todas_palavras)
            frequencia_palavras = freq_dist_palavras.most_common(2000)  # 2000 palavras mais frequentes
            
            self._palavras_frequentes = [palavra for palavra, frequencia in frequencia_palavras]
            
            # all_words = FreqDist(word.lower() for word in self.corpus.words())
            # self.word_features = list(all_words)[:2000]
        return self._palavras_frequentes

    def get_todas_palavras(self):
        if self._todas_palavras is None:
            print "-- Recuperando todas as palavras do corpus."
            self._todas_palavras = [word.lower() for word in self._corpus.words()]
            self._todas_palavras = set(self._todas_palavras)

        return self._todas_palavras

    def get_featuresets(self):
        """Configura os featuresets que são construídos na
        seguinte estrutura:
            (features_do_documento, categoria)
        
        Retorna uma lista de featuresets
        """
        if self._featuresets is None:
            
            if self._documentos is None:
                self.get_documentos()

            print "-- Recuperando featuresets."

            self._featuresets = apply_features(Documento.get_features, self._documentos)
        
        return self._featuresets

    def get_train_set(self):
        """Documentar
        """
        if self._featuresets is None:
            self.get_featuresets()

        print "-- Recuperando train_set."

        # Para não ocupar toda a memória RAM,
        # não armazena todos os documentos de uma vez nesta.
        # self._train_set = apply_features(Documento.get_features, self._documentos[100:])
        self._train_set = apply_features(Documento.get_features, self._documentos)

        return self._train_set

    def get_test_set(self):
        if self._featuresets is None:
            self.get_featuresets()

        print "-- Recuperando test_set."

        # self._test_set = apply_features(Documento.get_features, self._documentos[:100])

        return self._test_set

    def gravar_palavras_frequentes(self):
        diretorio_destino = "/home/lucas/Documents/mineracao_opiniao/palavras_frequentes_corpus"
        molde_nome_arquivo = "palavras_frequentes_%s.pickle"

        tempo_agora = str(datetime.now())
        # Substitui ':' e espaço em branco por '.'
        tempo_agora = re.sub(ur':|\s', '.', tempo_agora)
        nome_arquivo = molde_nome_arquivo % tempo_agora

        if self._palavras_frequentes is None:
            self.get_palavras_frequentes()

        f = open(diretorio_destino + "/" + nome_arquivo, 'wb')
        pickle.dump(self._palavras_frequentes, f)
        f.close()

        return True

    @staticmethod
    def abrir_arquivo_palavras_frequentes(arquivo_path):
        f = open(arquivo_path, 'rb')
        palavras_frequentes = pickle.load(f)
        f.close()

        return palavras_frequentes
