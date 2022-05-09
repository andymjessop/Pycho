#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 20:55:39 2022

@author: andymj
"""

#TODO:
    #- Add x, y axis (poll plots for quantity and Units)
    #- Add titles (based on label values)
    #- One x-axis title if linked?
    

from . import matplotlibPlot as mplP #eventually - allow Bokeh plots as well! But not yet.
from .. import _labelTools as lt
from . import _plotTools as pt
import copy

engine = mplP

def setPlotEngine(engineOption):
    global engine
    if engineOption in ['mplP']: #add bokeh soon!
        engine = engineOption
    else:
        raise ValueError('Invalid Plot Engine specified!')

def pollRecordsForAxisTitles(records):
    axisQuantities = pt.pollQuantities(records)
    xAxLabels=axisQuantities['x']
    yAxLabels=axisQuantities['y']
    axisUnits = pt.pollUnits(records)
    xAxUnits=axisUnits['x']
    yAxUnits=axisUnits['y']
    
    xLabel=f'{xAxLabels} ({xAxUnits})'
    yLabel=f'{yAxLabels} ({yAxUnits})'
    return xLabel, yLabel
    


def plot(echoRecords,filename = None,plotEngine = engine,**optionInputs):
    '''
    Plots echo Records with the options provided.
    
    Inputs allowed are:
    -----Line Options----
        - subplotLabels: Which labels to use to separate lines into subplots
        - lineStyleLabels: Which labels to use to generate line styles
        - colorLabels: Which labels to use to color lines
        - legendLabels: Which labels to use to generate label entries for each line
    ----Figure and Axis Options----
        - figureSize: The figure size, in inches as a two-entry array [Default = [10,6]]
        - figureDPI: The DPI resolution of the figure as a single integer [Default = 150]
        - subplotLayout: How the subplots are arranged. Options include 'column', 'row', or 'grid' [Default='column']
        - xLog: Whether to make the x-axis on Log scale [default = False]
        - yLog: Whether to make the y-axis on Log scale [default = False]
        - xyGrid: Whether or not to turn on major-axis grid lines [Default = True]
        - lineWidth: A global setting for Line Width [Default = 1]
        - fontSize: The font size for axis labels [Default = 12]
        - legendLocation: The font size for legend entries [Default = 12]
        - legendFontSize: The location of the legend. [Default = 'best']. Options include the standard matplotlib options plus "right outside", "top outside", and "bottom outside"            
    '''
    #check inputs for formatting. Takes lower-case entries and properly formats them to the proper names as well as checking input types
    sanitizedInputs = pt.sanitizeOptionsDict(optionInputs,pt.plotOptionParsing)
    
    #start with default options for that particular plot engine. Replace with any sanitized inputs given
    #need to poll Records for figure/axis information (if not given)
    plotOptions = copy.copy(engine.plotDefaults)
    for option in plotOptions:
        if option in optionInputs:
            plotOptions[option] = sanitizedInputs[option]
    
    for option in ['colorLabels','subplotLabels','lineStyleLabels','legendLabels']:
        if option in sanitizedInputs:
            plotOptions[option]=sanitizedInputs[option]
   
   #for each line option:
       # - determine how many unique options there are
       # - Query plot engine to produce available options
       # - Create an array of options that correspond to the Record at hand (pt.setPlotStyles)
       # - Add line/color label value to altLabels (in case legendLabels is not specified)
   
    altLabels = ['']*len(echoRecords) #define labels to auto-fill from subplotlabels, lineStyleLabels, and/or colorLabels
    
    #Generate figure and axes with options
    #get info for axes (if no subplots, nothing to poll):
    # - X, Y axis names (Quantity plus Units)
    # - figure title names (subplotlabels or figureLabels)
    if 'subplotLabels' in plotOptions:
        uniqueLabels = lt.findUniqueLabelValues(echoRecords,plotOptions['subplotLabels'],return_dict = True)
        
        f,ax = engine.makeSubplots(uniqueLabels,**plotOptions) 
        axisList = pt.setPlotStyles(echoRecords,ax,uniqueLabels)

        for axis,labels in zip(axisList,uniqueLabels):
            axRecords =  echoRecords.pull(labels)
            axisTitle = lt.labelString(labels)
            xLabel,yLabel = pollRecordsForAxisTitles(axRecords)  
            
            engine.axisProperties(axis,
                xLabel=xLabel,
                yLabel=yLabel,
                axisTitle = axisTitle,
                **plotOptions
            )
    else:
        f,ax = engine.makeSubplots(1,**plotOptions)
        axisList = pt.setPlotStyles(echoRecords,ax)

        xLabel,yLabel = pollRecordsForAxisTitles(echoRecords)  
        
        engine.axisProperties(ax[0],
            xLabel=xLabel,
            yLabel=yLabel,
            axisTitle = '',
            **plotOptions
            )

    
    
    #assign colors to lines
    if 'colorLabels' in plotOptions:
        uniqueLabels = lt.findUniqueLabelValues(echoRecords,plotOptions['colorLabels'],return_dict = True)
    
        colorList = pt.setPlotStyles(echoRecords,engine.colors,uniqueLabels)
        
        [altLabels.append(labelName) for labelName in pt.forceList(plotOptions['colorLabels'])]
        
    else:
        colorList = pt.setPlotStyles(echoRecords,engine.colors)
    
    
    #assign line styles to lines
    lineStyles = engine.lineStyles
    if 'lineStyleLabels' in plotOptions:
        uniqueLabels = lt.findUniqueLabelValues(echoRecords,plotOptions['lineStyleLabels'],return_dict = True)
        lineStyleList = pt.setPlotStyles(echoRecords,lineStyles,uniqueLabels)
        
        [altLabels.append(labelName) for labelName in pt.forceList(plotOptions['lineStyleLabels'])]
    else:
        lineStyleList = pt.setPlotStyles(echoRecords,engine.lineStyles[0])
  
    #assign legend labels to lines
    #this part is real messy - I should fix!
    if 'legendLabels' in plotOptions:
        labelNames = pt.forceList(plotOptions['legendLabels'])
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
        
    
    lines = []
    #plot all lines with options
    for Record,axis,color,lineStyle,legendName in zip(echoRecords,axisList,colorList,lineStyleList,labelList):
        X = getattr(Record,Record.PlotOptions['x_datum'])
        Y = getattr(Record,Record.PlotOptions['y_datum'])
        lineWidth = plotOptions['lineWidth']
        
        lines.append(engine.addLine(axis,X,Y,color,lineStyle,legendName,linewidth=lineWidth))
    
    #add legend
    [engine.addLegend(axis,**plotOptions) for axis in ax]
    
    #plot!
    engine.polishAndPlot(f)
    return f, ax, lines
    
# def saveFig()