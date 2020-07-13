import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
#import plotly.graph_objects as go

import os

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

# parameters for change: 
#Ns = [10**2, 2*10**2, 3*10**2, 4*10**2, 5*10**2, 6*10**2, \
#    7*10**2, 8*10**2, 9*10**2, 10**3, 2*10**3, 3*10**3, \
#     5*10**3, 10**4, 5*10**4]
#Ns = [10**2, 2*10**2, 3*10**2, 4*10**2, 5*10**2, 6*10**2, \
#    7*10**2, 8*10**2, 9*10**2, 10**3, 2*10**3]
Ns = [10**2]
extractNum = 6#18 #6
samples = 5# usually: 6
maxValIndices = [1, 2, 3, 4, 5]

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

clustersizesMaxPre = list()
clustersizesMaxPost = list()

#class lenNet2:
if True:

    xArgsName = ""
    clustersizesName = ""
    clustersizesAllErrName = ""
    diametersName = ""
    diametersAllErrName = ""
    eccentritiesName = ""
    degreeMeanName = ""
    degreeMeanAllErrName = ""
    
    xArgs = list()
    clustersizes = list()
    clustersizesAllErr = list()
    diameters = list()
    diametersAllErr = list()
    eccentrities = list()
    degreeMean = list()
    degreeMeanAllErr = list()

    def jaccardDist(name1, name2):
        """
        info: calculate the jaccard distance between the two strings 
            name1, name2
        input: name1:String, name2:String
        output: distance value dist (number)
        """
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
        """
        info: make graph, where each node denotes one element of names. 
            names is an array of strings.
        if the jaccard distance between the strings, corresponding 
        to two nodes, is lower than "maxDist", an edge is drawn
        input: names:[String], maxDist (number)
        output: 
        """
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
	
    def simulation(step): 
        """
        info: perform the simulation
        input: step (0, if pre selection; 1, if post selection)
        output: -
        """
      
        lenVals = list()
        itsMax = 10**3
        # info: jaccard distance is always in the range [0,1], 
        #     thus a maximum distance of e.g. 2 would make no sense, 
        #     that would always be fulfilled:
        maxDist = 0.05
        maxVal = maxDist

        for i in range(50):
            lenVals.append(0)

        #for step in range(2):
        if True:
            clustersizesAll = list()
            diametersAll = list()
            centersAll = list()
            eccentritiesAll = list()
            degreeMeanAll = list()
            xArgsAll = list()
   	
            clustersizesAllArray = list()
            diametersAllArray = list()
            centersAllArray = list()
            eccentritiesAllArray = list()
            degreeMeanAllArray = list()
            xArgsAllArray = list()	
	
            for sample in range(samples):		
                xArgs = list()
		
                seq = list()
                for j in range(len(lenVals)):
                    seq.append(list())
                nets = list()
                for j in range(len(lenVals)):
                    nets.append(nx.Graph())
                    lenVals[j] = j

                for i in range(len(lenVals)):
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
                                # info: attach the fourth element  to a4:
                                a4.append(a[its][3].replace('\n', ''))
                                 # info: choose with a certain length:
                                if len(a4[its]) == lenVals[i]:
                                    seq[i].append(a4[its])
                                #ls.append(len(seq[index]))
                                its += 1
			
                    if len(seq[i]) > 10:
                        #print("\n i: ", i, "; >10")
                        nets[i] = makeNet(seq[i], maxDist)
				
                # info: initialize the analyzed quantities
                clustersizes = list()
                diameters = list()
                centers = list()
                eccentrities = list()
                degreeMean = list()
                # What are interesting values to investigate?
	
                clusterMinLen = 10	
                for i in range(len(nets)):
                    if len(nets[i]) > clusterMinLen:
                        minL = 5 # 4
                        maxL = 10
                        min_ldVal = -1
                        max_ldVal = maxVal
				
                        #G = p.generate_graph(nets[i], min_ld=min_ldVal, max_ld=max_ldVal)
                        G = nets[i]
		 				
                        # info: find biggest cluster
                        testSub = list(G.subgraph(c) for c in nx.connected_components(G))
				
                        sub_graphs = sorted(list(G.subgraph(c) for c in \
                            nx.connected_components(G)), key = len, \
                            reverse = True)		
                        n = len(sub_graphs)
                        maxIndex = -1
                        maxVal = -1
						
                        for ii in range(n):
                            if len(list(sub_graphs[ii])) > 0: 
                                if len(sub_graphs[ii].nodes()) > maxVal:
                                    maxVal = len(sub_graphs[ii].nodes())
                                    maxIndex = ii
                        GSub = sub_graphs[maxIndex]
				
                        # append the values to the corresponding list:
				
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
                        print("\n degsBefore: ", degs)
                        degs = list(degs)
                        print("\n degsAfter: ", degs)
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
    	
                    clustersizesAllArray.append(clustersizesNew)
                    diametersAllArray.append(diametersNew)
                    centersAllArray.append(centers)
                    eccentritiesAllArray.append(eccentritiesNew)
                    degreeMeanAllArray.append(degreeMeanNew)
                    xArgsAllArray.append(xArgsNew)
    	
        """ Begin paste: """
	
        clustersizesAllMean = 0
        diametersAllMean = 0
        centersAllMean = 0
        eccentritiesAllMean = 0
        degreeMeanAllMean = 0

        clustersizesAllDifSquare = 0
        diametersAllDifSquare = 0
        centersAllDifSquare = 0
        eccentritiesAllDifSquare = 0
        degreeMeanAllDifSquare = 0
	
        lAll = len(clustersizesAllArray)
	
        for i in range(len(clustersizesAllArray)):
            clustersizesAllMean += np.divide(clustersizesAllArray[i],lAll)
            diametersAllMean += np.divide(diametersAllArray[i],lAll)
            #centersAllMean += np.divide(centersAllArray[i],lAll)
            #eccentritiesAllMean += np.divide(eccentritiesAllSumArray[i],lAll)
            degreeMeanAllMean += np.divide(degreeMeanAllArray[i],lAll)
   	
        for i in range(len(clustersizesAllArray)):
            clustersizesAllDifSquare += np.power(clustersizesAllArray[i] - \
                clustersizesAllMean, 2)
            diametersAllDifSquare += np.power(diametersAllArray[i] - \
                diametersAllMean, 2)
            #centersAllSumSquare += np.power(centersAllArray[i], 2)
            #eccentritiesAllSumSquare += np.power(eccentritiesAll[i], 2)
            degreeMeanAllDifSquare += np.power(degreeMeanAllArray[i] - \
                degreeMeanAllMean, 2)
 	
        clustersizesAllErr = np.sqrt(np.divide(clustersizesAllDifSquare,(lAll - 1)))
        diametersAllErr = np.sqrt(np.divide(diametersAllDifSquare,(lAll - 1)))
        #centersAllSumSquare = np.sqrt(np.divide(centersAllSumSquare,(lAll - 1)))
        #eccentritiesAllSumSquare = np.sqrt(np.divide(eccentritiesAllSumSquare,(lAll - 1)))
        degreeMeanAllErr = np.sqrt(np.divide(degreeMeanAllDifSquare,(lAll - 1)))
	
        """ End paste """
	
        xArgs = xArgsNew
        clustersizes = clustersizesNew
        diameters = diametersNew
        eccentrities = eccentritiesNew
        degreeMean = degreeMeanNew
	
        if step == 0:
            col = 'orange'
        if step == 1:
            col = 'blue'
    def write(step):
        """
        info: write data
        input: step - 0 if before Thymus selection, 1 if after Thymus 
            selection
        output: -
        """	
        xArgsName = str('txt/' + 'lenNet2_xArgs_' + str(step) + '.txt')
        clustersizesName = str('txt/' + 'lenNet2_clustersizes_' + str(step) \
            + '.txt')
        clustersizesAllErrName = str('txt/' + 'lenNet2_clustersizesAllErr_' \
            + str(step) + '.txt')
        diametersName = str('txt/' + 'lenNet2_diameters_' + str(step) \
            + '.txt')
        diametersAllErrName = str('txt/' + 'lenNet2_diametersAllErr_' \
            + str(step) + '.txt')
        eccentritiesName = str('txt/' + 'lenNet2_eccentrities_' + str(step) \
            + '.txt')
        degreeMeanName = str('txt/' + 'lenNet2_degreeMean_' + str(step) \
            + '.txt')
        degreeMeanAllErrName = str('txt/' + 'lenNet2_degreeMeanAllErr_' + str(step) \
            + '.txt')
	
        text_file = open(xArgsName, "w")
        for i in range(len(xArgs)):
            text_file.write(str("\n " + str(xArgs[i])))
        text_file.close()
		
        text_file = open(clustersizesName, "w")
        for i in range(len(clustersizes)):
            text_file.write(str("\n " + str(clustersizes[i])))
        text_file.close()

        text_file = open(clustersizesAllErrName, "w")
        for i in range(len(clustersizesAllErr)):
            text_file.write(str("\n " + str(clustersizesAllErr[i])))
        text_file.close()
	
        text_file = open(diametersName, "w")
        for i in range(len(diameters)):
            text_file.write(str("\n " + str(diameters[i])))
        text_file.close()
	
        text_file = open(diametersAllErrName, "w")
        for i in range(len(diametersAllErr)):
            text_file.write(str("\n " + str(diametersAllErr[i])))
        text_file.close()
	
        """
        text_file = open(???, "w")
        for i in range(len(centers)):
            text_file.write(str("\n " + str(centers[i])))
        text_file.close()
        """
        text_file = open(eccentritiesName, "w")
        for i in range(len(eccentrities)):
            text_file.write(str("\n " + str(eccentrities[i])))
        text_file.close()

        text_file = open(degreeMeanName, "w")
        for i in range(len(degreeMean)):
            text_file.write(str("\n " + str(degreeMean[i])))
        text_file.close()
	
        text_file = open(degreeMeanAllErrName, "w")
        for i in range(len(degreeMeanAllErr)):
            text_file.write(str("\n " + str(degreeMeanAllErr[i])))
        text_file.close()
    if __name__ == "__main__":
        #make_scVal()
        # somehow initialize values?
        for step in range(2):
            simulation(step)
            write(step)
