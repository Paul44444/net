import numpy as np
import networkx as nx # info: this time it is really used

from imnet import process_strings

from plotData import PlotDataManyNets
from plotData import InnerDataManyNets
import funcDictionary as dic

def divide_by_samples_pre(innerDataJobPre, plotData, samples):
    """
    info: divide all network property lists with "Pre" by the number "samples"; 
        thats part of calculating the Mean
    input: 
        innerDataJobPre: object, that stores the network properties in lists
        samples: number of samples
    output: innerDataJobPre: new objected with updates lists 
    """
    
    plotData.eccsPre = np.divide(innerDataJobPre.eccs,samples)
    plotData.diasPre = np.divide(innerDataJobPre.dias,samples)
    plotData.degMaxsPre = np.divide(innerDataJobPre.degMaxs,samples)
    plotData.nodesPre = np.divide(innerDataJobPre.nodes,samples)
    plotData.consPre = np.divide(innerDataJobPre.cons,samples)
    plotData.clustersizesMaxPre \
        = np.divide(innerDataJobPre.clustersizesMax,samples)
    plotData.isConnectedsPre = np.divide(innerDataJobPre.isConnected,samples)

    """
    why not also: 
    innerDataJobPre.clustersizesMaxPre \
                                    += np.divide(clustersizesMax,samples)
                                innerDataJobPre.isConnectedsPre += np.divide(innerDataJobPre.isConnected,samples)
    """
    return plotData

def divide_by_samples_pre_add(innerDataJobPre, plotData, samples):
    """
    info: divide all network property lists  with "Pre" by the number "samples"
        and add that to the current value
        ; thats part of calculating the Mean
    input: 
        innerDataJobPre: object, that stores the network properties in lists
        samples: number of samples
    output: innerDataJobPre: new objected with updates lists 
    """    

    plotData.eccsPre += np.divide(innerDataJobPre.eccs,samples)
    plotData.diasPre += np.divide(innerDataJobPre.dias,samples)
    plotData.degMaxsPre += np.divide(innerDataJobPre.degMaxs,samples)
    plotData.nodesPre += np.divide(innerDataJobPre.nodes,samples)
    plotData.consPre += np.divide(innerDataJobPre.cons,samples)
    plotData.clustersizesMaxPre \
        += np.divide(innerDataJobPre.clustersizesMax,samples)
    plotData.isConnectedsPre += np.divide(innerDataJobPre.isConnected,samples)
    return plotData

def divide_by_samples_post(innerDataJobPre, plotData, samples):
    """
    info: divide all network property lists  with "Post" by the number "samples"; 
        thats part of calculating the Mean
    input: 
        innerDataJobPre: object, that stores the network properties in lists
        samples: number of samples
    output: innerDataJobPre: new objected with updates lists 
    """
    plotData.eccsPost = np.divide(innerDataJobPre.eccs,samples)
    plotData.diasPost = np.divide(innerDataJobPre.dias,samples)
    plotData.degMaxsPost = np.divide(innerDataJobPre.degMaxs,samples)
    plotData.nodesPost = np.divide(innerDataJobPre.nodes,samples)
    plotData.consPost = np.divide(innerDataJobPre.cons,samples)
    plotData.clustersizesMaxPost \
        = np.divide(innerDataJobPre.clustersizesMax,samples)
    plotData.isConnectedsPost = np.divide(innerDataJobPre.isConnected,samples)
    return plotData

def divide_by_samples_post_add(innerDataJobPre, plotData, samples):
    """
    info: divide all network property lists with "Post" by the number "samples"; 
        and add that to the current value
        thats part of calculating the Mean
    input: 
        innerDataJobPre: object, that stores the network properties in lists
        samples: number of samples
    output: innerDataJobPre: new objected with updates lists 
    """
    plotData.eccsPost += np.divide(innerDataJobPre.eccs,samples)
    plotData.diasPost += np.divide(innerDataJobPre.dias,samples)
    plotData.degMaxsPost += np.divide(innerDataJobPre.degMaxs,samples)
    plotData.nodesPost += np.divide(innerDataJobPre.nodes,samples)
    plotData.consPost += np.divide(innerDataJobPre.cons,samples)
    plotData.clustersizesMaxPost \
        += np.divide(innerDataJobPre.clustersizesMax,samples)
    plotData.isConnectedsPost += np.divide(innerDataJobPre.isConnected,samples)
    return plotData

def sim(scVal, plotData, isExtractNum):
    """
    info: perform the simulation and write the results in the plotData object, which is finally returned
    input: scVal: spark context
        plotData: PlotData object, that contains the important data and parameters;
            for more detail see documentation in plotData.py
        isExtractNum: Bool, that says, if only a limited number of 
            letters should be extracted;
    output: 
        plotData: PlotData object with updated members 
        
    """
    for maxValIndex in range(len(plotData.maxValIndices)):
            maxVal = plotData.maxValIndices[maxValIndex]
            plotData.max_ldVal = maxVal
        	
            for sample in range(plotData.samples):
                """
                if output is wanted in order to see progress:
                print("\n sample/samples: ", (sample+1), "/ ", samples, 
                    "; maxValIndex: ", maxValIndex+1, "/ ", len(maxValIndices))
                """
                for step in range(2):
                    innerDataManyNets = InnerDataManyNets()
	
                    for i in range(len(plotData.Ns)):
                        # info: load data
                        a, a4, seq, filename, _ = dic.loadSequence(step, plotData, i, isExtractNum=isExtractNum)
                        
                        # info: generate graph
                        
                        G = process_strings.generate_graph(seq, min_ld=plotData.min_ldVal, \
                            max_ld=plotData.max_ldVal, sc=scVal)
                        
                        # info: make degrees and clusters (?)
                        # why is that called "makeDegreeDistributio"?
                        clustersizes, c  = dic.makeDegreeDistribution(G)
                        
                        innerDataManyNets.nodes.append(G.number_of_nodes())
                        innerDataManyNets.degMaxs.append(max(c))
                        innerDataManyNets.cons.append(nx.is_connected(G))
    
                        if nx.is_connected(G):
                            #eccs.append(nx.eccentricity(G)) - I think, 
                            # info: that is computationally expensive
                            #dias.append(nx.diameter(G, nx.eccentricity(G)))
                            innerDataManyNets.clustersizesMax.append(max(clustersizes))
                            innerDataManyNets.isConnected.append(1)
                        else:
                            #eccs.append(-1)
                            #dias.append(-1)
                            innerDataManyNets.clustersizesMax.append(max(clustersizes))
                            innerDataManyNets.isConnected.append(0)
		    
                    if step == 0:
                        if sample == 0:
                            plotData = divide_by_samples_pre(innerDataManyNets, plotData, plotData.samples)
                        else:
                            plotData = divide_by_samples_pre_add(innerDataManyNets, plotData, plotData.samples)	
				
                    if step == 1:
                        if sample == 0:
                            plotData = divide_by_samples_post(innerDataManyNets, plotData, plotData.samples)
                        else:
                            plotData = divide_by_samples_post_add(innerDataManyNets, plotData, plotData.samples)
    
    # still have to kind of check that part
    """
    plotData.clustersizesMaxPre = clustersizesMaxPre 
    plotData.clustersizesMaxPost = clustersizesMaxPost
    plotData.degMaxsPre = degMaxsPre
    plotData.degMaxsPost = degMaxsPost
    plotData.Ns = Ns
    plotData.isConnectedsPre = isConnectedsPre
    plotData.isConnectedsPost = isConnectedsPost
    plotData.clustersizesMaxPost = clustersizesMaxPost
    """
    return plotData
