import numpy as np
import networkx as nx

import pyspark
from imnet import process_strings as p

import textdistance as td # better cite that

from plotData import PlotData
from plotData import InnerDataLevenshtein

import funcDictionary as dic

# Check, if the description correspond to the functions

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

def sim(step, plotData): 
    """
    info: perform the simulation
    input: step (0, if pre selection; 1, if post selection)
    output: -
    """
    
    itsMax = 10**3
    # info: jaccard distance is always in the range [0,1], 
    #     thus a maximum distance of e.g. 2 would make no sense, 
    #     that would always be fulfilled:
   
    # initially, here they made all the plotData.[...] = 0
    
    for sample in range(plotData.samples):		
        innerData = InnerDataLevenshtein()
        innerData.xArgs = list()
        
        # info: load data
        a, a4, seq, filename, ls = dic.loadSequence(step, plotData)
        # info: sort into a list, where each entry contains all strains with a certain length l
        nets = dic.make_nets(ls, seq)
        
        # What are interesting values to investigate?
    
        clusterMinLen = 10	
        for i in range(len(nets)):
            if len(nets[i]) > clusterMinLen:
                G = makeNet(nets[i], plotData.maxDist)
     	
                # info: make subgraphs
                sub_graphs = dic.make_sub_graphs(G)
  
                # info: GSub: biggest subgraph
                GSub = dic.biggest_sub_graph(sub_graphs)
               
                # append the values to the corresponding list:		
                innerData = dic.append_values(innerData, GSub, G)
                #innerData.xArgs.append(plotData.lenVals[i])
            else: 
                innerData = dic.append_zero(innerData)
                #innerData.xArgs.append(plotData.lenVals[i])
        plotData = dic.convert_to_amino_acids(plotData, innerData)
    plotData = dic.mean_and_error_of(plotData) 
    return plotData

