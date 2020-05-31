# make a network based on amino acid sequences

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

# customized settings
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

aPre = list()
a4Pre = list()
lPre = list() # the length of each array

index = 0
indexMax = 10000

GPre = nx.Graph()
degreesPre = list()
clustersizesPre = list()

aPost = list()
a4Post = list()
lPost = list() # the length of each array
GPost = nx.Graph()
degreesPost = list()
clustersizesPost = list()

def near(str1, str2):
        isNear = 0
        difCount = 0

        if len(str1) == len(str2):
                for i in range(len(str1)):
                        if not (str1[i] == str2[i]):
                                difCount += 1
                if difCount < 10:
                        isNear = 1
        return isNear


with open('pre.txt') as f:
        for line in f.readlines():
                if index < indexMax:
                        aPre.append(line.split('\t'))
                        a4Pre.append(aPre[index][3].replace('\n', ''))          # info: attach the fourth element  to a4
                        lPre.append(len(a4Pre[index]))
                        GPre.add_node(index)

                        for i in range(index):
                                if near(a4Pre[i], a4Pre[index]) > 0:
                                        GPre.add_edge(i, index)

                        index = index + 1
                        if index%100 == 0:
                                print("\n index: ", index)

for index in range(indexMax):
        degreesPre.append(GPre.degree(index))
        if index%100 == 0:
                print("\n degree: ", degreesPre[index])

for el in list(nx.connected_components(GPre)):
        clustersizesPre.append(len(el))
        if len(el) > 1:
                print("\n elLen: ", len(el))

index = 0
with open('post.txt') as f:
        for line in f.readlines():
                if index < indexMax:
                        aPost.append(line.split('\t'))
                        a4Post.append(aPost[index][3].replace('\n', ''))                # info: attach the fourth element  to a4
                        lPost.append(len(a4Post[index]))
                        GPost.add_node(index)

                        for i in range(index):
                                if near(a4Post[i], a4Post[index]) > 0:
                                        GPost.add_edge(i, index)

                        index = index + 1
                        if index%100 == 0:
                                print("\n index: ", index)

for index in range(indexMax):
        degreesPost.append(GPost.degree(index))
        if index%100 == 0:
                print("\n degree: ", degreesPost[index])

for el in list(nx.connected_components(GPost)):
        clustersizesPost.append(len(el))
        if len(el) > 1:
                print("\n elLen: ", len(el))

alphaVal = 0.5

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()
ax1.hist(lPre, bins = (max(lPre)-min(lPre)), alpha = alphaVal)
ax1.hist(lPost, bins = (max(lPost)-min(lPost)), alpha = alphaVal)
ax2.hist(degreesPre, bins = (max(degreesPre)-min(degreesPre)), alpha = alphaVal, density = True)
ax2.hist(degreesPost, bins = (max(degreesPost)-min(degreesPost)), alpha = alphaVal, density = True)
ax3.hist(clustersizesPre, bins = (max(clustersizesPre)-min(clustersizesPre)), alpha = alphaVal)
ax3.hist(clustersizesPost, bins = (max(clustersizesPost)-min(clustersizesPost)), alpha = alphaVal)

ax1.set_xlim(min([min(lPre), min(lPost)]), max([max(lPre), max(lPost)]))
ax2.set_xlim(min([min(degreesPre), min(degreesPost)]), max([max(degreesPre), max(degreesPost)]))
ax3.set_xlim(min([min(clustersizesPre), min(clustersizesPost)]), max([max(clustersizesPre), max(clustersizesPost)]))
#ax2.set_xlim(min(degreesPre), max(lPre))
#ax3.set_xlim(min(lPre), max(lPre))

ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_xlim(10**0, 10**2)

fig1.savefig('histl.png', dpi=300, box_inches="tight")
fig2.savefig('histdegrees.png', dpi=300, box_inches="tight")
fig3.savefig('histclustersizes.png', dpi=300, box_inches="tight")

plt.show()
