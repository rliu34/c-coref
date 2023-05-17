# c-coref
An attempt to improve NeuralCoref clustering through the use of c-command rules. 

## Files
- `recoref.py` the primary source code for our implementation. 
- `recoref-test.py` a test suite for our recoref functions. 
- `coref-test.py` the same test suite but for NeuralCoref, without our re-scoring. 
- `test_reco.py` a file used for debugging and exploring recoref.py. 
- `test_sp.py` a file used for exploring the StatParser function. 

## Environment 
This was run in a Python 3.8.12 virtual environment in an Anaconda prompt, conda version 23.3.1. 
Uses: 
- spacy 2.3.9
- nltk 3.8.1
- neuralcoref 4.0 (manual install) 
- pyStatParser 0.0.1 (manual install) 

NeuralCoref required the following steps for install:
```
git clone https://github.com/huggingface/neuralcoref.git
cd neuralcoref
pip install -r requirements.txt
pip install -e .
```

We installed spacy's English model as well:
```
python -m spacy download en
```

pyStatParser was installed with the following lines: 
```
git clone https://github.com/emilmont/pyStatParser.git
cd pyStatParser
python setup.py install --user
```

## Execution 
`recoref-test.py` runs a number of test cases for our recoref functions. `coref-test.py` can be run to compare its performance to NeuralCoref alone. 

`test_reco.py` and `test_sp.py` were used for debugging and seeing outputs. The input strings can be changed as desired, though the string in `test_sp.py` should just be one sentence. 

