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


def fix_bad_unicode(text):
    u"""
    Something you will find all over the place, in real-world text, is text
    that's mistakenly encoded as utf-8, decoded in some ugly format like
    latin-1 or even Windows codepage 1252, and encoded as utf-8 again.

    This causes your perfectly good Unicode-aware code to end up with garbage
    text because someone else (or maybe "someone else") made a mistake.

    This function looks for the evidence of that having happened and fixes it.
    It determines whether it should replace nonsense sequences of single-byte
    characters that were really meant to be UTF-8 characters, and if so, turns
    them into the correctly-encoded Unicode character that they were meant to
    represent.

    The input to the function must be Unicode. It's not going to try to
    auto-decode bytes for you -- then it would just create the problems it's
    supposed to fix.

        >>> print fix_bad_unicode(u'Ãºnico')
        único

        >>> print fix_bad_unicode(u'This text is fine already :þ')
        This text is fine already :þ

    Because these characters often come from Microsoft products, we allow
    for the possibility that we get not just Unicode characters 128-255, but
    also Windows's conflicting idea of what characters 128-160 are.

        >>> print fix_bad_unicode(u'This â€” should be an em dash')
        This — should be an em dash

    We might have to deal with both Windows characters and raw control
    characters at the same time, especially when dealing with characters like
    \x81 that have no mapping in Windows.

        >>> print fix_bad_unicode(u'This text is sad .â\x81”.')
        This text is sad .⁔.

    This function even fixes multiple levels of badness:

        >>> wtf = u'\xc3\xa0\xc2\xb2\xc2\xa0_\xc3\xa0\xc2\xb2\xc2\xa0'
        >>> print fix_bad_unicode(wtf)
        ಠ_ಠ

    However, it has safeguards against fixing sequences of letters and
    punctuation that can occur in valid text:

        >>> print fix_bad_unicode(u'not such a fan of Charlotte Brontë…”')
        not such a fan of Charlotte Brontë…”

    Cases of genuine ambiguity can sometimes be addressed by finding other
    characters that are not double-encoding, and expecting the encoding to
    be consistent:

        >>> print fix_bad_unicode(u'AHÅ™, the new sofa from IKEA®')
        AHÅ™, the new sofa from IKEA®

    Finally, we handle the case where the text is in a single-byte encoding
    that was intended as Windows-1252 all along but read as Latin-1:

        >>> print fix_bad_unicode(u'This text was never Unicode at all\x85')
        This text was never Unicode at all…
    """
    if not isinstance(text, unicode):
        raise TypeError("This isn't even decoded into Unicode yet. "
                        "Decode it first.")
    if len(text) == 0:
        return text

    maxord = max(ord(char) for char in text)
    tried_fixing = []
    if maxord < 128:
        # Hooray! It's ASCII!
        return text
    else:
        attempts = [(text, text_badness(text) + len(text))]
        if maxord < 256:
            tried_fixing = reinterpret_latin1_as_utf8(text)
            tried_fixing2 = reinterpret_latin1_as_windows1252(text)
            attempts.append((tried_fixing, text_cost(tried_fixing)))
            attempts.append((tried_fixing2, text_cost(tried_fixing2)))
        elif all(ord(char) in WINDOWS_1252_CODEPOINTS for char in text):
            tried_fixing = reinterpret_windows1252_as_utf8(text)
            attempts.append((tried_fixing, text_cost(tried_fixing)))
        else:
            # We can't imagine how this would be anything but valid text.
            return text

        # Sort the results by badness
        attempts.sort(key=lambda x: x[1])
        # print attempts
        goodtext = attempts[0][0]
        if goodtext == text:
            return goodtext
        else:
            return fix_bad_unicode(goodtext)


def reinterpret_latin1_as_utf8(wrongtext):
    newbytes = wrongtext.encode('latin-1', 'replace')
    return newbytes.decode('utf-8', 'replace')


def reinterpret_windows1252_as_utf8(wrongtext):
    altered_bytes = []
    for char in wrongtext:
        if ord(char) in WINDOWS_1252_GREMLINS:
            altered_bytes.append(char.encode('WINDOWS_1252'))
        else:
            altered_bytes.append(char.encode('latin-1', 'replace'))
    return ''.join(altered_bytes).decode('utf-8', 'replace')


