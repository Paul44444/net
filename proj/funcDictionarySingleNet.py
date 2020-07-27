# info: dictionary of functions

from imnet import process_strings as p

from plotData import PlotDataSingleNet
import funcDictionary as dic

import pandas as pd
# Check, if the description correspond to the functions

def calculateProperties(G, c):
     # info: make Gnames -> distribution of number of each strain
    """
    info:  calculate the network properties for a graph G
    input: G: graph, c: ist of degree values of G
    output: 
        c: list of degree values of G; actually the function is just 
            outputting the input c as the output again, doing nothing 
            with it
        (clustersizes: ??? (currently not returned, why not?))
        GnamesHist1: list, containing the frequencies of the strains
    """

    # list of strains in G
    Gnames = list(G) 
    B = pd.Series(Gnames).value_counts()
    GnamesHist1 = list(B)
    """
    for i in range(len(Gnames)):
        print("\n step B; i: ", i)
        
        
        j = 0
        # info: I think he wants to remove all numbers, so that only letters remain ( I think,
        #     in the past, where the strings were attached to some numbers, which 
        #     had to be removed first
        while j < len(Gnames[i]):
            try:
                # info: take element the string Gnames[i] and take the letter at index j
                val = int(Gnames[i][j])
                Gnames[i] = Gnames[i][:j] + Gnames[i][(j+1):]
            except ValueError:
                j += 1

        # info: making array GnamesHist; Each element GnamesHist[i] is 
        #     an array again, containing the string at position 0 and 
        #     the frequency at position 1
        
        GnamesHist = list()
        for i in range(len(Gnames)):
            isIn = 0
            
            # info: check, if string already in the GnamesHist array; 
            #     if yes, than add 1 to the frequency value at the
            #     corresponding index
            # 
            #     else: (isIn == 0), append the strain to the GnamesHist array 
            #     and set the frequency to 1

            for j in range(len(GnamesHist)):
                #if GnamesHist[j][0] == Gnames[i]:
                if True:
                    GnamesHist[j][1] += 1
                    isIn = 1
            if isIn == 0:
                GnamesHist.append([Gnames[i], 1])
        
        # info: making array GnamesHist1, which just contains all frequency numbers
        GnamesHist1 = list()
        
        for i in range(len(GnamesHist)):
            GnamesHist1.append(GnamesHist[i][1])
        # info: return the values, can be assigned to the corresponding -post and corresponding -pre variables
    """
    return c, GnamesHist1

def sim(scVal, plotData, isExtractNum): 
    """
    info: perform the simulation and write the results in the plotData object, which is finally returned
    input: scVal: spark context
        plotData: PlotData object, that contains the important data and parameters;
            for more detail see documentation in plotData.py
        isExtractNum: Bool, that says, if only a limited number of 
            letters should be extracted;
    output: plotData: PlotData object with updated members 
    """
    # info: step == 0 -> analysis before Thymus selection
    # info: step == 1 -> analysis after Thymus selection
    for step in range(2):        
        # info: load data
        a, a4, seq, filename, _ = dic.loadSequence(step, plotData, isExtractNum=isExtractNum)
        # info: create graph from data
        G = p.generate_graph(seq, min_ld=plotData.min_ldVal, \
            max_ld=plotData.max_ldVal, sc=scVal)
        
        # info: calculate degrees 
        # check the description above
        degs = p.generate_degrees(seq, min_ld=plotData.min_ldVal, max_ld=plotData.max_ldVal, sc=scVal)

        index = 0 # What is that good for?
        indexMax = 10 # probably maximum extraction index, but it is used nowhere
   
        # info: clustersizes and c (which is the list of degree values of all the nodes)
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
