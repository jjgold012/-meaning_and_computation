import math
word = 'lead'
seeds_a = {'paint': 0, 'poisoning': 0}
seeds_b = {'country': 0, 'team': 0}
window_size = 2
file = open('./corpus_ex1').read()
words = file.split('\n')
# print(len([w for w in words if w.lower() == 'river']))
indices = [i for i, x in enumerate(words) if x.lower() == word]
examples = [(index,[words[i].lower() for i in range(index - window_size, index + (window_size + 1))]) for index in indices]


def add_to_collo(collo, example):
    for e in example:
        if word != e:
            collo[e] = 0



def tag_by_collo(examples, seeds_a, seeds_b):
    sense_a_examples = []
    sense_b_examples = []
    unknown_examples = []
    collo_a = seeds_a.copy()
    collo_b = seeds_b.copy()
    for e in examples:

        example = e[1]
        a = False
        b = False
        for seed_a in seeds_a.keys():
            if seed_a in example:
                a = True

        for seed_b in seeds_b.keys():
            if seed_b in example:
                b = True

        if a == b:
            unknown_examples.append(e)
        else:
            if a:
                sense_a_examples.append(e)
                add_to_collo(collo_a, example)
            if b:
                sense_b_examples.append(e)
                add_to_collo(collo_b, example)
    return collo_a, collo_b, sense_a_examples,sense_b_examples,unknown_examples



def count_for_collo(collo, examples):
    for e in examples:

        example = e[1]

        for c in collo.keys():
            if c in example:
                collo[c] += 1




collo_a, collo_b, sense_a_examples, sense_b_examples, unknown_examples = tag_by_collo(examples, seeds_a, seeds_b)




collo = collo_a.copy()
collo.update(collo_b)
count_for_collo(collo_a, sense_a_examples)
count_for_collo(collo_b, sense_b_examples)
count_for_collo(collo, examples)

rank_a = {}
rank_b = {}
for c in collo_a.keys():
    if c in collo_b.keys():
        rank_a[c] = math.log(float(collo_a[c])/float(collo_b[c]))
    else:
        rank_a[c] = math.inf

for c in collo_b.keys():
    if c in collo_a.keys():
        rank_b[c] = math.log(float(collo_b[c])/float(collo_a[c]))
    else:
        rank_b[c] = math.inf


print(len(unknown_examples))
print(len(sense_a_examples))
print(len(sense_b_examples))

print(len(collo_a))
print(len(collo_b))
print('number of appearances for collocation in taged sense for sense A:')
print(collo_a)
print('number of appearances for collocation in taged sense for sense B:')
print(collo_b)
print('collocation\'s ranking for sense A:')
print(sorted(rank_a.items(), key=lambda tup: tup[1], reverse=True))
print('collocation\'s ranking for sense B:')
print(sorted(rank_b.items(), key=lambda tup: tup[1], reverse=True))




