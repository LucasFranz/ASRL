#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 02:32:50 2015

@author: lucas
"""

from controle.fachada import Fachada
from dominio.entidades import Documento
from util.classificador_util import ClassificadorUtil
from util.corpus_util import CorpusUtil
import codecs
import os
from random import shuffle
from util.arquivo_util import ArquivoUtil

if __name__ == '__main__':
    # texto = raw_input("Resenha: ")

    raiz_corpus = "/home/lucas/Documents/mineracao_opiniao/corpus_resenhas_livros_processado_sem_stem_e_negacao"

    classificador_path = "/home/lucas/Documents/mineracao_opiniao/classificadores_treinados/" \
                         "classificadores_resenhas_livros/" \
                         "classificador_naive_bayes_resenhas_livros_3860_sem_stem_negacao_2015-09-23.16.17.32.802909.pickle"
    
    nova_fachada = Fachada()
    corpus = CorpusUtil(raiz_corpus)

    # texto = "Excelente livro, recomendo! Muito bom, vale a pena."
    '''texto = """Quando terminei de ler o livro fiquei admirada com o autor! Ele é simplesmente magnifico.
     Não vou negar que depois de começar a ler a segunda parte da obra fiquei entediada, mas não fui
     capaz de abandona-la, ainda bem, mas quando cheguei no final do livro entendi o motivo da segunda
     parte. O livro é muito bem bolado e vale a pena ler!"""'''

    documentos_path = raiz_corpus + "/pos"

    nomes = os.listdir(documentos_path)
    shuffle(nomes)

    documentos = []
    for nome_documento in nomes:
        if nome_documento.endswith('.txt'):
            # Lê todos os novos documentos coletados e monta uma
            # lista com o conteúdo de todos estes documentos.
            with codecs.open(documentos_path + '/' + nome_documento, 'r', 'utf-8') as f:
                texto = f.read()
                documentos.append(Documento(texto, None, corpus, nome_documento))

    classificador = ClassificadorUtil().abrir_classificador_treinado(classificador_path)


    qtde_pos = 0
    qtde_neg = 0
    for documento in documentos:
        # print documento.texto
        documento = nova_fachada.processar_documento(documento)
        sentimento = nova_fachada.analisar_sentimento_documento(documento, classificador)
        if sentimento == 'pos':
            qtde_pos += 1
            print documento.nome
            break
        elif sentimento == 'neg':
            qtde_neg += 1

        print "-- sentimento: %s." % sentimento

    print "-- quantidade positiva: %d" % qtde_pos
    print "-- quantidade negativa: %d" % qtde_neg

    # print palavras_frequentes_corpus
    # print "-- sentimento: %s." % sentimento
