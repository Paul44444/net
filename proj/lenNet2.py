import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go

import os
import sonia
from sonia.sonia_leftpos_rightpos import SoniaLeftposRightpos
from sonia.plotting import Plotter
from sonia.evaluate_model import EvaluateModel
from sonia.sequence_generation import SequenceGeneration
import numpy as np
import pandas as pd

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

import textdistance as td # better cite that

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
Ns = [10**2, 2*10**2, 3*10**2, 4*10**2, 5*10**2, 6*10**2, 7*10**2, 8*10**2, 9*10**2, 10**3, 2*10**3]

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

extractNum = 6#18 #6

clustersizesMaxPre = list()
clustersizesMaxPost = list()

samples = 6# usually: 6

maxValIndices = [1, 2, 3, 4, 5]


#index = 0
#a = list()
#a4 = list()
#seq = list()
				
#lPre = list() # the length of each array

#N = 10**4

fig4, ax4 = plt.subplots()
fig5, ax5 = plt.subplots()
fig6, ax6 = plt.subplots()
fig7, ax7 = plt.subplots()
fig8, ax8 = plt.subplots()

def jaccardDist(name1, name2):
	"""
	dist = 0
	
	for i in range(len(name1)):
		if not (name1[i] == name2[i]):
			dist += 1 
	#still have to calculate the real Jaccard distance
	"""

	dist = 1 - td.jaccard(name1, name2)
	return dist

def makeNet(names, maxDist):
	g = nx.Graph()
	
	#print("\n names: ", names)
	for i in range(len(names)):
		g.add_node(names[i])	
	
	for i in range(len(names)):
		for j in range(len(names)):
			if not (i == j):
				if jaccardDist(names[i], names[j]) < maxDist:
					g.add_edge(names[i], names[j])
	#print("\n names: ", list(names))
	#print("\n g.nodes(): ", g.nodes())
	return g
	

lenVals = list()
itsMax = 10**3
maxDist = 0.05 # jaccard distance is always in the range [0,1], thus a maximum distance of e.g. 2 would make no sense, that would always be fulfilled
maxVal = maxDist

for i in range(50):
	lenVals.append(0)

