# info: dictionary of functions

import numpy as np
import networkx as nx

from imnet import process_strings as p

import os
import pyspark
from scipy.sparse import csr_matrix
from sparkhpc import sparkjob
import findspark

from plotData import PlotDataSingleNet
import funcDictionary as dic

# Check, if the description correspond to the functions

def calculateProperties(G, c):
     # info: make Gnames -> distribution of number of each strain
    """
    info:  calculate the network properties for a graph G
    input: G: graph
    output: 
        cPre: 
        clustersizesPre:
        GnamesHist1Pre:
        cPost:
        clustersizesPost:
        GnamesHist1Post:
    """

    # What's Gnames?
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

        # info: return the values, can be assigned to the corresponding -post and corresponding -pre variables
        return c, GnamesHist1

def sim(scVal, plotData):
    
    # info: step == 0 -> analysis before Thymus selection
    # info: step == 1 -> analysis after Thymus selection
    for step in range(2):
        
        # info: load data
        a, a4, seq, filename, _ = dic.loadSequence(step, plotData)
        # info: create graph from data
        G = p.generate_graph(seq, min_ld=plotData.min_ldVal, \
            max_ld=plotData.max_ldVal, sc=scVal)
        
        # info: calculate degrees 
        # check the description above
        degs = p.generate_degrees(seq, min_ld=plotData.min_ldVal, max_ld=plotData.max_ldVal, sc=scVal)

        index = 0 # What is that good for?
        indexMax = 10 # probably maximum extraction index, but it is used nowhere
   
        # What's c? # What's "Gnames"?
        clustersizes, c  = dic.makeDegreeDistribution(G)
       
        if step == 0:
            # info: pre (before Thymus selection)
            plotData.clustersizesPre = clustersizes
            plotData.cPre, plotData.GnamesHist1Pre = calculateProperties(G, c)
        if step == 1:
            # info: post (after Thymus selection)
            plotData.clustersizesPost = clustersizes
            plotData.cPost, plotData.GnamesHist1Post = calculateProperties(G, c)
        
    return plotData
