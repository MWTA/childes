# -*- coding: utf-8 -*-
"""
    Software: Statistics Dataset
    Description: Generates some statistics from the processed dataset.
    Date: 27/06/2018
    Author: RodriguesFAS
    Contact: <franciscosouzaacer@gmail.com>
"""

import os
import nltk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib import style

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize

''' 
    Path of the parent directory containing all datasets to be processed.
    Caminho do diretório principal que contem todos os datasets a serem processados.
'''
dir_all_dataset = '/home/rodriguesfas/Mestrado/workspace/specana.prototype/dataset/corpora/childes/data/eng-uk/'

def loar_data(path):
    '''
        Loard dataset.
        Carrega o dataset.
    '''
    data_temp = []

    if os.path.isfile(path): # check file exists.
        with open(path) as file:
            for sentence in file:
                sentence = sentence.replace('.', '') # remove pontuaction.
                data_temp.append(sentence) 
            return data_temp


def average_sentences(dataset):
    '''
        Calculates the average size of the phrase by number of tokens.
        Calcula o tamanho médio das frase por número de tokens.

        @param dataset
        @return number of tokens.
    '''
    t_tokens = total_tokens(dataset)
    t_sentences = total_sentences(dataset)

    # verifica se os divisores são maiores que 0
    if t_tokens > 0 and t_sentences > 0:
        return t_tokens / t_sentences
    else:
        return 0 


def total_sentences(dataset):
    '''
        Calculate the number of sentences in the dataset.
        Calcular a quantidade de sentenças do dataset.

        @param dataset
        @return amount
    '''
    return len(dataset)


def total_tokens(dataset):
    '''
        Calculates the total number of tokens in the dataset.
        Calcula o total de tokens no dataset.

        @param dataset
        @return amount
    '''
    cont_tokens = 0

    for sentence in dataset:
        cont_tokens += len(word_tokenize(sentence))
    
    return cont_tokens


def list_tokens_sentences(dataset):
    '''
        Calcula o número de tokens por sentença.
    '''
    cont_tokens_sentence = []
    
    for sentence in dataset:
        cont_tokens_sentence.append(len(word_tokenize(sentence)))

    return cont_tokens_sentence


def pos_tag(dataset):
    '''
        Calculates the frequency number of tokens 'words' by grammar class 'POS'.
        Calcula o número de frequência de tokens 'palavras' por classe gramatical 'POS'.

        @param dataset
        @return 
    '''
    # [Alphabetical list of part-of-speech tags used in the Penn Treebank Project:](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html)
    data_temp = []

    for line in dataset:
        for word in nltk.pos_tag(word_tokenize(line)):
            # RB = "Adverb", JJ = "Adjective", VB = "Verb", NN = "Noun"
            if word[1] == 'RB' or word[1] == 'JJ' or word[1] == 'VB' or word[1] == 'NN':
                data_temp.append(word[1])
    
    return data_temp

def split_pos_tag(_dataset, _lemma=False):
    '''
        Calculates the frequency number of tokens per class, in different lists.
        Calcula o número de frequência de tokens por classes, em listas diferentes.

        @param
            _dataset
            _lemma

        @return
    '''
    rb_temp = []
    jj_temp = []
    vb_temp = []
    nn_temp = []
    outhers_temp = []
    all_temp = []
    
    for line in _dataset:
        
        if _lemma is False:
            words_tokens = word_tokenize(line)
        else:
            words_tokens = []
            lemmatizer = WordNetLemmatizer()

            for word in word_tokenize(line):
                if word.isalpha():
                    words_tokens.append(lemmatizer.lemmatize(word))

        for word in nltk.pos_tag(words_tokens):
            if word[0].isalpha():
                # RB = "Adverb", JJ = "Adjective", VB = "Verb", NN = "Noun"
                if word[1] == 'RB':
                    rb_temp.append(word[1]+'_lemma')
                elif word[1] == 'JJ':
                    jj_temp.append(word[1]+'_lemma')
                elif word[1] == 'VB':
                    vb_temp.append(word[1]+'_lemma')
                elif word[1] == 'NN':
                    nn_temp.append(word[1]+'_lemma')
                else:
                    outhers_temp.append('OUTHERS') # define identification all.
    
    return rb_temp, jj_temp, vb_temp, nn_temp, outhers_temp


