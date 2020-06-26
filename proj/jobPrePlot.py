import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go

from scipy.optimize import curve_fit
from matplotlib import rcParams
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap
from collections import OrderedDict

import imnet
import pyspark
from imnet import random_strings as r
from imnet import process_strings as p

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

# set nice figure sizes
fig_width_pt = 245    # Get this from LaTeX using \showthe\columnwidth
golden_mean = (np.sqrt(5.) - 1.) / 2.  # Aesthetic ratio
ratio = golden_mean
inches_per_pt = 1. / 72.27  # Convert pt to inches
fig_width = fig_width_pt * inches_per_pt  # width in inches
fig_height = fig_width*ratio  # height in inches
fig_size = [fig_width, fig_height]
rcParams.update({'figure.figsize': fig_size})

# tell matplotlib about your params
rcParams.update(params)

Ns = np.loadtxt('Ns.txt')

clustersizesMaxPre = np.loadtxt('clustersizesMaxPre.txt')
clustersizesMaxPost = np.loadtxt('clustersizesMaxPost.txt')
degMaxsPre = np.loadtxt('degMaxsPre.txt')
degMaxsPost = np.loadtxt('degMaxsPost.txt')
isConnectedsPre = np.loadtxt('isConnectedsPre.txt')
isConnectedsPost = np.loadtxt('isConnectedsPost.txt')

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()
fig4, ax4 = plt.subplots()
fig5, ax5 = plt.subplots() # info: plot the graph
fig6, ax6 = plt.subplots()
ydata = np.divide(clustersizesMaxPre, Ns)
withTitle = 0	# info: 0 -> don't show title; 1 -> show title
withParams = 0

def func(x, a, b):
	return(0.5*np.tanh((x-b)*a) + 0.5)
def func1(x, a, b, c):
	return(1 - c*(x-b)*np.exp(-a*(x-b)))
def digNum(x, dig):
	response = ""
	if not (x == float("inf") or x == float("-inf")):
		response = str(float(int(x*10**dig))/(10**dig))
	if x == float("inf"):
		response = "inf"
	if x == float("-inf"):
		response = "-inf"
	return response
def sci(x, dig = 1):
	i = 0
	check = 0
	print("\n step A")
	if abs(x) > 0.1 or abs(x) == 0.1:
		while check < 1:
			if abs(x) < 10**i:
				check = 1
				print("\n i(big): ", i)
				print("\n x: ", x)
			else:
				i += 1
		i -= 1 			# info: make i - 1, so that it is one unit smaller than the next higher power of ten, seeing from x
	print("\n step B")
	if abs(x) < abs(0.1):
		while check < 1:
			if abs(x) > 10**i:
				check = 1
				print("\n i(small): ", i)
				print("\n x: ", x)
			else:
				i -= 1
	print("\n step C")
	x = x/10**i		# info: x should not be an int, but a float or double
	x = digNum(x, dig) 
	xlabel = str(x) + "$\cdot 10^{" + str(i) + "}$"
	return xlabel
popt1, pcov1 = curve_fit(func1, Ns, ydata, [5*10**(-4),-1*10**(4), 1.5*10**(-2)], maxfev = 10**5)
ax2.plot(Ns, func1(Ns, *popt1), 'r-', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt1), color = 'red')
xdata = np.linspace(-10.0, 1000.0, 500)

ydata = np.zeros(len(xdata))
ydata = func(xdata, 2*10**(-3), 500.0)

alphaVal = 0.5
print("\n clustersizesMaxPreFinal: ", clustersizesMaxPre)

print("\n degMaxsPre: ", degMaxsPre)
ax1.plot(Ns, np.divide(degMaxsPre, Ns))
ax1.plot(Ns, np.divide(degMaxsPost, Ns)) # info: we have replaced nodesPre by Ns
ax1.set_xscale('log')
ax1.set_xlabel('sample size $N$')
ax1.set_ylabel('maximum degree $d_{max}$')
if withTitle > 0:
	ax1.set_title('degMaxsPre')

alphaVal = 0.5
print("\n clustersizesMaxPreFinal: ", clustersizesMaxPre)
ax2.plot(Ns, np.divide(clustersizesMaxPre, Ns), color = 'blue', zorder = 0)
ax2.plot(Ns, np.divide(clustersizesMaxPost, Ns), color = 'orange', zorder = 0)
Nperfect = np.linspace(0.5, 10**5, num = 1000)
print("\n Nperfect: ", Nperfect)

ax4.set_xlim(0.1, 10**4)
ax4.set_xscale('log')

ax2.legend(['fit', 'Pre selection', 'Post selection'], frameon = False)
ax2.set_xlim(min(Ns), max(Ns))
ax2.set_ylim(-1.0, 1.0)
ax2.set_xscale('log')
ax2.set_xlabel('cluster size')
ax2.set_ylabel('frequency')
ax2.set_title('clustersizes')
xText = 0.7
yText = 0.7
dxText = 0.2
dyText = 0.2
ax2.add_patch(Polygon([[xText, yText], [xText + dxText, yText], [xText + dxText, yText + dyText], [xText, yText + dyText]], closed=False, fill=True, color='white', alpha = 0.9, transform = ax2.transAxes, zorder = 2))
digits = 2

content = "a = " + digNum(popt1[0], digits)+ "(" + digNum(pcov1[0][0], digits) + ")" + "\n b = " + digNum(popt1[1], digits) + "(" + digNum(pcov1[1][1], digits) + ")"
print("\n popt1[0]: ", popt1[0], "; pcov1[1]: ", pcov1[1])
print("\n Almost finished")
content = "a = " + sci(popt1[0], digits) + "\n b = " + sci(popt1[1],  digits)

if withParams > 0:
	ax2.text(xText, yText, content, transform = ax2.transAxes, zorder = 3)

ax6.plot(Ns, isConnectedsPre, color = 'blue', zorder = 0)
ax6.plot(Ns, isConnectedsPost, color = 'orange', zorder = 0)
ax6.set_xlim(min(Ns), max(Ns))
ax6.set_ylim(0.0, 1.0)
ax6.set_xlabel('sample size $N$')
ax6.set_ylabel('probability $p$')

fig1.savefig('degreeNum.png', dpi=300,  bbox_inches="tight")
fig2.savefig('clusterProb.png', dpi=300, bbox_inches = "tight")
fig3.savefig('diameters.png', dpi=300, bbox_inches = "tight")
fig6.savefig('connectedProb.png', dpi=300, bbox_inches = "tight")

plt.show()
