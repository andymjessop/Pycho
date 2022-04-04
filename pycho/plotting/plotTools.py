#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 14:32:49 2022

@author: andymj
"""

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

plotOptions = dict(
    subplotLabels= isLabelInput,
    lineStyleLabels =isLabelInput,
    colorLabelss= isLabelInput,
    titleLabelss= isLabelInput,
    xLimits= is2Numeric,
    yLimits= is2Numeric,
    xLog= lambda a:type(a)==bool,
    yLog= lambda a:type(a)==bool,
    figSize = is2Numeric,
    fontSize = lambda a:type(a)==int,
    subplotLayout = lambda x:(x in ['column','row','grid']), #| (is2Numeric(x)),
    legendLabels = isLabelInput,
    legendLocation = lambda a:type(a) ==str,
    legendFontSize = lambda a:type(a)==int
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
        raise ValueError('The following values are not valid option inputs:' + ', '.join(leftoverKeys))
    
    return sanDict
            
#testing out the code:    
if __name__=='__main__':
    testDict = {'figSIZE' :[3,10],'linestyleLabels':['borp','sple']}
    q = sanitizeOptionsDict(testDict,plotOptions)
    print(q)