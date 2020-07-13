import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

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

import os
import subprocess, re
from IPython.display import HTML
import sparkhpc
from sparkhpc.sparkjob import LSFSparkJob
import findspark
import pyspark
import numpy as np
from scipy.sparse import csr_matrix

import imnet

from sparkhpc import sparkjob
import findspark
import pyspark

if True:

    """ info: global variable: """
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
 
    def make_scVal():
        """
        info: initialize the spark environment
        input: -
        output: scVal
        """
        os.environ['SPARK_HOME'] = os.path.join(os.path.expanduser('~'),'spark')
    
        findspark.init(spark_home = '/cluster/home/richterp/miniconda3/lib/python3.7/site-packages/pyspark')
    
        findspark.init() # this sets up the paths required to find spark libraries
    
        coresVal = 128
        sj = sparkjob.sparkjob(ncores=coresVal)
        #sj.wait_to_start()
        scVal = sj.start_spark()
        scVal.parallelize(range(scVal.defaultParallelism)).collect()

        return scVal
        # info: parameters for change:

        #Ns = [10**2, 2*10**2, 3*10**2, 4*10**2, 5*10**2, 6*10**2, 7*10**2, \
        #    8*10**2, 9*10**2, 10**3, 2*10**3, 3*10**3, 5*10**3, 10**4, 5*10**4]
        #Ns = [10**2, 2*10**2, 3*10**2, 4*10**2, 5*10**2, 6*10**2, 7*10**2, \
        #    8*10**2, 9*10**2, 10**3, 2*10**3]
        # Is Ns still relevant?

    def simulation(step, scVal):
        """
        info: make the simulation
        input: step: number is 1 or 2, indicating or Pre- or Post-Thymus selection
               scVal: scVal
        output: -
        """
       
        global xArgsName
        global clustersizesName
        global clustersizesAllErrName
        global diametersName
        global diametersAllErrName
        global eccentritiesName
        global degreeMeanName
        global degreeMeanAllErrName

        global xArgs
        global clustersizes
        global clustersizesAllErr
        global diameters
        global diametersAllErr
        global eccentrities
        global degreeMean
        global degreeMeanAllErr
        
        extractNum = 6#18 #6
        samples = 2# usually: 6
        maxValIndices = [1, 2, 3, 4, 5] # is that still relevant?
        N = 10**3
   
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
    
        #lPre = list() # the length of each array
    
        xArgs = list()

        if True: # könnte eigentlich weg	
            clustersizesAll = list()
            diametersAll = list()
            centersAll = list()
            eccentritiesAll = list()
            degreeMeanAll = list()

            clustersizesAllArray = list()
            diametersAllArray = list()
            centersAllArray = list()
            eccentritiesAllArray = list()
            degreeMeanAllArray = list()
	
            for sample in range(samples):			
                if step == 0:
                    filename = 'pre.txt'
                if step == 1:
                    filename = 'post.txt'
                ls = list()
                index = 0
                a = list()
                a4 = list()
                seq = list()
	
                with open(filename) as f:
                    for line in f.readlines():
                        if index < N:
                            a.append(line.split('\t'))
                            # info: attach the fourth element  to a4: 
                            a4.append(a[index][3].replace('\n', ''))
                            seq.append(a4[index])
			    		
                            ls.append(len(seq[index]))
                            index += 1
                #lsHist = np.histogram(ls, bins = int((max(ls) - min(ls))/3))
                # we still have to achieve, that the intervals have the 
                #     same limits for all samples
                lsHist = np.histogram(ls, bins = np.arange(0, 120, 3))
		
                xArgs = lsHist[1][:]
                maxVal = 5
		
                nets = list()
                # keep in mind, that this is the average:
                for i in range(len(lsHist[0])+1):
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
                        G = p.generate_graph(nets[i], min_ld=min_ldVal, max_ld=max_ldVal, sc = scVal)	
                        #print("\n G.nodes(): ", len(G.nodes()))
                        if len(G.nodes()) == 0:
                            G = nx.Graph()
                            G.add_node("ZeroNode")
				
                        # info: find biggest cluster
                        testSub = list((G.subgraph(c) for c in nx.connected_components(G)))
                        
                        sub_graphs = sorted(list(G.subgraph(c) for c in nx.connected_components(G)), key = len, reverse = True)
                        
                        if len(sub_graphs) == 0:
                            sub_graphs = list()
                            sub_graphs.append(nx.Graph())
                            sub_graphs[0].add_node('FillNode')
				
                        n = len(sub_graphs)
                        maxIndex = -1
                        maxValue = -1
					
                        for ii in range(n):
                            if len(list(sub_graphs[ii])) > 0: 
                                if len(sub_graphs[ii].nodes()) > maxValue:
                                    maxValue = len(sub_graphs[ii].nodes())
                                    maxIndex = ii
                        GSub = sub_graphs[maxIndex]
				
                        # append the values to the corresponding list:
				
                        clustersizes.append(len(GSub.nodes())/len(G.nodes()))
                    
                        diameters.append(nx.diameter(GSub))
                        centerList = nx.center(GSub)
                        centers.append(centerList[0])
                        eccentrities.append(0)
				
                        deg = 0
                        degs = GSub.degree()
                        degs = list(degs)
                        for el in degs:
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
	
                    clustersizesAllArray.append(clustersizes)
                    diametersAllArray.append(diameters)
                    centersAllArray.append(centers)
                    eccentritiesAllArray.append(eccentrities)
                    degreeMeanAllArray.append(degreeMean)	
                else:
                    clustersizesAll = clustersizes
                    diametersAll = diameters
                    centersAll = centers
                    eccentritiesAll = eccentrities
                    degreeMeanAll = degreeMean
		
                clustersizesAllArray.append(clustersizes)
                diametersAllArray.append(diameters)
                centersAllArray.append(centers)
                eccentritiesAllArray.append(eccentrities)
                degreeMeanAllArray.append(degreeMean)	
		
            if step == 0:
                col = 'orange'
            if step == 1:
                col = 'blue'		
	
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
                clustersizesAllDifSquare += np.power(clustersizesAllArray[i] \
                    - clustersizesAllMean, 2)
                diametersAllDifSquare += np.power(diametersAllArray[i] \
                    - diametersAllMean, 2)
                #centersAllSumSquare += np.power(centersAllArray[i], 2)
                #eccentritiesAllSumSquare += np.power(eccentritiesAll[i], 2)
                degreeMeanAllDifSquare += np.power(degreeMeanAllArray[i] \
                    - degreeMeanAllMean, 2)
	
            
            
            clustersizesAllErr = np.sqrt(np.divide( \
                clustersizesAllDifSquare,(lAll - 1)))
            diametersAllErr = np.sqrt(np.divide( \
                diametersAllDifSquare,(lAll - 1)))
            #centersAllSumSquare = np.sqrt(np.divide( \
            #    centersAllSumSquare,(lAll - 1)))
            #eccentritiesAllSumSquare = np.sqrt(np.divide( \
            #    eccentritiesAllSumSquare,(lAll - 1)))
            degreeMeanAllErr = np.sqrt(np.divide( \
                degreeMeanAllDifSquare,(lAll - 1)))
    def write(step):
            """
            info: save data .txt-file
            input: step - 0 if before Thymus selection, 1 if after Thymus selection
            output: -
            """

            global xArgsName
            global clustersizesName
            global clustersizesAllErrName
            global diametersName
            global diametersAllErrName
            global eccentritiesName
            global degreeMeanName
            global degreeMeanAllErrName

            global xArgs
            global clustersizes
            global clustersizesAllErr
            global diameters
            global diametersAllErr
            global eccentrities
            global degreeMean
            global degreeMeanAllErr

            xArgsName = str('txt/' + 'lenNet1_xArgs_' + str(step) + '.txt')
            clustersizesName = str('txt/' + 'lenNet1_clustersizes_' \
                + str(step) + '.txt')
            clustersizesAllErrName = str('txt/' + 'lenNet1_clustersizesAllErr_' \
                + str(step) + '.txt')
            diametersName = str('txt/' + 'lenNet1_diameters_' + str(step) \
                + '.txt')
            diametersAllErrName = str('txt/' + 'lenNet1_diametersAllErr_' \
                + str(step) + '.txt')
            eccentritiesName = str('txt/' + 'lenNet1_eccentrities_' \
                + str(step) + '.txt')
            degreeMeanName = str('txt/' + 'lenNet1_degreeMean_' \
                + str(step) + '.txt')
            degreeMeanAllErrName = str('txt/' + 'lenNet1_degreeMeanAllErr_' \
                + str(step) + '.txt')
	
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
            text_file = open("lenNet1_centers.txt", "w")
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
        scVal = make_scVal()
        # somehow initialize values?
        for step in range(2):
            simulation(step, scVal)
            write(step)
	