def generate_file_statistics(path_out, dataset_name, res_as, res_ts, res_tt):
    '''
        Generates a file containing all the information in the dataset.
        Gera um arquivo contendo todas as informações do dataset.

        @param
            path_out, dataset_name, res_as, res_ts, res_tt

        @return
    '''
    file = open(path_out, 'w') # a+
    file.write("## Estátistica - Dataset {} ##" '\n'.format(dataset_name))
    file.write("1. Tamanho médio das frases em número de tokens: " +str(res_as) + '\n')
    file.write("2. Total de frases: " + str(res_ts) + '\n')
    file.write("3. Total de tokens: " + str(res_tt) + '\n')
    file.write("4. Gráfico de barra (distribuição de frequência) do número de tokens por frase.\n")
    file.write("5. Gráfico de barra (distribuição de frequência) do número de tokens por classe gramatical.\n")
    file.write("6. Gráfico de barra (distribuição de frequência) do número de tokens por classe gramatical com lemmas.")
    file.close()

def generate_graph_bar(_path_out, _data, _title, _sub_title, _xlabel, _ylabel, _legend=None, _bins=None, _save=True):
    '''
        Generate image or 'histogram' view based on processed data.
        Gera imagem ou visualização 'histograma' com base nos dados processados.

        @param
            _path_out, _data, _title, _sub_title, _xlabel, _ylabel, _legend=None, _bins=None, _save=True
        
        @return
            save image graphic
            view image graphic
    '''

    style.use('ggplot')

    if _bins is None:
        plt.hist(_data, label=_legend, histtype='bar' )
    else:
        plt.hist(_data, bins=_bins, label=_legend, histtype='bar')

    plt.xlabel(_xlabel)
    plt.ylabel(_ylabel)

    plt.title(_title)
    plt.suptitle(_sub_title)
    plt.legend()

    if _save is True:
        plt.savefig(_path_out, dpi=1200, bbox_inches='tight', format='svg')
        plt.close()
    else:
        plt.show()


