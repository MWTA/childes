# -*- coding: utf-8 -*-

'''
    Github: https://github.com/myint/language-check
'''

import os
import logging
import language_check

logging.basicConfig(filename='grammar_check.txt',
                    filemode='a',
                    format='%(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

dir_all_dataset = '/home/rodriguesfas/Mestrado/workspace/specana.prototype/dataset/corpora/childes/data/eng-uk/'


tool = language_check.LanguageTool('en-US')

def load_raw_data(path):
    data_temp = []

    with open(path) as document:
        for sentence in document:
            data_temp.append(sentence.strip())

    return data_temp

def check_sentence(cont, sentence):  
    valid = False

    try:
        matches = tool.check(sentence)
        suggestions = language_check.correct(sentence, matches)

        if sentence != suggestions:
            logging.info('{} - Sentence: {}'.format(cont, sentence))
            logging.info('{} - Suggestion: {} \n'.format(cont, suggestions))

            print '{} - Sentence: {}'.format(cont, sentence)
            print '{} - Suggestion: {}'.format(cont, suggestions)
    except Exception as err:
        logging.error('{} - Sentence: {}'.format(cont, sentence))
        print err

if __name__ == '__main__':
    print 'Processing..'

    cont = 0
    for index, dataset in enumerate(os.listdir(dir_all_dataset)):

        logging.info('======================================================')
        logging.info('> Processing dataset {}: {}'.format(index, dataset))

        raw_data = load_raw_data(dir_all_dataset + dataset + '/' + dataset.lower() + '_dataset_all_speaks_chi.txt')

        for sentence in raw_data:
            cont +=1
            check_sentence(cont, sentence)