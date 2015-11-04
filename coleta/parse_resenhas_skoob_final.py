#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import codecs
import time
import sys
import platform
import unicodedata


SENTIMENTO_NEG = 'neg'
SENTIMENTO_POS = 'pos'
SENTIMENTO_INCERTO = 'incerto'

TITULO_LIVRO = 'titulo_livro'
RESENHA_SENTIMENTO = 'resenha_sentimento'
RESENHA_TEXTO = 'resenha_texto'
QTDE_ESTRELAS = 'qtde_estrelas'
RESENHA_ID = 'resenha_id'

URL_SITE = "http://www.skoob.com.br"

SISTEMA_OPERACIONAL = platform.system()

if SISTEMA_OPERACIONAL == 'Linux':
    ARQUIVO_LIVRO_ID_CONTINUACAO = ('/home/lucas/Documents/mineracao_opiniao/arquivos_utilizados_scripts/'
                                    'livro_id_continuacao_parsing.txt')
elif SISTEMA_OPERACIONAL == 'Windows':
    ARQUIVO_LIVRO_ID_CONTINUACAO = "C:\\Users\\lucas_000\\Documents\\livro_id_continuacao_parsing.txt"

def get_htmls_resenhas(links_resenhas):

    todos_htmls = []

    for url_resenha in links_resenhas:
        resultado = None

        time.sleep(30)  # Pausa de 30 segundos para fazer a requisição seguinte

        print url_resenha

        while resultado is None:
            try:
                resultado = requests.get(url_resenha)
            except requests.ConnectionError, e:
                print e

        # HTML com as resenhas de url_resenha
        html_resenhas = resultado.text

        # Inclue esse HTML na lista com todos os htmls,
        # que serão retornados.
        todos_htmls.append(html_resenhas)

    return todos_htmls


def get_html_resenhas_primeira_pagina(livro_id):
    url_anexo_livro = "/livro/resenhas/" + livro_id + "/mpage:1"
    url_resenhas_primeira_pagina = URL_SITE + url_anexo_livro

    time.sleep(5)  # Pausa de 5 segundos para fazer a requisição seguinte

    print url_resenhas_primeira_pagina

    resultado = None
    
    while resultado is None:
        try:
            resultado = requests.get(url_resenhas_primeira_pagina)
        except requests.ConnectionError, e:
            print e
        
    resenhas_html = resultado.text

    return resenhas_html


def get_resenhas(resenhas_html):
    soup = BeautifulSoup(resenhas_html)
    
    titulo_livro = soup.find('strong',
                             {'itemprop': 'name', 'class': 'sidebar-titulo'})
                             
    if titulo_livro is None:
        return False
    
    titulo_livro = titulo_livro.string
    
    padrao_resenhas = re.compile(r'resenha[0-9]{8}')
    divs_resenhas = soup.find_all('div', {'id': padrao_resenhas})
    
    if divs_resenhas is None:
        return False
    
    resenhas = []
    
    # Para cada tag
    for div in divs_resenhas:
        # Avaliação por estrelas
        avaliacao_estrelas = div.find('star-rating')
        qtde_estrelas = avaliacao_estrelas.get('rate')
        qtde_estrelas = int(qtde_estrelas)
        
        resenha_id = div.get('id')
        
        if qtde_estrelas == 0 or qtde_estrelas == 3:  # Descarta resenha
            continue  # Próxima iteração
        if qtde_estrelas < 3:
            sentimento_resenha = SENTIMENTO_NEG
        else:
            sentimento_resenha = SENTIMENTO_POS
        
        padrao_resenha_interno = re.compile(r'resenhac[0-9]{8}')
        div_resenha_interna = div.find('div', {'id': padrao_resenha_interno})
        
        nome_autor_resenha = div_resenha_interna.find('strong',
                                                      {'style': 'font-size:11px; font-family:arial; display:block; float:left; margin-right:5px;'})
        
        # Remove o nome do autor da resenha
        nome_autor_resenha.replace_with('')
        
        data_resenha = div_resenha_interna.find('span',
                                                {'style': 'color:#666666; font-size:11px; display:block; float:left;'})

        if data_resenha is not None:
            # Remove a data da resenha
            data_resenha.replace_with('')
        
        titulo_resenha = div_resenha_interna.find('strong')
        
        if titulo_resenha is not None:
            # Adiciona uma quebra de linha entre o título e a resenha
            titulo_resenha_corrigido = titulo_resenha.get_text()
            titulo_resenha_corrigido += '\n'
            titulo_resenha.replace_with(titulo_resenha_corrigido)
        
        
        resenha_texto = div_resenha_interna.get_text()
        
        resenha = {TITULO_LIVRO: titulo_livro,
                   RESENHA_TEXTO: resenha_texto,
                   QTDE_ESTRELAS: str(qtde_estrelas),
                   RESENHA_SENTIMENTO: sentimento_resenha,
                   RESENHA_ID: resenha_id}
                                    
        resenhas.append(resenha)
        
    return resenhas
    

