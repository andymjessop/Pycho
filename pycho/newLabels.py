#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  7 21:52:35 2022

@author: andymj
"""

# new label interface:
    
#     - Add label with __setitem__
#     - Acces label with __getitem__
#     - Case-insensitive (keeps lowercase keys)
#     - print string of all labels given
#     - equals is if label dict is contained in set
#     - how to get multiple labels??
#     - make all labeldicts as label object?
#     - 

class Label:
    def __init__(self):
        self.labels = {}
        self.keys = []
        self.lowerKeys = []
        
    
    def __setitem__(self,key,value):
        #check if value is set, list, or other
        #set value to string if number
        realKey = self.checkInsensitiveKey(key)
        if realKey:
            self.labels[realKey].add(value)
        else:
            self.labels[key]={value}
            self.keys.append(key)
            self.lowerKeys.append(key.lower())
    
    
    def __getitem__(self,key):
        realKey = self.checkInsensitiveKey(key)
        if realKey:
            return self.labels[realKey]
        else:
            raise ValueError('Label Name "' + key + '" not found in labels')
            
    def checkInsensitiveKey(self,key):
        if key.lower() in self.lowerKeys:
            return self.keys[key==self.lowerKeys]    
        else:
            return False
            
    def printLabel(self,labelNames):
        #make labelNames a set
        outString = ''
        for key in labelNames:
            labelString = ' & '.join(self.labels[key])
            outString = labelString + '|'
        outString = outString[:-1]
        
        return outString
        
    def iterLabelValues(self,labelName):
    	realKey = self.checkInsensitiveKey(labelName)
    	for value in list(self.labels[realKey]):
    		yield value
    
    def keys(self):
        return self.keys
    
    def __contains__(self,item):
        #sort out item into proper label set
        
        #check that all keys are in item (if case is off)
        for key in item.keys():
        	return
        
        #check values to keys
    
    def outputDictionary(self):
    	return self.labels
    
    
    
    def __repr__(self):
        return repr(self.labels)



f = Label()
f['borp'] = 'TWEEDLE'
f['Borp'] = 'Dee'
f['beep'] = 'Kazoo'

