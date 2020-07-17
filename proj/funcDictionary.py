# info: some general functions:

import numpy as np
import networkx as nx

import os

import pyspark
from imnet import process_strings as p

import subprocess
import re
from IPython.display import HTML

import sparkhpc
from sparkhpc import sparkjob
from sparkhpc.sparkjob import LSFSparkJob
import findspark
from scipy.sparse import csr_matrix

from plotData import PlotData
from plotData import InnerDataLevenshtein
from plotData import PlotDataLevenshtein

def make_nets(ls, seq): # We still need seq? What is that?
    """
    info: make a list "nets", where each element "net" is 
        a list again, containing all sequences with a certain 
        length
    input:
        seq: array of nucleic acid sequences 
        ls:  list of length values for each sequence in seq
    output: 
        nets: list of nets, where each element "net" is 
        a list again, containing all sequences with a certain 
        length  
    """

    lsHist = np.histogram(ls, bins = np.arange(0, 120, 3))
    xArgs = lsHist[1][:]

    # keep in mind, that this is the average:

    # info: make empty list of nets:
    nets = list()
    for i in range(len(lsHist[0])+1):
        nets.append(list())

    # info: insert every sequence in the net for its size.
    #     Thus all sequences with one size are in one net
    for seqEl in seq:
        seqElIndex = int((len(seqEl) - lsHist[1][0])/3)
        nets[seqElIndex].append(seqEl)
    return nets
def loadSequence(step, plotData):
    """
    info: - load the nucleic acid sequences, generated from SONIA 
        (and stored in a file 'pre.txt' or 'post.txt')
          - cut of all acids after a certain length, defined by 
              the threshold "extractNum"
          - store the sequences in the list "seq" and the lengths of the 
        the sequences in "ls"
    input: step: 0 -> data before the Thymus selection (load from pre.txt)
                 1 -> data after the Thymus selection (load from post.txt)
    output: a: list, containing all the loaded data
        a4: list, containing the nucleic acid sequences
        seq: list, containing the nucleic acid sequences first acids until 
            the upper threshold "extractNum"
    """
    # info: define filename
    if step == 0:
        filename = 'pre.txt'
    if step == 1:
        filename = 'post.txt'

    # info: make variables and lists as empty or zero objects
    index = 0
    a = list()
    a4 = list()
    seq = list()
    ls = list() # right place to define ls?

    # info: opening the list of generated sequences 
    # info: (sequences generated done with SONIA, 
    # info: which simulates VDJ recombination)
    
    with open(filename) as f:
        for line in f.readlines():
            if index < plotData.N:
                a.append(line.split('\t'))
                # info: attach the fourth element  to a4
                a4.append(a[index][3].replace('\n', ''))
                seq.append(a4[index][:plotData.extractNum])
                ls.append(len(seq[index]))
                
                index += 1
    return a, a4, seq, filename, ls

def make_sub_graphs(G):
    """
    info: make list of connected subgraphs of G (subgraph with the highest number of nodes) 
    input: G: graph
    output: sub_graphs: list of subgraphs, sorted according to size
    """
    # info: make sorted list of subgraphs
    sub_graphs = sorted(list(G.subgraph(c) for c in nx.connected_components(G)), key = len, reverse = True)


    # info: if sub_graphs is empty , make a base graph
    if len(sub_graphs) == 0:
        sub_graphs = list()
        sub_graphs.append(nx.Graph())
        sub_graphs[0].add_node('FillNode')

    return sub_graphs

def biggest_sub_graph(sub_graphs):
    """
    info: choose the biggest sub_graph
    input: sub_graphs: list of graphs
    output: GSub: biggest subgraph in sub_graphs
    """
    # info: setting values n, maxIndex, maxValue
    #     maxValue: number of nodes of the biggest subgraph
    #     maxIndex: index of the biggest subgraph

    n = len(sub_graphs) # info: number of sub_graphs
    maxIndex = -1 # info: will become index of the biggest found sub_graph
    maxValue = -1 # info: will become the size of the biggest found sub_graph

    # info: find the value of the biggest subgraph and its index
    for ii in range(n):
        if len(list(sub_graphs[ii])) > 0:
            if len(sub_graphs[ii].nodes()) > maxValue:
                maxValue = len(sub_graphs[ii].nodes())
                maxIndex = ii
    # info: GSub: biggest subgraph
    GSub = sub_graphs[maxIndex]
    return GSub

def append_zero(innerData):
    """
    info: append 0 to all members of an innerData - object
    input: innerData: an object, containing all the important network properties
    output: innerData: new object, containing the updated members
    """

    innerData.clustersizes.append(0)
    innerData.diameters.append(0)
    innerData.centers.append(0)
    innerData.eccentrities.append(0)
    innerData.degreeMean.append(0)
    return innerData

def append_values(innerData, GSub, G):
    """
    info: calculate the network properties of a graph "GSub" and append them to the corresponding lists in the innerData object
    input: innerData: object, that stores  network properties of many graphs in lists
    output: innerData: new object with updated lists
    """
    innerData.clustersizes.append(len(GSub.nodes())/len(G.nodes()))
    innerData.diameters.append(nx.diameter(GSub))
    centerList = nx.center(GSub)
    innerData.centers.append(centerList[0])
    innerData.eccentrities.append(0)

     # info: calculate the mean degree
    innerData.degreeMean.append(degree_mean(GSub))
    return innerData

