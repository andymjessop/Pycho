#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 20:43:26 2021

@author: andymj
"""

import h5py as h5
import labelTools as lt
import codecs
import numpy as np
import bokehPlotTools as bp
import math
import datetime as dt
import os

DefaultPlotOptions = {'x_datum':'','y_datum':'',
               'xlog':False,'ylog':False,
               'color':'','lineStyle':'','width':1}

class InstanceDescriptor(object):
    '''
    Class to allow for instance-based descriptors. With these, I can add lazyDatum classes to records loaded from a file.
    Found on https://blog.brianbeck.com/post/74086029/instance-descriptors
    Not sure if this will screw something up....
    '''
    def __getattribute__(self, name):
        value = object.__getattribute__(self, name)
        if hasattr(value, '__get__'):
            value = value.__get__(self, self.__class__)
        return value

    def __setattr__(self, name, value):
        try:
            obj = object.__getattribute__(self, name)
        except AttributeError:
            pass
        else:
            if hasattr(obj, '__set__'):
                return obj.__set__(self, value)
        return object.__setattr__(self, name, value)
    
class lazyDatum():
    '''
    Class used to implement lazy loading of data from HDF5 file.
    '''
    def __init__(self,filename,path):
        if os.path.isfile(filename) and isinstance(path,str):
            self.file = filename
            self.path = path      
        else:
            raise TypeError('Invalid input given for datum!')

    def __get__(self,instance,cls):
            f = h5.File(self.file)
            data = f[self.path][:]
            return data
        
    def __set__(self,instance,value):
        raise AssertionError('Use addDatum or deleteDatum to manipulate datums!')    

class Record(InstanceDescriptor):

    def __init__(self,datums,Labels=None,Units=None,Quantities=None,TimeStamp=None):
        self.Datums = []
        self.Units = {}
        self.Labels = {}
        self.Quantities = {}
        self.TimeStamp = None
        self.PlotOptions = DefaultPlotOptions
        
        self.addDatum(datums)

        #add units - check that each datum exists!!
        if Units:
            self.assignUnits(Units)

        #add labels
        if Labels:
            self.label(Labels)
            
        if Quantities:
            self.assignQuantity(Quantities)
        else:
            self.defaultQuantities()

        if TimeStamp:
            self.assignTimeStamp(TimeStamp)
        
   
    def defaultQuantities(self):
        specialDefaults = {'t':'Time','f':'Frequency','data':'Data','y':'Data','x':'x'}
        for datum in self.Datums:
            if datum in specialDefaults:
                self.assignQuantity({datum:specialDefaults[datum]})
            
    def assignQuantity(self,datum_dict):
        #check that datum exists
        for datum in datum_dict:
            if datum in self.Datums:
                self.Quantities[datum] = datum_dict[datum]
            else:
                raise NameError(f'Datum {datum} does not exist in record!')
            
    
    @classmethod
    def loadFromFile(cls,filename):
        '''
        Creates a Record from an .h5 file. Pulls all relevant data from file and puts into Record.
        To-do: 
            - Load datums lazily?!?
            - Parse extra data in Properties
        '''
        with h5.File(filename,'r') as file:

            #compile dictionary of inputs:
            Data = file['Record/Data']
            Labels = file['Record/Labels']
            
            #filter out units and datums from all data
            unitData = {datumname:codecs.decode(Data[datumname][0],'UTF-8') for datumname in 
                        list(filter(lambda name:name.endswith('_units'),Data))}
            DataNames = list(filter(lambda name:not name.endswith('_units') and not name.endswith('_dimensions'),Data))
            
            datumData = {}
            for datumname in DataNames:
                datumData[datumname]=lazyDatum(filename,'Record/Data/{}'.format(datumname)) 
            
            #create label dictionary:
            AllLabelNames = Labels['Names'][:]
            AllLabelValues = Labels['Values'][:]
            
            label_dict = {}
            
            for name in AllLabelNames:
                labelName =codecs.decode(name['name'],'UTF-8')
                
                labelValues = []
                values = AllLabelValues[labelName]
    
                for labelVal in values:
                    [labelValues.append(codecs.decode(val,'UTF-8')) for val in values[0]]
                
                label_dict[labelName] = set(labelValues)
                 
            
            def pullTimeStamp(file):
                
                recordProps = file['Record/Properties']
                try:
                    hour = int(recordProps['timeStampHour'][0])
                except ValueError:
                    return None
                
                minute = int(recordProps['timeStampMinute'][0])
                secondfrac = float(recordProps['timeStampSecond'][0])
                second = int(math.floor(secondfrac))
                microsecond = int(secondfrac%1*1000)
                
                day = int(recordProps['timeStampDay'][0])
                month = int(recordProps['timeStampMonth'][0])
                year = int(recordProps['timeStampYear'][0])
                timezone = int(recordProps['timeStampTimeZone'][0])
                
                timeStamp = dt.datetime(year, month, day, hour, minute, second,microsecond)
                #timeStamp.timezone(timedelta(hours=timezone))
                return timeStamp
        
            timeStamp = pullTimeStamp(file)
        
        output = cls(datumData,Labels = label_dict,Units = unitData,TimeStamp = timeStamp)
        setattr(output,'filename',filename)
        
        return output
    
    def addDatum(self,datum_dict):
        #check if equal to length of other datums!
        [setattr(self,datumname,datum_dict[datumname]) for datumname in datum_dict]
        [self.Datums.append(datumname) for datumname in datum_dict]
    
    def assignUnits(self,unit_dict):
        for datumname in unit_dict:
            datumValue = unit_dict[datumname]
            datumname = datumname.replace('_units','')
            
            if datumname in self.Datums:
                self.Units[datumname] = datumValue
            else:
                raise AttributeError('Record has no datum named ' + datumname) 
                
    def label(self,label_dict):
        #parse label entries to dictionary? not yet
        clean_label_dict = lt.ParseNargsToDict(label_dict)
        for labelname in clean_label_dict:
            if labelname in self.Labels:
                self.Labels[labelname] = self.Labels[labelname].union(clean_label_dict[labelname])
            else:       
                self.Labels[labelname] = clean_label_dict[labelname]
             
    def setPlotOptions(self,option_dict):
        for dict_key in option_dict:
            self.PlotOptions[dict_key] = option_dict[dict_key]
            
    def assignTimeStamp(self,TimeStamp):
        if type(TimeStamp) is dt.datetime:
            self.TimeStamp= TimeStamp
        else:
            raise TypeError('Timestamp input must be a datetime object! datetime 64 is not support because it''s experimental.')
        
            
    def plot(self,outfilename,**OpArgs):
        bp.bokehPlot(self,outfilename)        
     
        
if __name__=='__main__':
    filename = '/Users/andymj/Library/Mobile Documents/com~apple~CloudDocs/pycho/echoData/TimeRecord_2.h5'
    q=Record.loadFromFile(filename)
    q.setPlotOptions({'x_datum':'t','y_datum':'data'})       
    # q.plot('test')
