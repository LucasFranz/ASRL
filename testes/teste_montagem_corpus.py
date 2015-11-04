# -*- coding: utf-8 -*-

import os
from nltk import FreqDist
from random import shuffle
from util.arquivo_util import ArquivoUtil
import shutil


if __name__ == '__main__':
    dir_resenhas_raiz = "/home/lucas/Documents/mineracao_opiniao/resenhas_desde_inicio_18-09-2015"
    dir_resenhas_pos = dir_resenhas_raiz + "/pos"
    dir_resenhas_neg = dir_resenhas_raiz + "/neg"

    dir_destino_raiz = "/home/lucas/Documents/mineracao_opiniao/corpus_resenhas_novo_teste"
    dir_destino_pos = dir_destino_raiz + "/pos"
    dir_destino_neg = dir_destino_raiz + "/neg"

    qtde_resenhas_cada_categoria = 3860

    # Resenhas Positivas
    print "-- lendo o nome das resenhas positivas."
    arquivos_resenhas_pos = [dir_resenhas_pos + "/" + nome_arquivo for nome_arquivo in os.listdir(dir_resenhas_pos)
                             if nome_arquivo.endswith('.txt')]

    print " -- len(arquivos_resenhas_pos) = %s." % len(arquivos_resenhas_pos)

    print "-- embaralhando a ordem das resenhas positivas."
    for i in range(0, 7):
        shuffle(arquivos_resenhas_pos)

    print "-- copiando resenhas positivas para o destino."
    for i in range(0, qtde_resenhas_cada_categoria):
        resenha = arquivos_resenhas_pos[i]
        shutil.copy(resenha, dir_destino_pos)

    del arquivos_resenhas_pos

    # Resenhas Negativas
    print "-- lendo o nome das resenhas negativas."
    arquivos_resenhas_neg = [dir_resenhas_neg + "/" + nome_arquivo for nome_arquivo in os.listdir(dir_resenhas_neg)
                             if nome_arquivo.endswith('.txt')]

    print "-- copiando resenhas negativas para o destino."
    for i in range(0, qtde_resenhas_cada_categoria):
        resenha = arquivos_resenhas_neg[i]
        shutil.copy(resenha, dir_destino_neg)

    del arquivos_resenhas_neg



