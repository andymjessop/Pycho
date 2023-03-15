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
#     -

def sanitizeLabelInput(inputDict):
    '''Formats a label input dictionary so that:
    - There are no spaces in the key values
    - All values are in a set
    - All inputs are strings'''
    outputDict = {}
    for keyvalue in inputDict:
        if ' ' in keyvalue:
            raise ValueError('Label names cannot contain spaces!')
        else:
            outputDict[keyvalue] = forceString(forceSet(inputDict[keyvalue]))
    return outputDict
 
def arbLabelInput(*narg,**darg):
    '''Just a convenience function to bundle parseNargsToDict and sanitizeLabelInput'''
    return sanitizeLabelInput(parseNargsToDict(*narg,**darg))


class Label:
    def __init__(self, inputDict=None):
        self.labels = {}
        self.names = []
        self.lowerNames = []
        # need to parse inputDict for proper format!
        if inputDict:
            for name in inputDict.keys():
                self[name] = inputDict[name]

    def __setitem__(self, name, value):
        # check if value is set, list, or other
        # set value to string if number
        realName = self.checkInsensitiveKey(name)
        if realName:
            self.labels[realName].add(value)
        else:
            self.labels[name] = {value}
            self.names.append(name)
            self.lowerNames.append(name.lower())

    def __getitem__(self, name):
        realName = self.checkInsensitiveKey(name)
        if realName:
            return self.labels[realName]
        else:
            raise ValueError('Label Name "' + name + '" not found in labels')

    def checkInsensitiveKey(self, name):
        if name.lower() in self.lowerNames:
            return self.names[name == self.lowerNames]
        else:
            return False

    def printLabel(self, labelNames):
        # make labelNames a set
        
        outString = ''
        for name in labelNames:
            labelString = ' & '.join(self.labels[name])
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

    def iterLabelValues(self, labelName):
    	realName = self.checkInsensitiveKey(labelName)
    	for value in list(self.labels[realName]):
    	    yield value

    def keys(self):
        return self.names

    def __contains__(self, item):
        # checks if labels and entries are a subset of labels
        # sort out item into proper label set (maybe make a label instance?)

        if type(item) is not Label:
            item = Label(inputDict=item)

        # check that all keys are in item (if case is off)
        for name in item.names:
            if name in self.names:
                # check that all entries exist in there:
                for value in item[name]:
                    if value not in self[name]:
                        return False

            else:
                return False



        return True
        
        # check values to keys
    
    def outputDictionary(self):
    	return self.labels
    
    def removeLabel(self,labelName):
        if labelName in self.keys:
            self.labels.pop(labelName)
            self.keys.pop(labelName)
            self.lowerKeys.pop(labelName)
    
    def __repr__(self):
        return repr(self.labels)


f = Label()
f['borp'] = 'TWEEDLE'
f['Borp'] = 'Dee'
f['beep'] = 'Kazoo'
# f.printLabel('borp')
print({'beep':'Dee'} in f)

