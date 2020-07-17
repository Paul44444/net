import numpy as np
import networkx as nx

from imnet import process_strings as p

import os
import pyspark
from scipy.sparse import csr_matrix
from sparkhpc import sparkjob
import findspark

from plotData import PlotDataSingleNet
import funcDictionarySingleNet as fd

def make_scVal():
    """
    info: start making scVal
    input: -
    output: scVal: instance of an spark environment # correct?
    """

    os.environ['SPARK_HOME'] = os.path.join(os.path.expanduser('~'),'spark')

    spark_home_name =  '/cluster/home/richterp/miniconda3/' \
        + 'lib/python3.7/site-packages/pyspark'
    findspark.init(spark_home = spark_home_name)

    findspark.init() # this sets up the paths required to find spark libraries

    coresVal = 128
    sj = sparkjob.sparkjob(ncores=coresVal)
    #sj.wait_to_start()
    scVal = sj.start_spark()
    scVal.parallelize(range(scVal.defaultParallelism)).collect()
    # ---------------------- info: End making scVal -----------------------
    
    return scVal

def write(plotData):
    """
    info: write the results to txt files
    input: plotData
    output: -
    """
    
    cPre = plotData.cPre
    cPost = plotData.cPost
    clustersizesPre = plotData.clustersizesPre
    clustersizesPost = plotData.clustersizesPost
    GnamesHist1Pre = plotData.GnamesHist1Pre
    GnamesHist1Post = plotData.GnamesHist1Post
    
    """
    info: write the results as txt-files
    input: - 
    output: - 
    """
    
    text_file = open("txt/cPre.txt", "w")
    for i in range(len(cPre)):
        text_file.write(str("\n " + str(cPre[i])))
    text_file.close()

    text_file = open("txt/cPost.txt", "w")
    for i in range(len(cPost)):
        text_file.write(str("\n " + str(cPost[i])))
    text_file.close()

    text_file = open("txt/clustersizesPre.txt", "w")
    for i in range(len(clustersizesPre)):
        text_file.write(str("\n " + str(clustersizesPre[i])))
    text_file.close()

    text_file = open("txt/clustersizesPost.txt", "w")
    for i in range(len(clustersizesPost)):
        text_file.write(str("\n " + str(clustersizesPost[i])))
    text_file.close()

    text_file = open("txt/GnamesHist1Pre.txt", "w")
    for i in range(len(GnamesHist1Pre)):
        text_file.write(str("\n " + str(GnamesHist1Pre[i])))
    text_file.close()

    text_file = open("txt/GnamesHist1Post.txt", "w")
    for i in range(len(GnamesHist1Post)):
        text_file.write(str("\n " + str(GnamesHist1Post[i])))
    text_file.close()

if __name__ == "__main__":
    # info: initialize spark environment
    scVal = make_scVal()
 
    # info: initialize plotData object
    plotData = PlotDataSingleNet()

    # info: set parameters
    plotData.N = 10**3
    plotData.min_ldVal = 0
    plotData.max_ldVal = 1
    plotData.extractNum = 18
    plotData.alphaVal = 0.5
    
    # info: perform the simulation and save the results in the plotData object
    plotData = fd.sim(scVal, plotData)
    
    # info: write the plotData to .txt-files
    write(plotData)
