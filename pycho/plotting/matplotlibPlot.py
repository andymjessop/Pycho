#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 10:49:20 2021

@author: andymj
"""

#MatPlotLib library for Pycho

fig_defaults = {'figsize':[10,6],'dpi':150,
                'subplotlayout':'column',
                'xLog':False,'yLog':False,
                'fontSize':12,'legendFontSize':12,
                'xGrid':False,'yGrid':False}


import cycler
import matplotlib as mpl
from matplotlib import pyplot as plt

lineStyles =  cycler(['solid','dashed','dotted','dotdash'])
colors = cycler(*mpl.cm.get_cmap('tab20').colors[0::2],*mpl.cm.get_cmap('tab20').colors[1::2])

def makeSubplots(N,layout,size,xLog=False, yLog=False):
    if layout=='column':
        f,ax = plt.subplots(N,1,sharex=True)
        
    elif layout =='row':
        f,ax = plt.subplots(1,N,sharex=True)
    elif layout == 'grid':
        #make as close to square as possible with more rows than columns
        n_row = np.ceil(np.sqrt(N))
        n_col = np.ceil(N/n_row)
        f,ax = plt.subplots(n_row,n_col)
        
    ax= pt.forceList(ax)
    
    f.set_size_inches(*figsize)
    
    for axis in ax:
        axis.margins(0) #set margin to zero - this is not a settable default because I hate having margins
        axis.set_yscale(yLog)
        axis.set_xscale(xLog)
    
    
    return f, ax

def addLine(ax,Xdata,Ydata,color,lineStyle,name,linewidth):
    pass

def addLegend(ax,location,fontSize):
    if 'outside' in location:
       if location=='right outside':
           ax.legend(loc='upper left',bbox_to_anchor = [1.05,1])
       elif location=='top outside':
           ax.legend(loc='lower left',bbox_to_anchor = [0,1.02])
       elif location=='bottom outside':
           ax.legend(loc='upper left',bbox_to_anchor = [0,-.02])
    else:
        ax.legend(location=loc)
    

    
def polishAndPlot(f,ax):
    plt.tight_layout()
    plt.show(f)
    
def saveFig(f,format = 'png'):
 
