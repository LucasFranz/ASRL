#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 12:34:31 2015

@author: lucas
"""
import os
import shutil
import codecs


class ClassificacaoManual(object):
    
    def __init__(self, flg_revisao=False):
        self.dir_raiz = ""
        self.dir_positivo = ""
        self.dir_negativo = ""
        self.dir_neutro = ""
        self.dir_sem_classificacao = ""
        
        self.rotulo_correto = 'c'
        self.rotulo_positivo = 'p'
        self.rotulo_negativo = 'n'
        self.rotulo_neutro = 't'
        self.rotulo_revisado = self.rotulo_correto
        self.apagar_tweet = 'q'
        self.sair = 'sair'
        
        self.flg_revisao = flg_revisao
        
        # Estilos de escrita para utilizar no terminal (cores, negrito).
        self.AZUL = '\033[94m'
        self.VERDE = '\033[92m'
        self.VERMELHO = '\033[91m'
        self.ENDC = '\033[0m'
        self.NEGRITO = '\033[1m'
    
    
    def _mover_tweet(self, tweet, classificacao_usuario):
        
        classificacao_usuario = classificacao_usuario.lower()
        
        if classificacao_usuario == self.rotulo_positivo:
            shutil.move(tweet, self.dir_positivo)
        elif classificacao_usuario == self.rotulo_negativo:
            shutil.move(tweet, self.dir_negativo)
        elif classificacao_usuario == self.rotulo_neutro:
            shutil.move(tweet, self.dir_neutro)
        elif classificacao_usuario == self.apagar_tweet:
            os.remove(tweet)
        else:
            print 'Opção inválida.\n'
            return False
        
        return True
    
    
    def ler_tweets(self):
        if self.flg_revisao:            
            """Lista o nome de todos os tweets positivos."""
            if self.rotulo_revisado.startswith('pos'):
                nome_tweets = os.listdir(self.dir_positivo)
                dir_tweets = self.dir_positivo
                
            elif self.rotulo_revisado.startswith('neg'):
                nome_tweets = os.listdir(self.dir_negativo)
                dir_tweets = self.dir_negativo
                
            elif self.rotulo_revisado.startswith('neu'):
                nome_tweets = os.listdir(self.dir_neutro)
                dir_tweets = self.dir_neutro
        else:  # Não é revisão
            nome_tweets = os.listdir(self.dir_sem_classificacao)
            dir_tweets = self.dir_sem_classificacao
        
        
        # salva apenas o nome dos arquivos de tweets que serão revisados
        tweets = [dir_tweets + nome_tweet for nome_tweet in nome_tweets if nome_tweet.endswith('.txt')]
        
        return tweets
        
    
    def classificar_tweets(self, tweets):        
        # Lê todos os tweets
        for tweet in tweets:
            
            with codecs.open(tweet, 'r', 'utf-8') as f:
                tweet_texto = f.read()
            
            # Executa comando 'clear' no terminal do linux
            os.system('clear')
            
            print tweet, '\n'  # Nome do tweet com o seu diretorio
            print self.NEGRITO + tweet_texto + self.ENDC, '\n'  # Conteúdo do tweet
            
            if self.flg_revisao:
                menu = ("[c] = correto, ler próximo tweet\n"
                        "[p] = positivo\n"
                        "[n] = negativo\n"
                        "[t] = neutro\n"
                        "[q] = apagar tweet\n"
                        "[sair] = sair\n\n"
                        "Digite sua classificação: ")
            else:
                menu = ("[p] = positivo\n"
                        "[n] = negativo\n"
                        "[t] = neutro\n"
                        "[q] = apagar tweet\n"
                        "[sair] = sair\n\n"
                        "Digite sua classificação: ")
            
            classificacao_usuario = raw_input(menu)
            
            if classificacao_usuario.lower() == self.rotulo_correto:
                continue  # Próximo tweet
            elif classificacao_usuario.lower() == self.sair:
                print 'Saindo ...'
                return
            
            # Move o tweet de diretório
            if self._mover_tweet(tweet, classificacao_usuario) == False:
                return
        
        # Fim da revisão
        print ('Todos os tweets já foram apresentados.\n'
               'Classificação concluída.\n')
        return True
        
    
    def ler_diretorio_raiz(self):
        self.dir_raiz = raw_input("Diretório raiz: ")
        
        # Anexa uma barra ao final, caso o usuário não a tenha digitado
        if not self.dir_raiz.endswith('/'):
            self.dir_raiz = self.dir_raiz + '/'
        
        
        self.dir_positivo = self.dir_raiz + "pos/"
        self.dir_negativo = self.dir_raiz + "neg/"
        self.dir_neutro = self.dir_raiz + "neu/"
        self.dir_sem_classificacao = self.dir_raiz + "sem_classificacao/"
        
        if self.flg_revisao:
            self.rotulo_revisado = raw_input("[pos] = revisar tweets positivos\n"
                                             "[neg] = revisar tweets negativos\n"
                                             "[neu] = revisar tweets neutros\n\n"
                                             "Digite sua classificação: ")
        
        return True
        

if __name__ == '__main__':
    opcao_usuario = raw_input("[r] = revisão\n"
                              "[c] = classificação\n\n"
                              "Escolha a operação: ")
    if opcao_usuario.lower() == 'r':
        classificao = ClassificacaoManual(flg_revisao=True)
    elif opcao_usuario.lower() == 'c':
        classificao = ClassificacaoManual()
    
    classificao.ler_diretorio_raiz()
    tweets = classificao.ler_tweets()
    classificao.classificar_tweets(tweets)
