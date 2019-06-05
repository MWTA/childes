# -*- coding: utf-8 -*-

"""
    File: extraction_sentences.py
    Description: Processing dataset childes.
    Create: 27/06/2018
    Contact: <franciscosouzaacer@gmail.com>
"""

import os
import nltk
import logging
import language_check
from nltk.corpus.reader import CHILDESCorpusReader
from nltk.tokenize import word_tokenize


logging.basicConfig(filename='grammar_check.txt',
                    filemode='a',
                    format='%(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

dir_all_dataset = '/home/rodriguesfas/Mestrado/workspace/specana.prototype/dataset/corpora/childes/data/eng-uk/'

tokens_limit = 5
age_child_limit = '3'

tool = language_check.LanguageTool('en-US')


def check_sentence(sentence):
    try:
        matches = tool.check(sentence)
        suggestions = language_check.correct(sentence, matches)

        if sentence != suggestions:
            logging.info('Sentence: {}'.format(sentence))
            logging.info('Suggestion: {} \n'.format(suggestions))

            # print 'Sentence: {}'.format(sentence)
            # print 'Suggestion: {}'.format(suggestions)

            return suggestions
    except Exception as err:
        logging.error('Sentence: {}'.format(sentence))
        print err
        return sentence


def to_treat_bigram(word_tokenize):
    '''
        remove special underline character from bigrama
        remover caractere especial underline do bigrama.
    '''
    filtered_sentence = []

    for word in word_tokenize:
        word = word.replace('_', ' ')
        filtered_sentence.append(word)

    return ' '.join(filtered_sentence)


def remove_stops_words(word_tokens):
    '''
        Remove inconvenient words.
        Remover palavras inconvenientes.
    '''
    stops_words = [
        'xxx', 'Xxx', 'www', 'mm', 'chi', 'fam', 'neo',
        'b', 'B', 'c', 'C', 'd', 'D', 'f', 'F', 'g', 'G', 'h', 'H', 'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'p', 'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T', 'v', 'V', 'x', 'X', 'z', 'Z', 'w', 'W', 'y', 'Y',
        ':',
    ]

    filtered_sentence = []

    for word in word_tokens:
        if word not in stops_words:
            filtered_sentence.append(word)

    return ' '.join(filtered_sentence)


def spellchecker(word_tokens):
    '''
        Correct wrong words.
        Corrige palavras erradas.

        Lib.: https://github.com/barrust/pyspellchecker
    '''
    from spellchecker import SpellChecker

    spell = SpellChecker(
        language='en', local_dictionary='/home/rodriguesfas/Mestrado/workspace/specana.prototype/assets/src/resource/en.json.gz')
    misspelled = spell.unknown(word_tokens)

    for word in misspelled:
        print 'word: {} , correction: {}'.format(word, spell.correction(word))


def extraction_sentences():
    '''
        Processes all datasets individually by children.
        Processa o todos os datasets individualmente por crianças.
    '''

    # lists all directories (dataset).
    for index, dataset in enumerate(os.listdir(dir_all_dataset)):
        print '======================================================'
        path_dataset = dir_all_dataset + dataset
        print '> Dataset {} : {} \n'.format(index, dataset)

        # lists all subdirectories (children).
        for dir_child in os.listdir(path_dataset):
            # check if it's a directory.
            if os.path.isdir(os.path.join(path_dataset, dir_child)):
                print '>> Child:', dir_child

                '''
                    Read all .XML files by extracting only child's speech and saving in a new .TXT file.
                    Ler todos os arquivos .XML extraindo somente a fala da criança e salva em um novo arquivo .TXT .
                '''
                path_files_xml = path_dataset + '/' + dir_child + '/xml'
                corpus_root = nltk.data.find(path_files_xml)
                ccr = CHILDESCorpusReader(corpus_root, '/.*.xml')

                file_speaks_child = open(
                    path_dataset + '/' + dir_child + '/' + dir_child.lower() + '_speaks_chi.txt', 'w')

                for file_xml in os.listdir(path_files_xml):
                    if file_xml.endswith('.xml'):
                        age = ccr.age(file_xml)  # get age child.
                        age = str(age)  # coverte em string

                        if age != '[None]':  # check age is None.
                            # model age: P 2Y 4M 9D | P 1Y 11M 29D
                            new_age = []

                            # out = P-1Y-1M-29D-
                            for ch in str(age):
                                new_age.append(ch)
                                if ch.isalpha():
                                    new_age.append('-')

                            new_age = ''.join(new_age)  # split.
                            # clear.
                            new_age = new_age.replace('[', '').replace(']', '').replace("'", '')

                            # separa as cadeias
                            P, Y = new_age.split('-', 1)

                            if Y[0] == age_child_limit:  # check age child is >= age_child_limit
                                sentences = ccr.sents(
                                    file_xml, speaker=['CHI'])

                                for sentence in sentences:
                                    try:
                                        file_speaks_child.write(
                                            str(" ".join(sentence) + '\n'))
                                    except:
                                        file_speaks_child.write(
                                            str(" ".join(sentence).encode('utf-8') + '\n'))

                file_speaks_child.close()

                print '>> Extracted child speech: ' + dir_child.lower() + '_speaks_chi.txt'

                '''
                    Create a new file with the sentences that have five or more tokens.
                    Crie um novo arquivo com as frases que tenham cinco ou mais tokens.
                '''
                if dir_child != 'xml':
                    list_sentences_temp = []

                    file_input = dir_child.lower() + '_speaks_chi.txt'
                    file_output = dir_child.lower() + '_speaks_chi_selected.txt'

                    with open(path_dataset + '/' + dir_child + '/' + file_input) as document:
                        for line in document:
                            sentence = to_treat_bigram(line.split())
                            sentence = remove_stops_words(sentence.split())
                            sentence = check_sentence(sentence)
                            # spellchecker(sentence.split())

                            if sentence != '' and sentence != None and len(sentence.split()) >= tokens_limit:
                                # Add ponto final nas sentenças e salva em uma lista temporária.
                                list_sentences_temp.append(sentence.capitalize() + '.')

                    # Remove sentenças repetidas.
                    list_sentences_temp = set(list_sentences_temp)

                    # Salva as sentenças selecionadas.
                    file_speaks_child_selected = open(path_dataset + '/' + dir_child + '/' + file_output, 'w')  # a+
                    for sent in list_sentences_temp:
                        file_speaks_child_selected.write(str(sent) + '\n')
                    file_speaks_child_selected.close()

                    print '>> Selected child speech: ' + dir_child.lower() + '_speaks_chi_selected.txt'

                print ''

        print ''


def join_speeches_dataset():
    '''
        Joins all of a participant's speeches into a new dataset.
        Junta todas as falas das crianças em um novo dataset.
    '''

    for index, dataset in enumerate(os.listdir(dir_all_dataset)):
        path_dataset = dir_all_dataset + dataset

        file_output = dataset.lower() + '_dataset_all_speaks_chi.txt'
        temp_file_out = open(path_dataset + '/' + file_output, 'w')

        for dir_child in os.listdir(path_dataset):
            file_input = dir_child.lower() + '_speaks_chi_selected.txt'

            if os.path.isdir(os.path.join(path_dataset, dir_child)):
                with open(path_dataset + '/' + dir_child + '/' + file_input) as file:
                    for line in file:
                        temp_file_out.write(line)

        temp_file_out.close()

        print '> {} Join all speeches {} : {}'.format(
            index, dataset, dataset.lower() + '_dataset_all_speaks_chi.txt')


if __name__ == '__main__':
    print 'Begin processing dataset!\n'

    extraction_sentences()
    join_speeches_dataset()

    print 'END processing!'