def montar_nome_arquivo(resenha):
    MOLDE_NOME = "%s_%s_-_%s_estrelas.txt"
    nome_arquivo = MOLDE_NOME % (resenha[TITULO_LIVRO], resenha[RESENHA_ID], resenha[QTDE_ESTRELAS])
    
    nome_arquivo = nome_arquivo.lower()
    nome_arquivo = re.sub(r'[\s\\/]', '_', nome_arquivo)
    # print nome_arquivo
    return nome_arquivo


"""
def encodar_para_utf8(resenha_texto):
    # resenha_texto = resenha_texto.decode('ISO-8859-1')
    # resenha_texto = resenha_texto.decode('utf-8')
    return resenha_texto
"""


def gravar_arquivo(nome_arquivo, diretorio_destino, resenha_texto):
    if SISTEMA_OPERACIONAL == 'Linux':
        nome_final = "%s/%s" % (diretorio_destino, nome_arquivo)
    elif SISTEMA_OPERACIONAL == 'Windows':
        nome_final = "%s\\%s" % (diretorio_destino, nome_arquivo)
        
    with codecs.open(nome_final, 'w', 'utf-8') as f:
        f.write(resenha_texto)
        
    return True


def ler_livro_id_continuacao():
    with open(ARQUIVO_LIVRO_ID_CONTINUACAO, 'r') as f:
        livro_id_inicial = f.read()
    return int(livro_id_inicial)


def atualizar_livro_id_continuacao(novo_livro_id_inicial):
    with open(ARQUIVO_LIVRO_ID_CONTINUACAO, 'w+') as f:
        f.write(novo_livro_id_inicial)
        return True


def get_links_resenhas_livro(html_resenhas_primeira_pagina):
    soup = BeautifulSoup(html_resenhas_primeira_pagina)

    # Procura os links para as páginas com outras resenhas do mesmo livro,
    # uma vez que nem sempre é existem sete (7) páginas de resenha para cada livro.
    paginas_encontradas = soup.find('div', {'class': 'numeros'})  # Procura a classe com os links

    if paginas_encontradas is None:
        return False

    links_encontrados = paginas_encontradas.find_all('a')  # Retorna uma lista com todos os links, exceto o da página corrente

    links_resenhas = []

    for link in links_encontrados:
        link_resenha = URL_SITE + link.get('href')
        links_resenhas.append(link_resenha)

    # Retorna os links das demais páginas encontradas,
    # que contém resenhas sobre o livro identificado
    # por 'livro_id'
    return links_resenhas


