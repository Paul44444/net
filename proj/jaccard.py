"""
info (this is all done in the sim-function, the other functions don't do scientific analysis):
    - choose all DNA strains with a certain length l and construct a network, only from 
    these strains;
    - investigate network properties
    - analyze the results over different lengths l.
    - use the JACCARD DISTANCE
"""

from plotData import PlotDataLevenshtein
import funcDictionaryJaccard as fd

def write(step, plotData):
    """
    info: write data
    input: step - 0 if before Thymus selection, 1 if after Thymus 
        selection
    output: -
    """	

    xArgsName = plotData.xArgsName
    clustersizesName = plotData.clustersizesName
    clustersizesAllErrName = plotData.clustersizesAllErrName
    diametersName = plotData.diametersName
    diametersAllErrName = plotData.diametersAllErrName
    eccentritiesName = plotData.eccentritiesName
    degreeMeanName = plotData.degreeMeanName
    degreeMeanAllErrName = plotData.degreeMeanAllErrName

    xArgs = plotData.xArgs
    clustersizes = plotData.clustersizes
    clustersizesAllErr = plotData.clustersizesAllErr
    diameters = plotData.diameters
    diametersAllErr = plotData.diametersAllErr
    eccentrities = plotData.eccentrities
    degreeMean = plotData.degreeMean
    degreeMeanAllErr = plotData.degreeMeanAllErr

    xArgsName = str('txt/' + 'lenNet2_xArgs_' + str(step) + '.txt')
    clustersizesName = str('txt/' + 'lenNet2_clustersizes_' + str(step) \
        + '.txt')
    clustersizesAllErrName = str('txt/' + 'lenNet2_clustersizesAllErr_' \
        + str(step) + '.txt')
    diametersName = str('txt/' + 'lenNet2_diameters_' + str(step) \
        + '.txt')
    diametersAllErrName = str('txt/' + 'lenNet2_diametersAllErr_' \
        + str(step) + '.txt')
    eccentritiesName = str('txt/' + 'lenNet2_eccentrities_' + str(step) \
        + '.txt')
    degreeMeanName = str('txt/' + 'lenNet2_degreeMean_' + str(step) \
        + '.txt')
    degreeMeanAllErrName = str('txt/' + 'lenNet2_degreeMeanAllErr_' + str(step) \
        + '.txt')
    
    text_file = open(xArgsName, "w")
    for i in range(len(xArgs)):
        text_file.write(str("\n " + str(xArgs[i])))
    text_file.close()
    	
    text_file = open(clustersizesName, "w")
    for i in range(len(clustersizes)):
        text_file.write(str("\n " + str(clustersizes[i])))
    text_file.close()

    text_file = open(clustersizesAllErrName, "w")
    for i in range(len(clustersizesAllErr)):
        text_file.write(str("\n " + str(clustersizesAllErr[i])))
    text_file.close()
    
    text_file = open(diametersName, "w")
    for i in range(len(diameters)):
        text_file.write(str("\n " + str(diameters[i])))
    text_file.close()
    
    text_file = open(diametersAllErrName, "w")
    for i in range(len(diametersAllErr)):
        text_file.write(str("\n " + str(diametersAllErr[i])))
    text_file.close()
    
    """
    text_file = open(???, "w")
    for i in range(len(centers)):
        text_file.write(str("\n " + str(centers[i])))
    text_file.close()
    """
    text_file = open(eccentritiesName, "w")
    for i in range(len(eccentrities)):
        text_file.write(str("\n " + str(eccentrities[i])))
    text_file.close()

    text_file = open(degreeMeanName, "w")
    for i in range(len(degreeMean)):
        text_file.write(str("\n " + str(degreeMean[i])))
    text_file.close()
    
    text_file = open(degreeMeanAllErrName, "w")
    for i in range(len(degreeMeanAllErr)):
        text_file.write(str("\n " + str(degreeMeanAllErr[i])))
    text_file.close()
if __name__ == "__main__":
    # info: make no scVal, because it is not needed
    scVal = -1
    
    for step in range(2):
        # info: initialize plotData object
        plotData = PlotDataLevenshtein()
        
        # info: set important parameters
        #plotData.Ns = [10**2, 2*10**2, 3*10**2, 5*10**2, 10**3]
        # info: Don't set plotData.N = [1000], that will give an error, do plotData.N = 1000 instead
        plotData.N = 10**3

        #plotData.extractNum = 6#18 #6
        plotData.samples = 5# usually: 6
        #plotData.maxValIndices = [1, 2, 3, 4, 5]
        
        # info: set "unimportant" parameters
        plotData.lenVals = list()
        for i in range(2):
            plotData.lenVals.append(0)
        plotData.itsMax = 10**3  # What's that?
        
        # info: jaccard distance is always in the range [0,1], 
        #     thus a maximum distance of e.g. 2 would make no sense, 
        #     that would always be fulfilled:
        plotData.maxDist = 0.05 # What is a good value?
        plotData.maxValue = plotData.maxDist
        
        # info: perform the simulation and save the results in the plotData object
        plotData = fd.sim(step, plotData, isExtractNum=False)
        
        # info: write the plotData to .txt-files
        #write(step, plotData)
