"""
info (this is all done in the sim()-function, the other functions don't do scientific analysis): 
    - choose all DNA strains with a certain length l and construct a network, only from 
    these strains;
    - investigate network properties
    - analyze the results over different lengths l.
    - use the LEVENSHTEIN DISTANCE
"""

import os
import pyspark

from sparkhpc import sparkjob
import findspark

from plotData import PlotDataLevenshtein
import funcDictionaryLevenshtein as fd

def make_scVal():
    """
    info: initialize the spark environment
    input: -
    output: scVal
    """
    os.environ['SPARK_HOME'] = os.path.join(os.path.expanduser('~'),'spark')

    findspark.init(spark_home = '/cluster/home/richterp/miniconda3/lib/python3.7/site-packages/pyspark')

    findspark.init() # this sets up the paths required to find spark libraries

    coresVal = 128
    sj = sparkjob.sparkjob(ncores=coresVal)
    #sj.wait_to_start()
    scVal = sj.start_spark()
    scVal.parallelize(range(scVal.defaultParallelism)).collect()

    return scVal

def write(step, plotData):
        """
        info: save data .txt-file
        input: step - 0 if before Thymus selection, 1 if after Thymus selection
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

        xArgsName = str('txt/' + 'lenNet1_xArgs_' + str(step) + '.txt')
        clustersizesName = str('txt/' + 'lenNet1_clustersizes_' \
            + str(step) + '.txt')
        clustersizesAllErrName = str('txt/' + 'lenNet1_clustersizesAllErr_' \
            + str(step) + '.txt')
        diametersName = str('txt/' + 'lenNet1_diameters_' + str(step) \
            + '.txt')
        diametersAllErrName = str('txt/' + 'lenNet1_diametersAllErr_' \
            + str(step) + '.txt')
        eccentritiesName = str('txt/' + 'lenNet1_eccentrities_' \
            + str(step) + '.txt')
        degreeMeanName = str('txt/' + 'lenNet1_degreeMean_' \
            + str(step) + '.txt')
        degreeMeanAllErrName = str('txt/' + 'lenNet1_degreeMeanAllErr_' \
            + str(step) + '.txt')
    
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
        text_file = open("lenNet1_centers.txt", "w")
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
    # info: initialize spark environment
    scVal = make_scVal()
    
    # info: step == 0 -> analysis before Thymus selection
    # info: step == 1 -> analysis after Thymus selection
    for step in range(2):
        # info: initialize plotData object
        plotData = PlotDataLevenshtein()

        # info: set parameters
        plotData.clusterMinLen = 10
        plotData.N = 10**3
        plotData.min_ldVal = -1
        plotData.maxVal = 1
        plotData.max_ldVal = plotData.maxVal

        # info: if only a certain number of acids should be extracted, 
        #     set isExtractNum = True when calling the sim() function
        #     and set plotData.extractNum to the desired value
        #plotData.extractNum = 15#18 #6

        plotData.samples = 2# usually: 6

        # info: perform the simulation and save the results in the plotData object
        plotData = fd.sim(step, scVal, plotData, isExtractNum=False)

        # info: write the plotData to .txt-files
        #write(step, plotData)
	
