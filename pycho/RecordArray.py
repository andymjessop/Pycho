#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 20:32:07 2021

@author: andymj
"""

from . import _labelTools as lt
from .Record import Record 
import os
from .plotting import plotter
from ._miscTools import progressBar
import numpy as np
import random

class RecordArray():
    '''
    An array of records, providing a few advantages over a simple list:
            - Limits array to a single Record type (which makes things much easier)
            - Allows passes of entry-specific methods
            - Allows implementation of pull/purge operations
    '''
    def __init__(self,*entries):
        self.records = []
        [self.append(entry) for entry in entries]

    def __repr__(self):
        return 'RecordArray'
    
    def __str__(self):
        N = len(self.records)
        return f'RecordArray containing {N} Records'
    
    def __len__(self):
        return len(self.records)
    
    def __getitem__(self,index):
        return self.records[index]
    
    def plot(self,filename = None,**OpArgs):
        plotter.plot(self,filename,**OpArgs)  
        
    def append(self,*entries):
        for entry in entries:
            if len(self.records)==0:
                self.records.append(entry)
                self.type = type(entry)
            else:     
                if type(entry)==self.type:
                    self.records.append(entry)
                else:
                    raise TypeError('Record Arrays must contain the same type of record!')
        
   
    def pull(self,*labelsAndValues,**dict_LandV):
        search_dict = lt.arbLabelInput(*labelsAndValues,**dict_LandV)
        
        pulledRecords = lt.pullRegex(self.records,search_dict)
        
        output = RecordArray(*pulledRecords)
        
        return output
    
    def pullSub(self,*labelsAndValues,**dict_LandV):
        input_dict = lt.arbLabelInput(*labelsAndValues,**dict_LandV)
        search_dict = []
        for label in input_dict:
            search_dict[label] = {'.*' + value + '.*' for value in input_dict[label]}
        
        pulledRecords = lt.pullRegex(self.records,search_dict)
        
        output = RecordArray(*pulledRecords)
        
        return output
    
    def purge(self,*labelsAndValues,**dict_LandV):
        search_dict = lt.arbLabelInput(*labelsAndValues,**dict_LandV)
        
        remainingRecords = lt.purgeRegex(self.records,search_dict)
        
        output = RecordArray(*remainingRecords)
        
        return output
    
    def purgeSub(self,*labelsAndValues,**dict_LandV):
        input_dict = lt.arbLabelInput(*labelsAndValues,**dict_LandV)
        search_dict = []
        for label in input_dict:
            search_dict[label] = {'.*' + value + '.*' for value in input_dict[label]}
        
        remainingRecords = lt.purgeRegex(self.records,search_dict)
        
        output = RecordArray(*remainingRecords)
        
        return output

    def pullSample(self):
        return random.sample(self.records,1)
    
    def __iter__(self):
        self.i = 0
        return self
    
    def __next__(self):
        if self.i<len(self.records):
            
            record = self.records[self.i]
            self.i+=1
            return record
        else:
            raise StopIteration


    @classmethod
    def loadFromFolder(cls,pathInput):
        print('Looking for HDF5 files...',end='')
        h5filefilter = lambda x:'.h5' in x
        if os.path.isdir(pathInput):
            allfiles = list(os.listdir(pathInput))
            h5files = list(filter(h5filefilter,allfiles))  
            echoFiles = [os.path.join(pathInput,filename) for filename in h5files]      
        elif not isinstance(pathInput,list):
            echoFiles = [pathInput]
        else:
            echoFiles = list(filter(h5filefilter,pathInput))
        
        Nfiles = len(echoFiles)
        print(f'{Nfiles} Echo files found!')   
        
        with progressBar('Loading files') as pb:
            output = cls()
            next_percent = 0.05
            for i,filename in enumerate(echoFiles):
                
                output.append(Record.loadFromFile(filename))
                #update progress bar, but only pass a print message every 5%
                if i/Nfiles>next_percent: #only update every 5%!
                    pb.update(i/Nfiles)
                    next_percent+=0.05
        
        return output
    
    def __getattr__(self,func,*args):
       def method(*args):
           for record in self.records:
               try:
                   getattr(record,func)(*args)
               except:
                   raise TypeError(f'Record type does not have function {func}!')
       return method
    
    def labelReport(self):
        lt.labelReport(self.records)

    

   
        
#a quick sample of what we can do here
if __name__=='__main__':        
    q = RecordArray.loadFromFolder('/Users/andymj/Library/Mobile Documents/com~apple~CloudDocs/pycho/echoData2')
    
    q.setPlotOptions({'x_datum':'t','y_datum':'data'})  
    w= lt.findUniqueLabelValues(q.records,['ChannelID','Sequence'],return_dict = True)
    
    
    q.pull('Sequence','One').plot('test',colorLabels = ['Event','ChannelID'],legendLabels=['Event','ChannelID'])
 
                
