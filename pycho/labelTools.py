#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 22:06:56 2021

@author: andymj
"""

import re

try:
    import pandas as pd
except:
    print('You''ll need to install Pandas for all of these label functions to work!')
    pass

def parseNargsToDict(*narg,**darg): 
    '''
    Takes arguments and converts to a properly-formatted label dicionary. 
    All values in dictionary must be as a set!!
    '''
    #to-do: format so all values are strings!
    arguments = narg
    def forceString(inputSet):
        if type(inputSet) is not set:
            raise TypeError('Inputs to forceString must be a set, preferably of integers and strings')
        else:
            output = []
            for entry in inputSet:
                if type(entry) is str:
                    output.append(entry)
                elif type(entry) is int:
                    output.append(str(entry))
                elif type(entry) is float:
                    output.append('{:.2f}'.format(entry))
        return set(output)
    
    def forceSet(val):
     if type(val) is set:
         output = forceString(val)
     
     elif type(val) is list:
         output = forceString(set(val))
     else:
         output = forceString({val})
     return output
 
    
    if len(arguments)==1 and isinstance(arguments[0],dict): #if someone put a dictionary in the first time!  
        old_dictionary = arguments[0]
        dictionary = {}
        
        for labelName in old_dictionary.keys():
            #make itmes into set (if it wasn't already)
            searchString = old_dictionary[labelName]
            dictionary[labelName] = forceSet(searchString)
        
        #scrub dictionary to assure labels are properly formatter
        
    else: #if we just have a bunch of name-value pairs
        N = len(arguments)
        if (N % 2) == 0: 
            dictionary = {}
            for i in range(0,N,2):
                key = arguments[i]
                value = arguments[i+1] 
                dictionary[key]=forceSet(value)        
        else:
            raise ValueError('Not an odd number of name-value pairs!')
            return
    #add dictionary arguments
    dictionary ={**dictionary,**darg}
    
    return dictionary  
   
def pullRegex(inputRecordList,*narg,**darg):
    '''
    The most generic pull command available.
    '''
    if len(inputRecordList)==0: return None

    search_dict = ParseNargsToDict(*narg,**darg)
    
    #need option to skip missing label
    #From/To commands like MATLAB?
       
    output = list()
    
    labelnames = list(search_dict.keys())
    
    while len(labelnames)>1: #recursively run until there's only one label name
        
        searchedLabel = labelnames[0]
        miniDict = {searchedLabel:search_dict[searchedLabel]}
        inputRecordList = pullRegex(inputRecordList,miniDict)
        search_dict.pop(searchedLabel)
        labelnames = list(search_dict.keys())
    
    #perform pull on a single label
    labelName = labelnames[0]
    for record in inputRecordList:
        allLabelValues = record.Labels[labelName]
        for stringToMatch in search_dict[labelName]:
            for labelValue in allLabelValues:
                stringMatch = re.fullmatch(stringToMatch,labelValue)
                if type(stringMatch) is re.Match:
                    if record not in output:
                        output.append(record)
            
    return output

def purgeRegex(inputRecordList,*narg):
    '''
    The most generic purge command available!
    '''
    search_dict = ParseNargsToDict(*narg)
    output = inputRecordList.copy()
     
    labelnames = list(search_dict.keys())
    
    while len(labelnames)>1: #recursively run until there's only one label name
        
        searchedLabel = labelnames[0]
        miniDict = {searchedLabel:search_dict[searchedLabel]}
        output = purgeRegex(output,miniDict)
        search_dict.pop(searchedLabel)
        labelnames = list(search_dict.keys())
    
    #perform pull on a single label
    labelName = labelnames[0]
    for record in output:
        allLabelValues = record.Labels[labelName]
        for stringToMatch in search_dict[labelName]:
            for labelValue in allLabelValues:
                stringMatch = re.fullmatch(stringToMatch,labelValue)
                if type(stringMatch) is re.Match:
                    output.remove(record)
    
    return output


def findUniqueLabelValues(inputRecordList,labelNames,return_dict = False):
    '''
    Returns list of all unique label values. Useful for plotting! Will error if
    requested label(s) are not in all records
    '''
    #need way to fine for more than 1 labelName at a time
    
    labelNames = (labelNames,[labelNames])[type(labelNames) is not list]
    #check if label is in all records
    for record in inputRecordList:
        for name in labelNames:
            if name not in record.Labels.keys():
                raise NameError(f'The label name {name} is not present in all records in set!')
    
    uniqueValues = [];
    for record in inputRecordList:
        ValueSet = [record.Labels[name] for name in labelNames]
        if ValueSet not in uniqueValues:
            uniqueValues.append(ValueSet)
    if return_dict:
        output_dict=[]
        for entry in uniqueValues:
            output_dict.append({Name:Value for Name,Value in zip(labelNames,entry)})
        return output_dict 
    else:
        return uniqueValues


def findAllLabelNames(inputRecordList):
    '''
    Finds all label names in the given records. If you want the common label names,
    call findCommonLabelNames
    '''
    allLabelNamesInAllRecords = []
    for record in inputRecordList:
        [allLabelNamesInAllRecords.append(name) for name in record.Labels.keys()]
        allLabelNames = set(allLabelNamesInAllRecords)
    return allLabelNames

def findCommonLabelNames(inputRecordList):
    '''
    Finds common (ie, exist in all Records) label names.
    '''
    N = len(inputRecordList)
    allLabelNames = findAllLabelNames(inputRecordList)
    commonLabelNames = []
    for name in allLabelNames:
        recordsWithName = list(filter(lambda x:name in x.Labels.keys(),inputRecordList))
        if len(recordsWithName)==N:
            commonLabelNames.append(name)
    
    return set(commonLabelNames)
    
def makeLabelTable(inputRecords):
    '''
    Returns a Pandas table of all labels in a list of records. 
    '''
    titleNames = findAllLabelNames(inputRecords)
    try:
        labelTable = pd.DataFrame(columns = titleNames)
    except:
        print('Pands table not working!')
    for record in inputRecords:
        recordLabels = {labelName:'& '.join(record.Labels[labelName]) for labelName in record.Labels.keys()}
        labelTable = labelTable.append(recordLabels,ignore_index=True)
    labelTable = labelTable.fillna('')       
    return labelTable      

def isValidLabel(input):
    '''Checks if label name is valid:
        - Only alphanumerics
        - No spaces
    '''
    print('Should check for label validation here!')

def labelReport(inputRecords,labelNames = []):
    '''
    Takes input records, generates table (calling other function), prints labels and returns table.
    To-do: right alignment!
    '''
    table = makeLabelTable(inputRecords)
    if len(labelNames)>0:
        labelNames = labelNames if isinstance(labelNames,list) else [labelNames]
        outtable = table[labelNames]
    else:
        outtable =table
        
    outtable.style.set_properties(**{'text-align': 'left'})
    
    print(outtable)
    return outtable

# a few tests if you want to see what the labelTools can do!
if __name__ =='__main__':
    dict1 = ParseNargsToDict({'Label1':'Test1','Label2':{'Test2','Test3'}})
    dict2 = ParseNargsToDict('Label1','Test1','Label2',['Test2','Test3'])
    
    