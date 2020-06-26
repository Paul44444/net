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

N = 20000
#minL = 5 # 4
#maxL = 6
min_ldVal = 0
max_ldVal = 1
extractNum = 18 #20
#lets = 'ACDEFGHIKLMNPQRSTVWY'
#lets = 'ACD'
#seq = r.generate_random_sequences(N, minimum_length=minL, maximum_length=maxL, seed=1, letters=lets)

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
withTitle = 0 	# info: 0 -> don't show title; 1 -> show title
withParams = 0

cPre = np.loadtxt('cPre.txt')
cPost = np.loadtxt('cPost.txt')
clustersizesPre = np.loadtxt('clustersizesPre.txt')
clustersizesPost = np.loadtxt('clustersizesPost.txt')
GnamesHist1Pre = np.loadtxt('GnamesHist1Pre.txt')
GnamesHist1Post = np.loadtxt('GnamesHist1Post.txt')

cPreHist = np.histogram(cPre, bins = int(max(cPre) - min(cPre)))
cPostHist = np.histogram(cPost, bins = int(max(cPost) - min(cPost)))
clustersizesPreHist = np.histogram(clustersizesPre, bins = int(max(clustersizesPre) - min(clustersizesPre)))
clustersizesPostHist = np.histogram(clustersizesPost, bins = int(max(clustersizesPost) - min(clustersizesPost)))
GnamesHist1PreHist = np.histogram(GnamesHist1Pre, bins = int(max(GnamesHist1Pre) - min(GnamesHist1Pre)))
GnamesHist1PostHist = np.histogram(GnamesHist1Post, bins = int(max(GnamesHist1Post) - min(GnamesHist1Post)))

def func(x, a, b):
	#return a * np.exp(-b * x) + c
	return a*np.power(x, -b)
def digNum(x, dig):
	return str(float(int(x*10**dig))/(10**dig))
def sci(x, dig = 1):
	i = 0
	check = 0
	if x > 0.1 or x == 0.1:
		while check < 1:
			if x < 10**i:
				check = 1
				print("\n i: ", i)
			else:
				i += 1
		i -= 1 			# info: make i - 1, so that it is one unit smaller than the next higher power of ten, seeing from x
	
	if x < 0.1:
		while check < 1:
			if x > 10**i:
				check = 1
				print("\n i: ", i)
			else:
				i -= 1
	x = x/10**i		# info: x should not be an int, but a float or double
	x = digNum(x, dig) 
	xlabel = str(x) + "$\cdot 10^{" + str(i) + "}$"
	return xlabel
def removeZero(x):
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
		i -= 1 			# info: make i - 1, so that it is one unit smaller than the next higher power of ten, seeing from x
	
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
	
constFac = 0.2
popt1, pcov1 = curve_fit(func, cPreHist[1][1:], cPreHist[0])

cPreHist = removeZero(cPreHist)
ax1.plot(cPreHist[1][1:], constFac*func(cPreHist[1][1:], *popt1), 'r-', label='fit: a=%5.3f, b=%5.3f' % tuple(popt1))

clustersizesPreHist = removeZero(clustersizesPreHist)
popt2, pcov2 = curve_fit(func, clustersizesPreHist[1][1:], clustersizesPreHist[0])
ax2.plot(cPreHist[1][1:], constFac*func(cPreHist[1][1:], *popt2), 'r-', label='fit: a=%5.3f, b=%5.3f' % tuple(popt2))

GnamesHist1PreHist = removeZero(GnamesHist1PreHist)
popt3, pcov3 = curve_fit(func, GnamesHist1PreHist[1][1:], GnamesHist1PreHist[0])
ax3.plot(cPreHist[1][1:], constFac*func(cPreHist[1][1:], *popt3), 'r-', label='fit: a=%5.3f, b=%5.3f' % tuple(popt3))

