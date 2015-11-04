# -*- coding: utf-8 -*-

from controle.fachada import Fachada
from util.arquivo_util import ArquivoUtil

documento_path = "/home/lucas/Documents/mineracao_opiniao"

nova_fachada = Fachada()

# Lê documento
documentos = ArquivoUtil().ler_documentos(documento_path, "INDEFINIDA")

print "-- processando todos os documentos."
print " -- Texto original"
print documentos[0].texto
nova_fachada.processar_documento(documentos[0])
