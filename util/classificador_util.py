# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 21:50:47 2015

@author: lucas
"""

import pickle
from datetime import datetime
import re
from nltk import classify


# REVISADO EM 11-09-2015
class ClassificadorUtil(object):
    """Documentar
    """
    def __init__(self):
        """Documentar
        """
        self._MOLDE_NOME_ARQUIVO_NAIVE_BAYES = "naive_bayes_%s_%s.pickle"
        # self._NOME_ARQUIVO_SVM = "svm_%s.pickle"

    @staticmethod
    def calcular_acuracia(classificador, test_set):
        """Calcula a acurácia do classificador treinado,
        recebido por parâmetro.
        """
        return classify.accuracy(classificador, test_set)

    def salvar_classificador_treinado(self, classificador, nome_arquivo, diretorio_destino):
        """Recebe o classificador treinado por parâmetro,
        e o salva no diretório de destino, também recebido
        por parâmetro.
        """        
        tempo_agora = str(datetime.now())
        # Substitui ':' e espaço em branco por '.'
        tempo_agora = re.sub(ur':|\s', '.', tempo_agora)
        
        # Anexa o tempo atual no fim do nome do classificador,
        # a fim de ajudar a lembrar a data em que o classificador
        # foi treinado e salvo.
        nome_arquivo = self._MOLDE_NOME_ARQUIVO_NAIVE_BAYES % (nome_arquivo, tempo_agora)
        
        # Salva o classificador em um arquivo '.pickle'
        f = open(diretorio_destino + "/" + nome_arquivo, 'wb')
        pickle.dump(classificador, f)
        f.close()
        
        return True
        
    @staticmethod
    def abrir_classificador_treinado(classificador_path):
        """Recebe por parâmetro o caminho para um classificador
        treinado, salvo em um arquivo com a extensão '.pickle'.
        
        Retorna o classificador treinado.
        """
        # Abre o classificador, sendo este um objeto Python.
        f = open(classificador_path, 'rb')
        classificador = pickle.load(f)
        f.close()
        
        return classificador
