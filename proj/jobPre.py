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

#Ns = [10**2, 2*10**2, 3*10**2, 4*10**2, 5*10**2, 6*10**2, 7*10**2, 8*10**2, 9*10**2, 10**3, 2*10**3, 3*10**3, 5*10**3, 10**4, 5*10**4]

#Ns = [10**2, 2*10**2, 3*10**2, 4*10**2, 5*10**2, 6*10**2, 7*10**2, 8*10**2, 9*10**2, 10**3, 2*10**3]
Ns = [10**2, 2*10**2, 3*10**2, 4*10**2, 5*10**2, 6*10**2, 7*10**2, 8*10**2, 9*10**2, 10**3]

consPre = list() # probability that everything is connected
consPost = list()
eccsPre = list() # info: list of eccentricities
diasPre = list() # info: list of dias
eccsPost = list() # info: list of eccentricities
diasPost = list() # info: list of dias
degMaxsPre = list()
degMaxsPost = list()
nodesPre = list()
nodesPost = list()
isConnectedsPre = list()
isConnectedsPost = list()

extractNum = 18#18 #6

clustersizesMaxPre = list()
clustersizesMaxPost = list()

samples = 2# usually: 6

maxValIndices = [6]

for maxValIndex in range(len(maxValIndices)):
	maxVal = maxValIndices[maxValIndex]
	
	for sample in range(samples):
		print("\n sample/samples: ", (sample+1), "/ ", samples, "; maxValIndex: ", maxValIndex+1, "/ ", len(maxValIndices))
		for step in range(2):
			eccs = list()
			dias = list()
			degMaxs = list()
			cons = list()
			nodes = list()
			clustersizesMax = list()	
			isConnected = list()
			
			for i in range(len(Ns)):
				N = Ns[i]
				minL = 5 # 4
				maxL = 10
				min_ldVal = -1
				max_ldVal = maxVal
				#lets = 'ACDEFGHIKLMNPQRSTVWY'
				lets = 'ACD'
			
				index = 0
				a = list()
				a4 = list()
				seq = list()
				
				lPre = list() # the length of each array
				
				if step == 0:
					filename = 'pre.txt'
				if step == 1:
					filename = 'post.txt'
				with open(filename) as f:
					for line in f.readlines():
						if index < N:
							a.append(line.split('\t'))
							a4.append(a[index][3].replace('\n', ''))                # info: attach the fourth element  to a4
							seq.append(a4[index][0:extractNum])
							#print("\n seq[index]: ", seq[index])
							index += 1
				#print("\n seq: ", list(seq))
				#print("\n generating graph ...")	
				G = p.generate_graph(seq, min_ld=min_ldVal, max_ld=max_ldVal)
				#print("\n list(G): ", list(G))
				#print("\n graph generated.")
				#degs = p.generate_degrees(seq, min_ld=1, max_ld=1, sc=None)
		
				degreesPre = list()
				
				diameterPre = list()
				eccentricityPre = list()
				neighborsPre = list()
			
				# ---
				clustersizesPre = list()
			
				lPost = list() # the length of each array
				
				# info: make the clusters, clustersizes
				clusters = list(nx.connected_components(G))
				clustersizes = list()
				#print("\n step 1")
				for ii in range(len(clusters)):
					clustersizes.append(len(clusters[ii]))
		
				a = G.degree()
				b = list(a)
				c = list()
				for i in range(len(b)):
					c.append(b[i][1])
				nodes.append(G.number_of_nodes())
				degMaxs.append(max(c))
				cons.append(nx.is_connected(G))
	
				#print("\n nodes: ", G.number_of_nodes(), "; clustersizes: ", clustersizes)
				
				#print("\n step 2")
				if nx.is_connected(G):
					#eccs.append(nx.eccentricity(G)) - I think, that is computationally expensive
					#dias.append(nx.diameter(G, nx.eccentricity(G)))
					clustersizesMax.append(max(clustersizes))
					isConnected.append(1)
				else:
					#eccs.append(-1)
					#dias.append(-1)
					clustersizesMax.append(max(clustersizes))
					isConnected.append(0)
				
			if step == 0:
				if sample == 0:
					eccsPre = np.divide(eccs,samples)
					diasPre = np.divide(dias,samples)
					degMaxsPre = np.divide(degMaxs,samples)
					nodesPre = np.divide(nodes,samples)
					consPre = np.divide(cons,samples)
					clustersizesMaxPre = np.divide(clustersizesMax,samples)
					isConnectedsPre = np.divide(isConnected,samples)
				else: 	
					eccsPre += np.divide(eccs,samples)
					diasPre += np.divide(dias,samples)
					degMaxsPre += np.divide(degMaxs,samples)
					nodesPre += np.divide(nodes,samples)
					consPre += np.divide(cons,samples)
					clustersizesMaxPre += np.divide(clustersizesMax,samples)
					isConnectedsPre += np.divide(isConnected,samples)
				
			if step == 1:
				if sample == 0:
					eccsPost = np.divide(eccs,samples)
					diasPost = np.divide(dias,samples)
					degMaxsPost = np.divide(degMaxs,samples)
					nodesPost = np.divide(nodes,samples)
					consPost = np.divide(cons,samples)
					clustersizesMaxPost = np.divide(clustersizesMax,samples)
					isConnectedsPost = np.divide(isConnected,samples)
				else:
					eccsPost += np.divide(eccs,samples)
					diasPost += np.divide(dias,samples)
					degMaxsPost += np.divide(degMaxs,samples)
					nodesPost += np.divide(nodes,samples)
					consPost += np.divide(cons,samples)
					clustersizesMaxPost += np.divide(clustersizesMax,samples)
					isConnectedsPost += np.divide(isConnected,samples)

