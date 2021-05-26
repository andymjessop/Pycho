#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 23 22:00:12 2021

@author: andymj
"""

from RecordArray import RecordArray
from Record import Record
import numpy as np
import datetime as dt

amp = [2,6,3,1,5]
offset = [2,2,2,-3,-3,3,0,0]
freq = [10,14,20,10,14,20,10,14]

Trigger = ['A','A','A','B','B','B','C','C']
Sequence = ['One','Two','Three','One','Two','Three','One','Two']

timeStamps = [dt.datetime.now() + dt.timedelta(minutes=step) for step in range(8)]

ChannelNames = ['Head','Shoulders','Knees','Toes','Nose']

T = 4
fs = 100
t = np.linspace(0,T,fs*T)

allData = RecordArray()
j=1
for o,f,trig,seq,time in zip(offset,freq,Trigger,Sequence,timeStamps):
    i=1
    for a,name in zip(amp,ChannelNames):
        y = a* np.sin(2*np.pi*f*t) + o
        allData.append(Record({'t':t,'data':y},Units = {'t':'s','data':'G'},
                              Labels = {'ChannelID':i,'Trigger':trig,'Sequence':seq,'ChannelName':name,'Event':j}))
        i+=1
    j+=1
        

allData.pull({'ChannelID':[1,2,3],'Trigger':'A'}).label({'ChannelDataQuality':'BAD'})
allData.pull({'ChannelID':4,'Sequence':'Two'}).label({'ChannelDataQuality':'Cheugy'})
allData.pull({'ChannelID':1,'Sequence':'Three'}).label({'ChannelName':'Noggin'})

allData.labelReport()
allData.setPlotOptions({'x_datum':'t','y_datum':'data'})  
allData.pull({'Event':1}).plot('samplePlot',colorLabels = ['Event','ChannelID'],legendLabels=['Event','ChannelID'])
allData.pull({'Sequence':'Two'}).plot('samplePlot1',colorLabels = ['Event','ChannelID'],legendLabels=['Event','ChannelID'])