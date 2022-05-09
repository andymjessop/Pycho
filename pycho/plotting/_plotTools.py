#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 14:32:49 2022

@author: andymj
"""
import numpy as np

def isLabelInput(inputStringOrList)->bool:
    '''Input should be:
            - Str or list
            - List should contain only strings
    '''
    #To-Do:Check for proper label name (need function to verify label names)
    if inputStringOrList is str:
        return True
    elif inputStringOrList is list:
        for item in inputStringOrList:
            if type(item)!=str():
                raise TypeError('Input in list is not a valid label')
    return True

def is2Numeric(inputArray)->bool:
    '''Input should be:
            - List with 2 entries
            - Of all floats or ints
    '''
    if type(inputArray)!=list: 
        raise TypeError('Limits input is not a list of 2 numbers')
   
    if len(inputArray)!=2:
        raise ValueError('Limits input is not a list of 2 numbers')
    for i,item in enumerate(inputArray):
        if type(item)!=float and type(item)!=int:
            raise ValueError('Array input ' + str(i) + ' is not numeric')
     
    return True

plotOptionParsing = dict(
    subplotLabels= isLabelInput,
    lineStyleLabels =isLabelInput,
    colorLabels= isLabelInput,
    titleLabels= isLabelInput,
    xLimits= is2Numeric,
    yLimits= is2Numeric,
    xLog= lambda a:type(a)==bool,
    yLog= lambda a:type(a)==bool,
    figureSize = is2Numeric,
    figureDPI = lambda a:type(a)==int,
    fontSize = lambda a:type(a)==int,
    subplotLayout = lambda x:(x in ['column','row','grid']), #| (is2Numeric(x)),
    legendLabels = isLabelInput,
    legendLocation = lambda x:(x in ['best','upper right','upper left', 'lower right','lower left',
                                     'right outside', 'top outside','bottom outside']),
    legendFontSize = lambda a:type(a)==int,
    lineWidth = lambda a:type(a)==int
    )

def sanitizeOptionsDict(inputDictAllCase,validDict)->dict:
    '''
    Checks a dictionary input against a dictionary of valid names and input types. Used for weird possible inputs to plot options
    '''
    #make inputDict all lower-case values
    inputDict = {key.lower():value for (key,value) in inputDictAllCase.items()}
    
    sanDict =  {}
    #go through each possible entry, check if exists, and copy over to sanDict
    for key in validDict:
        lKey = key.lower()
        if lKey in inputDict:   #check if exists
            inputValue = inputDict[lKey]
            
            #check if valid
            if validDict[key](inputValue):
                #assign to new Dict
                sanDict[key] = inputValue
                inputDict.pop(lKey) #remove input from original dict
            else:
                raise ValueError('Input is not of correct type')
            
    #check if any remaining inputs are left over (invalid input options)        
    if len(inputDict)>0:
        leftoverKeys = list(inputDict.keys())
        raise ValueError('The following values are not valid option inputs: \n' + ', '.join(leftoverKeys))
    
    return sanDict
     
def setPlotStyles(recordList,styleOptions,style_dicts = []):
    '''
    Assigns any line-based styles to the record list, producing an array equal in length to the original record list with each option corresponding to the record in the array.
    If styleOptions are the length of style_dicts, then 1-to-1 correspondence is observed.
    If styleOptions is shorter than style_dicts, then the options will be recycled after reaching the end
    If styleOptions is longer than style_dicts, it will be truncated
    '''
    N_styles = len(styleOptions)
    N_labels = len(style_dicts)
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
     if isinstance(val, (list, np.ndarray)):
         output = val
     
     elif type(val) is set:
         output = list(val)
     else:
         output = [val]
     return output

def pollQuantities(Records): #returns dictionary of 'x','y' with strings
    xQuantities = set()
    yQuantities = set()
    for record in Records:
        xQuantities.add(record.Quantities[record.PlotOptions['x_datum']])
        yQuantities.add(record.Quantities[record.PlotOptions['y_datum']])
    Quantities = {}
    
    Quantities['x'] = 'Assorted Quantities' if len(xQuantities)>1 else xQuantities.pop()
    Quantities['y'] = 'Assorted Quantities' if len(yQuantities)>1 else yQuantities.pop()

    return Quantities

def pollUnits(Records): #returns dictionary of 'x','y' with strings
    xUnits = set()
    yUnits = set()
    for record in Records:
        xUnits.add(record.Units[record.PlotOptions['x_datum']])
        yUnits.add(record.Units[record.PlotOptions['x_datum']])
    Units = {}
    
    Units['x'] = 'Assorted Units' if len(xUnits)>1 else xUnits.pop()
    Units['y'] = 'Assorted Units' if len(yUnits)>1 else yUnits.pop()

    return Units


 
# def pollRecordsForOptions(recordList):
    #check if record has PlotOptions!
    
    #check all plotOptions given
    