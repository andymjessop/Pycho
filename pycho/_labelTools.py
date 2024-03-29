#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 22:06:56 2021

@author: andymj
"""

import re
from ._miscTools import forceString, forceSet, parseNargsToDict

try:
    import pandas as pd
except:
    print('You''ll need to install Pandas for some of these label functions to work!')
    pass

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
 
def pullRegex(inputRecordList,search_dict):
    '''
    The most generic pull command available.
    '''
    if len(inputRecordList)==0: return None

    
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

def purgeRegex(inputRecordList,search_dict):
    '''
    The most generic purge command available! 
    '''

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
    requested label(s) are not in all records.
    Resulting output is a little messy:
        - Array of all unique sets of labels given
        - Each entry in the array is another array, corresponding to labels in the order given
        - Each array is the set of entries.
    '''
    
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
    N = len(inputRecords)
    
    labelTableDict = {label:list('')*N for label in titleNames}
    
    for i,Record in enumerate(inputRecords):
        for label in titleNames:
            if label in Record.Labels.keys():
                labelTableDict[label].append(' & '.join(Record.Labels[label]))
    
    labelTable = pd.DataFrame(labelTableDict)
    
    # try:
    #     labelTable = pd.DataFrame(columns = titleNames)
    # except:
    #     print('Pands table not working!')
    # for record in inaputRecords:
    #     recordLabels = {labelName:' & '.join(record.Labels[labelName]) for labelName in record.Labels.keys()}
    #     labelTable = labelTable.append(recordLabels,ignore_index=True)
    # labelTable = labelTable.fillna('')       
    return labelTable      

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
    
    print(outtable.to_string())
    return outtable

def labelByFile(inputRecord,labelFile,labelNamesToMatch,sheet=0):
    #import
    labelNamesToMatch = forceSet(labelNamesToMatch)
    if labelFile.endswith('csv'):    
        labelData = pd.read_csv(labelFile)
    elif labelFile.endswith('xls') or labelFile.endswith('xlsx'):  
        labelData=pd.read_excel(labelFile,sheet=sheet)
    #find matches to labelNames
    labelsToMatch = {}
    for label in labelNamesToMatch:
        if len(inputRecord.Labels[label])>1:
            print('Warning: label ' + label + ' has more than 1 value. This may affect labelByFile performance!')
        labelsToMatch[label]=' & '.join(inputRecord.Labels[label])
    #find matching columns in labelTable (trim down rowMatch until all labels have been accounted for)
    rowMatch = labelData.copy()
    for label in labelsToMatch:
        rowMatch = rowMatch[rowMatch[label]==labelsToMatch[label]]
    
    #apply matches to record (build label Dictionary)
    labelDict = {}
    for num,row in rowMatch.iterrows():
        for labelCol in rowMatch:
        #build label dictionary to add
            labelDict[labelCol]={entry for entry in str(rowMatch.loc[num,labelCol]).split(' & ')}
            inputRecord.label(labelDict)
    


    