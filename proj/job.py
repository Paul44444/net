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

N = 10000
#minL = 5 # 4
#maxL = 6
min_ldVal = 0
max_ldVal = 1
extractNum = 18 #20
#lets = 'ACDEFGHIKLMNPQRSTVWY'
#lets = 'ACD'
#seq = r.generate_random_sequences(N, minimum_length=minL, maximum_length=maxL, seed=1, letters=lets)

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

cPre = list()
clustersizesPre = list()
GnamesHist1Pre = list()

cPost = list()
clustersizesPost = list()
GnamesHist1Post = list()

alphaVal = 0.5

for step in range(2):
	if step == 0:
		filename = 'pre.txt'
	if step == 1:
		filename = 'post.txt'

	index = 0
	a = list()
	a4 = list()
	seq = list()
	
	with open(filename) as f:
		for line in f.readlines():
			if index < N:
				a.append(line.split('\t'))
				a4.append(a[index][3].replace('\n', ''))                # info: attach the fourth element  to a4
				seq.append(a4[index][:extractNum])
				index += 1
	G = p.generate_graph(seq, min_ld=min_ldVal, max_ld=max_ldVal)
	# make sc
	#gsc = generate_spark_graph(seq, sc)
	
	degs = p.generate_degrees(seq, min_ld=1, max_ld=1, sc=None)

	index = 0
	indexMax = 10
	
	# info: make the degree distribution
	a = G.degree()
	b = list(a)
	c = list()
	for i in range(len(b)):
		c.append(b[i][1])
	
	# info: make the clusters, clustersizes
	clusters = list(nx.connected_components(G))
	print("\n list(clusters): ", list(clusters))
	clustersizes = list()
	for i in range(len(clusters)):
		clustersizes.append(len(clusters[i]))
	
	# info: make Gnames -> distribution of number of each strain
	Gnames = list(G)
	for i in range(len(Gnames)):
		j = 0
		while j < len(Gnames[i]):
			try:
				val = int(Gnames[i][j])
				Gnames[i] = Gnames[i][:j] + Gnames[i][(j+1):]
			except ValueError:
				print("")
				j += 1
	print("\n Gnames after loop: ", Gnames)
	
	GnamesHist = list()
	for i in range(len(Gnames)):
		isIn = 0
		for j in range(len(GnamesHist)):
			if GnamesHist[j][0] == Gnames[i]:
				GnamesHist[j][1] += 1
				isIn = 1
		if isIn == 0:
			GnamesHist.append([Gnames[i], 1])
	GnamesHist1 = list()
	for i in range(len(GnamesHist)):
		GnamesHist1.append(GnamesHist[i][1])
	
	if step == 0:
		cPre = c
		clustersizesPre = clustersizes
		GnamesHist1Pre = GnamesHist1
	if step == 1:
		cPost = c
		clustersizesPost = clustersizes
		GnamesHist1Post = GnamesHist1

text_file = open("cPre.txt", "w")
for i in range(len(cPre)):
        text_file.write(str("\n " + str(cPre[i])))
text_file.close()

text_file = open("cPost.txt", "w")
for i in range(len(cPost)):
        text_file.write(str("\n " + str(cPost[i])))
text_file.close()

text_file = open("clustersizesPre.txt", "w")
for i in range(len(clustersizesPre)):
        text_file.write(str("\n " + str(clustersizesPre[i])))
text_file.close()

text_file = open("clustersizesPost.txt", "w")
for i in range(len(clustersizesPost)):
        text_file.write(str("\n " + str(clustersizesPost[i])))
text_file.close()

text_file = open("GnamesHist1Pre.txt", "w")
for i in range(len(GnamesHist1Pre)):
        text_file.write(str("\n " + str(GnamesHist1Pre[i])))
text_file.close()

text_file = open("GnamesHist1Post.txt", "w")
for i in range(len(GnamesHist1Post)):
        text_file.write(str("\n " + str(GnamesHist1Post[i])))
text_file.close()

ax1.hist(cPre, bins = int(max(cPre) - min(cPre)), color='blue', alpha = alphaVal)
ax1.hist(cPost, bins = int(max(cPost) - min(cPost)), color='orange', alpha = alphaVal)
ax1.legend(['Pre selection', 'Post selection'])
#ax1.set_xlim()
#ax1.set_ylim()
ax1.set_xscale('log')
ax1.set_xlabel('degree')
ax1.set_ylabel('frequency')
ax1.set_xlim(1, N-1)
ax1.set_ylim(10**0, 200)
ax1.set_title('frequency distribution')

ax2.hist(clustersizesPre, bins = max(clustersizesPre) - min(clustersizesPre), color='blue', alpha = alphaVal)
ax2.hist(clustersizesPost, bins = max(clustersizesPost) - min(clustersizesPost), color='orange', alpha = alphaVal)
ax2.legend(['Pre selection', 'Post selection'])
print("\n clustersizes: ", clustersizes)
ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_xlabel('cluster size')
ax2.set_ylabel('frequency')
#ax2.set_xlim(1, N-1)
#ax2.set_ylim(0, max(len(clustersizesPre), len(clustersizesPost)))
ax2.set_title('clustersizes')

#print("\n (max(GnamesHist1) - min(GnamesHist1)): ",  (max(GnamesHist1) - min(GnamesHist1)))
#print("\n GnamesHist1: ", GnamesHist1)
ax3.hist(GnamesHist1Pre, bins = (max(GnamesHist1Pre) - min(GnamesHist1Pre)), color='blue', alpha = alphaVal)
ax3.hist(GnamesHist1Post, bins = (max(GnamesHist1Post) - min(GnamesHist1Post)), color='orange', alpha = alphaVal)
ax3.legend(['Pre selection', 'Post selection'])
#ax3.set_xscale()
#ax3.set_yscale()
ax3.set_title('GnamesHist')
ax3.set_xscale('log')
ax3.set_yscale('log')

fig1.savefig('degreesDist.png', dpi=300,  bbox_inches="tight")
fig2.savefig('clustersizes.png', dpi=300, bbox_inches="tight")
fig3.savefig('GnamesHist.png', dpi=300, bbox_inches="tight")

plt.show()