if __name__ == '__main__':
    
    qtde_resenhas = 0
    qtde_urls_livros_visitadas = 0
    
    LIVRO_ID_INICIAL = ler_livro_id_continuacao()
    LIVRO_ID_LIMITE = LIVRO_ID_INICIAL + 5000

    # Backup para atualizar o id no arquivo de texto,
    # a fim de continuar de onde parou, na próxima
    # vez que o script for executado
    NOVO_LIVRO_ID_INICIAL = LIVRO_ID_INICIAL
    
    # Resenhas sobre livros diferentes
    for livro_id in range(LIVRO_ID_INICIAL, LIVRO_ID_LIMITE):
        html_resenhas_primeira_pagina = get_html_resenhas_primeira_pagina(str(livro_id))
        links_demais_paginas_resenha = get_links_resenhas_livro(html_resenhas_primeira_pagina)

        htmls_resenhas = []

        if links_demais_paginas_resenha is not False:
            htmls_resenhas = get_htmls_resenhas(links_demais_paginas_resenha)

        # Anexa o html da primeira página com resenhas do livro
        htmls_resenhas.append(html_resenhas_primeira_pagina)

        for html_resenhas in htmls_resenhas:
            # Faz parsing no arquivo html, e extrai
            # as resenhas deste.
            resenhas = get_resenhas(html_resenhas)

            if resenhas is False or len(resenhas) == 0:
                continue  # Próxima iteração
            
            qtde_resenhas += len(resenhas)

            # Para cada resenha
            for resenha in resenhas:
                # Em casos de spoiler, a resenha não é apresentada,
                # portanto, está vem vazia e é descartada.
                if len(resenha) == 0:
                    continue

                # Verifica qual será o diretório no qual o arquivo
                # com a resenha será salvo, de acordo com a quantidade
                # de estrelas da resenha, bem como o sistema operacional
                # no qual o script está sendo executado.
                if SISTEMA_OPERACIONAL == 'Linux':
                    DIRETORIO_DESTINO_RAIZ = "/home/lucas/Documents/mineracao_opiniao/resenhas_continuacao_25-09-2015"

                    if resenha[RESENHA_SENTIMENTO] == SENTIMENTO_POS:
                        DIRETORIO_DESTINO = DIRETORIO_DESTINO_RAIZ + "/pos"
                    elif resenha[RESENHA_SENTIMENTO] == SENTIMENTO_NEG:
                        DIRETORIO_DESTINO = DIRETORIO_DESTINO_RAIZ + "/neg"
                    elif resenha[RESENHA_SENTIMENTO] == SENTIMENTO_INCERTO:
                        DIRETORIO_DESTINO = DIRETORIO_DESTINO_RAIZ + "/incerto"

                elif SISTEMA_OPERACIONAL == 'Windows':
                    DIRETORIO_DESTINO_RAIZ = "C:\\Users\\lucas_000\\Documents\\resenhas_livros"

                    if resenha[RESENHA_SENTIMENTO] == SENTIMENTO_POS:
                        DIRETORIO_DESTINO = DIRETORIO_DESTINO_RAIZ + "\\pos"
                    elif resenha[RESENHA_SENTIMENTO] == SENTIMENTO_NEG:
                        DIRETORIO_DESTINO = DIRETORIO_DESTINO_RAIZ + "\\neg"
                    elif resenha[RESENHA_SENTIMENTO] == SENTIMENTO_INCERTO:
                        DIRETORIO_DESTINO = DIRETORIO_DESTINO_RAIZ + "\\incerto"

                # Monta o nome do arquivo de texto, no qual a resenha será gravada
                nome_arquivo = montar_nome_arquivo(resenha)

                # Corrige caracteres com problema
                # resenha[RESENHA_TEXTO] = fix_bad_unicode(resenha[RESENHA_TEXTO])

                try:
                    # Remove caractere de new line do Windows
                    # resenha[RESENHA_TEXTO] = resenha[RESENHA_TEXTO].replace("\r", "")

                    # Grava o arquivo com a resenha no diretório especificado
                    gravar_arquivo(nome_arquivo,
                                   DIRETORIO_DESTINO,
                                   resenha[RESENHA_TEXTO])
                except KeyboardInterrupt, e:
                    atualizar_livro_id_continuacao(str(NOVO_LIVRO_ID_INICIAL))
                    sys.exit(0)

        NOVO_LIVRO_ID_INICIAL += 1
        atualizar_livro_id_continuacao(str(NOVO_LIVRO_ID_INICIAL))
        qtde_urls_livros_visitadas += 1

        print '\nNumero de resenhas salvas: %s.' % (str(qtde_resenhas))

        porcentagem_urls_livros_visitadas = qtde_urls_livros_visitadas * 100 / (LIVRO_ID_LIMITE - LIVRO_ID_INICIAL)
        print '%s%% das urls de livros foram visitadas.' % (str(porcentagem_urls_livros_visitadas))
        print '\n-----\n'
