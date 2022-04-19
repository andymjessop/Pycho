#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 19:36:11 2021

@author: andymj
"""

import bokeh.palettes as bpalettes
import bokeh.plotting as bp
from bokeh.models import HoverTool
from .. import _labelTools as lt
from bokeh.models import Range1d

# Need to support:
#     X legendLabels
#     X styleLabels
#     X colorLabels
#     - subplotLabels
#     - figsize (is size per plot for bokeh)
#     - subplotLayout
#     - xLimits
#     - yLimits
#     - xLog
#     - yLog
#     - titleLabels
#     - legendLocation
#     - fontSize
#     - legendFontSize
#     - xGrid
#     - yGrid
#     - pushToRecords

fig_defaults = {'figsize':[10,6],'dpi':150,
                'xLog':False,'yLog':False,
                'fontSize':12,'legendFontSize':12,
                'colorMap':'tab20',
                'xGrid':False,'yGrid':False,
                'style':'seaborn-white'}


def bokehPlot(echoRecords,outfilename,**OpArgs):
    #force all the options to lowercase so you don't have to think about it (what happens if you have 2 with different cases?)
    OpArgs = {k.lower():v for k,v in OpArgs.items()}
    
    #generate BokehPlot and my favorite tools
    
    #build list if input is not a list
    echoRecords = (echoRecords,[echoRecords])[type(echoRecords) is not list]
    
    #check filename to be sure it ends in ".html"
    outfilename = (outfilename + '.html',outfilename)[outfilename.endswith('.html')]
    #set color, linestyle parameters. If no legendLabels, 
    
    
    print('Generating Plot...')
    #Bokeh Plot    
    bp.output_file(outfilename,mode='inline')        

    HOVERTOOL = HoverTool(
        tooltips = [
        ("data","$name"),
        ("x", "@x"),
        ("y", "@y"),
        ],
        line_policy="prev"
        )
    
    # if 'subplotLabels' in OpArgs:
    #     uniqueLabels = lt.findUniqueLabelValues(echoRecords,OpArgs['subplotLabels'],return_dict = True)
    #     Nsubplots =len(uniqueLabels)
        
    # else:
    #     Nsubplots = 1
    #     axes = 
    
    
    p = bp.figure(plot_width=1000, plot_height=600)
    
    
   
        
    
    altLabels = []
    if 'colorLabels' in OpArgs:
        uniqueLabels = lt.findUniqueLabelValues(echoRecords,OpArgs['colorLabels'],return_dict = True)
        colorList = setPlotStyles(echoRecords,
                                  setPlotPalette(len(uniqueLabels))
                                  ,uniqueLabels)
        [altLabels.append(labelName) for labelName in forceList(OpArgs['colorLabels'])]
    else:
        
        colorList = setPlotStyles(echoRecords,
                                  setPlotPalette(len(echoRecords)))
        
    lineStyles =  ['solid','dashed','dotted','dotdash']
    if 'lineStyleLabels' in OpArgs:
        uniqueLabels = lt.findUniqueLabelValues(echoRecords,OpArgs['lineStyleLabels'],return_dict = True)
        lineStyleList = setPlotStyles(echoRecords,lineStyles,uniqueLabels)
        [altLabels.append(labelName) for labelName in forceList(OpArgs['lineStyleLabels'])]
    else:
        lineStyleList = setPlotStyles(echoRecords,lineStyles)
     
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
        
   
    x_limits = []
    for record,color,lineStyle,labelText in zip(echoRecords,colorList,lineStyleList,labelList):
        x_data = getattr(record,record.PlotOptions['x_datum'])
        if x_limits:
            x_limits[0] = (x_limits[0],min(x_data))[min(x_data)<x_limits[0]]
            x_limits[1] = (x_limits[1],max(x_data))[max(x_data)<x_limits[0]]  
        else:
            x_limits = [min(x_data),max(x_data)]
        y_data = getattr(record,record.PlotOptions['y_datum'])
        
        
        
        p.line(x_data,y_data,
               name=labelText,legend_label=labelText,
               line_color = color,line_dash = lineStyle)
        
    p.add_tools(HOVERTOOL)
    p.toolbar.logo = None
    p.x_range = Range1d(x_limits[0], x_limits[1])
    p.xaxis.axis_label = echoRecords[0].Quantities[echoRecords[0].PlotOptions['x_datum']] + '['+echoRecords[0].Units[echoRecords[0].PlotOptions['x_datum']]  +']'
    p.yaxis.axis_label= echoRecords[0].Quantities[echoRecords[0].PlotOptions['y_datum']] + '['+echoRecords[0].Units[echoRecords[0].PlotOptions['y_datum']]  +']'
    p.legend.location = "bottom_right"
    p.legend.click_policy="hide"
    
    bp.show(p)
    print(f'Plot Generated as {outfilename}')

def setPlotPalette(N):
    N=(N,3)[N<3] #set N to at least 3
    if N<=10:
        return bpalettes.Category10[N]
    elif N<=20:
        custom_palette = bpalettes.Category10[10] +bpalettes.Category20[20][1::2]
        return custom_palette
    elif N>20: #just cycle though a few pallettes!
        custom_palette = bpalettes.Category10[10] +bpalettes.Category20[20][1::2]
        mult = int(N/20)+1
        return custom_palette *mult
    
def setPlotStyles(recordList,styleOptions,style_dicts = []):
    N_styles = len(styleOptions)
    if style_dicts:
        labelNames = [name for name in style_dicts[0]]
        styleList = []
        for entry in recordList:
            entry_dict = {Name:entry.Labels[Name] for Name in labelNames}
            styleIndex = style_dicts.index(entry_dict)
            styleList.append(styleOptions[styleIndex%N_styles])                        
    else:
        styleList = [styleOptions[i%N_styles] for i,record in enumerate(recordList)]
        
    return styleList

def forceList(val):
     if type(val) is list:
         output = val
     
     elif type(val) is set:
         output = list(val)
     else:
         output = [val]
     return output
        
    

    
