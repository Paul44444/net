import networkx as nx

from imnet import process_strings as p

from plotData import InnerDataLevenshtein 

import funcDictionary as dic

def make_graph(nets_i, min_ld, max_ld, scVal):
    """
    info: use imnet in order to generate a network from the strains 
        in "nets_i" (usually an element of nets)  
    input: nets_i: list of DNA strains with same length (usually
            an element of net) # check that
           min_ld: minimum Levenshtein 
               distance to make an edge, usually 0 # right?
           max_ld: maximum Levenshtein 
               distance to make an edge
           scVal: sparkContext (only important to increase processing 
               speed, no scientific relevance)
    output: G: graph, that has been generated; every node denotes one 
               DNA strain; an edge is drawn between two nodes, if the 
               Levenshtein distance is between min_ld, 
               max_ld (usually min_ld is 0)# right? 
    """
    G = p.generate_graph(nets_i, min_ld, max_ld, sc = scVal)
    if len(G.nodes()) == 0:
        G = nx.Graph()
        G.add_node("ZeroNode")
    return G

def sim(step, scVal, plotData, isExtractNum):

    """
    info: kind of, perform the total simulation
    input: step (0, if pre selection; 1, if post selection),  
        scVal: sparkContext (only important to increase processing 
            speed, no scientific relevance)
        plotData: PlotData object, that contains the important data and parameters;
            for more detail see documentation in plotData.py
        isExtractNum: Bool, that says, if only a limited number of 
            letters should be extracted;
    output: plotData: PloData object with updated members
    """
 
    # ... (see lenNet.py)
    for sample in range(plotData.samples):
        # info: initialize the analyzed quantities
        innerData = InnerDataLevenshtein()
        
        # for lsHist: # we still have to achieve, that the intervals have the 
        #     same limits for all samples
        a, a4, seq, filename, ls = dic.loadSequence(step, plotData, isExtractNum=isExtractNum)
        print("\n list(ls): ", list(ls))  
        # info: make nets
        nets = dic.make_nets(ls, seq)
       
        for i in range(len(nets)):
            if len(nets[i]) > plotData.clusterMinLen:
        	       # info: generate graph	
                G = make_graph(nets[i], min_ld=plotData.min_ldVal, max_ld=plotData.max_ldVal, scVal = scVal)
 
                # info: make subgraphs
                sub_graphs = dic.make_sub_graphs(G)
 
                # info: GSub: biggest subgraph
                GSub = dic.biggest_sub_graph(sub_graphs)
                	
                # append the values to the corresponding list:	
                innerData = dic.append_values(innerData, GSub, G)
            else: 
                innerData = dic.append_zero(innerData)
        plotData = dic.make_all_data(plotData, innerData, sample)
    plotData = dic.mean_and_error_of(plotData)
    return plotData
