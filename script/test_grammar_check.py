# -*- coding: utf-8 -*-

'''
    Gituhb: https://github.com/myint/language-check
'''

import os
import logging
import grammar_check

logging.basicConfig(filename='grammar_check.txt',
                    filemode='a',
                    format='%(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

dir_all_dataset = '/home/rodriguesfas/Mestrado/workspace/specana.prototype/dataset/corpora/childes/data/eng-uk/'

tool = grammar_check.LanguageTool('en-UK')


def load_raw_data(path):
    data_temp = []

    with open(path) as document:
        for sentence in document:
            data_temp.append(sentence.strip())

    return data_temp

def check_sentence(cont, sentence):
    '''
    '''
    try:
            # Automatically apply suggestions to the text.
            matches = tool.check(sentence)
            suggestions = grammar_check.correct(sentence, matches)
            print cont, sentence

            if sentence != suggestions:
                logging.info('Sentence: {}'.format(sentence))
                logging.info('Suggestion: {} \n'.format(suggestions))
    except Exception as err:
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
