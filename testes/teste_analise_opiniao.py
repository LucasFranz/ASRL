# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 14:27:37 2015

@author: lucas
"""
"""
fachada = Fachada()
fachada.coletar_tweets(qtde_tweets=15)

tweets = Util().ler_documentos_nao_processados()

# Analisa opinião dos novos tweets coletados
tweets_classificados = fachada.analisar_opiniao_tweets(tweets)
print '-- %s Tweets classificados com sucesso!' % (len(tweets_classificados))

qtde_opinioes = Util().contar_documentos_cada_opiniao([opiniao for tweet, opiniao in tweets_classificados])
qtde_positiva = qtde_opinioes[Util().QTDE_POSITIVA]
qtde_negativa = qtde_opinioes[Util().QTDE_NEGATIVA]
qtde_neutra = qtde_opinioes[Util().QTDE_NEUTRA]

porcentagem_opinioes = Util().calcular_porcentagem_opinioes(qtde_positiva, qtde_negativa, qtde_neutra)
porcentagem_pos = porcentagem_opinioes[Util().PORCENTAGEM_POSITIVA]
porcentagem_neg = porcentagem_opinioes[Util().PORCENTAGEM_NEGATIVA]
porcentagem_neu = porcentagem_opinioes[Util().PORCENTAGEM_NEUTRA]

# Constroe gráfico de pizza
Util().construir_grafico_pizza(porcentagem_pos, porcentagem_neg, porcentagem_neu)
print '-- gráfico construído com sucesso!'


print '-- Amostra dos tweets analisados:'
for tweet, opiniao in tweets_classificados:
    print opiniao, ' ~> ', tweet
"""
"""
palavra_chave = 'Dilma'
fachada = Fachada()
utilidades = Util()

# Coleta novos tweets para analisar o sentimento
fachada.coletar_tweets(qtde_tweets=0, palavras_chave=[palavra_chave])
tweets_nao_classificados = utilidades.ler_documentos_nao_processados()

# Analisa a opinião de todos os tweets coletados
tweets_classificados = fachada.analisar_opiniao_tweets(tweets_nao_classificados)

qtde_opinioes = utilidades.contar_documentos_cada_opiniao([opiniao for tweet, opiniao in tweets_classificados])
qtde_positiva = qtde_opinioes[utilidades.QTDE_POSITIVA]
qtde_negativa = qtde_opinioes[utilidades.QTDE_NEGATIVA]
qtde_neutra = qtde_opinioes[utilidades.QTDE_NEUTRA]

porcentagem_opinioes = utilidades.calcular_porcentagem_opinioes(qtde_positiva, qtde_negativa, qtde_neutra)
porcentagem_pos = porcentagem_opinioes[utilidades.PORCENTAGEM_POSITIVA]
porcentagem_neg = porcentagem_opinioes[utilidades.PORCENTAGEM_NEGATIVA]
porcentagem_neu = porcentagem_opinioes[utilidades.PORCENTAGEM_NEUTRA]

nome_grafico = fachada.construir_grafico(porcentagem_pos, porcentagem_neg, porcentagem_neu)
data_e_horario = str(datetime.now())
ex
"""
