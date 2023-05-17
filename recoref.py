from stat_parser import Parser, display_tree
import nltk

def c_command(tree, word1, word2): 
    """Determine whether a pair of references c-command one or the other in a sentence. Assumes these words are not repeated.
    arguments:
        sentence - string. The sentence in question. 
        word1 - string. The first word. 
        word2 - string. The second word.

    returns: 
        True if the first c-commands the second
        False otherwise"""

    parent1 = tree[word_parent(tree, word1)]
    # path2 = word_path(tree, word1) 

    # a node c-commands another if the other node is a child of
    # the first node's immediate ancestor
    return word2 in parent1.leaves() or word2.lower() in parent1.leaves()

# def index_tree(tree):
#     idx = 0 
#     for path in tree.treepositions():
#         # make sure type is not str (leaf)
#         if isinstance(tree[path], str):
#             tree[path].set_value()
#             if word in tree[path].leaves():
                
#                 paths.append(path)
#                 lens.append(len(path))

def contains_phrase(tree, words): 
    """Return True if the tree or subtree contains the word(s)."""
    if not ' ' in words: 
        return words in tree.leaves() or words.lower() in tree.leaves()
    else: # multiple words
        treephrase = ' '.join(tree.leaves()).lower()
        phrase = words.lower()
        return phrase in treephrase

def word_path(tree, word): 
    """Return the path of the word."""
    # print("word_path")
    #print(word)
    paths = []
    lens = []
    for path in tree.treepositions():
        # make sure type is not str (leaf)
        if isinstance(tree[path], nltk.tree.tree.Tree):
            if contains_phrase(tree[path], word):
                # print(path)
                paths.append(path)
                lens.append(len(path))

    #print("--")
    # find longest path, which should be the word's path 
    path = paths[lens.index(max(lens))]
    return path


def word_parent(tree, word): 
    """Return the path of the closest ancestor of the word that has more than one child."""
    path = word_path(tree, word)
    chs = len(tree[path])
    # traverse upwards from path to word 
    while chs < 2: 
        path = path[:-1] 
        chs = len(tree[path])
        # print(chs)
    # print(word)
    # print("Parent: " + tree[path].label())
    return path 

# def word_core(tree, word): 
#     """Return the path of the first ancestor of the word that has only one child."""
#     path = word_path(tree, word)
#     chs = len(tree[path])
#     # traverse upwards from path to word 
#     while chs < 2 and len(path) > 1: 
#         prev = path
#         path = path[:-1] 
#         chs = len(tree[path])

#     return prev 

def is_pronoun(tree, word): 
    path = word_path(tree, word)
    pos = tree[path].label() 
    pronoun_labels = ["PRP"]

    return pos in pronoun_labels

def is_reflexive(tree, word):
    """Checks if the word is a reflexive pronoun."""
    if ' ' not in word:
        return is_pronoun(tree, word) and ("self" in word) 
    return False

def close_cc(tree, word1, word2):
    """Check if word1 closely c-commands word2."""
    # print("close_cc")
    
    # if not c-commanded, return False 
    if not c_command(tree, word1, word2): 
        # print("not c-commanded")
        return False 
    
    parent1 = word_parent(tree, word1)
    parent2 = word_parent(tree, word2)

    # grandparent of word2 
    gp2 = parent2[:-1]

    # if grandparent of word2 is parent of the word1, return True
    if gp2 == parent1: 
        return True
    
    path2 = word_path(tree, word2)

    parent1 = word_parent(tree, word1)

    lbl = tree[parent1].label()
    # print("Parent1: " + lbl)
    trace2 = path2 
    par = trace2[:-1]
    while par != parent1: 
        lbl = tree[trace2].label()
        # print(lbl)
        if 'SBAR' in lbl: 
            return False 
        trace2 = trace2[:-1]
        par = trace2[:-1]
    # print("close")
    return True




