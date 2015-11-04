# -*- coding: utf-8 -*-

from util.classificador_util import ClassificadorUtil

if __name__ == '__main__':
    classificador_path = "/home/lucas/Documents/mineracao_opiniao/classificadores_treinados/" \
                         "naive_bayes_3860_resenhas_2015-09-25.00.52.23.944959.pickle"

    classificador = ClassificadorUtil().abrir_classificador_treinado(classificador_path)

    print classificador.show_most_informative_features(15)
