# -*- coding: utf-8 -*-

from sklearn import cross_validation
from util.corpus_util import CorpusUtil
from nltk.classify import NaiveBayesClassifier
from nltk.classify import accuracy
from random import shuffle


def calcular_media_aritmetica(lista_numeros):
    soma = 0
    for numero in lista_numeros:
        soma += numero

    media_aritmetica = soma / len(lista_numeros)

    return media_aritmetica


if __name__ == '__main__':
    raiz_corpus = "/home/lucas/Documents/mineracao_opiniao/corpus_resenhas_livros"

    corpus = CorpusUtil(raiz_corpus)
    features_set = corpus.get_featuresets()
    cv = cross_validation.KFold(len(features_set), n_folds=10)

    acuracias = []

    i = 1
    for train_range_indices, test_range_indices in cv:
        print "-- Treinando classificador."
        classificador = NaiveBayesClassifier.train(features_set[train_range_indices[0]:train_range_indices[-1]])

        print "-- Calculando acuracia."
        acuracia = accuracy(classificador, features_set[test_range_indices[0]:test_range_indices[-1]])

        print '--- acuracia fold %d: %s.' % (i, str(acuracia))

        acuracias.append(acuracia)

        i += 1

    print "-- acuracia media do classificador: %s" % str(calcular_media_aritmetica(acuracias))
