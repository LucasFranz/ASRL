# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 15:10:22 2015

@author: lucas
"""

from flask import Flask
from flask import request
from flask import render_template
from controle.fachada import  *

app = Flask(__name__)

"""
@app.route('/')
def hello_world():
    return 'Hello World!'
"""

@app.route('/analisarSentimento', methods=['GET', 'POST'])
def analisar_sentimento():
    fachada = Fachada()
    palavra_chave = request.form['palavraChave']
    resultado = u''
    # Classifica a opinião de cada novo tweet coletado
    for i in fachada.analisar_opiniao_tweets([str(palavra_chave)]):
         resultado += str((i[1], ' ~> ', i[0])) + '\n'
         
    return resultado


@app.route('/', methods=['GET', 'POST'])
def testar_jinja_template():
    return render_template('template.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])


if __name__ == '__main__':
    app.run()