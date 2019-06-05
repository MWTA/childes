# -*- coding: utf-8 -*-
"""
    Software: CHILDES Corpus Reader
    Description: 
    Date: 29/06/2018
    Author: RodriguesFAS
    Contact: <franciscosouzaacer@gmail.com>
    Tutorial: http://www.nltk.org/howto/childes.html 
              http://ling-blogs.bu.edu/lx390f17/standoff-annotation-xml-and-more-childes
              
"""
#%%
import nltk
from nltk.corpus.reader import CHILDESCorpusReader

corpus_root = nltk.data.find(
    '/home/rodriguesfas/Mestrado/workspace/specana.prototype/dataset/corpora/childes/data/eng-uk/Belfast/')

ccr = CHILDESCorpusReader(corpus_root, 'Barbara/.*.xml')

print ccr.fileids()

# Conte o número de arquivos.
print len(ccr.fileids())

# Imprimindo propriedades dos arquivos corpus.
corpus_data = ccr.corpus(ccr.fileids())
print(corpus_data[0]['Lang'])

for key in sorted(corpus_data[0].keys()):
    print(key, ": ", corpus_data[0][key])

# Imprimindo informações dos participantes do corpus. Os códigos mais comuns para os 
# participantes são 'CHI' (filho alvo), 'MOT' (mãe) e 'INV' (investigador).
corpus_participants = ccr.participants(ccr.fileids())

for this_corpus_participants in corpus_participants[:2]:
    for key in sorted(this_corpus_participants.keys()):
        dct = this_corpus_participants[key]
        print(key, ": ", [(k, dct[k]) for k in sorted(dct.keys())])


# printing words.
print ccr.words('Barbara/020409.xml')

# printing sentences.
print ccr.sents('Barbara/020409.xml')

# Você pode especificar os participantes com o argumento speaker.
print ccr.words('Barbara/020409.xml',speaker=['INV'])
print ccr.words('Barbara/020409.xml',speaker=['MOT'])
print ccr.words('Barbara/020409.xml',speaker=['CHI'])

# tagged_words () e tagged_sents () retornam as listas usuais de tuplas (word, pos). 
# As tags POS nos CHILDES são automaticamente atribuídas pelos programas MOR e POST (MacWhinney, 2000).
print ccr.tagged_words('Barbara/020409.xml')[:30]
print ccr.tagged_sents('Barbara/020409.xml')[:10]

# Quando o argumento stem é true, a palavra stems (por exemplo, 'is' -> 'be-3PS') 
# é usada como instrumental das palavras originais.
print ccr.words('Barbara/020409.xml')[:30]
print ccr.words('Barbara/020409.xml',stem=True)[:30]

# Quando o argumento replace é true, as palavras substituídas são usadas com base nas palavras originais.
print ccr.words('Barbara/020409.xml',speaker='CHI')[247]
print ccr.words('Barbara/020409.xml',speaker='CHI',replace=True)[247]

# Quando a relação de argumento é verdadeira, os relacionamentos relacionais na sentença 
# são retornados. Veja Sagae et al. (2010) para detalhes da estrutura relacional adotada 
# nas CRIANÇAS.
print ccr.words('Barbara/020409.xml',relation=True)[:10]

# Idade de impressão. Quando o mês do argumento é verdadeiro, as informações de idade no 
# formato CHILDES são convertidas no número de meses.
print ccr.age()
print ccr.age('Barbara/020409.xml')
print ccr.age('Barbara/020409.xml',month=True)

# Imprimindo MLU. Os critérios para o cálculo do MLU são amplamente baseados em Brown (1973).
print ccr.MLU()
print ccr.MLU('Barbara/020409.xml')

## Coisas básicas

# Conte o número de palavras e frases de cada arquivo.
ccr = CHILDESCorpusReader(corpus_root, 'Barbara/.*.xml')

for this_file in ccr.fileids()[:6]:
    print(ccr.corpus(this_file)[0]['Corpus'], ccr.corpus(this_file)[0]['Id'])
    print("num of words: %i" % len(ccr.words(this_file)))
    print("num of sents: %i" % len(ccr.sents(this_file)))