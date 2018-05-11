from nltk.corpus import wordnet
from nltk.corpus import wordnet_ic


class Tree(object):
    def __init__(self):
        self.children = []
        self.data = None

    def extract_words(self, root, words=None):
        if words is None:
            words = []
        words.append(root.data)
        children = root.children
        for child in children:
            self.extract_words(child, words)
        return words


def create_subtree(synset):
    root = Tree()
    root.data = synset
    hyponyms = root.data.hyponyms()
    for child in hyponyms:
        root.children.append(create_subtree(child))
    return root


def compute_similarity(words):
    semcor_ic = wordnet_ic.ic('ic-semcor.dat')
    lin_similarities_dict = {}
    path_similarities_dict = {}
    for i in range(len(words)):
        for j in range(i + 1, len(words), 1):
            key = words[i]._name.split(".")[0] + " - " + words[j]._name.split(".")[0]
            path_value = words[i].path_similarity(words[j])
            lin_value = words[i].lin_similarity(words[j], semcor_ic)
            path_similarities_dict[key] = path_value
            lin_similarities_dict[key] = lin_value
    factor = max(path_similarities_dict.values())
    for value in path_similarities_dict:
        path_similarities_dict[value] = path_similarities_dict[value] / factor
    factor = max(lin_similarities_dict.values())
    for value in lin_similarities_dict:
        lin_similarities_dict[value] = lin_similarities_dict[value] / factor
    return path_similarities_dict, lin_similarities_dict


if __name__ == '__main__':
    synset = wordnet.synsets("emotion")[0]
    tree = create_subtree(synset)
    all_words = tree.extract_words(tree)
    path_similarities, lin_similarities = compute_similarity(all_words)