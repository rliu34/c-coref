import spacy
import recoref
nlp = spacy.load("en_core_web_sm")

import neuralcoref

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

coref = neuralcoref.NeuralCoref(nlp.vocab)
nlp.add_pipe(coref, name='neuralcoref')

txt = 'John knows that he saw himself.'

doc = nlp(u'John knows that he saw himself.')

nc_scores = doc._.coref_scores
print(nc_scores)
print("Rescore:")

re_scores = recoref.rescore(nc_scores, txt)

print(re_scores)

print(cluster(re_scores))