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

samples = 5# usually: 6

maxValIndices = [1, 2, 3, 4, 5]

#lPre = list() # the length of each array

N = 10**3

xArgs = list()

fig4, ax4 = plt.subplots()
fig5, ax5 = plt.subplots()
fig6, ax6 = plt.subplots()
fig7, ax7 = plt.subplots()
fig8, ax8 = plt.subplots()

for step in range(2):	
	clustersizesAll = list()
	diametersAll = list()
	centersAll = list()
	eccentritiesAll = list()
	degreeMeanAll = list()

	for sample in range(samples):			
		if step == 0:
			filename = 'pre' + str(sample+1) + '.txt'
		if step == 1:
			filename = 'post' + str(sample+1) + '.txt'
		ls = list()
		index = 0
		a = list()
		a4 = list()
		seq = list()
	
		with open(filename) as f:
			for line in f.readlines():
				if index < N:
					a.append(line.split('\t'))
					a4.append(a[index][3].replace('\n', ''))                # info: attach the fourth element  to a4
					seq.append(a4[index])
					
					ls.append(len(seq[index]))
					index += 1
		#lsHist = np.histogram(ls, bins = int((max(ls) - min(ls))/3))
		# we still have to achieve, that the intervals have the same limits for all samples
		lsHist = np.histogram(ls, bins = np.arange(0, 120, 3))
		
		xArgs = lsHist[1][:]
		maxVal = 5
		
		"""
		if step == 0:
			ax1.plot(lsHist[1][1:], lsHist[0], color = 'orange')
		if step == 1:
			ax1.plot(lsHist[1][1:], lsHist[0], color = 'blue')
		"""
		nets = list()
		for i in range(len(lsHist[0])+1): # keep in mind, that this is the average
			nets.append(list())
		for seqEl in seq:
			seqElIndex = int((len(seqEl) - lsHist[1][0])/3)
			nets[seqElIndex].append(seqEl)		
	
		# info: initialize the analyzed quantities
		clustersizes = list()
		diameters = list()
		centers = list()
		eccentrities = list()
		degreeMean = list()
		# What are interesting values to investigate?
		
		clusterMinLen = 10	
			
		print("\n nets: ", len(nets))
		
		for i in range(len(nets)):
			if len(nets[i]) > clusterMinLen:
				minL = 5 # 4
				maxL = 10
				min_ldVal = -1
				#max_ldVal = maxVal
				max_ldVal = maxVal
				
				#print("\n nets[i]: ", list(nets[i]))
				G = p.generate_graph(nets[i], min_ld=min_ldVal, max_ld=max_ldVal)	
				#print("\n G.nodes(): ", len(G.nodes()))
				if len(G.nodes()) == 0:
					G = nx.Graph()
					G.add_node("ZeroNode")
				
				# info: find biggest cluster
				#print("\n list(nx.connected_component_subgraphs(G)): ", list(nx.connected_component_subgraphs(G)))
				testSub = list(nx.connected_component_subgraphs(G))
				#if len(testSub) > 0:
				#	testSub = G
				
				#print("\n testSub: ", list(testSub[0].nodes()))
				#print("\n testSub: ", list(testSub))
				sub_graphs = sorted(list(nx.connected_component_subgraphs(G)), key = len, reverse = True)
				if len(sub_graphs) == 0:
					sub_graphs = list()
					sub_graphs.append(nx.Graph())
					sub_graphs[0].add_node('FillNode')
				
				#print("sub_graphs: ",  list(sub_graphs[0].nodes()))
				n = len(sub_graphs)
				maxIndex = -1
				maxValue = -1
					
				for ii in range(n):
					if len(list(sub_graphs[ii])) > 0: 
						#print("\n sub_graphs[ii].nodes(): ", sub_graphs[ii].nodes())
						if len(sub_graphs[ii].nodes()) > maxValue:
							maxValue = len(sub_graphs[ii].nodes())
							maxIndex = ii
				#print("\n list(sub_graphs): ", list(sub_graphs))
				GSub = sub_graphs[maxIndex]
				
				#print("\n len(list(GSub.nodes())): ", len(list(GSub.nodes())), "; len(list(G.nodes())): ",  len(list(G.nodes())))
				# append the values to the corresponding list:
				
				clustersizes.append(len(GSub.nodes())/len(G.nodes()))
				diameters.append(nx.diameter(GSub))
				centerList = nx.center(GSub)
				centers.append(centerList[0])
				eccentrities.append(0)
				
				deg = 0
				degs = GSub.degree()
				for el in degs:
					#print("\n el: ", el)
					deg += el[1]/(len(degs))	
				degreeMean.append(deg)
			else: 
				clustersizes.append(0)
				diameters.append(0)
				centers.append(0)
				eccentrities.append(0)
				degreeMean.append(0)
		if sample > 0:
			clustersizesAll = np.add(clustersizesAll, clustersizes)
			diametersAll = np.add(diametersAll, diameters)
			#centersAll = np.add(centersAll, centers)
			eccentritiesAll = np.add(eccentritiesAll, eccentrities)
			degreeMeanAll = np.add(degreeMeanAll, degreeMean)
		else:
			clustersizesAll = clustersizes
			diametersAll = diameters
			centersAll = centers
			eccentritiesAll = eccentrities
			degreeMeanAll = degreeMean
			
	if step == 0:
		col = 'orange'
	if step == 1:
		col = 'blue'		
	ax4.plot(xArgs, clustersizesAll, color = col)
	ax4.set_xlabel('length $l$')
	ax4.set_ylabel('clustersize $c$') # what's the right letter?  
	ax4.set_xlim(min(xArgs), max(xArgs))
	ax4.set_ylim(min(clustersizesAll), max(clustersizesAll))
	ax4.legend(['Pre-selection', 'Post-selection'], frameon = False)
	#ax4.set_title('fractional size of the biggeest cluster')

	ax5.plot(xArgs, diametersAll, color = col)
	ax5.set_xlabel('length $l$')
	ax5.set_ylabel('diameter $d$')	
	ax5.set_xlim(min(xArgs), max(xArgs))
	ax5.set_ylim(min(diametersAll), max(diametersAll))
	ax5.legend(['Pre-selection', 'Post-selection'], frameon = False)
	
	#ax6.plot(xArgs, centers, color = col)	
	#ax6.set_xlabel('length $l$')
	#ax6.set_ylabel('center $c$') # what are the right letters for the sizes	
	#ax6.set_xlim(min(xArgs), max(xArgs))
	#print("\n centers: ", list(centers))
	#ax6.set_ylim(min(centers), max(centers))
	#ax6.legend(['Pre-selection', 'Post-selection'])
	
	ax7.plot(xArgs, eccentritiesAll, color = col)
	ax7.set_xlabel('length $l$')
	ax7.set_ylabel('eccentricities $e$')	
	ax7.set_xlim(min(xArgs), max(xArgs))
	ax7.set_ylim(min(eccentritiesAll), max(eccentritiesAll))
	ax7.legend(['Pre-selection', 'Post-selection'], frameon = False)
	
	ax8.plot(xArgs, degreeMeanAll, color = col)	
	ax8.set_xlabel('length $l$')
	ax8.set_ylabel('degree $d$')	
	ax8.set_xlim(min(xArgs), max(xArgs))
	ax8.set_ylim(min(degreeMeanAll), max(degreeMeanAll))
	ax8.legend(['Pre-selection', 'Post-selection'], frameon = False)
	
fig4.savefig('lenNetclustersizes.png', dpi=300,  bbox_inches="tight")
fig5.savefig('lenNetdiameters.png', dpi=300,  bbox_inches="tight")
fig6.savefig('lenNetcenters.png', dpi=300,  bbox_inches="tight")
fig7.savefig('lenNeteccentrities.png', dpi=300,  bbox_inches="tight")
fig8.savefig('lenNetdegreeMean.png', dpi=300,  bbox_inches="tight")

plt.show()
