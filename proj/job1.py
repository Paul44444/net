import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go

from scipy.optimize import curve_fit
from matplotlib import rcParams
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap
from collections import OrderedDict

import imnet
import pyspark
from imnet import random_strings as r
from imnet import process_strings as p

N = 1000
minL = 5 # 4
maxL = 6
min_ldVal = -1
max_ldVal = 2
#lets = 'ACDEFGHIKLMNPQRSTVWY'
lets = 'ACD'
seq = r.generate_random_sequences(N, minimum_length=minL, maximum_length=maxL, seed=1, letters=lets)
#print("\n seqs: ", list(seq))
print("\n generate graph ...")
GPre = p.generate_graph(seq, min_ld=min_ldVal, max_ld=max_ldVal)
print("\n finished;")
print("\n first GPre: ", GPre.number_of_nodes())
# make sc
#gsc = generate_spark_graph(seq, sc)

#degs = p.generate_degrees(seq, min_ld=1, max_ld=1, sc=None)

params = { #'backend': 'ps',
        #'font.family': 'serif',
        #'font.serif': 'Latin Modern Roman',
        'font.family': 'sans serif',
        'font.serif': 'Helvetica',
        'font.size': 10,
        'axes.labelsize': 'medium',
        'axes.titlesize': 'medium',
        'legend.fontsize': 'medium',
        'xtick.labelsize': 'small',
        'ytick.labelsize': 'small',
        'savefig.dpi': 15,
        'text.usetex': True
}

rcParams['axes.labelsize'] = 50
rcParams['xtick.labelsize'] = 46
rcParams['ytick.labelsize'] = 46
rcParams['legend.fontsize'] = 46
rcParams['font.family'] = 'sans serif'
rcParams['font.serif'] = ['Helvetica']
rcParams['text.usetex'] = True
rcParams['figure.figsize'] = 12, 8

# set nice figure sizes
fig_width_pt = 245    # Get this from LaTeX using \showthe\columnwidth
golden_mean = (np.sqrt(5.) - 1.) / 2.  # Aesthetic ratio
ratio = golden_mean
inches_per_pt = 1. / 72.27  # Convert pt to inches
fig_width = fig_width_pt * inches_per_pt  # width in inches
fig_height = fig_width*ratio  # height in inches
fig_size = [fig_width, fig_height]
rcParams.update({'figure.figsize': fig_size})

# tell matplotlib about your params
rcParams.update(params)

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()

aPre = list()
a4Pre = list()
lPre = list() # the length of each array

index = 0
indexMax = 10

#GPre = nx.Graph() - GPre is already defined before
degreesPre = list()
diameterPre = list()
eccentricityPre = list()
neighborsPre = list()

clustersizesPre = list()

aPost = list()
a4Post = list()
lPost = list() # the length of each array
GPost = nx.Graph()
degreesPost = list()
clustersizesPost = list()

nx.draw(GPre)

print("\n esgesGPre: ", GPre.number_of_edges())

#G = nx.Graph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
#G.add_path([0,1,2,3])
#G.degree(1)
print("\n GPre.number_of_nodes(): ", GPre.number_of_nodes())
print("\n GPre.degree: ", (GPre.degree()))
a = GPre.degree()
print("\n lista: ", list(a))
b = list(a)
c = list()
for i in range(len(b)):
	c.append(b[i][1]) # info: degree distribution

for i in range(GPre.number_of_nodes()):
	

ax1.hist(c)
#ax1.set_xlim()
#ax1.set_ylim()
ax1.set_xscale('log')
ax1.set_xlabel('degree')
ax1.set_ylabel('frequency')

"""
print("\n ecc: ", nx.eccentricity(GPre))
print("\n diameter: ", nx.diameter(GPre, nx.eccentricity(GPre)))
ns = list(GPre.neighbors('AAAAA'))
print("\n neighborsPre.append(GPre.neighbors(index)): ", ns[0])
print("\n degree_centrality: ", nx.degree_centrality(GPre))
"""

plt.show()
