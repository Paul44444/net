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
import sparkhpc
import findspark
import pyspark
import numpy as np
from scipy.sparse import csr_matrix
import imnet
from sparkhpc import sparkjob
import findspark

#class job:
if True:

    cPre = list()
    cPost = list()
    clustersizesPre = list()
    clustersizesPost = list()
    GnamesHist1Pre = list()
    GnamesHist1Post = list()

    def make_scVal():
        """
        info: start making scVal
        input: -
        output: scVal: instance of an spark environment # correct?
        """

        os.environ['SPARK_HOME'] = os.path.join(os.path.expanduser('~'),'spark')

        spark_home_name =  '/cluster/home/richterp/miniconda3/' \
            + 'lib/python3.7/site-packages/pyspark'
        findspark.init(spark_home = spark_home_name)

        findspark.init() # this sets up the paths required to find spark libraries

        coresVal = 128
        sj = sparkjob.sparkjob(ncores=coresVal)
        #sj.wait_to_start()
        scVal = sj.start_spark()
        scVal.parallelize(range(scVal.defaultParallelism)).collect()
        # ---------------------- info: End making scVal -----------------------
        
        return scVal
    
    # info: parameters for change:
    
    #N = 10**5
    N = 10**3
    #minL = 5 # 4
    #maxL = 6
    min_ldVal = 0
    max_ldVal = 1
    extractNum = 18 #20
    #lets = 'ACDEFGHIKLMNPQRSTVWY'
    #lets = 'ACD'
    #seq = r.generate_random_sequences(N, minimum_length=minL,
        # maximum_length=maxL, seed=1, letters=lets)
   
    cPre = list()
    clustersizesPre = list()
    GnamesHist1Pre = list()
    
    cPost = list()
    clustersizesPost = list()
    GnamesHist1Post = list()

    alphaVal = 0.5
    
    def simulation(scVal):
        """
        info: perform the simulation
        input: scVal
        output: -
        """

        global cPre
        global cPost
        global clustersizesPre
        global clustersizesPost
        global GnamesHist1Pre
        global GnamesHist1Post
  
        for step in range(2):
            if step == 0:
                filename = 'pre.txt'
            if step == 1:
                filename = 'post.txt'
        
            index = 0
            a = list()
            a4 = list()
            seq = list()
    	    
            # info: opening the list of generated sequences 
            # info: (sequences generated done with SONIA, 
            # info: which simulates VDJ recombination)
            with open(filename) as f:
                for line in f.readlines():
                    if index < N:
                        a.append(line.split('\t'))
                        # info: attach the fourth element  to a4
                        a4.append(a[index][3].replace('\n', ''))
                        seq.append(a4[index][:extractNum])
                        index += 1
            G = p.generate_graph(seq, min_ld=min_ldVal, \
                max_ld=max_ldVal, sc=scVal)
    	
            degs = p.generate_degrees(seq, min_ld=1, max_ld=1, sc=scVal)
    
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
                        j += 1
    	
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
    def write():
        """
        info: write the results to txt files
        input: -
        output: -
        """
        
        global cPre
        global cPost
        global clustersizesPre
        global clustersizesPost
        global GnamesHist1Pre
        global GnamesHist1Post

        """
        info: write the results as txt-files
        input: - 
        output: - 
        """
        
        text_file = open("txt/cPre.txt", "w")
        for i in range(len(cPre)):
            text_file.write(str("\n " + str(cPre[i])))
        text_file.close()
    
        text_file = open("txt/cPost.txt", "w")
        for i in range(len(cPost)):
            text_file.write(str("\n " + str(cPost[i])))
        text_file.close()
    
        text_file = open("txt/clustersizesPre.txt", "w")
        for i in range(len(clustersizesPre)):
            text_file.write(str("\n " + str(clustersizesPre[i])))
        text_file.close()
    
        text_file = open("txt/clustersizesPost.txt", "w")
        for i in range(len(clustersizesPost)):
            text_file.write(str("\n " + str(clustersizesPost[i])))
        text_file.close()
    
        text_file = open("txt/GnamesHist1Pre.txt", "w")
        for i in range(len(GnamesHist1Pre)):
            text_file.write(str("\n " + str(GnamesHist1Pre[i])))
        text_file.close()
    
        text_file = open("txt/GnamesHist1Post.txt", "w")
        for i in range(len(GnamesHist1Post)):
            text_file.write(str("\n " + str(GnamesHist1Post[i])))
        text_file.close()
    
    if __name__ == "__main__":
        scVal = make_scVal()
        # somehow initialize values?
        simulation(scVal)
        write()