def reinterpret_latin1_as_windows1252(wrongtext):
    """
    Maybe this was always meant to be in a single-byte encoding, and it
    makes the most sense in Windows-1252.
    """
    return wrongtext.encode('latin-1').decode('WINDOWS_1252', 'replace')


def text_badness(text):
    u'''
    Look for red flags that text is encoded incorrectly:

    Obvious problems:
    - The replacement character \ufffd, indicating a decoding error
    - Unassigned or private-use Unicode characters

    Very weird things:
    - Adjacent letters from two different scripts
    - Letters in scripts that are very rarely used on computers (and
      therefore, someone who is using them will probably get Unicode right)
    - Improbable control characters, such as 0x81

    Moderately weird things:
    - Improbable single-byte characters, such as ƒ or ¬
    - Letters in somewhat rare scripts
    '''
    assert isinstance(text, unicode)
    errors = 0
    very_weird_things = 0
    weird_things = 0
    prev_letter_script = None
    for pos in xrange(len(text)):
        char = text[pos]
        index = ord(char)
        if index < 256:
            # Deal quickly with the first 256 characters.
            weird_things += SINGLE_BYTE_WEIRDNESS[index]
            if SINGLE_BYTE_LETTERS[index]:
                prev_letter_script = 'latin'
            else:
                prev_letter_script = None
        else:
            category = unicodedata.category(char)
            if category == 'Co':
                # Unassigned or private use
                errors += 1
            elif index == 0xfffd:
                # Replacement character
                errors += 1
            elif index in WINDOWS_1252_GREMLINS:
                lowchar = char.encode('WINDOWS_1252').decode('latin-1')
                weird_things += SINGLE_BYTE_WEIRDNESS[ord(lowchar)] - 0.5

            if category.startswith('L'):
                # It's a letter. What kind of letter? This is typically found
                # in the first word of the letter's Unicode name.
                name = unicodedata.name(char)
                scriptname = name.split()[0]
                freq, script = SCRIPT_TABLE.get(scriptname, (0, 'other'))
                if prev_letter_script:
                    if script != prev_letter_script:
                        very_weird_things += 1
                    if freq == 1:
                        weird_things += 2
                    elif freq == 0:
                        very_weird_things += 1
                prev_letter_script = script
            else:
                prev_letter_script = None

    return 100 * errors + 10 * very_weird_things + weird_things


def text_cost(text):
    """
    Assign a cost function to the length plus weirdness of a text string.
    """
    return text_badness(text) + len(text)

#######################################################################
# The rest of this file is esoteric info about characters, scripts, and their
# frequencies.
#
# Start with an inventory of "gremlins", which are characters from all over
# Unicode that Windows has instead assigned to the control characters
# 0x80-0x9F. We might encounter them in their Unicode forms and have to figure
# out what they were originally.

WINDOWS_1252_GREMLINS = [
    # adapted from http://effbot.org/zone/unicode-gremlins.htm
    0x0152,  # LATIN CAPITAL LIGATURE OE
    0x0153,  # LATIN SMALL LIGATURE OE
    0x0160,  # LATIN CAPITAL LETTER S WITH CARON
    0x0161,  # LATIN SMALL LETTER S WITH CARON
    0x0178,  # LATIN CAPITAL LETTER Y WITH DIAERESIS
    0x017E,  # LATIN SMALL LETTER Z WITH CARON
    0x017D,  # LATIN CAPITAL LETTER Z WITH CARON
    0x0192,  # LATIN SMALL LETTER F WITH HOOK
    0x02C6,  # MODIFIER LETTER CIRCUMFLEX ACCENT
    0x02DC,  # SMALL TILDE
    0x2013,  # EN DASH
    0x2014,  # EM DASH
    0x201A,  # SINGLE LOW-9 QUOTATION MARK
    0x201C,  # LEFT DOUBLE QUOTATION MARK
    0x201D,  # RIGHT DOUBLE QUOTATION MARK
    0x201E,  # DOUBLE LOW-9 QUOTATION MARK
    0x2018,  # LEFT SINGLE QUOTATION MARK
    0x2019,  # RIGHT SINGLE QUOTATION MARK
    0x2020,  # DAGGER
    0x2021,  # DOUBLE DAGGER
    0x2022,  # BULLET
    0x2026,  # HORIZONTAL ELLIPSIS
    0x2030,  # PER MILLE SIGN
    0x2039,  # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    0x203A,  # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    0x20AC,  # EURO SIGN
    0x2122,  # TRADE MARK SIGN
]