print("\n cPreHist: popt: ", popt1, "; pcov: ", pcov1)
print("\n clustersizesPreHist: popt: ", popt2, "; pcov: ", pcov2)
print("\n GnamesHist1PreHist: popt: ", popt3, "; pcov: ", pcov3)

distY1 = 500.0
distY2 = 5.0
distY3 = 5.0

#ax1.hist(cPre, bins = int(max(cPre) - min(cPre)), color='blue', alpha = alphaVal)
#ax1.hist(cPost, bins = int(max(cPost) - min(cPost)), color='orange', alpha = alphaVal)
ax1.plot(cPreHist[1][1:], cPreHist[0], color='blue', alpha = alphaVal)
ax1.plot(cPostHist[1][1:], cPostHist[0], color='orange', alpha = alphaVal)
ax1.set_xlim(roundTen(min(cPreHist[1][1:]), mode = 'Down'), roundTen(max(cPreHist[1][1:]), mode = 'Up'))
ax1.set_ylim(roundTen(10**0, mode = 'Down'), roundTen(max(cPostHist[0])*distY1, mode = 'Up'))
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
ax1.add_patch(Polygon([[xText, yText], [xText + dxText, yText], [xText + dxText, yText + dyText], [xText, yText + dyText]], closed=False, fill=True, color='white', alpha = 0.9, transform = ax1.transAxes, zorder = 2))
digits = 2

locs = [10**0, 10**1, 10**2, 10**3, 10**4, 10**5, 10**6]
locator= matplotlib.ticker.FixedLocator(locs)
ax1.yaxis.set_major_locator(locator)

#content = "a = " + digNum(popt1[0], digits)+ "(" + digNum(pcov1[0][0], digits) + ")" + "\n b = " + digNum(popt1[1], digits) + "(" + digNum(pcov1[1][1], digits) + ")"
content1 = "a = " + sci(popt1[0], digits) + "\n b = " + sci(popt1[1], digits)

a = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
b = [10**0, 10**1, 10**2, 10**3, 10**4, 10**5, 10**6]
c = list()

for aEl in a:
	for bEl in b:
		c.append(aEl*bEl)

print("\n c: ", c)
locs = c
locator = matplotlib.ticker.FixedLocator(locs)
ax1.yaxis.set_minor_locator(locator)


#axB.legend(['s = 25', 's = 50', 's = 100', 's = 200'], prop={'size': 6}, ncol=3, frameon=False)


print("\n bins2: ",  int(max(clustersizesPre) - min(clustersizesPre)))
#ax2.hist(clustersizesPre, bins = int(max(clustersizesPre) - min(clustersizesPre)), color='blue', alpha = alphaVal)
#ax2.hist(clustersizesPost, bins = int( max(clustersizesPost) - min(clustersizesPost)), color='orange', alpha = alphaVal)
ax2.plot(clustersizesPreHist[1][1:], clustersizesPreHist[0], color='blue', alpha = alphaVal)
ax2.plot(clustersizesPostHist[1][1:], clustersizesPostHist[0], color='orange', alpha = alphaVal)
#ax2.set_xlim(min(clustersizesPreHist[1][1:]), max(clustersizesPreHist[1][1:]))
ax2.set_xlim(roundTen(min(clustersizesPreHist[1][1:]), mode = 'Down'), roundTen(10**(0), mode = 'Up'))
ax2.set_ylim(roundTen(10**(-1), mode = 'Down'), roundTen(max(clustersizesPreHist[0]*distY2), mode = 'Up'))
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
ax2.add_patch(Polygon([[xText, yText], [xText + dxText, yText], [xText + dxText, yText + dyText], [xText, yText + dyText]], closed=False, fill=True, color='white', alpha = 0.9, transform = ax2.transAxes, zorder = 2))
digits = 2
#content = "a = " + digNum(popt2[0], digits)+ "(" + digNum(pcov2[0][0], digits) + ")" + "\n b = " + digNum(popt2[1], digits) + "(" + digNum(pcov2[1][1], digits) + ")"
content2 = "a = " + sci(popt2[0], digits) + "\n b = " + sci(popt2[1], digits)

