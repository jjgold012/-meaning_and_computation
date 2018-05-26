import csv
import gensim
import scipy.stats as stats
import pprint

corpus = open('./corpus_ex2', encoding='iso-8859-1')
simlex_999 = csv.reader(open('./SimLex-999/SimLex-999.txt', encoding='us-ascii'), delimiter='\t')
headers = next(simlex_999)

pos_tags = set()
word_pairs = []
for row in simlex_999:
    pair = dict(zip(headers, row))
    word_pairs.append(pair)
    pos_tags.add(pair['POS'])


print(pos_tags)

sentences = []
cur_sent = []
for line in corpus:
    line = line.strip()
    # print(line)
    if line == '</s>':
        sentences.append(cur_sent)
        cur_sent = []
    elif line == '<s>' or line.startswith('<text'):
        continue
    else:
        cur_sent.append(line)

models = []
for window_size in [1, 5]: #TODO [1, 5]
    for dim in [10, 100, 1000]: #TODO [10, 100, 1000]
        print('blah' + str(window_size)+' '+ str(dim))
        model = gensim.models.Word2Vec(sentences, min_count=5,window=window_size,size=dim)
        models.append((model, (window_size, dim)))


for pair in word_pairs:
    for model in models:
        if pair['word1'] in model[0].wv.vocab.keys() and pair['word2'] in model[0].wv.vocab.keys():
            pair[str(model[1])] = model[0].similarity(pair['word1'], pair['word2'])
        else:
            pair[str(model[1])] = 0
correlation = {}

for model in models:
    model_correlation = {}
    a = [float(pair['SimLex999']) for pair in word_pairs]
    b = [pair[str(model[1])] for pair in word_pairs]
    rho, p = stats.spearmanr(a, b)

    model_correlation['all'] = rho
    for tag in pos_tags:
        pairs = [p for p in word_pairs if p['POS'] == tag]
        a = [float(pair['SimLex999']) for pair in pairs]
        b = [pair[str(model[1])] for pair in pairs]
        rho, p = stats.spearmanr(a, b)
        model_correlation[tag] = rho
    correlation[str(model[1])] = model_correlation

pprint.pprint(word_pairs)
pprint.pprint(correlation)