for step in range(2):
	
	xArgs = list()
	
	seq = list()
	for j in range(len(lenVals)):
		seq.append(list())
	nets = list()
	for j in range(len(lenVals)):
		nets.append(nx.Graph())
		lenVals[j] = j
	
	for i in range(len(lenVals)): # What are good values?
		if step == 0:
			filename = 'pre.txt'
		if step == 1:
			filename = 'post.txt'
		ls = list()
		index = 0
		a = list()
		a4 = list()
		
		its = 0
	
		with open(filename) as f:
			for line in f.readlines():
				if its < itsMax:
					a.append(line.split('\t'))
					a4.append(a[its][3].replace('\n', ''))                # info: attach the fourth element  to a4
					#print("\n its: ", its, "; a4[its]: ", a4[its], "; len(a4[its]): ", len(a4[its]), "; lenVals[i]: ", lenVals[i])
					#print("\n  len(a4[its]): ",  len(a4[its]), "; lenVals[i]: ", lenVals[i])
					if len(a4[its]) == lenVals[i]:					# info: choose with a certain length
						seq[i].append(a4[its])
						#print("\n something is equal")
					#ls.append(len(seq[index]))
					its += 1
		
		if len(seq[i]) > 10:
			#print("\n i: ", i, "; >10")
			nets[i] = makeNet(seq[i], maxDist)
			print("\n nets[i]: ", list(nx.connected_components(nets[i])))
			
			"""
			fig, ax = plt.subplots()
			plt.axis('off')
			nx.draw_networkx_nodes(nets[i], pos,nodelist=pA.keys(), node_size=szVal, node_color=list(pA.values()), cmap='viridis', mode = 'random')
			nx.draw_networkx_edges(nets[i],pos,nodelist=[centerVal],alpha=0.4, edge_color='gray')
			plt.show()
			"""
		#else:
			#print("\n i: ", i, "; not > 10")
		"""
		lsHist = np.histogram(ls, bins = int((max(ls) - min(ls))/3))
		xArgs = lsHist[1][:]
		maxVal = 100
		if step == 0:
			ax1.plot(lsHist[1][1:], lsHist[0], color = 'orange')
		if step == 1:
			ax1.plot(lsHist[1][1:], lsHist[0], color = 'blue')
		
		nets = list()
		for i in range(len(lsHist[0])+1): # keep in mind, that this is the average
			nets.append(list())
		for seqEl in seq:
			seqElIndex = int((len(seqEl) - lsHist[1][0])/3)
			nets[seqElIndex].append(seqEl)
		"""

	"""
	for i in range(len(seq)):
		print("\n seq[i]: ", list(seq[i]))
	"""
	
	# info: initialize the analyzed quantities
	clustersizes = list()
	diameters = list()
	centers = list()
	eccentrities = list()
	degreeMean = list()
	# What are interesting values to investigate?

	clusterMinLen = 10	
	for i in range(len(nets)):
		#print("\n len(nets[i]): ", len(nets[i]))
		print("\n len(nets[i].nodes()): ", len(nets[i].nodes()))
		#print("\n len(nets[i].edges()): ", len(nets[i].edges()))
		if len(nets[i]) > clusterMinLen:
			minL = 5 # 4
			maxL = 10
			min_ldVal = -1
			max_ldVal = maxVal
			
			#G = p.generate_graph(nets[i], min_ld=min_ldVal, max_ld=max_ldVal)
			G = nets[i]
					
			# info: find biggest cluster
			#print("\n list(nx.connected_component_subgraphs(G)): ", list(nx.connected_component_subgraphs(G)))
			testSub = list(nx.connected_component_subgraphs(G))
				
			#print("\n testSub: ", list(testSub[0].nodes()))
			sub_graphs = sorted(list(nx.connected_component_subgraphs(G)), key = len, reverse = True)
			#print("sub_graphs: ",  list(sub_graphs[0].nodes()))
			n = len(sub_graphs)
			maxIndex = -1
			maxVal = -1
					
			for ii in range(n):
				if len(list(sub_graphs[ii])) > 0: 
					#print("\n sub_graphs[ii].nodes(): ", sub_graphs[ii].nodes())
					if len(sub_graphs[ii].nodes()) > maxVal:
						maxVal = len(sub_graphs[ii].nodes())
						maxIndex = ii
			#print("\n list(sub_graphs): ", list(sub_graphs))
			GSub = sub_graphs[maxIndex]
				
			# append the values to the corresponding list:
			
			print("\n len(GSub.nodes()): ", len(GSub.nodes()), "; len(G.nodes()): ", len(G.nodes()))
			clustersizes.append(len(GSub.nodes())/len(G.nodes()))
			diameters.append(nx.diameter(GSub))
			centerList = nx.center(GSub)
			centers.append(centerList[0])
			
			"""
			ecc = 0
			eccs = nx.eccentricity(GSub)
			
			for el in eccs:
				print("\n el: ", el)
				ecc += el/(len(eccs))
			"""
			
			deg = 0
			degs = GSub.degree()
			for el in degs:
				print("\n el: ", el)
				deg += el[1]/(len(degs))
				
			eccentrities.append(0)
			degreeMean.append(deg)
			xArgs.append(lenVals[i])
		else: 
			clustersizes.append(0)
			diameters.append(0)
			centers.append(0)
			eccentrities.append(0)
			degreeMean.append(0)
			xArgs.append(lenVals[i])
	
	xArgsNew = list()
	clustersizesNew = list()
	diametersNew = list()
	eccentritiesNew = list()
	degreeMeanNew = list()
	
	for i in range(len(xArgs)):
		if i%3 == 0:
			xArgsNew.append(xArgs[i])
			clustersizesNew.append(clustersizes[i])
			diametersNew.append(diameters[i])
			eccentritiesNew.append(eccentrities[i])
			degreeMeanNew.append(degreeMean[i])
	
	print("\n clustersizes: ", list(clustersizes))
	print("\n diameters: ", list(diameters))
	print("\n xArgs: ", list(xArgs))
	
	xArgs = xArgsNew
	clustersizes = clustersizesNew
	diameters = diametersNew
	eccentrities = eccentritiesNew
	degreeMean = degreeMeanNew
	
	#ax4.set_title('fractional size of the biggeest cluster')
	
	if step == 0:
		col = 'orange'
	if step == 1:
		col = 'blue'
	#print("\n len(xArgs): ", len(xArgs), "; len(clustersizes): ", len(clustersizes))
			
	ax4.plot(xArgs, clustersizes, color = col)
	ax4.set_xlabel('length $l$')
	ax4.set_ylabel('clustersize $c$') # what's the right letter?  
	ax4.set_xlim(min(xArgs), max(xArgs))
	ax4.set_ylim(0, 1)
	ax4.legend(['Pre-selection', 'Post-selection'], frameon = False)
	
	"""
	ax4.set_xlabel()
	ax4.set_ylabel()
	ax4.set_xscale()
	ax4.set_yscale()
	"""
	
	"""
	ax5.plot(xArgs, diameters, color = col)
	ax6.plot(xArgs, centers, color = col)
	ax7.plot(xArgs, eccentrities, color = col)
	ax8.plot(xArgs, degreeMean, color = col)
	"""
	
	ax5.plot(xArgs, diameters, color = col)
	ax5.set_xlabel('length $l$')
	ax5.set_ylabel('diameter $d$')
	ax5.set_xlim(min(xArgs), max(xArgs))
	ax5.set_ylim(min(diameters), max(diameters))
	ax5.legend(['Pre-selection', 'Post-selection'], frameon = False)

	#ax6.plot(xArgs, centers, color = col)
	#ax6.set_xlabel('length $l$')
	#ax6.set_ylabel('center $c$') # what are the right letters for the sizes
	#ax6.set_xlim(min(xArgs), max(xArgs))
	#print("\n centers: ", list(centers))
	#ax6.set_ylim(min(centers), max(centers))
	#ax6.legend(['Pre-selection', 'Post-selection'])

	ax7.plot(xArgs, eccentrities, color = col)
	ax7.set_xlabel('length $l$')
	ax7.set_ylabel('eccentricities $e$')
	ax7.set_xlim(min(xArgs), max(xArgs))
	ax7.set_ylim(min(eccentrities), max(eccentrities))
	ax7.legend(['Pre-selection', 'Post-selection'], frameon = False)

	ax8.plot(xArgs, degreeMean, color = col)
	ax8.set_xlabel('length $l$')	
	ax8.set_ylabel('degree $d$')
	ax8.set_xlim(min(xArgs), max(xArgs))
	ax8.set_ylim(min(degreeMean), max(degreeMean))
	ax8.legend(['Pre-selection', 'Post-selection'], frameon = False)

fig4.savefig('lenNet2clustersizes.png', dpi=300,  bbox_inches="tight")
fig5.savefig('lenNet2diameters.png', dpi=300,  bbox_inches="tight")
fig6.savefig('lenNet2centers.png', dpi=300,  bbox_inches="tight")
fig7.savefig('lenNet2eccentrities.png', dpi=300,  bbox_inches="tight")
fig8.savefig('lenNet2degreeMean.png', dpi=300,  bbox_inches="tight")
	
plt.show()
#ydata = np.divide(clustersizesMaxPost, Ns)
"""
fig1.savefig('degreeNum.png', dpi=300,  bbox_inches="tight")
fig2.savefig('connectedProb.png', dpi=300, bbox_inches = "tight")
fig3.savefig('diameters.png', dpi=300, bbox_inches = "tight")

fig4.savefig('clustersizes.png', dpi=300,  bbox_inches="tight")
fig5.savefig('diameters.png', dpi=300,  bbox_inches="tight")
fig6.savefig('centers.png', dpi=300,  bbox_inches="tight")
fig7.savefig('eccentrities.png', dpi=300,  bbox_inches="tight")
fig8.savefig('degreeMean.png', dpi=300,  bbox_inches="tight")

plt.show()
"""