print("\n bins3: ", (max(GnamesHist1Pre) - min(GnamesHist1Pre)))
#ax3.hist(GnamesHist1Pre, bins = int((max(GnamesHist1Pre) - min(GnamesHist1Pre))), color='blue', alpha = alphaVal)
#ax3.hist(GnamesHist1Post, bins = int((max(GnamesHist1Post) - min(GnamesHist1Post))), color='orange', alpha = alphaVal)
ax3.plot(GnamesHist1PreHist[1][1:], GnamesHist1PreHist[0], color='blue', alpha = alphaVal)
ax3.plot(GnamesHist1PostHist[1][1:], GnamesHist1PostHist[0], color='orange', alpha = alphaVal)
ax3.set_xlim(roundTen(min(GnamesHist1PreHist[1][1:]), mode = 'Down'), roundTen(max(GnamesHist1PreHist[1][1:]), mode = 'Up'))
ax3.set_ylim(roundTen(10**0, mode = 'Down'), roundTen(max(GnamesHist1PreHist[0])*distY3, mode = 'Up'))

#locs = list(ax3.get_yticks())+ [roundTen(max(GnamesHist1PreHist[0])*distY3, mode = 'Up')]
#locator= matplotlib.ticker.FixedLocator(locs)
#ax3.yaxis.set_major_locator(locator)

#ax3.yaxis.set_major_locator(matplotlib.ticker.LogLocator(10**0, subs = 1.0, numdecs = 1.0))
#ax3.set_yticks([10**1, 10**2, 10**3, 10**4, 10**5])
#ax3.set_yticklabels([10**1, 10**2, 10**3, 10**4, 10**5])

#print("\n locs: ", locs)
if withTitle > 0:
	ax3.set_title('Distribution of clonotype frequencies')
ax3.set_xscale('log')
ax3.set_yscale('log')
xText = 0.7
yText = 0.7
dxText = 0.2
dyText = 0.2
ax3.add_patch(Polygon([[xText, yText], [xText + dxText, yText], [xText + dxText, yText + dyText], [xText, yText + dyText]], closed=False, fill=True, color= 'white', alpha = 0.9, transform = ax3.transAxes, zorder = 2))
digits = 2
#content = "a = " + format(digNum(popt3[0], digits), 'e')+ "(" + digNum(pcov3[0][0], digits) + ")" + "\n b = " + digNum(popt3[1], digits) + "(" + digNum(pcov3[1][1], digits) + ")"
content3 = "a = " + sci(popt3[0], digits) + "\n b = " + sci(popt3[1], digits)
#locs = list(ax3.get_yticks())+ [roundTen(max(GnamesHist1PreHist[0])*distY3, mode = 'Up')]
locs = [10**0, 10**1, 10**2, 10**3, 10**4, 10**5]
locator= matplotlib.ticker.FixedLocator(locs)
ax3.yaxis.set_major_locator(locator)
#ax3.yaxis.set_major_locator(matplotlib.ticker.LogLocator(10**1, 1.0))

a = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
b = [10**0, 10**1, 10**2, 10**3, 10**4]
c = list()

for aEl in a:
	for bEl in b:
		c.append(aEl*bEl)

print("\n c: ", c)
locs = c
locator = matplotlib.ticker.FixedLocator(locs)
ax3.yaxis.set_minor_locator(locator)
ax3.set_xlabel("clonotype index")
ax3.set_ylabel("frequency")

"""
ax1.text(xText, yText, content1, transform = ax1.transAxes, zorder = 3)
ax2.text(xText, yText, content2, transform = ax2.transAxes, zorder = 3)
ax3.text(xText, yText, content3, transform = ax3.transAxes, zorder = 3)
"""
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

print("\n clustersizes.png: ", list(clustersizesPreHist))
print("\n GnamesHist.png:  ", list(GnamesHist1PreHist))

plt.show()
