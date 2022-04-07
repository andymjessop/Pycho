#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 21:29:49 2022

@author: andymj
"""

class progressBar:
    def __init__(self,ProgressMessage):
        self.ProgressMessage = ProgressMessage
        print(ProgressMessage + ':[' + '{0: <20}'.format('') +']',end='')
        
    def update(self,percentage):
        print(r'',end = '')
        n_x = int(percentage*20)
        print('\r'+self.ProgressMessage + ':[' + '{0: <20}'.format('x'*n_x) +']',end='')

    def __enter__(self):
        return self
        
    def __exit__(self,type, value, traceback):
       print('\r'+self.ProgressMessage + ':[' + '{0: <20}'.format('x'*20) +']',end='\n')
        
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
                output.append('{:.2f}'.format(entry)) #is this the right format to use for a float??
    return set(output)

def forceSet(val):
    if type(val) is set:
        output = val
    elif type(val) is list:
        output = set(val)
    else:
        output = {val}
    return output

def parseNargsToDict(*narg,**darg): 
    '''
    Takes arguments given MATLAB-style ('name','value') and converts to a properly-formatted label dictionary {'name':'value'}}.
    '''
    #to-do: format so all values are strings!
    arguments = narg
    dictionary = {}
    if len(arguments)==1 and isinstance(arguments[0],dict): #if someone put a dictionary in the first time!  
        dictionary = arguments[0]
    else: #if we just have a bunch of name-value pairs
        N = len(arguments)
        if (N % 2) == 0: 
            dictionary = {}
            for i in range(0,N,2):
                key = arguments[i]
                value = arguments[i+1] 
                dictionary[key]=forceSet(value)        
        else:
            raise ValueError('Inputs must be name,value pairs!')
            return
    #add dictionary arguments
    dictionary ={**dictionary,**darg}
    
    return dictionary  