def condC(tree, word1, word2): 
    """Checks Condition C: An R-expression(proper noun or named object) cannot be bound by something which c-commands it. Return False if the condition is violated."""
    # print("condC")
    # if word1 is a pronoun but not word2 
    if (is_pronoun(tree, word1) and not is_pronoun(tree, word2)):  
        # print("word1 is a pronoun but not word2")
        # return False if word1 c-commands word2
        return not c_command(tree, word1, word2)
    
    # if word2 is a pronoun but not word1
    if (not is_pronoun(tree, word1) and is_pronoun(tree, word2)):  
        # print("word2 is a pronoun but not word1")
        # return False if word2 c-commands word1
        return not c_command(tree, word2, word1)

    return True

def condB(tree, word1, word2): 
    """Checks Condition B: Pronouns cannot be closely c-commanded. Return False if the condition is violated."""
    # print("condB")
    # if word1 is a pronoun, not reflexive
    if is_pronoun(tree, word1) and not is_reflexive(tree, word1):  
        # if closely c-commanded by word2, return False
        return not close_cc(tree, word2, word1)
    
    # if word2 is a pronoun, not reflexive
    if is_pronoun(tree, word2) and not is_reflexive(tree, word2):  
        # if closely c-commanded by word1, return False
        return not close_cc(tree, word1, word2)

    return True

def condA(tree, word1, word2):
    """Condition A: Anaphors (reflexive pronouns) must be closely c-commanded. Return -1 if the condition is violated, 0 if irrelevant, 1 if condition is met."""
    # print("condA")
    if is_reflexive(tree, word1): 
        # word1 must c-command word2
        if close_cc(tree, word2, word1):
            return 1
        else:
            return -1
    
    if is_reflexive(tree, word2): 
        # word2 must c-command word1
        if close_cc(tree, word1, word2):
            return 1
        else:
            return -1

    return 0

def remove_phrases(nc_scores): 
    """Remove phrases of more than two words from the score dictionary."""
    new_dict = {}
    for word1_tok in nc_scores.keys():
        if len(str(word1_tok).split(' ')) <= 2:
            new_dict[word1_tok] = {}
            for word2_tok in nc_scores[word1_tok].keys(): 
                if len(str(word2_tok).split(' ')) <= 2:
                    new_dict[word1_tok][word2_tok] = nc_scores[word1_tok][word2_tok]

    return new_dict

def rescore(nc_scores, txt): 
    """Modify NeuralCoref scores based on c-command rules. Assumes the text does not have repeat words. 
    arguments:
        nc_scores - dictionary. the original NeuralCoref scores. 
        txt - string. The original string text. 

    returns: 
        rescores - the new scores, in the same format as the original NeuralCoref scores. Forbidden pairings will have -1000 set as the score."""
    
    sents = nltk.sent_tokenize(txt)
    # print(sents)

    clean_scores = remove_phrases(nc_scores)
    
    for sent in sents: 
        parser = Parser()
        tree = parser.parse(sent)
        for word1_tok in clean_scores.keys():
            word1 = str(word1_tok)
            # print("word1: " + word1)
            if word1 in sent: 
                for word2_tok in clean_scores[word1_tok].keys(): 
                    word2 = str(word2_tok)
                    # print("word2: " + word2)
                    if word2 in sent and (word1 != word2): 
                        # if any condition is violated 
                        if not (condC(tree, word1, word2) and condB(tree, word1, word2)):
                            clean_scores[word1_tok][word2_tok] = -1000
                        if condA(tree, word1, word2) == 1: 
                            clean_scores[word1_tok][word2_tok] = 1000

    return clean_scores

def cluster(scores):
    #choose the highest likelihood coreference
    clusters = []

    for entity in scores:
        max_score = float("-inf")
        curr_score = 0
        for i,cluster in enumerate(clusters):
            for val in cluster:
                curr_score += scores[entity][val]
            if curr_score > max_score:
                max_score = curr_score
                max_index = i
        if scores[entity][entity] > max_score:
            clusters.append([entity])
        else:
            clusters[max_index].append(entity)



    return clusters

def clusters_to_str(clusters): 
    """Typecase clusters of spacy tokens to str."""

    for i in range(len(clusters)):
        for j in range(len(clusters[i])):
            clusters[i][j] = str(clusters[i][j])

    return clusters
