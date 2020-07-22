import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go
import matplotlib

from scipy.optimize import curve_fit
from matplotlib import rcParams
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap
from collections import OrderedDict

import imnet
import numpy as np
import pyspark
from imnet import random_strings as r
from imnet import process_strings as p
import math

class jobPlot:
    def setPlotDesign():
        """
        info: set the parameters for the plot etc.
        input: - 
        output: -
        """
        N = 20000
        min_ldVal = 0
        max_ldVal = 1
        extractNum = 18
    
        params = { #'backend': 'ps',
            #'font.family': 'serif',
       	    #'font.serif': 'Latin Modern Roman',
            'font.family': 'sans serif',
            'font.serif': 'Helvetica',
            'font.size': 10,
            'axes.labelsize': 'medium',
            'axes.titlesize': 'medium',
            'legend.fontsize': 'medium',
            'xtick.labelsize': 'small',
            'ytick.labelsize': 'small',
            'savefig.dpi': 15,
            'text.usetex': True
        }
	
        rcParams['axes.labelsize'] = 50
        rcParams['xtick.labelsize'] = 46
        rcParams['ytick.labelsize'] = 46
        rcParams['legend.fontsize'] = 46
        rcParams['font.family'] = 'sans serif'
        rcParams['font.serif'] = ['Helvetica']
        rcParams['text.usetex'] = True
        rcParams['figure.figsize'] = 12, 8
 
        # info: set nice figure sizes
        
        # info: Get this from LaTeX using \showthe\columnwidth:
        fig_width_pt = 245
        # info: Aesthetic ratio: 
        golden_mean = (np.sqrt(5.) - 1.) / 2.
        ratio = golden_mean
        # info: Convert pt to inches
        inches_per_pt = 1. / 72.27
        # info: width in inches
        fig_width = fig_width_pt * inches_per_pt
        # info: height in inches
        fig_height = fig_width*ratio
        fig_size = [fig_width, fig_height]
        rcParams.update({'figure.figsize': fig_size})

        # info: tell matplotlib about your params
        rcParams.update(params)

        # info: define variables etc.
        fig1, ax1 = plt.subplots()
        fig2, ax2 = plt.subplots()
        fig3, ax3 = plt.subplots()
    
        cPre = list()
        clustersizesPre = list()
        GnamesHist1Pre = list()
    
        cPost = list()
        clustersizesPost = list()
        GnamesHist1Post = list()
    
        alphaVal = 0.5
        # info: 0 -> don't show title; 1 -> show title : 
        withTitle = 0
        withParams = 0
    def load(): 
        """
        info: load the data from txt file (this data was generated by the job.py)
        input: -
        output: -
        """
        cPre = np.loadtxt('txt/txt/cPre.txt')
        cPost = np.loadtxt('txt/txt/cPost.txt')
        clustersizesPre = np.loadtxt('txt/txt/clustersizesPre.txt')
        clustersizesPost = np.loadtxt('txt/txt/clustersizesPost.txt')
        GnamesHist1Pre = np.loadtxt('txt/txt/GnamesHist1Pre.txt')
        GnamesHist1Post = np.loadtxt('txt/txt/GnamesHist1Post.txt')
        
        cPreHist = np.histogram(cPre, bins = int(max(cPre) - min(cPre)))
        cPostHist = np.histogram(cPost, bins = int(max(cPost) - min(cPost)))
        clustersizesPreHist = np.histogram(clustersizesPre, 
            bins=int(max(clustersizesPre) - min(clustersizesPre) + 1))
        clustersizesPostHist = np.histogram(clustersizesPost, 
            bins=int(max(clustersizesPost) - min(clustersizesPost) + 1))
        GnamesHist1PreHist = np.histogram(GnamesHist1Pre, 
            bins=int(max(GnamesHist1Pre) - min(GnamesHist1Pre) + 1))
        GnamesHist1PostHist = np.histogram(GnamesHist1Post, 
            bins=int(max(GnamesHist1Post) - min(GnamesHist1Post) + 1))

    # info: define functions
    def func(x, a, b):
        """
        info: polynomial - fitting function
        input: arbitrary real number x
        output: function value, calculated for the argument x
        """        
        return a*np.power(x, -b)
    def digNum(x, dig):
        """ 
        info: convert to decimal number with only one digit before ".".
        Used for representation of a number in the diagram legend;
        used by sci() - function
        
        input: an arbitrary real number x
        output: a string, showing the decimal notation of the number x
        """        

        return str(float(int(x*10**dig))/(10**dig))
    def sci(x, dig = 1):
        """
        info: make scientific notation; used for plotting
            
        input: an arbitrary real number x
        output: a string, showing the scientific notation of the number x
        """

        i = 0
        check = 0
        if x > 0.1 or x == 0.1:
            while check < 1:
                if x < 10**i:
                    check = 1
                    print("\n i: ", i)
                else:
                    i += 1
            # info: make i - 1, so that it is one unit smaller
            # info: than the next higher power of ten, seeing from x
            i -= 1

        if x < 0.1:
            while check < 1:
                if x > 10**i:
                    check = 1
                    print("\n i: ", i)
                else:
                    i -= 1
        # info: x should not be an int, but a float or double
        x = x/10**i
        x = digNum(x, dig) 
        xlabel = str(x) + "$\cdot 10^{" + str(i) + "}$"
        return xlabel

    def removeZero(x): # check if indent is correct
        for i in range(len(x[1][1:])):
            if x[1][1+i] == 0:
                del x[0][i]
                del x[1][1:]
        return x

    def roundTen(x, mode):
        i = 0
        check = 0
        if x > 0.1 or x == 0.1:
            while check < 1:
                if x < 10**i:
                    check = 1
                    print("\n i: ", i)
                else:
                    i += 1
            # info: make i - 1, so that it is one unit smaller
            # info: than the next higher power of ten, seeing from x
            i -= 1

        if x < 0.1:
            while check < 1:
                if x > 10**i:
                    check = 1
                    print("\n i: ", i)
                else:
                    i -= 1
        val = 0.0
        if mode == "Up":
            val = 10**(i+1)
        if mode == "Down":
            val = 10**(i)
        return val
	
    def fit(constFac = 0.2):
        """
        info: model fit of the parameters
        input: -
        output: -
        """
        
        popt1, pcov1 = curve_fit(func, cPreHist[1][1:], cPreHist[0])
        
        cPreHist = removeZero(cPreHist)
        ax1.plot(cPreHist[1][1:], constFac*func(cPreHist[1][1:], *popt1), 
            'r-', label='fit: a=%5.3f, b=%5.3f' % tuple(popt1))

        clustersizesPreHist = removeZero(clustersizesPreHist)
        popt2, pcov2 = curve_fit(func, clustersizesPreHist[1][1:], 
            clustersizesPreHist[0])
        ax2.plot(cPreHist[1][1:], constFac*func(cPreHist[1][1:], *popt2), 
            'r-', label='fit: a=%5.3f, b=%5.3f' % tuple(popt2))

        GnamesHist1PreHist = removeZero(GnamesHist1PreHist)
        popt3, pcov3 = curve_fit(func, GnamesHist1PreHist[1][1:], 
            GnamesHist1PreHist[0])
        ax3.plot(cPreHist[1][1:], constFac*func(cPreHist[1][1:], *popt3), 
            'r-', label='fit: a=%5.3f, b=%5.3f' % tuple(popt3))

    def plot():
        """
        info: plots the results and saves them
        input: -
        output: -
        """

        distY1 = 500.0
        distY2 = 5.0
        distY3 = 5.0
    
        ax1.plot(cPreHist[1][1:], cPreHist[0], color='blue', alpha=alphaVal)
        ax1.plot(cPostHist[1][1:], cPostHist[0], color='orange', alpha=alphaVal)
        ax1.set_xlim(roundTen(min(cPreHist[1][1:]), mode='Down'), 
            roundTen(max(cPreHist[1][1:]), mode='Up'))
        ax1.set_ylim(roundTen(10**0, mode='Down'), 
            roundTen(max(cPostHist[0])*distY1, mode='Up'))
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel('degree')
        ax1.set_ylabel('frequency')
        if withTitle > 0:
            ax1.set_title('frequency distribution')
        xText = 0.7
        yText = 0.7
        dxText = 0.2
        dyText = 0.2
        ax1.add_patch(Polygon([[xText, yText], [xText + dxText, yText], 
            [xText + dxText, yText + dyText], [xText, yText + dyText]], 
            closed=False, fill=True, color='white', alpha=0.9, 
            transform=ax1.transAxes, zorder=2))
        digits = 2
    
        locs = [10**0, 10**1, 10**2, 10**3, 10**4, 10**5, 10**6]
        locator= matplotlib.ticker.FixedLocator(locs)
        ax1.yaxis.set_major_locator(locator)
    
        content1 = "a = " + sci(popt1[0], digits) + "\n b = " + sci(popt1[1], digits)
    
        a = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        b = [10**0, 10**1, 10**2, 10**3, 10**4, 10**5, 10**6]
        c = list()
    
        for aEl in a:
            for bEl in b:
                c.append(aEl*bEl)

        locs = c
        locator = matplotlib.ticker.FixedLocator(locs)
        ax1.yaxis.set_minor_locator(locator)

        ax2.plot(clustersizesPreHist[1][1:], clustersizesPreHist[0], color='blue', 
            alpha=alphaVal)
        ax2.plot(clustersizesPostHist[1][1:], clustersizesPostHist[0], color='orange', 
            alpha=alphaVal)
        ax2.set_xlim(roundTen(min(clustersizesPreHist[1][1:]), mode='Down'), 
            roundTen(10**(0), mode='Up'))
        ax2.set_ylim(roundTen(10**(-1), mode='Down'), 
            roundTen(max(clustersizesPreHist[0]*distY2), mode='Up'))
        ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax2.set_xlabel('cluster size')
        ax2.set_ylabel('frequency')
        if withTitle > 0:
            ax2.set_title('clustersizes')
        xText = 0.7
        yText = 0.7
        dxText = 0.2
        dyText = 0.2
        ax2.add_patch(Polygon([[xText, yText], [xText + dxText, yText], 
            [xText + dxText, yText + dyText], [xText, yText + dyText]], 
            closed=False, fill=True, color='white', alpha=0.9, 
            transform=ax2.transAxes, zorder=2))
        digits = 2
        content2 = "a = " + sci(popt2[0], digits) + "\n b = " + sci(popt2[1], digits)

        ax3.plot(GnamesHist1PreHist[1][1:], GnamesHist1PreHist[0], color='blue', 
            alpha=alphaVal)
        ax3.plot(GnamesHist1PostHist[1][1:], GnamesHist1PostHist[0], color='orange', 
            alpha=alphaVal)
        ax3.set_xlim(roundTen(min(GnamesHist1PreHist[1][1:]), mode='Down'), 
            roundTen(max(GnamesHist1PreHist[1][1:]), mode='Up'))
        ax3.set_ylim(roundTen(10**0, mode='Down'), 
            roundTen(max(GnamesHist1PreHist[0])*distY3, mode='Up'))

        if withTitle > 0:
            ax3.set_title('Distribution of clonotype frequencies')
        ax3.set_xscale('log')
        ax3.set_yscale('log')
        xText = 0.7
        yText = 0.7
        dxText = 0.2
        dyText = 0.2
        ax3.add_patch(Polygon([[xText, yText], [xText + dxText, yText], 
            [xText + dxText, yText + dyText], [xText, yText + dyText]], 
            closed=False, fill=True, color='white', alpha=0.9, 
            transform=ax3.transAxes, zorder=2))
        digits = 2
        content3 = "a = " + sci(popt3[0], digits) + "\n b = " + sci(popt3[1], digits)
        locator= matplotlib.ticker.FixedLocator(locs)
        ax3.yaxis.set_major_locator(locator)
        
        a = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        b = [10**0, 10**1, 10**2, 10**3, 10**4]
        c = list()
    
        for aEl in a:
            for bEl in b:
                c.append(aEl*bEl)

        locs = c
        locator = matplotlib.ticker.FixedLocator(locs)
        ax3.yaxis.set_minor_locator(locator)
        ax3.set_xlabel("clonotype index")
        ax3.set_ylabel("frequency")
   
        if withParams == 1:
            content1 = 'fit: ' + content1
            content2 = 'fit: ' + content2
            content3 = 'fit: ' + content3
        if withParams == 0:	
            content1 = 'fit'
            content2 = 'fit'
            content3 = 'fit'
        
        ax1.legend([content1, 'Pre selection', 'Post selection'], frameon = False)
        ax2.legend([content2, 'Pre selection', 'Post selection'], frameon = False)
        ax3.legend([content3, 'Pre selection', 'Post selection'], frameon = False)
    
        fig1.savefig('degreesDist.png', dpi=300,  bbox_inches="tight")
        fig2.savefig('clustersizes.png', dpi=300, bbox_inches="tight")
        fig3.savefig('GnamesHist.png', dpi=300, bbox_inches="tight")
    
        plt.show()

    if __name__ == "__main__":
        # somehow initialize values?
        setPlotDesign()
        load()
        fit()
        plot()