name = "clustersizesMaxPre.txt"
text_file = open(name, "w")
for i in range(len(clustersizesMaxPre)):
        text_file.write(str("\n " + str(clustersizesMaxPre[i])))
text_file.close()

name = "clustersizesMaxPost.txt"
text_file = open(name, "w")
for i in range(len(clustersizesMaxPost)):
        text_file.write(str("\n " + str(clustersizesMaxPost[i])))
text_file.close()

name = "degMaxsPre.txt"
text_file = open(name, "w")
for i in range(len(degMaxsPre)):
        text_file.write(str("\n " + str(degMaxsPre[i])))
text_file.close()

name = "degMaxsPost.txt"
text_file = open(name, "w")
for i in range(len(degMaxsPost)):
        text_file.write(str("\n " + str(degMaxsPost[i])))
text_file.close()

name = "Ns.txt"
text_file = open(name, "w")
for i in range(len(Ns)):
        text_file.write(str("\n " + str(Ns[i])))
text_file.close()

name = "isConnectedsPre.txt"
text_file = open(name, "w")
for i in range(len(Ns)):
	text_file.write(str("\n " + str(isConnectedsPre[i])))

name = "isConnectedsPost.txt"
text_file = open(name, "w")
for i in range(len(Ns)):
	text_file.write(str("\n " + str(isConnectedsPost[i])))

ydata = np.divide(clustersizesMaxPost, Ns)

"""
def func(x, b):
	#return a * np.exp(-b * x) + c
	return (1 - np.exp(-b * (x))) # info: c represents Ncrit

popt1, pcov1 = curve_fit(func, Ns, ydata)
ax2.plot(Ns, func(Ns, *popt1), 'r-', label='fit: b=%5.3f' % tuple(popt1))

print("\n degMaxsPre: ", degMaxsPre)
print("\n nodesPre: ", nodesPre)
print("\n np.divide(degMaxsPre, nodesPre): ", np.divide(degMaxsPre, nodesPre))
ax1.plot(Ns, np.divide(degMaxsPre, nodesPre))
ax1.plot(Ns, np.divide(degMaxsPost, nodesPost))
ax1.set_xscale('log')
ax1.set_xlabel('sample size $N$')
ax1.set_ylabel('maximum degree $d_{max}$')
#ax1.set_xlim(min(Ns), max(Ns))
#ax1.set_ylim(0, 1.0)
ax1.set_title('degMaxsPre')

alphaVal = 0.5
print("\n clustersizesMaxPreFinal: ", clustersizesMaxPre)
#ax2.hist(np.divide(clustersizesMaxPre, 1), bins = int(max(clustersizesMaxPre) - min(clustersizesMaxPre)), color='blue', alpha = alphaVal)
#ax2.hist(np.divide(clustersizesMaxPost, 1), bins = int(max(clustersizesMaxPost) - min(clustersizesMaxPost)), color='orange', alpha = alphaVal)
ax2.plot(Ns, np.divide(clustersizesMaxPre, Ns), color = 'blue')
ax2.plot(Ns, np.divide(clustersizesMaxPost, Ns), color = 'orange')
ax2.legend(['Pre selection', 'Post selection'])
#ax2.set_xlim(min(Ns), max(Ns))
#ax2.set_ylim(0, 1.0)
ax2.set_xscale('log')
#ax2.set_yscale('log')
ax2.set_xlabel('cluster size')
ax2.set_ylabel('frequency')
ax2.set_title('clustersizes')
"""
"""
ax2.plot(Ns, consPre)
ax2.plot(Ns, consPost)
ax2.set_xscale('log')
ax2.set_xlabel('sample size $N$')
ax2.set_ylabel('probability $p_{all connected}$')
ax2.set_xlim(min(Ns), max(Ns))
ax2.set_ylim(0.0, 1.0)
"""

"""
ax3.plot(Ns, eccs)
ax3.set_xscale('log')
ax3.set_xlabel('degree')
ax3.set_ylabel('frequency')
"""
"""
ax3.plot(Ns,  diasPre)
ax3.plot(Ns,  diasPost)
ax3.set_xscale('log')
ax3.set_xlabel('sample size $N$')
ax3.set_ylabel('diameter $d$')
ax3.set_xlim(min(Ns), max(Ns))
ax3.set_ylim(0.0, 1.0)
"""
fig1.savefig('degreeNum.png', dpi=300,  bbox_inches="tight")
fig2.savefig('connectedProb.png', dpi=300, bbox_inches = "tight")
fig3.savefig('diameters.png', dpi=300, bbox_inches = "tight")

plt.show()

