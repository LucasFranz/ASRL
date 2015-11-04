__author__ = 'lucas'

from util.corpus_util import CorpusUtil
import pickle

if __name__ == "__main__":

    corpus_raiz = "/home/lucas/Documents/mineracao_opiniao/corpus_resenhas_livros_processadas"
    corpus = CorpusUtil(corpus_raiz)
    palavras_frequentes = corpus.gravar_palavras_frequentes()
