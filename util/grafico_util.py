# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 21:51:34 2015

@author: lucas
"""

import matplotlib.pyplot as plt
import re
from datetime import datetime


class GraficoUtil(object):
    """Documentar
    """
    @staticmethod
    def construir_grafico_pizza(porcentagem_pos, porcentagem_neg,
                                nome_grafico, diretorio_destino):
        """Documentar
        """
        # The slices will be ordered and plotted counter-clockwise.
        labels = []  # Descrição das fatias do gráfico
        sizes = []
        colors = []
        
        maior_porcentagem = max([porcentagem_pos, porcentagem_neg])
        
        if porcentagem_pos > 0:
            labels.append(u'Opiniões Positivas')
            colors.append('#2CA02C')
            sizes.append(porcentagem_pos)
        if porcentagem_neg > 0:
            labels.append(u'Opiniões Negativas')
            colors.append('#D62728')
            sizes.append(porcentagem_neg)

        # Converte lista em tupla
        labels = tuple(labels)

        plt.pie(sizes, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=90)
        
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        plt.axis('equal')

        tempo_agora = str(datetime.now())
        tempo_agora = re.sub(ur':|\s', '.', tempo_agora)  # Substitui ':' por '.'
        nome_grafico = 'grafico_pizza_%s_%s.png' % (nome_grafico, tempo_agora)

        plt.savefig(diretorio_destino + "/" + nome_grafico, transparent=True)

        plt.clf()

        # Retorna o gráfico
        # return plt
        return nome_grafico

    @staticmethod
    def salvar_grafico(grafico, nome_grafico, diretorio_destino):
        tempo_agora = str(datetime.now())
        tempo_agora = re.sub(ur':|\s', '.', tempo_agora)  # Substitui ':' por '.'
        nome_grafico = 'grafico_pizza_%s_%s.png' % (nome_grafico, tempo_agora)

        # Salva um gráfico com o fundo transparente
        # plt.savefig(diretorio_destino + "/" + nome_grafico, transparent=True)
        grafico.savefig(diretorio_destino + "/" + nome_grafico, transparent=True)

        grafico.clf()

        return nome_grafico
