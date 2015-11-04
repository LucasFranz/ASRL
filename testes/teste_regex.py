# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 00:05:23 2015

@author: lucas
"""
import re

def remover_camel_case(tweet):
    # tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    regex_hash_tags = re.compile(r'#[^\s]+')  # Padrão para encontrar as hashtags dos tweets
    hash_tags = regex_hash_tags.findall(tweet)  # Lista com todas as hastags
    palavras_separadas = []  # [camel, Case]
    
    # Separa palavras escritas em camelCase ~> [camel, Case]
    for hash_tag in hash_tags:
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', hash_tag)
        palavras_separadas = [m.group(0) for m in matches]
        tweet = re.sub(hash_tag, ' '.join(palavras_separadas), tweet)
    
    return tweet
    
if __name__ == '__main__':
    print remover_camel_case('tweet #lucasFranz teste')