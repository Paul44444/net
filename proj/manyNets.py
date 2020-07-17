import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

import pyspark
from imnet import process_strings as p

import os
from sparkhpc.sparkjob import LSFSparkJob
import findspark
import pyspark
from scipy.sparse import csr_matrix
from sparkhpc import sparkjob

from plotData import PlotDataManyNets
import funcDictionaryManyNets as fd

def make_scVal():
    """
    info: initilize spark environment; make scVal
    input: -
    output: -
    """
    
    os.environ['SPARK_HOME'] = os.path.join(os.path.expanduser('~'),'spark')

    spark_home_string = '/cluster/home/richterp/miniconda3/lib/python3.7/' \
        + 'site-packages/pyspark'
    findspark.init(spark_home=spark_home_string)

    findspark.init() # this sets up the paths required to find spark libraries

    coresVal = 128
    sj = sparkjob.sparkjob(ncores=coresVal)
    #sj.wait_to_start()
    scVal = sj.start_spark()
    scVal.parallelize(range(scVal.defaultParallelism)).collect()

    return scVal 

def write(plotData):
    """
    info: write the results as txt-files
    input: - 
    output: - 
    """
   
    clustersizesMaxPre = plotData.clustersizesMaxPre
    clustersizesMaxPost = plotData.clustersizesMaxPost
    degMaxsPre = plotData.degMaxsPre
    degMaxsPost = plotData.degMaxsPost
    Ns = plotData.Ns
    isConnectedsPre = plotData.isConnectedsPre
    isConnectedsPost = plotData.isConnectedsPost
    clustersizesMaxPost = plotData.clustersizesMaxPost

    name = "txt/clustersizesMaxPre.txt"
    text_file = open(name, "w")
    for i in range(len(clustersizesMaxPre)):
        text_file.write(str("\n " + str(clustersizesMaxPre[i])))
    text_file.close()

    name = "txt/clustersizesMaxPost.txt"
    text_file = open(name, "w")
    for i in range(len(clustersizesMaxPost)):
        text_file.write(str("\n " + str(clustersizesMaxPost[i])))
    text_file.close()

    name = "txt/degMaxsPre.txt"
    text_file = open(name, "w")
    for i in range(len(degMaxsPre)):
        text_file.write(str("\n " + str(degMaxsPre[i])))
    text_file.close()

    name = "txt/degMaxsPost.txt"
    text_file = open(name, "w")
    for i in range(len(degMaxsPost)):
       text_file.write(str("\n " + str(degMaxsPost[i])))
    text_file.close()
    
    name = "txt/Ns.txt"
    text_file = open(name, "w")
    for i in range(len(Ns)):
        text_file.write(str("\n " + str(Ns[i])))
    text_file.close()
     
    name = "txt/isConnectedsPre.txt"
    text_file = open(name, "w")
    for i in range(len(Ns)):
        if len(isConnectedsPre)>i: # find a way to remove that afterwards
            text_file.write(str("\n " + str(isConnectedsPre[i])))

    name = "txt/isConnectedsPost.txt"
    text_file = open(name, "w")
    for i in range(len(Ns)):
        if len(isConnectedsPre)>i: # find a way to remove that afterwards
            text_file.write(str("\n " + str(isConnectedsPost[i])))

    #ydata = np.divide(clustersizesMaxPost, Ns) - should be not commented out

if __name__ == "__main__":
    # info: initialize spark environment
    scVal = make_scVal()

    # info: initialize plotData object
    plotData = PlotDataManyNets()
    
    # info: initialize params
    plotData.Ns = [10**2, 10**3]
    plotData.N = 10**2 # just added, so that it works for now
    #info: number of extracted letters from the DNA sequence 
    plotData.extractNum = 18

    # info: samples = 6 is usual
    plotData.samples = 2

    # info: maximum levenshtein distance
    plotData.maxValIndices = [6] 
   
    plotData.minL = 5 # 4
    plotData.maxL = 10
    plotData.min_ldVal = -1

    # info: perform the simulation and save the results in the plotData object
    plotData = fd.sim(scVal, plotData)

    # info: write the plotData to .txt-files
    write(plotData)
