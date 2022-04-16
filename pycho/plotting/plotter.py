#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 20:55:39 2022

@author: andymj
"""

import matplotlibPlot as mplP #eventually - allow Bokeh plots as well! But not yet.
from .. import labelTools as lt
from . import _plotTools as pt


def plot(echoRecords,filename = None,**plotOptions):
    OpArgs = pt.sanitizeOptionsDict(plotOptions,pt.plotOptionParsing)
    
    #need to poll Records for general plot information (return option of majority of records, otherwise return defaults)
    #Need:
        # - figsize
        # - subplotlayout
        # - xLog
        # - yLog
        # - xGrid
        # - yGrid
        # - fontSize
        # - legendFontSize
        # - lineWidth (default)
 
    
    altLabels = [] #define labels to auto-fill from subplotlabels, 
    #Generate base figure with options
    if 'subplotLabels' in OpArgs:
        uniqueLabels = lt.findUniqueLabelValues(echoRecords,OpArgs['subplotLabels'],return_dict = True)
        
        N = len(uniqueLabels)
        f,ax = mplP.makeSubplots(N,**figureOptions) 
    else:
        f,ax = mplP.makeSubplots(1,**figureOptions)
        subplotList = pt.setPlotStyles(echoRecords,ax)
    
    #assign subplots to lines
    
    
    
    #assign colors to lines
    if 'colorLabels' in OpArgs:
        uniqueLabels = lt.findUniqueLabelValues(echoRecords,OpArgs['colorLabels'],return_dict = True)
        colors = matplotlibPlot.colors
        
        colorList = pt.setPlotStyles(echoRecords,
                                  colors
                                  ,uniqueLabels)
        [altLabels.append(labelName) for labelName in pt.forceList(OpArgs['colorLabels'])]
    else:
        
        colorList = pt.setPlotStyles(echoRecords,
                                  matplotlibPlot.defineColors(len(uniqueLabels)))
    
    
    #assign line styles to lines
    lineStyles = mplP.lineStyles
    if 'lineStyleLabels' in OpArgs:
        uniqueLabels = lt.findUniqueLabelValues(echoRecords,OpArgs['lineStyleLabels'],return_dict = True)
        lineStyleList = setPlotStyles(echoRecords,lineStyles,uniqueLabels)
        [altLabels.append(labelName) for labelName in pt.forceList(OpArgs['lineStyleLabels'])]
    else:
        lineStyleList = pt.setPlotStyles(echoRecords,lineStyles)
     
 
    
    
    
    #assign legend labels to lines
    #this part is real messy - I should fix!
   if 'legendLabels' in OpArgs:
       labelNames = forceList(OpArgs['legendLabels'])
       labelList=[]
       for record in echoRecords:
           labelText = ''
           for labelName in labelNames:
               labelText +='|'.join(record.Labels[labelName]) +'|'
           labelList.append(labelText[:-1])
   elif altLabels:
       labelList=[]
       for record in echoRecords:
           labelText = ''
           for labelName in altLabels:
               labelText +='|'.join(record.Labels[labelName])+'|'
           labelList.append(labelText[:-1])
   else:
      labelList = ['Record'+str(i) for i,r in enumerate(echoRecords)]
    
    
    #plot all lines with options
    
    
    #add legend
    
    
    #plot!
    

def saveFig()