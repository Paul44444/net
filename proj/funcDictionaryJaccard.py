import networkx as nx

from imnet import process_strings as p

import textdistance as td # better cite that

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
def makeNet(names, maxDist):
    """
    info: make graph, where each node denotes one element of names. 
        names is an array of strings.
        if the jaccard distance between the strings, corresponding 
        to two nodes, is lower than "maxDist", an edge is drawn
    input: names:[String]:  list of strings
        maxDist (real number from 0 to 1): maximum jaccard distance between two strings,
            which is required to form a bond
    output: g: created graph, where each string is a node and two nodes are
        connected via an edge, if there jaccard distance is smaller
        than maxDist
    """
    g = nx.Graph()

    for i in range(len(names)):
        g.add_node(names[i])

    for i in range(len(names)):
        for j in range(len(names)):
            if not (i == j):
                if jaccardDist(names[i], names[j]) < maxDist:
                    g.add_edge(names[i], names[j])                    
    return g

def jaccardDist(name1, name2):
    """
    info: calculate the jaccard distance between the two strings 
        name1, name2
    input: name1:String, name2:String
    output: distance value dist (real number within [0, 1])
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

def sim(step, plotData, isExtractNum): 
    """
    info: perform the simulation
    input: step (0, if pre selection; 1, if post selection), 
        plotData: PlotData object, that contains the important data and parameters;
            for more detail see documentation in plotData.py
        isExtractNum: Bool, that says, if only a limited number of 
            letters should be extracted;
    output: -
    """
    
    #itsMax = 10**3 - probably not relevant
    # info: jaccard distance is always in the range [0,1], 
    #     thus a maximum distance of e.g. 2 would make no sense, 
    #     that would always be fulfilled:
   
    # initially, here they made all the plotData.[...] = 0
    
    for sample in range(plotData.samples):		
        innerData = InnerDataLevenshtein()
        innerData.xArgs = list()
        
        # info: load data
        a, a4, seq, filename, ls = dic.loadSequence(step, plotData, isExtractNum = isExtractNum)
        # info: sort into a list, where each entry contains all strings with a certain length l
        nets = dic.make_nets(ls, seq)
        
        # What are interesting values to investigate?
    
        clusterMinLen = 10	2560
        for i in range(len(nets)):
            if len(nets[i]) > clusterMinLen:
                G = makeNet(nets[i], plotData.maxDist)
     	
                # info: GSub: biggest subgraph
                GSub = dic.largest_sub_graph(G)
               
                # append the values to the corresponding list:		
                innerData = dic.append_values(innerData, GSub, G)
                #innerData.xArgs.append(plotData.lenVals[i])
            else: 
                innerData = dic.append_zero(innerData)
                #innerData.xArgs.append(plotData.lenVals[i])
        plotData = dic.convert_to_amino_acids(plotData, innerData)
    plotData = dic.mean_and_error_of(plotData) 
    return plotData


