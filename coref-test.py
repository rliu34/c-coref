import unittest
import spacy
import recoref
# nlp = spacy.load("en_core_web_sm")

import neuralcoref

class TestCorefMethods(unittest.TestCase):

# Condition C
    def test_condC_close(self):
        nlp = spacy.load("en_core_web_sm")

        coref = neuralcoref.NeuralCoref(nlp.vocab)
        nlp.add_pipe(coref, name='neuralcoref')
        sent = u"He saw John."
        doc = nlp(sent) 

        nc_scores = doc._.coref_scores
        res = recoref.clusters_to_str(recoref.cluster(nc_scores))
        print(res)
        self.assertTrue(["John"] in res and ["He"] in res)# he and john should be in separate clusters

    def test_condC_far(self):
        nlp = spacy.load("en_core_web_sm")

        coref = neuralcoref.NeuralCoref(nlp.vocab)
        nlp.add_pipe(coref, name='neuralcoref')
        sent = u"He knows that she saw John."
        doc = nlp(sent)

        nc_scores = doc._.coref_scores
        res = recoref.clusters_to_str(recoref.cluster(nc_scores))
        print(res)
        self.assertTrue(["John"] in res)# john in separate cluster
        
# Condition B

    def test_condB_close(self):
        nlp = spacy.load("en_core_web_sm")

        coref = neuralcoref.NeuralCoref(nlp.vocab)
        nlp.add_pipe(coref, name='neuralcoref')
        sent = u"She was very upset with her."
        doc = nlp(sent) 

        nc_scores = doc._.coref_scores
        res = recoref.clusters_to_str(recoref.cluster(nc_scores))
        print(res)
        self.assertTrue(["She"] in res and ["her"] in res)# she and her should be separate

    def test_condB_far(self):
        nlp = spacy.load("en_core_web_sm")

        coref = neuralcoref.NeuralCoref(nlp.vocab)
        nlp.add_pipe(coref, name='neuralcoref')
        sent = u"John knows that she saw him."
        doc = nlp(sent) 

        nc_scores = doc._.coref_scores
        res = recoref.clusters_to_str(recoref.cluster(nc_scores))
        print(res)
        self.assertTrue(["she", "him"] not in res and ["him", "she"] not in res)# she and him dont corefer

# Condition A
    def test_condA_close(self):
        nlp = spacy.load("en_core_web_sm")

        coref = neuralcoref.NeuralCoref(nlp.vocab)
        nlp.add_pipe(coref, name='neuralcoref')
        sent = u"John knows himself."
        doc = nlp(sent) 

        nc_scores = doc._.coref_scores
        res = recoref.clusters_to_str(recoref.cluster(nc_scores))
        print(res)
        self.assertTrue(["John", "himself"] in res or ["him", "John"] in res)# himself and john should be in same cluster

    def test_condA_far(self):
        nlp = spacy.load("en_core_web_sm")

        coref = neuralcoref.NeuralCoref(nlp.vocab)
        nlp.add_pipe(coref, name='neuralcoref')
        sent = u"John knows that she saw himself."
        doc = nlp(sent) 

        nc_scores = doc._.coref_scores
        res = recoref.clusters_to_str(recoref.cluster(nc_scores))
        print(res)
        self.assertTrue(["she", "himself"] in res or ["himself", "she"] in res)#she and himself in same cluster
        self.assertTrue(["John", "himself"] not in res and ["himself", "John"] not in res) # john in separate cluster from himself



if __name__ == '__main__':
    unittest.main()
