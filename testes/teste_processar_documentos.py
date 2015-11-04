# -*- coding: utf-8 -*-

from controle.fachada import Fachada
from util.arquivo_util import ArquivoUtil

RESENHAS_RAIZ = "/home/lucas/Documents/mineracao_opiniao/resenhas_percy_jackson"
RESENHAS_POS = RESENHAS_RAIZ + "/pos"
RESENHAS_NEG = RESENHAS_RAIZ + "/neg"

diretorio_destino_raiz = "/home/lucas/Documents/mineracao_opiniao/resenhas_percy_jackson_processadas"
diretorio_destino_pos = diretorio_destino_raiz + "/pos"
diretorio_destino_neg = diretorio_destino_raiz + "/neg"

nova_fachada = Fachada()

print "-- lendo todos os documentos."
documentos = ArquivoUtil().ler_documentos(RESENHAS_RAIZ, "INDEFINIDA")

print "-- processando todos os documentos."
nova_fachada.processar_documentos_corpus(documentos, diretorio_destino_raiz)

# print "-- lendo documentos positivos"
# documentos_pos = ArquivoUtil().ler_documentos(RESENHAS_POS, 'pos')

# print "-- processando documentos positivos"
# nova_fachada.processar_documentos_corpus(documentos_pos, diretorio_destino_pos)

# print "-- lendo documentos negativos"
# documentos_neg = ArquivoUtil().ler_documentos(RESENHAS_NEG, 'neg')

# print "-- processando documentos negativos"
# nova_fachada.processar_documentos_corpus(documentos_neg, diretorio_destino_neg)