if __name__ == '__main__':

    for index, dataset in enumerate(os.listdir(dir_all_dataset)):
        print '======================================================'
        print '> Estátistica Dataset {}: {}'.format(index, dataset)
        
        dataset_name = dataset
        
        path_dataset = dir_all_dataset + dataset
        path_file_out_statistics = path_dataset + '/' + dataset.lower() + '_dataset_all_speaks_chi_statistics.txt'

        path_out_hist_4_class = path_dataset + '/' + dataset.lower() + '_dataset_all_speaks_chi_hist_4_class_grammtical.svg'
        path_out_hist_4_class_lemmas = path_dataset + '/' + dataset.lower() + '_dataset_all_speaks_chi_hist_4_class_grammtical_lemmas.svg'

        path_file_out_hist_all_class = path_dataset + '/' + dataset.lower() + '_dataset_all_speaks_chi_hist_all_class_grammtical.svg'
        path_file_out_hist_all_class_lemmas = path_dataset + '/' + dataset.lower() + '_dataset_all_speaks_chi_hist_all_class_grammtical_lemmas.svg'
        
        path_file_out_hist_number_tokens_for_sentences = path_dataset + '/' + dataset.lower() + '_dataset_all_speaks_chi_hist_number_tokens_for_sentences.svg'

        dataset = loar_data(dir_all_dataset + dataset + '/' + dataset.lower() + '_dataset_all_speaks_chi.txt')

        if dataset:

            res_as = average_sentences(dataset)
            res_ts = total_sentences(dataset)
            res_tt = total_tokens(dataset)

            data_lts = list_tokens_sentences(dataset)

            print '>> 1. Tamanho médio das frases em numero de tokens:', res_as
            print '>> 2. Total de frases:', res_ts
            print '>> 3. Total de tokens:', res_tt
            print '>> 4. Grafico de barra (distribuição de frequência) do número de tokens por frase.'
            print '>> 5. Gráfico de barra (distribuição de frequência) do número de tokens por classe gramatical.'
            print '>> 6. Gráfico de barra (distribuição de frequência) do número de tokens por classe gramatical com Lemmas.\n'

            generate_file_statistics(path_file_out_statistics, dataset_name, res_as, res_ts, res_tt)

            rb_temp, jj_temp, vb_temp, nn_temp, outhers_temp  = split_pos_tag(dataset)
            rb_temp_lemma, jj_temp_lemma, vb_temp_lemma, nn_temp_lemma, outhers_temp_lemma  = split_pos_tag(dataset, True)

            # 4 class pos.
            generate_graph_bar(
                _path_out=path_out_hist_4_class,
                _data=[rb_temp, jj_temp, vb_temp, nn_temp], 
                _legend=['Adverb', 'Adjective', 'Verb', 'Noun'], 
                _title='Frequency of Tokens per Grammatical Class', 
                _sub_title='Dataset {}'.format(dataset_name),  
                _xlabel='Grammatical Class', 
                _ylabel='Words Frequency',
                _bins=4,
                )

            # 4 class pos + lemmas.
            generate_graph_bar(
                _path_out=path_out_hist_4_class_lemmas,
                _data=[rb_temp, rb_temp_lemma, jj_temp, jj_temp_lemma, vb_temp, vb_temp_lemma, nn_temp, nn_temp_lemma], 
                _legend=['Adverb', 'Adverb_lemma', 'Adjective', 'Adjective_lemma', 'Verb', 'Verb_lemma', 'Noun', 'Noun_lemma'], 
                _title='Frequency of Tokens per Grammatical Class',
                _sub_title='Dataset {}'.format(dataset_name),  
                _xlabel='Grammatical Class', 
                _ylabel='Words Frequency',
                _bins=8,
                )

            # all class pos.
            generate_graph_bar(
                _path_out=path_file_out_hist_all_class,
                _data=[rb_temp, jj_temp, vb_temp, nn_temp, outhers_temp], 
                _legend=['Adverb', 'Adjective', 'Verb', 'Noun', 'Outhers'], 
                _title='Frequency of Tokens per Grammatical Class', 
                _sub_title='Dataset {}'.format(dataset_name),  
                _xlabel='Grammatical Class', 
                _ylabel='Words Frequency',
                _bins=5,
                )

            # all class pos + lemmas.
            generate_graph_bar(
                _path_out=path_file_out_hist_all_class_lemmas,
                _data=[rb_temp, rb_temp_lemma, jj_temp, jj_temp_lemma, vb_temp, vb_temp_lemma, nn_temp, nn_temp_lemma, outhers_temp, outhers_temp_lemma], 
                _legend=['Adverb', 'Adverb_lemma', 'Adjective', 'Adjective_lemma', 'Verb', 'Verb_lemma', 'Noun', 'Noun_lemma', 'Outhers', 'Outhers_lemma'], 
                _title='Frequency of Tokens per Grammatical Class', 
                _sub_title='Dataset {}'.format(dataset_name),  
                _xlabel='Grammatical Class', 
                _ylabel='Words Frequency',
                _bins=10,
                )
            
            generate_graph_bar(
                _path_out=path_file_out_hist_number_tokens_for_sentences,
                _data=data_lts,
                _title='Number Tokens for Sentences', 
                _sub_title='Dataset {}'.format(dataset_name),  
                _xlabel="Tokens Quant.", 
                _ylabel='Sentence Frequency',
                _bins='auto',#range(min(data_lts), max(data_lts)),
                )

    print 'End processing!'
