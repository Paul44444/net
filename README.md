The goal of this project is to explore the network properties of T-cell repertoires.
# code structure

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

The files singleNet.py, manyNets.py, levenshtein.py, jaccard.py perform network analysis and save them as txt files. 
The use functions from dictionaries in the corresponding funcDictionarySingleNet.py, funcDictionaryManyNets.py, 
funcDictionaryLevenshtein.py, funcDictionaryJaccard.py, funcDictionary.py. The letter dictionary contains 
general functions, which are used by all of the for analysis script.

The file singleNet.py analyses a network from a number N of DNA strains, generated with the SONIA package.
The file manyNets.py compares the network properties of Networks with different sizes N.
The file levenshtein.py analyses the network properties in dependence of the maximum allowed levenshtein distance for 
creating an edge between two nodes, where each node represents a DNA strain.
The file jaccard.py  does the same, but uses the jaccard distance.

<img src="https://render.githubusercontent.com/render/math?math=e^{i \pi} = -1">

![Image of Yaktocat](https://octodex.github.com/images/yaktocat.png)

```math
a^2+b^2=c^2
```

<img src="https://render.githubusercontent.com/render/math?math=(lev_{a, b}\left(i, j\right) = \left\{ \begin{array}{c} \max \left(i, j\right) \\ \min \left\{ \begin{array}{c}
lev_{a,b} \left(i-1, j\right) + 1\\
lev_{a,b} \left(i, j-1\right) + 1\\
lev_{a,b} \left(i-1, j-1\right) + 1_{\left(a_i \neq b_j\right)}
\end{array}
 \right.
 \end{array}
\right.)">
