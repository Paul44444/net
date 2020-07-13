import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

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
import subprocess
import re
from IPython.display import HTML
import sparkhpc
from sparkhpc.sparkjob import LSFSparkJob
import findspark
import pyspark
import numpy as np
from scipy.sparse import csr_matrix
import imnet
from sparkhpc import sparkjob

#class jobPre:
if True:

    clustersizesMaxPre = list()
    clustersizesMaxPost = list()
    degMaxsPre = list()
    degMaxsPost = list()
    Ns = list()
    isConnectedsPre = list()
    isConnectedsPost = list()
    clustersizesMaxPost = list()
    
    def make_scVal():
        """
        info: initilize spark environment; make scVal
        input: -
        output: -
        """
        
        os.environ['SPARK_HOME'] = os.path.join(os.path.expanduser('~'),'spark')
    
        spark_home_string = '/cluster/home/richterp/miniconda3/lib/python3.7/' \
            + 'site-packages/pyspark'
        findspark.init(spark_home=spark_home_string)
    
        findspark.init() # this sets up the paths required to find spark libraries
    
        coresVal = 128
        sj = sparkjob.sparkjob(ncores=coresVal)
        #sj.wait_to_start()
        scVal = sj.start_spark()
        scVal.parallelize(range(scVal.defaultParallelism)).collect()
   
        return scVal 
    # info: parameters for change: 

    # info: array of N values, from which the net is constructed
    #Ns = [10**2, 2*10**2, 3*10**2, 4*10**2, 5*10**2, 6*10**2, 7*10**2, 8*10**2, 
    #    9*10**2, 10**3, 10**4, 10**5, 5*10**5]
    Ns = [10**2, 10**3]
    #info: number of extracted letters from the DNA sequence 
    extractNum = 18
    
    # info: samples = 6 is usual
    samples = 2
    
    # info: maximum levenshtein distance
    maxValIndices = [6]
    
    """
    info: 
    consPre: probability that everything is connected
    eccsPre: list of eccentricities
    diasPre: list of dias
    eccsPost: list of eccentricities
    diasPost: list of dias
    """
    consPre = list()
    consPost = list()
    eccsPre = list()
    diasPre = list()
    eccsPost = list()
    diasPost = list()
    degMaxsPre = list()
    degMaxsPost = list()
    nodesPre = list()
    nodesPost = list()
    isConnectedsPre = list()
    isConnectedsPost = list()
    
    clustersizesMaxPre = list()
    clustersizesMaxPost = list()

    def simulation(scVal):
        """
        info: perform the simulation
        input: scVal
        output: -
        """        
 
        global clustersizesMaxPre
        global clustersizesMaxPost
        global degMaxsPre
        global degMaxsPost
        global Ns
        global isConnectedsPre
        global isConnectedsPost
        global clustersizesMaxPost
        
        for maxValIndex in range(len(maxValIndices)):
            maxVal = maxValIndices[maxValIndex]
        	
            for sample in range(samples):
                """
                if output is wanted in order to see progress:
                print("\n sample/samples: ", (sample+1), "/ ", samples, 
                    "; maxValIndex: ", maxValIndex+1, "/ ", len(maxValIndices))
                """
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
			
                        index = 0
                        a = list()
                        a4 = list()
                        seq = list()

                        # info: the length of each array
                        lPre = list()
    				
                        if step == 0:
                            filename = 'pre.txt'
                        if step == 1:
                            filename = 'post.txt'
                        with open(filename) as f:
                            for line in f.readlines():
                                if index < N:
                                    a.append(line.split('\t'))
                                    # info: attach the fourth element  to a4
                                    a4.append(a[index][3].replace('\n', ''))
                                    seq.append(a4[index][0:extractNum])
                                    index += 1
                        G = p.generate_graph(seq, min_ld=min_ldVal, \
                            max_ld=max_ldVal, sc=scVal)
    
                        degreesPre = list()		
                        diameterPre = list()
                        eccentricityPre = list()
                        neighborsPre = list()
                        clustersizesPre = list()
     
                        # info: the length of each array
                        lPost = list()
    
                        # info: make the clusters, clustersizes
                        clusters = list(nx.connected_components(G))
                        clustersizes = list()
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
    
                        if nx.is_connected(G):
                            #eccs.append(nx.eccentricity(G)) - I think, 
                            # info: that is computationally expensive
                            #dias.append(nx.diameter(G, nx.eccentricity(G)))
                            clustersizesMax.append(max(clustersizes))
                            isConnected.append(1)
                        else:
                            #eccs.append(-1)
                            #dias.append(-1)
                            clustersizesMax.append(max(clustersizes))
                            isConnected.append(0)
		    
                    print("\n len(isConnected): ", len(isConnected))	
                    if step == 0:
                        if sample == 0:
                            eccsPre = np.divide(eccs,samples)
                            diasPre = np.divide(dias,samples)
                            degMaxsPre = np.divide(degMaxs,samples)
                            nodesPre = np.divide(nodes,samples)
                            consPre = np.divide(cons,samples)
                            clustersizesMaxPre \
                                = np.divide(clustersizesMax,samples)
                            isConnectedsPre = np.divide(isConnected,samples)
                        else: 	
                            eccsPre += np.divide(eccs,samples)
                            diasPre += np.divide(dias,samples)
                            degMaxsPre += np.divide(degMaxs,samples)
                            nodesPre += np.divide(nodes,samples)
                            consPre += np.divide(cons,samples)
                            clustersizesMaxPre \
                                += np.divide(clustersizesMax,samples)
                            isConnectedsPre += np.divide(isConnected,samples)
				
                    if step == 1:
                        if sample == 0:
                            eccsPost = np.divide(eccs,samples)
                            diasPost = np.divide(dias,samples)
                            degMaxsPost = np.divide(degMaxs,samples)
                            nodesPost = np.divide(nodes,samples)
                            consPost = np.divide(cons,samples)
                            clustersizesMaxPost \
                                = np.divide(clustersizesMax,samples)
                            isConnectedsPost = np.divide(isConnected,samples)
                        else:
                            eccsPost += np.divide(eccs,samples)
                            diasPost += np.divide(dias,samples)
                            degMaxsPost += np.divide(degMaxs,samples)
                            nodesPost += np.divide(nodes,samples)
                            consPost += np.divide(cons,samples)
                            clustersizesMaxPost \
                                += np.divide(clustersizesMax,samples)
                            isConnectedsPost += np.divide(isConnected,samples)
               
    def write():
        """
        info: write the results as txt-files
        input: - 
        output: - 
        """
       
        global clustersizesMaxPre
        global clustersizesMaxPost
        global degMaxsPre
        global degMaxsPost
        global Ns
        global isConnectedsPre
        global isConnectedsPost
        global clustersizesMaxPost

        name = "txt/clustersizesMaxPre.txt"
        text_file = open(name, "w")
        for i in range(len(clustersizesMaxPre)):
            text_file.write(str("\n " + str(clustersizesMaxPre[i])))
        text_file.close()
    
        name = "txt/clustersizesMaxPost.txt"
        text_file = open(name, "w")
        for i in range(len(clustersizesMaxPost)):
            text_file.write(str("\n " + str(clustersizesMaxPost[i])))
        text_file.close()
    
        name = "txt/degMaxsPre.txt"
        text_file = open(name, "w")
        for i in range(len(degMaxsPre)):
            text_file.write(str("\n " + str(degMaxsPre[i])))
        text_file.close()

        name = "txt/degMaxsPost.txt"
        text_file = open(name, "w")
        for i in range(len(degMaxsPost)):
           text_file.write(str("\n " + str(degMaxsPost[i])))
        text_file.close()
        
        name = "txt/Ns.txt"
        text_file = open(name, "w")
        for i in range(len(Ns)):
            text_file.write(str("\n " + str(Ns[i])))
        text_file.close()
    
        name = "txt/isConnectedsPre.txt"
        text_file = open(name, "w")
        for i in range(len(Ns)):
            text_file.write(str("\n " + str(isConnectedsPre[i])))

        name = "txt/isConnectedsPost.txt"
        text_file = open(name, "w")
        for i in range(len(Ns)):
            text_file.write(str("\n " + str(isConnectedsPost[i])))

        ydata = np.divide(clustersizesMaxPost, Ns)

    if __name__ == "__main__":
        scVal = make_scVal()
        # somehow initialize values?
        simulation(scVal)
        write()
