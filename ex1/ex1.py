
word = 'bank'
seed_a = {'river': 0, 'right': 0}
seed_b = {'money': 0, 'loan': 0}

window_size = 2
file = open('./corpus_ex1').read()
words = file.split('\n')
indices = [i for i, x in enumerate(words) if x.lower() == word]
examples = [[words[i].lower() for i in range(index - window_size, index + (window_size + 1))] for index in indices]


sense_a_examples = []
sense_b_examples = []
unknown_examples = []

for e in examples:
    a = False
    b = False
    for k in seed_a.keys():
        if k in e:
            a = True

    for k in seed_b.keys():
        if k in e:
            b = True

    if a == b:
        unknown_examples.append(e)
    if a:
        print('blah')
    if b:
        print('blah')