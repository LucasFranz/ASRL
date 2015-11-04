#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 11:16:00 2015

@author: lucas
"""

from flask import Flask, render_template, url_for, request
from controle.fachada import Fachada
from util.arquivo_util import ArquivoUtil
import time
from util.grafico_util import GraficoUtil
from util.calculo_util import CalculoUtil
from negocio.regras_de_negocio import DivideCamelCaseCommand
from dominio.entidades import Documento

app = Flask(__name__, static_folder='/home/lucas/Documents/mineracao_opiniao/graficos')
# app = Flask(__name__)
PERCY_JACKSON = "PercyJackson"
JOGOS_VORAZES = "JogosVorazes"
CONVERGENTE = "Convergente"
CIDADES_DE_PAPEL = "CidadesDePapel"


@app.route("/ASRL")
def index():
    return render_template('home.html')


@app.route("/ASRL/analisar_sentimento", methods=['POST'])
def analiasar_sentimento():
    nova_fachada = Fachada()
    resenha = request.form['txtResenha']

    documento = nova_fachada.analisar_sentimento_documento(resenha)

    if documento.categoria == 'pos':
        sentimento = 'positivo'
    elif documento.categoria == 'neg':
        sentimento = 'negativo'

    # sentimento = documento.categoria

    # Dispoẽ os elementos no template html 'resultado_analise' (gráfico, tweets)
    return render_template('home.html', sentimento=sentimento, resenha=resenha)


@app.route("/ASRL/escolher_livro", methods=['GET'])
def escolher_livro():
    return render_template("escolha_livro.html")


@app.route("/ASRL/analisar_sentimento_conjunto", methods=['POST'])
def analisar_sentimento_conjunto():
    paths = {PERCY_JACKSON: "/home/lucas/Documents/mineracao_opiniao/resenhas_percy_jackson",
             JOGOS_VORAZES: "/home/lucas/Documents/mineracao_opiniao/resenhas_jogos_vorazes",
             CONVERGENTE: "/home/lucas/Documents/mineracao_opiniao/resenhas_convergente",
             CIDADES_DE_PAPEL: "/home/lucas/Documents/mineracao_opiniao/resenhas_cidades_de_papel"}

    diretorio_destino_grafico = "/home/lucas/Documents/mineracao_opiniao/graficos"

    titulo_livro = request.form['titulo_livro']
    documentos_path = paths[titulo_livro]
    documentos = ArquivoUtil().ler_documentos(documentos_path, None)
    documentos_classificados = []

    # Pequena correção no título do livro
    documento = Documento(titulo_livro, None, None, None)
    titulo_livro = DivideCamelCaseCommand().execute(documento).texto

    data_analise = time.strftime("%d/%m/%Y")
    horario_analise = time.strftime("%H:%M:%S")

    nova_fachada = Fachada()

    qtde_pos = 0
    qtde_neg = 0
    for documento in documentos:
        documento_classificado = nova_fachada.analisar_sentimento_documento(documento.texto)
        documento_classificado.texto = documento.texto  # Substitui o texto processado pelo original
        documentos_classificados.append(documento_classificado)
        if documento_classificado.categoria == "pos":
            qtde_pos += 1
        elif documento_classificado.categoria == "neg":
            qtde_neg += 1

    # Calcula porcentagem de resenhas positivas e negativas
    porcentagens = CalculoUtil().calcular_porcentagem_opinioes(qtde_pos, qtde_neg)
    porcentagem_pos = porcentagens[CalculoUtil().PORCENTAGEM_POSITIVA]
    porcentagem_neg = porcentagens[CalculoUtil().PORCENTAGEM_NEGATIVA]

    grafico = GraficoUtil()

    nome_grafico = grafico.construir_grafico_pizza(porcentagem_pos, porcentagem_neg, titulo_livro, diretorio_destino_grafico)
    '''nome_grafico = grafico.salvar_grafico(grafico_pizza, titulo_livro,
                                          diretorio_destino_grafico)'''

    return render_template('resultado_analise.html',
                           documentos=documentos_classificados, titulo_livro=titulo_livro,
                           data_analise=data_analise, horario_analise=horario_analise,
                           grafico_pizza=nome_grafico)

if __name__ == '__main__':
    app.run(debug=True)
