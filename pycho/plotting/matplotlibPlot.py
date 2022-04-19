#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 10:49:20 2021

@author: andymj
"""

#MatPlotLib library for Pycho

plotDefaults = {'figureSize':[10,6],'figureDPI':150,
                'subplotLayout':'column',
                'xLog':False,'yLog':False,
                'fontSize':12,'legendFontSize':12,
                'legendLocation':'best',
                'xyGrid':True,
                'lineWidth':1}

import matplotlib as mpl
from matplotlib import pyplot as plt
from . import _plotTools as pt
import numpy as np

lineStyles =  ['-','--',':','-.']
colors = [*mpl.cm.get_cmap('tab20').colors[0::2],*mpl.cm.get_cmap('tab20').colors[1::2]]

def makeSubplots(layoutN,**plotOptions):

    layout = plotOptions['subplotLayout']
    
    
    if type(layoutN) == int:
        N = layoutN
    else:
        N = len(layoutN)
    
    #make general subplots
    if layout=='column':
        f,ax = plt.subplots(N,1,sharex=True)
        
    elif layout =='row':
        f,ax = plt.subplots(1,N)
    elif layout == 'grid':
        #make as close to square as possible with more rows than columns
        n_row = np.ceil(np.sqrt(N))
        n_col = np.ceil(N/n_row)
        f,ax = plt.subplots(n_row,n_col)
        
    ax= pt.forceList(ax)
    
    
    #set up figure size, dpi
    f.set_size_inches(plotOptions['figureSize'])
    f.set_dpi(plotOptions['figureDPI'])
    
    return f, ax

def axisProperties(axis,xTitle = '',yTitle='',axisTitle='',**plotOptions):
        #TODO: Need xaxis, yaxis names!!
    # set up each axis:
    # Margins
    # Scale (log or linear)
    # grid
    # Font size

    axis.margins(x=0,y=.1) #set margin to zero - this is not a settable default because I hate having margins
    
    if plotOptions['yLog']:
        axis.set_yscale('log')
    if plotOptions['xLog']:       
        axis.set_xscale('log')
    axis.grid(plotOptions['xyGrid'])
    # axis.set_fontsize(plotOptions['fontSize'])
    #TODO: Add axis names based on layoutN


def addLine(ax,Xdata,Ydata,color,lineStyle,name,linewidth=1):
    line =ax.plot(Xdata,Ydata,color=color,linestyle=lineStyle,label=name,linewidth=linewidth)
    return line

def addLegend(ax,**plotOptions):
    
    location = plotOptions['legendLocation']
    fontsize = plotOptions['legendFontSize']
    if 'outside' in location:
       if location=='right outside':
           ax.legend(loc='upper left',bbox_to_anchor = [1.05,1],fontsize = fontsize)
       elif location=='top outside':
           ax.legend(loc='lower left',bbox_to_anchor = [0,1.02],fontsize = fontsize)
       elif location=='bottom outside':
           ax.legend(loc='upper left',bbox_to_anchor = [0,-.02],fontsize = fontsize)
    else:
        ax.legend(loc=location,fontsize = fontsize)
        
def polishAndPlot(f):
    f.tight_layout()
    f.show(f)
    
# def saveFig(f,format = 'png'):
 
