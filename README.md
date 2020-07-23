The goal of this project is to explore the network properties of T-cell repertoires.
# Code structure

```
net
├─ singleNet.py
├─ manyNets.py
├─ levenshtein.py
├─ jaccard.py
├─ funcDictionarySingleNet.py
├─ funcDictionaryManyNets.py
├─ funcDictionaryLevenshtein.py
├─ funcDictionaryJaccard.py
├─ funcDictionary.py
└─ plotData.py
```

This repository is still under construction and not yet finished. Please do not yet use it.

The files ```singleNet.py```, ```manyNets.py```, ```levenshtein.py```, ```jaccard.py``` perform network analysis and save corresponding results as ```.txt``` files. The use functions from dictionaries in the corresponding ```funcDictionarySingleNet.py```, ```funcDictionaryManyNets.py```, 
```funcDictionaryLevenshtein.py```, ```funcDictionaryJaccard.py```, ```funcDictionary.py```. The letter dictionary contains 
general functions, which are used by all of the for analysis script.

* ```singleNet.py``` analyzes a network that is based on the similarity characteristics of ```N``` TCR sequences, which we generated with the ```SONIA``` package.
* ```manyNets.py``` compares the network properties of networks.
* ```levenshtein.py``` analyzes the network properties in dependence of the maximum allowed Levenshtein distance for 
creating an edge between two nodes, where each node represents a DNA strain.
* ```jaccard.py```  does the same, but uses the jaccard distance.

<!--- <img src="https://render.githubusercontent.com/render/math?math=e^{i \pi} = -1"> --->

The files should be executed as follows: 

```
python singleNet.py
python manyNets.py
python levenshtein.py
python jaccard.py
```

The results are saved in the txt-directory. In order to plot the data and save the plots as ```.png``` files, you have to simply run:

```
python singleNetPlot.py
python manyNetsPlot.py
python levenshteinPlot.py
python jaccardPlot.py
```

# Related repositories
* https://github.com/statbiophys/SONIA
* https://github.com/rokroskar/imnet