def mean_and_error_of(plotData):
    """
    info: calculate the average values of the network properties, using the data in "plotData"
    input: plotData
    output: plotData with updated members
    """
    # info: calculate the Means and the Errors
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

    lAll = len(plotData.clustersizesAllArray)

    for i in range(len(plotData.clustersizesAllArray)):
        clustersizesAllMean += np.divide(plotData.clustersizesAllArray[i],lAll)
        diametersAllMean += np.divide(plotData.diametersAllArray[i],lAll)
        #centersAllMean += np.divide(centersAllArray[i],lAll)
        #eccentritiesAllMean += np.divide(eccentritiesAllSumArray[i],lAll)
        degreeMeanAllMean += np.divide(plotData.degreeMeanAllArray[i],lAll)



    for i in range(len(plotData.clustersizesAllArray)):
        clustersizesAllDifSquare += np.power(plotData.clustersizesAllArray[i] \
            - clustersizesAllMean, 2)
        diametersAllDifSquare += np.power(plotData.diametersAllArray[i] \
            - diametersAllMean, 2)
        #centersAllSumSquare += np.power(centersAllArray[i], 2)
        #eccentritiesAllSumSquare += np.power(eccentritiesAll[i], 2)
        degreeMeanAllDifSquare += np.power(plotData.degreeMeanAllArray[i] \
            - degreeMeanAllMean, 2)

    plotData.clustersizesAllErr = np.sqrt(np.divide( \
        clustersizesAllDifSquare,(lAll - 1)))
    plotData.diametersAllErr = np.sqrt(np.divide( \
        diametersAllDifSquare,(lAll - 1)))
    #centersAllSumSquare = np.sqrt(np.divide( \
    #    centersAllSumSquare,(lAll - 1)))
    #eccentritiesAllSumSquare = np.sqrt(np.divide( \
    #    eccentritiesAllSumSquare,(lAll - 1)))
    plotData.degreeMeanAllErr = np.sqrt(np.divide( \
        degreeMeanAllDifSquare,(lAll - 1)))
    # Shouldn't we also set the Mean properties?

    return plotData

def make_all_data(plotData, innerData, sample): # check description
    """
    info: calculate the sum of the clusterproperties of innerData and 
        plotData (thus the mean over all samples can be calculated later) # right? # Where is the normalization?
    input: plotData: object, storing the network properties
        innerData: object, storing the network properties for one sample # right?
        sample: the current sample # right? Or better "samples" as input? Where is it used?
    output: plotData: 
    """

    plotData.clustersizesAllArray.append(innerData.clustersizes)
    plotData.diametersAllArray.append(innerData.diameters)
    plotData.centersAllArray.append(innerData.centers)
    plotData.eccentritiesAllArray.append(innerData.eccentrities)
    plotData.degreeMeanAllArray.append(innerData.degreeMean)
    
    return plotData

def convert_to_amino_acids(plotData, innerData): # check description
    """
    info: convert lengths to the aminoacids
    input: plotData, innerData: objects, that store network properties in list # in more detail perhaps
    output: plotData: object, that stores the network properties, now with updated members
    """

    xArgsNew = list()
    clustersizesNew = list()
    diametersNew = list()
    eccentritiesNew = list()
    degreeMeanNew = list()

    for i in range(len(innerData.xArgs)):
        if i%3 == 0:
            xArgsNew.append(innerData.xArgs[i])
            clustersizesNew.append(innerData.clustersizes[i])
            diametersNew.append(innerData.diameters[i])
            eccentritiesNew.append(innerData.eccentrities[i])
            degreeMeanNew.append(innerData.degreeMean[i])

    plotData.clustersizesAllArray.append(clustersizesNew)
    plotData.diametersAllArray.append(diametersNew)
    #plotData.centersAllArray.append(centers)
    plotData.eccentritiesAllArray.append(eccentritiesNew)
    plotData.degreeMeanAllArray.append(degreeMeanNew)
    plotData.xArgsAllArray.append(xArgsNew)
    
    return plotData # that belongs here, right?

def degree_mean(GSub):
    """
    info: calculate the average degree in the graph GSub
    input: GSub: graph
    output: deg: average degree number (real number)
    """
    deg = 0
    degs = GSub.degree()
    degs = list(degs)
    for el in degs:
        deg += el[1]/(len(degs))
    return deg

def makeDegreeDistribution(G): # I think the name does not describe, what that actually does; better change name
    """
    info: calculate a list, which contains the sizes (number of nodes) of each connected subgraph (thus each cluster)
    input: G: graph
    output: clustersizes: list with the lengths of all clusters in G
    """

    # info: make the degree distribution
    a = G.degree()
    b = list(a)
    c = list()
    for i in range(len(b)):
        # what is this element? ...; Is that later used?
        c.append(b[i][1])

        # info: make the clusters, clustersizes
    clusters = list(nx.connected_components(G))
    clustersizes = list()
    for i in range(len(clusters)):
        clustersizes.append(len(clusters[i]))
    return clustersizes, c