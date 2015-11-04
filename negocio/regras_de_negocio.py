# -*- coding: utf-8 -*-

import re
from nltk.stem.snowball import PortugueseStemmer
from util.arquivo_util import ArquivoUtil
from unicodedata import normalize
from dominio.entidades import Documento
import sys


# REVISADO EM 14-09-2015


class Command(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding("utf-8")
        
        self.EMOTICON_FELIZ = "EMOTICON_FELIZ"
        self.EMOTICON_TRISTE = "EMOTICON_TRISTE"
        self.SITE_LINK = "SITE_LINK"
        self.SIMBOLO_MONETARIO = "SIMBOLO_MONETARIO"
        self.NAO_ = "NÃO_"
        
        # Atributo com todas as notacoes
        self.NOTACOES = [self.EMOTICON_FELIZ, self.EMOTICON_TRISTE,
                         self.SITE_LINK, self.SIMBOLO_MONETARIO,
                         self.NAO_]

    def execute(self, documento):
        raise NotImplementedError()
    

class CorrigeAbreviacaoContracaoCommand(Command):
    """Documentar
    """
    def execute(self, documento):
        texto_documento = documento.texto
        
        # Substitui 'c/' por 'com'
        # 'flags=re.I' para operação ser case INsensitive
        texto_documento = re.sub(r'c/', u' com ', texto_documento, flags=re.I)
        
        # Substitui 'p/', 'pra' e 'p' por 'para'
        texto_documento = re.sub(r'p/|\spra\s|\sp\s', u' para ', texto_documento, flags=re.I)
        
        # Substitui 'tbm' e 'tb' por 'também'
        texto_documento = re.sub(r'tbm|tb|tbem', u' também ', texto_documento, flags=re.I)
        
        # Substitui 'vcs' e 'vc' por 'você'
        texto_documento = re.sub(r'vcs|vc', u' você ', texto_documento, flags=re.I)
        
        # Substitui 'q' por 'que'
        texto_documento = re.sub(r'\sq\s', u' que ', texto_documento, flags=re.I)
        
        # Substitui 'dq' por 'do que'
        texto_documento = re.sub(r'\sdq\s', u' do que ', texto_documento, flags=re.I)
        
        # Substitui 'prq' e 'pq' por 'porque'
        texto_documento = re.sub(r'prq|pq', u' porque ', texto_documento, flags=re.I)
        
        # Substitui 'n' e 'ñ' por 'não'
        texto_documento = re.sub(ur'\sn\s|\sñ\s', u' não ', texto_documento, flags=re.I)
        
        # Substitui 'qr' por 'quer'
        texto_documento = re.sub(r'\sqr\s', u' quer ', texto_documento, flags=re.I)
        
        # Substitui 'dsd' por 'desde'
        texto_documento = re.sub(r'\sdsd\s', u' desde ', texto_documento, flags=re.I)
        
        # Substitui 'qdo' por 'quando'
        texto_documento = re.sub(r'\sqdo\s', u' quando ', texto_documento, flags=re.I)
        
        # Substitui 'd' por 'de'
        texto_documento = re.sub(r'\sd\s', u' de ', texto_documento, flags=re.I)
        
        # Substitui 'hj' por 'hoje'
        texto_documento = re.sub(r'\shj\s', u' hoje ', texto_documento, flags=re.I)
        
        # Substitui 'ctz' por 'certeza'
        texto_documento = re.sub(r'\sctz\s', u' certeza ', texto_documento, flags=re.I)
        
        # Substitui 'ngm' por 'ninguém'
        texto_documento = re.sub(r'\sngm\s', u' ninguém ', texto_documento, flags=re.I)
        
        # Substitui 'tava' por 'estava'
        texto_documento = re.sub(r'\stava\s', u' estava ', texto_documento, flags=re.I)

        # Substitui 'pres' por 'presidente'
        texto_documento = re.sub(r'\spres\s', u' presidente ', texto_documento, flags=re.I)

        # Substitui 'mto' por 'muito'
        texto_documento = re.sub(r'\smto\s', u' muito ', texto_documento, flags=re.I)

        # Extende a abreviação da ofensa
        texto_documento = re.sub(r'\sfdp\s|\sfdps\s', u' filha da puta ', texto_documento, flags=re.I)

        # Atualiza o texto do documento, pelo texto processado.
        documento.texto = texto_documento
        
        # Retorna o documento processado
        return documento
        

class CorrigeRisadaCommand(Command):
    """Documentar
    """
    def execute(self, documento):
        # Reduz 'kkkkkk' ou 'kkkkshsha' ou ainda 'KKKKKashu' para 'kkk'
        documento.texto = re.sub(r'[kK]{2,}[^\W\d_]*', 'kkk', documento.texto)
        return documento
        

class ProcessaEmoticonsCommand(Command):
    def execute(self, documento):
        """Substitui emoticons por notações que indicam a emoção
        representada pelo emoticon.
        
        emoticons felizes ~~> :-) :) :] :3 :> =] 8) =) :}
                              :D 8D xD XD =-D =D ;) *-*
        notação: EMOTICON_FELIZ
        
                                 
        emoticons tristes ~~> :-( :( :[ 3: :< =[ 8( =( :{
                              D: D8 Dx DX D-= D= ;(
        notação: EMOTICON_TRISTE
        """
        emoticons_feliz = [":-)", ":)", ":]", ":3", ":>", "=]", "8)", "=)", ":}",
                           ":D", "8D", "xD", "XD", "=-D", "=D", ";)", "*-*"]

        emoticons_triste = [":-(", ":(", ":[", "3:", ":<", "=[", "8(", "=(", ":{",
                            "D:", "D8", "Dx", "DX", "D-=", "D=", ";("]

        emoticons_feliz = [re.escape(emoticon) for emoticon in emoticons_feliz]
        emoticons_triste = [re.escape(emoticon) for emoticon in emoticons_triste]

        padrao_emoticons_feliz = "|".join(emoticons_feliz)
        padrao_emoticons_triste = "|".join(emoticons_triste)
        
        # Substitui os emoticons feliz por 'EMOTICON_FELIZ'
        documento.texto = re.sub(padrao_emoticons_feliz, self.EMOTICON_FELIZ, documento.texto)
        
        # Substitui os emoticons triste por 'EMOTICON_TRISTE'
        documento.texto = re.sub(padrao_emoticons_triste, self.EMOTICON_TRISTE, documento.texto)
        
        return documento
        

class StemmerCommand(Command):
    """Documentar
    """
    def execute(self, documento):
        stemmer = PortugueseStemmer()
        palavras_processadas = []  # Lista com as raizes de todas as palavras do documento
        stoplist = ArquivoUtil().get_stoplist()

        for palavra in documento.texto.split():

            # print " +++ palavra = %s" % palavra

            resultado = self.remover_pontuacao_palavra(palavra)
            palavra_sem_pontuacao = resultado[0]
            pontuacoes_antecedentes = resultado[1]
            pontuacoes_posteriores = resultado[2]

            palavras_processadas.append(pontuacoes_antecedentes)

            # Se todas as letras da palavras estão em caixa alta,
            # ou se a palavra é uma stopword.
            if palavra_sem_pontuacao.isupper() or palavra_sem_pontuacao.lower() in stoplist:
                palavras_processadas.append(palavra_sem_pontuacao)  # A palavra não passa pelo stemmer
                palavras_processadas.append(pontuacoes_posteriores)
                continue

            is_notacao = False  # Indica se a palavra contém alguma das notações adotadas nos textos
            # Se a palavra contém alguma das notações adotadas no texto.
            for notacao in self.NOTACOES:
                if notacao in palavra_sem_pontuacao:
                    palavras_processadas.append(palavra_sem_pontuacao)  # A palavra permanece inalterada
                    palavras_processadas.append(pontuacoes_posteriores)
                    is_notacao = True
                    break

            if is_notacao is True:
                continue  # Próxima iteração

            # A palavra passa pelo stemmer
            palavras_processadas.append(stemmer.stem(palavra_sem_pontuacao))
            palavras_processadas.append(pontuacoes_posteriores)

        # Une todos os stems em uma única string, separando-os por um espaço em branco
        documento_processado = Documento(" ".join(palavras_processadas), documento.categoria,
                                         documento.corpus_pertencente, documento.nome)
        
        return documento_processado

    @staticmethod
    def remover_pontuacao_palavra(palavra):
        # sinais_pontuacao = (',', '.', ';', ':', '(', ')', '[', ']', '"', "'", "“" "”")
        sinais_pontuacao = ("'", '"', '!', '#', '£', '%', '¢', '¨', '¬', '&', '*', '(', ')', '=',
                            '+', "\\", '\|', '\[', '\{', '\]', '\}', ',', '<', '.', '>', ';', ':',
                            '\/', '?', u'“', u'”', u'–', u'‘', u'’', u'…', '^', '~')

        pontuacoes_antecedentes = ""
        pontuacoes_posteriores = ""

        palavra_sem_pontuacao = palavra

        for i in reversed(range(0, len(palavra))):
            if len(palavra_sem_pontuacao) == 1:
                    break
            if palavra_sem_pontuacao[-1] in sinais_pontuacao:
                pontuacoes_posteriores += palavra[i]
                palavra_sem_pontuacao = palavra_sem_pontuacao[:-1]
            else:
                break

        # Coloca as pontuações posteriores na ordem correta
        # Exemplo: brilham!),
        #   'pontuacoes_posteriores' sem correção: ',)!'
        #   'pontuacoes_posteriores' corrigida: '!),'
        pontuacoes_posteriores = pontuacoes_posteriores[::-1]

        for i in range(0, len(palavra_sem_pontuacao)):
            if len(palavra_sem_pontuacao) == 1:
                break
            if palavra_sem_pontuacao[0] in sinais_pontuacao:
                pontuacoes_antecedentes += palavra[i]
                palavra_sem_pontuacao = palavra_sem_pontuacao[1:]
            else:
                break

        return [palavra_sem_pontuacao, pontuacoes_antecedentes, pontuacoes_posteriores]


class RemoveEspacosExtraCommand(Command):
    """Documentar
    """
    def execute(self, documento):
        # Remove espacos em branco desnecessarios
        documento.texto = re.sub(r'[\s]+', ' ', documento.texto)
        
        # Remove caracteres espaço do começo e do final do documento
        documento.texto = documento.texto.strip()
        
        return documento
        

class DivideCamelCaseCommand(Command):
    """Divide todas as ocorrências de camelCase de um documento.
    
    'BrasilPotenciaGlobal' é convertido para 'Brasil Potencia Global'
    'brasilPotenciaGlobal' é convertido para 'brasil Potencia Global'
    
    ---
    É obrigatório passar pela remoção de pontuação antes
    de dividir os camelCases. Caso o documento tenha uma
    notação como as abaixo:
    
        '#BrasilPotenciaGlobal'
        '@BrasilPotenciaGlobal'
        'BrasilPotenciaGlobal.'
    
    onde o camelCase inicia com um caractere '#' ou '@',
    ou ainda, é terminado por um '.',
    ocorrerá problemas ao tentar substituir as palavras
    separadas pelo camelCase inicial.
    """
    def execute(self, documento):
        # Detecta todas as ocorrências de camelCase no documento
        camel_cases = re.findall(r'[A-Za-z]+[A-Z][a-z]+[A-Z]*', documento.texto)
        # print "-- camel_cases = %s" % camel_cases

        # Para cada ocorrencia de camelCase encontrada
        for camel_case in camel_cases:
            # Separa cada uma das palavras de camel_case ~> ['Camel', 'Case']
            matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', camel_case)
            palavras_separadas = [m.group(0) for m in matches]

            # print 'palavras_separadas = ', palavras_separadas

            correcao_camel_case = " ".join(palavras_separadas)

            # print 'correcao_camel_case = %s' % correcao_camel_case

            documento.texto = re.sub(camel_case, correcao_camel_case, documento.texto)

        return documento
        

class RomoveAcentuacaoCommand(Command):
    """Remove acentuação das palavras do documento.
    
    Entrada:
        'A oposição queria recessão para solucionar a crise.'
        
    Saída:
        'A oposicao queria recessao para solucionar a crise.'
    """
    def execute(self, documento):
        return normalize('NFKD', documento.texto.decode('utf-8')).encode('ASCII', 'ignore')
        

class PadronizaLinksCommand(Command):
    """Documentar
    """
    def execute(self, documento):
        """Substitui links --> www.* ou https?://*
        pela notação 'SITE_LINK', que serve para indicar
        que o documento continha links para outros sites.
        """
        # documento.texto = re.sub(ur'www\.[^\s]+|https?://[^\s]+|https?[\s…\.]+', self.SITE_LINK, documento.texto)
        documento.texto = re.sub(ur'www\.[^\s]+|https?://[^\s]+', self.SITE_LINK, documento.texto)

        return documento
        

class RemoveNomeUsuarioCommand(Command):
    """Documentar
    """
    def execute(self, documento):
        # Remove nome dos @usuarios presentes em tweets
        documento.texto = re.sub(r'@[^\s]+', ' ', documento.texto)
        
        return documento


class RemoveEmailCommand(Command):
    """Documentar
    """
    def execute(self, documento):
        # Remove emails presentes no texto do documento
        documento.texto = re.sub(r'[^\s]+@[^\s]+', ' ', documento.texto)

        return documento


class RemoveNumerosCommand(Command):
    """Documentar
    """
    def execute(self, documento):
        # Remove números do documento
        documento.texto = re.sub(r'[0-9]+', '', documento.texto)
        
        return documento
        

class RemoveRTCommand(Command):
    """Documentar
    """
    def execute(self, documento):
        # Remove rt (retweet)
        documento.texto = re.sub(r'\sRT\s', '', documento.texto, flags=re.I)
        
        return documento
        

class RemoveStopwordsCommand(Command):
    """Documentar
    """
    def execute(self, documento):
        stoplist = ArquivoUtil().get_stoplist()
        palavras_documento = documento.texto.split()
        
        # Cria uma lista com todas as palavras que não são stopwords
        palavras_mantidas = [palavra for palavra in palavras_documento if palavra.lower() not in stoplist]
        
        # Une todas as palavras em uma única string, separanda-as por um espaço em branco,
        # Substituindo o antigo texto, pelo texto processado.
        documento.texto = " ".join(palavras_mantidas)
        
        return documento
        

class PadronizaSimboloMonetarioCommand(Command):
    """Os símbolos monetários [R$, US$] são substituídos
    pela string 'SIMBOLO_MONETARIO'
    """
    def execute(self, documento):
        documento.texto = re.sub(r'R\$', " " + self.SIMBOLO_MONETARIO + " ", documento.texto, flags=re.I)
        documento.texto = re.sub(r'US\$', " " + self.SIMBOLO_MONETARIO + " ", documento.texto, flags=re.I)
        
        return documento
        

class RemovePontuacaoCommand(Command):
    """Subtitui alguns dos símbolos de pontuação do documento por um espaço em branco.
    Preserva os caractéres '$', '@'
    
    Mantém traços e underlines em nomes compostos como:
        guarda-chuva
        GUARDA-CHUVA
        guarda_chuva
    
    nos demais casos, os traços e underlines são substituídos
    por um espaço em branco.
    """
    def execute(self, documento):
        padrao_simbolos = ur'[\'\"\!\#\£\%\¢\¨\¬\&\*\(\)\=\+\§\\\|\[\{\ª\]\}\º\,\<\.\>\;\:\/\?\°\“\”\–\‘\’\…\^\~]+'
        documento.texto = re.sub(padrao_simbolos, ' ', documento.texto)
        
        padrao_tracos = r'[\d\W\_]+[\-\_][\d\W\_]*|[\d\W\_]*[\-\_][\d\W\_]+'
        documento.texto = re.sub(padrao_tracos, ' ', documento.texto)
        
        return documento
        

class ConverteLowerCaseCommand(Command):
    def execute(self, documento):
        """Recebe um documento e o retorna com todas as letras de suas
        palavras em caixa baixa, porém mantém inalteradas as palavras
        escritas com todas as letras em caixa alta.
        """
        palavras_doc_processado = []

        for palavra in documento.texto.split():
            # Se todas as letras da palavra estão em caixa alta.
            if palavra.isupper():
                palavras_doc_processado.append(palavra)  # A palavra permanece inalterada
                continue

            is_notacao = False  # Indica a palavra contém alguma das notações adotadas nos textos
            # Se a palavra contém alguma das notações adotadas no texto.
            for notacao in self.NOTACOES:
                if notacao in palavra:
                    palavras_doc_processado.append(palavra)  # A palavra permanece inalterada
                    is_notacao = True
                    break

            if is_notacao:
                continue  # Próxima iteração

            # Caso contrário, todas as letras da palavra são convertidas
            # para caixa baixa.
            palavras_doc_processado.append(palavra.lower())

        # Atualiza o texto do documento, pelo texto processado.
        documento.texto = " ".join(palavras_doc_processado)
        
        return documento
        

class ProcessaNegacaoCommand(Command):
    def execute(self, documento):
        """Documentar
        entrada:
             'Também, não poderia ser diferente: muitos foram os dias e noites em
             que passei lendo sobre as aventuras de Mestre Frodo Bolseiro e Samwise Gamgee.'
             
        saída:
             'Também, não NÃO_poderia NÃO_ser NÃO_diferente: muitos foram os dias e noites em
             que passei lendo sobre as aventuras de Mestre Frodo Bolseiro e Samwise Gamgee.'
        """
        indicadores_negacao = ['não', 'nao', 'nem', 'nunca', 'jamais']
        # sinais_pontuacao = (',', '.', ';', ':', '(', ')', '[', ']', '"', "'", "“" "”")
        sinais_pontuacao = ("'", '"', '!', '#', '£', '%', '¢', '¨', '¬', '&', '*', '(', ')', '=',
                            '+', "\\", '\|', '\[', '\{', '\]', '\}', ',', '<', '.', '>', ';', ':',
                            '\/', '?', u'“', u'”', u'–', u'‘', u'’', u'…', '^', '~')

        texto_processado = ""

        # O prefixo de negação "NÃO_", é anexado em todas as palavras que
        # seguem um indicador de negação. Ao encontrar algum sinal de pontuação,
        # o prefixo deixa de ser anexado nas palavras seguintes.
        encontrou_negacao = False
        for palavra in documento.texto.split():

            # Evita problemas como: NÃO_"segredos
            # Onde há um sinal de pontuação entre
            # a notação 'NÃO' e a palavra 'segredos'
            if encontrou_negacao:
                if palavra == 'e':
                    texto_processado += " " + palavra
                    encontrou_negacao = False
                    continue

                # Verifica se a palavra é iniciada por um sinal de pontuação
                #   Exemplo: "Autor
                if palavra.startswith(sinais_pontuacao):
                    palavra_processada = ""
                    # Indica se o caractere é a primeira letra da palavra,
                    # uma vez que as palavras podem esta acompanhadas de
                    # sinais de pontuação.
                    is_primeira_letra = False
                    for caractere in palavra:
                        if caractere in sinais_pontuacao:  # Se o caractere é um sinal de pontuação
                            palavra_processada += caractere
                            is_primeira_letra = True
                        else:
                            if is_primeira_letra:
                                palavra_processada += self.NAO_ + caractere
                                is_primeira_letra = False
                            else:
                                palavra_processada += caractere

                    texto_processado += " " + palavra_processada
                else:
                    texto_processado += " " + self.NAO_ + palavra

                # Indica que o prefixo de negação não será anexado na próxima palavra
                #    Exemplo: Eu não gosto de pecar e estou cansado de pecar.
                # O 'e' na frase desfaz a negação.
                if palavra.endswith(sinais_pontuacao) or palavra == 'e':
                    encontrou_negacao = False
                continue  # Próxima iteração
            # Se a palavra é um indicador de negação, e
            # não é seguida por um sinal de pontuação.
            elif palavra.lower() in indicadores_negacao:
                encontrou_negacao = True

            texto_processado += " " + palavra

        # Atualiza o texto do documento pelo texto processado.
        documento.texto = texto_processado

        # Retorna o documento processado.
        return documento
