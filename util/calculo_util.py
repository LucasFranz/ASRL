# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 21:53:11 2015

@author: lucas
"""

# REVISADO EM 11-09-2015


class CalculoUtil(object):
    """Documentar
    """
    def __init__(self):
        self.PORCENTAGEM_POSITIVA = 'porcentagem_positiva'
        self.PORCENTAGEM_NEGATIVA = 'porcentagem_negativa'

    def calcular_porcentagem_opinioes(self, qtde_positiva, qtde_negativa):
        """Documentar
        """
        # Valor total, 100%
        qtde_total = qtde_positiva + qtde_negativa
        
        porcentagem_positiva = qtde_positiva * 100 / qtde_total
        porcentagem_negativa = qtde_negativa * 100 / qtde_total
        
        porcentagens = {self.PORCENTAGEM_POSITIVA: porcentagem_positiva,
                        self.PORCENTAGEM_NEGATIVA: porcentagem_negativa}

        return porcentagens
