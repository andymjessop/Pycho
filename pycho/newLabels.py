#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  7 21:52:35 2022

@author: andymj
"""

# new label interface:
#     - Add label with __setitem__
#     - Acces label with __getitem__
#     - Case-insensitive values (keeps a record of lowercase keys)
#     - print string of all labels given
#     - equals is if label dict is contained in set
#     - how to get multiple labels??
#     - make all labeldicts as label object?

class Label:
    def __init__(self,inputDict={}):
        self.labels = {}
        self.keys = []
        self.lowerKeys = []
        for name,value in inputDict.items():
            self[name]=value
        
    
    def __setitem__(self,key,value):
        #check if value is set, list, or other
        #set value to string if number
        realKey = self.checkInsensitiveKey(key) #check to see if key already exists
        if realKey:
            self.labels[realKey].add(value)
        else: #if it doesn't - make a new key (and add to lowerKeys)
            self.labels[key]={value}
            self.keys.append(key)
            self.lowerKeys.append(key.lower())

    def __getitem__(self,key):
        realKey = self.checkInsensitiveKey(key)
        if realKey:
            return self.labels[realKey]
        else:
            raise ValueError('Label Name "' + key + '" not found in labels')
            
    def checkInsensitiveKey(self,key): #insenstive check of a key value
        if key.lower() in self.lowerKeys:
            return self.keys[key==self.lowerKeys]    
        else:
            return False
            
    def printLabel(self,labelNames):
    ''' prints label values when given label names in format with:
        all values in label name joined with "&"
        Different label names joined with "|"
        ''' 
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
        #sort out input into proper label set
        
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

