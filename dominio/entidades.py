# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 10:41:32 2015

@author: lucas
"""

# REVISADO EM 11-09-2015


class EntidadeDominio(object):
    def __init__(self):
        pass    


class Documento(EntidadeDominio):
    """Documentar
    """
    def __init__(self, texto, categoria, corpus_pertencente, nome):
        """Documentar
        """
        self.texto = texto
        self.categoria = categoria
        self.nome = nome
        self.corpus_pertencente = corpus_pertencente

    def get_stop_words(self):
        """Retorna uma lista com as stopwords contidas no
        documento
        """
        raise NotImplementedError

    @staticmethod
    def get_features(documento, palavras_frequentes_corpus=None):
        """Esse método é um feature extractor para classificação de documentos;
        as features indicam se palavras individuais, palavras estas que compõe
        o dicionário com todas as palavras existentes no corpus que está sendo
        utilizado (word_features), estão presentes ou não no documento recebido
        por parâmetro.
        Dessa forma, o classificador aprende com base nos aspectos dos dados
        que lhe são ensinados, a prestar atenção, nesse caso, se determinadas
        palavras estão ou não presentes em um documento.
        """
        if palavras_frequentes_corpus is None:
            palavras_frequentes_corpus = documento.corpus_pertencente.get_palavras_frequentes()

        palavras_documento = set(documento.texto.split())

        features = {}  # Features que serão retornadas {possui('palavra'): True}
        
        # Pra cada uma das palavras do corpus.
        for palavra_corpus in palavras_frequentes_corpus:
            # Verifica se a 'palavra_corpus' está presente no documento
            if palavra_corpus in palavras_documento:
                features['possui(%s)' % palavra_corpus] = True

        if documento.categoria is None:
            return features

        # tupla ({possui('palavra'): True}, 'pos')
        features_com_categoria = (features, documento.categoria)

        # print features
        return features_com_categoria
