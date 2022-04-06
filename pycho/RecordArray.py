#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 20:32:07 2021

@author: andymj
"""

from . import labelTools as lt
from .Record import Record 
import os
from .plotting import bokehPlot as bp

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
    
    def plot(self,outfilename,**OpArgs):
        bp.bokehPlot(self.records,outfilename,**OpArgs)  
        
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
        pulledRecords = lt.pullRegex(self.records,*labelsAndValues,**dict_LandV)
        
        output = RecordArray(*pulledRecords)
        
        return output
    
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
        
        output = cls()
        [output.append(Record.loadFromFile(filename)) for filename in echoFiles]
        
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
 
                