# a list of Unicode characters that might appear in Windows-1252 text
WINDOWS_1252_CODEPOINTS = range(256) + WINDOWS_1252_GREMLINS

# Rank the characters typically represented by a single byte -- that is, in
# Latin-1 or Windows-1252 -- by how weird it would be to see them in running
# text.
#
#   0 = not weird at all
#   1 = rare punctuation or rare letter that someone could certainly
#       have a good reason to use. All Windows-1252 gremlins are at least
#       weirdness 1.
#   2 = things that probably don't appear next to letters or other
#       symbols, such as math or currency symbols
#   3 = obscure symbols that nobody would go out of their way to use
#       (includes symbols that were replaced in ISO-8859-15)
#   4 = why would you use this?
#   5 = unprintable control character
#
# The Portuguese letter Ã (0xc3) is marked as weird because it would usually
# appear in the middle of a word in actual Portuguese, and meanwhile it
# appears in the mis-encodings of many common characters.

SINGLE_BYTE_WEIRDNESS = (
#   0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 5,  # 0x00
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,  # 0x10
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0x20
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0x30
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0x40
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0x50
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0x60
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5,  # 0x70
    2, 5, 1, 4, 1, 1, 3, 3, 4, 3, 1, 1, 1, 5, 1, 5,  # 0x80
    5, 1, 1, 1, 1, 3, 1, 1, 4, 1, 1, 1, 1, 5, 1, 1,  # 0x90
    1, 0, 2, 2, 3, 2, 4, 2, 4, 2, 2, 0, 3, 1, 1, 4,  # 0xa0
    2, 2, 3, 3, 4, 3, 3, 2, 4, 4, 4, 0, 3, 3, 3, 0,  # 0xb0
    0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0xc0
    1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0,  # 0xd0
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0xe0
    1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0,  # 0xf0
)

# Pre-cache the Unicode data saying which of these first 256 characters are
# letters. We'll need it often.
SINGLE_BYTE_LETTERS = [
    unicodedata.category(unichr(i)).startswith('L')
    for i in xrange(256)
]

# A table telling us how to interpret the first word of a letter's Unicode
# name. The number indicates how frequently we expect this script to be used
# on computers. Many scripts not included here are assumed to have a frequency
# of "0" -- if you're going to write in Linear B using Unicode, you're
# you're probably aware enough of encoding issues to get it right.
#
# The lowercase name is a general category -- for example, Han characters and
# Hiragana characters are very frequently adjacent in Japanese, so they all go
# into category 'cjk'. Letters of different categories are assumed not to
# appear next to each other often.
SCRIPT_TABLE = {
    'LATIN': (3, 'latin'),
    'CJK': (2, 'cjk'),
    'ARABIC': (2, 'arabic'),
    'CYRILLIC': (2, 'cyrillic'),
    'GREEK': (2, 'greek'),
    'HEBREW': (2, 'hebrew'),
    'KATAKANA': (2, 'cjk'),
    'HIRAGANA': (2, 'cjk'),
    'HIRAGANA-KATAKANA': (2, 'cjk'),
    'HANGUL': (2, 'cjk'),
    'DEVANAGARI': (2, 'devanagari'),
    'THAI': (2, 'thai'),
    'FULLWIDTH': (2, 'cjk'),
    'MODIFIER': (2, None),
    'HALFWIDTH': (1, 'cjk'),
    'BENGALI': (1, 'bengali'),
    'LAO': (1, 'lao'),
    'KHMER': (1, 'khmer'),
    'TELUGU': (1, 'telugu'),
    'MALAYALAM': (1, 'malayalam'),
    'SINHALA': (1, 'sinhala'),
    'TAMIL': (1, 'tamil'),
    'GEORGIAN': (1, 'georgian'),
    'ARMENIAN': (1, 'armenian'),
    'KANNADA': (1, 'kannada'),  # mostly used for looks of disapproval
    'MASCULINE': (1, 'latin'),
    'FEMININE': (1, 'latin')
}


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
                resenha[RESENHA_TEXTO] = fix_bad_unicode(resenha[RESENHA_TEXTO])

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
