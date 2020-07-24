import numpy as np
import networkx as nx

from imnet import process_strings as p  # used?

def make_nets(ls, seq): 
    """
    info: make a list "nets", where each element "net" is 
        a list again, containing all sequences with a certain 
        length
    input:
        ls:  list of length values for each sequence in seq
        seq: array of nucleic acid sequences 
    output: 
        nets: list of nets, where each element "net" is 
        a list again, containing all sequences with a certain 
        length  
    """

    lsHist = np.histogram(ls, bins = np.arange(0, 120, 3))
    xArgs = lsHist[1][:]

    # info: make empty list of nets:
    nets = list()
    for i in range(len(lsHist[0])+1):
        nets.append(list())

    # info: insert every sequence in the net for its size.
    #     Thus all sequences with one size are in one net
    #     Note that dividing by 3 is used to convert 
    #     nucleic acids to amino acids.
    for seqEl in seq:
        seqElIndex = int((len(seqEl) - lsHist[1][0])/3)
        nets[seqElIndex].append(seqEl)
    return nets
def loadSequence(step, plotData, i = -1, isExtractNum = True):
    """
    info: - load the nucleic acid sequences, generated from SONIA 
        (and stored in a file 'pre.txt' or 'post.txt')
          - cut of all acids after a certain length, defined by 
              the threshold "extractNum"
          - store the sequences in the list "seq" and the lengths of the 
        the sequences in "ls"
    input: step: 0 -> data before the Thymus selection (load from pre.txt)
                 1 -> data after the Thymus selection (load from post.txt)
        plotData: PlotData object, that contains the important data and parameters;
            for more detail see documentation in plotData.py
        i: int number of letters to be extracted from each string, e.g. if i = 18,
            then only the first 18 letters from each string are extracted, the rest
            is ignored
        isExtractedNum: Bool, that says, if only a limited number of 
            letters should be extracted; Thus, if isExtractNum == False, it makes no
            sense, to set i > -1, because everything is extracted anyway.
            If isExtractNum == True, i must be set to a certain value > -1.
    output: a: list, containing all the loaded data
        a4: list, containing the nucleic acid sequences
        seq: list, containing the nucleic acid sequences first acids until 
            the upper threshold "extractNum"
        filename: string (either 'pre.txt' or 'post.txt')
        ls: list of length values for each sequence in seq
    """
    # info: define filename
    if step == 0:
        filename = 'pre.txt'
    if step == 1:
        filename = 'post.txt'

    # info: check, if plotData has an Ns-array, then choose N = plotData.Ns[i]; alternatively choose N = plotData.N[i]
    if i > -1:
        try: 
            N = plotData.Ns[i]
        except: 
            print("\n Could not load element plotData.Ns[i]. Perhaps it does not exist?")
            N = -1
    else:
        N = plotData.N

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
            if index < N:
                a.append(line.split('\t'))
                # info: attach the fourth element  to a4
                #     the txt data consists of 4 columns. The 4th column
                #     contains the string, which are relevant
                #     for our analysis. In order to load
                #     them, we extract the fourth
                #     element of each line.
                a4.append(a[index][3].replace('\n', ''))
                if isExtractNum == True:
                    seq.append(a4[index][:plotData.extractNum])
                else:
                    seq.append(a4[index][:])
                ls.append(len(seq[index]))
                
                index += 1
    return a, a4, seq, filename, ls

def make_sub_graphs(G):
    """
    info: make list of connected subgraphs of G (subgraph with the largest number of nodes) 
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

def largest_sub_graph(G):
    """
    info: choose the largest component
    input: G: a graph
    output: Gc: largest component of G as subgraph
    """
    Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
    Gc = G.subgraph(Gcc[0])
    return Gc
    
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
    input: plotData: PlotData object, that contains the important data and parameters;
            for more detail see documentation in plotData.py
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
    input: plotData: PlotData object, that contains the important data and parameters;
            for more detail see documentation in plotData.py
        innerData: objects, that store network properties in list # in more detail perhaps
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
    info: calculate the mean degree in the graph GSub
    input: GSub: graph
    output: degree_mean: mean degree number (real number)
    """
   
    degrees = [el[1] for el in GSub.degree()]
    degree_mean = sum(degrees)/len(degrees)
    return degree_mean

def makeDegreeDistribution(G): # I think the name does not describe, what that actually does; better change name
    """
    info: calculate a list, which contains the sizes (number of nodes) of each connected subgraph (thus each cluster)
    input: G: graph
    output: clustersizes: list with the lengths of all clusters in G
        c: list of degree values of each node
    """

    # info: make a list of degrees of all nodes
    a = G.degree()
    
    # info: b: list, where each element is an array: element 0 is the string and element 1 is the corresponding degree value
    b = list(a)

    # info: make list c, which only contains the degree values
    c = list()
    
    c = [el[1] for el in b]
    #for i in range(len(b)):
    #    # what is this element? ...; Is that later used?
    #    c.append(b[i][1])
    #    
    
    # info: make the clusters, clustersizes    
    clusters = list(nx.connected_components(G))
    #clustersizes = list()
    #for i in range(len(clusters)):
    #     clustersizes.append(len(clusters[i]))
    clustersizes = [cluster.size for cluster in clusters]
    return clustersizes, c

