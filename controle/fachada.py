# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 22:11:43 2015

@author: lucas
"""

from negocio.regras_de_negocio import *
# from coleta.coleta_tempo_real import ColetaTempoReal
from nltk.classify import NaiveBayesClassifier
from util.corpus_util import CorpusUtil
from datetime import datetime
from util.classificador_util import ClassificadorUtil


class Fachada(object):
    def __init__(self):
        # Commands disponiveis.
        # Regras de negócio para processar os documentos.
        # Existe uma ordem correta de processamento das regras,
        # portanto a ordem das regras nessa lista é importante.
        #
        # No momento, notações como 'emoticon_feliz' e 'simbolo_monetario'
        # também são alterados pelo stemmer.

        # Processar 'DivideCamelCaseCommand' antes de 'ProcessaNegacaoCommand',
        # evita erros como 'NAO_JKRowling'.
        self.regras_negocio = [CorrigeAbreviacaoContracaoCommand(),
                               RemoveRTCommand(),
                               CorrigeRisadaCommand(),
                               RemoveNumerosCommand(),
                               PadronizaSimboloMonetarioCommand(),
                               PadronizaLinksCommand(),
                               RemoveEmailCommand(),
                               ProcessaEmoticonsCommand(),
                               DivideCamelCaseCommand(),
                               ConverteLowerCaseCommand(),
                               # StemmerCommand(),
                               # ProcessaNegacaoCommand(),
                               RemovePontuacaoCommand(),
                               RemoveStopwordsCommand(),
                               RemoveEspacosExtraCommand()]

        '''self.regras_negocio = [StemmerCommand()]'''

        self._CLASSIFICADOR_PATH = "/home/lucas/Documents/mineracao_opiniao/classificadores_treinados/" \
                                   "naive_bayes_3860_resenhas_2015-09-25.00.52.23.944959.pickle"

        '''self._CLASSIFICADOR_PATH = "/home/lucas/Documents/mineracao_opiniao/classificadores_treinados/" \
                                   "naive_bayes_3860_resenhas_negacao_2015-10-10.16.54.27.113297.pickle"'''

        self._CORPUS_RAIZ = "/home/lucas/Documents/mineracao_opiniao/corpus_resenhas_livros_processadas"

        self._PATH_PALAVRAS_FREQUENTES_CORPUS = "/home/lucas/Documents/mineracao_opiniao/palavras_frequentes_corpus/" \
                                                "palavras_frequentes_2015-09-25.15.05.22.013713.pickle"

        # self._MODO_ANALISE_PROBABILISTICO = "modo_probabilistico"
        # self._MODO_ANALISE_DICIONARIO = "modo_dicionario"

        self._CORPUS = CorpusUtil(self._CORPUS_RAIZ)

    """
    def coletar_documentos(self, palavras_chave=['dilma', 'lula'],
                           qtde_tweets=50, dir_destino=""):
        '''Coleta uma porção de tweets que mencionam
        determinada entidade, salvando cada tweet coletado
        em um arquivo de texto, no direório especificado.
        '''
        coleta_tr = ColetaTempoReal(palavras_chave=palavras_chave,
                                    qtde_tweets=qtde_tweets,
                                    dir_destino=dir_destino,
                                    idiomas=['pt'])
        coleta_tr.coletar_tweets()
        
        return True
    """

    def analisar_sentimento_documento(self, texto):
        # Instancia um documento com o texto recebido por parametro
        documento = Documento(texto, None, self._CORPUS, "nome")

        # Processa o documento, antes de analisar o sentimento deste
        documento = self.processar_documento(documento)

        # Abre classificador
        classificador = ClassificadorUtil().abrir_classificador_treinado(self._CLASSIFICADOR_PATH)

        # Abre o arquivo com as palavras frequentes do corpus
        palavras_frequentes = self._CORPUS.abrir_arquivo_palavras_frequentes(self._PATH_PALAVRAS_FREQUENTES_CORPUS)
        # palavras_frequentes = None

        # Analisa o sentimento do texto do documento e o retorna
        sentimento = classificador.classify(Documento.get_features(documento, palavras_frequentes))

        documento.categoria = sentimento

        return documento

    @staticmethod
    def treinar_classificador(raiz_corpus):
        """Documentar
        """
        minuto_incio = datetime.now().minute

        corpus = CorpusUtil(raiz_corpus)

        train_set = corpus.get_train_set()

        '''print " ++ len(train_set): %d" % len(train_set)
        print " ++ type(train_set): %s" % type(train_set)

        test_set = corpus.get_test_set()

        print " ++ len(test_set): %d" % len(test_set)
        print " ++ type(test_set): %s" % type(test_set)

        # test_set
        qtde_pos = 0
        qtde_neg = 0
        for features in test_set:

            if features[1] == 'pos':
                qtde_pos += 1
            elif features[1] == 'neg':
                qtde_neg += 1

            # print " ++ features[1]: ", features[1]

        print "Quantidade de documentos positivos em 'test_set': %d" % qtde_pos
        print "Quantidade de documentos negativos em 'test_set': %d" % qtde_neg'''

        classificador = NaiveBayesClassifier.train(train_set)
        print " -- Classificador treinado com sucesso."

        minuto_fim = datetime.now().minute

        tempo_decorrido = minuto_fim - minuto_incio

        print "-- Tempo decorrido: %s minutos." % str(tempo_decorrido)

        return classificador

    def processar_documentos_corpus(self, documentos, diretorio_destino):
        """Passa todos os documentos de um corpus, por
         todas as regras de negócio de processamento.
        """
        qtde_docs_processados = 0
        porcentagem_processada = 0
        for documento in documentos:
            doc_processado = documento  # Cópia do documento a ser processada

            # print "\n\n"

            # print doc_processado.nome
            # Passa por todas as regras de negócio
            for cmd in self.regras_negocio:
                # print "  -- Command: %s" % cmd.__class__.__name__

                doc_processado = cmd.execute(doc_processado)

                # print doc_processado.texto

            ArquivoUtil().gravar_documento_processado(doc_processado, diretorio_destino)

            qtde_docs_processados += 1

            porcentagem_corrente = qtde_docs_processados * 100 / len(documentos)

            if porcentagem_processada != porcentagem_corrente:
                porcentagem_processada = porcentagem_corrente
                print "%s%% dos documentos foram processados." % str(porcentagem_processada)
            # documentos_processados.append(doc_processado)

        return True

    def processar_documento(self, documento):
        """Documentar
        """
        doc_processado = documento

        for cmd in self.regras_negocio:
            print "  -- Command: %s" % cmd.__class__.__name__

            doc_processado = cmd.execute(doc_processado)
            print doc_processado.texto

            print "\n"

        return doc_processado
