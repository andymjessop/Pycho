#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 10:49:20 2021

@author: andymj
"""

#MatPlotLib library for Pycho

'''
    #NEED:
        - Line Info:
            Subplotlabel
            LineStyleLabel
            ColorLabels
            TitleLabels
        - Figrue Info:
            - X, Y Limits
            - Log or not Log
            - Image Size
            - Font Size?
            - Custom color map? Can I use bokeh colors?
        - Legend Stuff
            - Legend Labels
            - Legend Placement
            - Font Size?
        
'''

fig_defaults = {'figsize':[10,6],'dpi':150,
                'xLog':False,'yLog':False,
                'fontSize':12,'legendFontSize':12,
                'colorMap':'tab20',
                'xGrid':False,'yGrid':False,
                'style':'seaborn-white'}


from cycler import cycler
import matplotlib as mpl
from matplotlib import pyplot as plt
from . import labelTools as lt

# lineStyles =  cycler(['solid','dashed','dotted','dotdash'])

def mplPlot(echoRecords,**OpArgs):
    #Need to add way to output to file. Something easy!!
    #define a new plot subclass?
   
    #build list if input is not a list - need for RecordArray?
    echoRecords = (echoRecords,[echoRecords])[type(echoRecords) is not list]

    #figure out how many subplots to make
    if 'subplotlabels' in OpArgs:
        ubplots = len(lt.findUniqueLabelValues(echoRecords,OpArgs['subplotlabels'],return_dict = True))
    else:
        subplots = 1    

    #create figure
    figure,ax = plt.subplots(**fig_defaults,sharex= True)
    ax.xmargins=0
    

 
