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

The files ```singleNet.py```, ```manyNets.py```, ```levenshtein.py```, ```jaccard.py``` perform network analysis and save corresponding results as ```.txt``` files. These files use functions from dictionaries in the corresponding files ```funcDictionarySingleNet.py```, ```funcDictionaryManyNets.py```, 
```funcDictionaryLevenshtein.py```, ```funcDictionaryJaccard.py```, ```funcDictionary.py```. The file ```funcDictionary.py``` contains 
general functions, which are used in all our analyses.

* ```singleNet.py``` calls all network analysis functions that we use to study networks that are based on the Levensthein distance between ```N``` TCR sequences, which we generated with the ```SONIA``` package.
* ```manyNets.py``` also calls network analysis functions as ```singleNet.py```, but for multiple networks.
* ```levenshtein.py``` computes network properties for different Levenshtein-distance thresholds that determine when an edge between two nodes (i.e., unique TCR-receptor sequences) is established.
* ```jaccard.py```  does the same as ```levenshtein.py```, but uses the Jaccard distance metric instead.

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
