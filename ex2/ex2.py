f = open(filename) sentences = [] cur_sent = []
for line in f:
    line = line.strip() if line == '</s>':
    sentences.append(cur_sent)
cur_sent = []
elif line == '<s>' or line.startswith('<text'):
continue else:
cur_sent.append(line)
model = gensim.models.Word2Vec(sentences, min_count=5,window=5,size=100)
