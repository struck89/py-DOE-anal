# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 18:15:02 2016

@author: eta2
"""
import pandas as pd
import numpy as np
#%% Stupid functions to check if list contains numbers or strings
def isanum(val):
    try:
        abs(val)
        return True
    except:
        return False

def isastr(val):
    try:
        val.capitalize()
        return True
    except:
        return False

def ispanda(data):
    try:
        data.columns[0]
        return True
    except:
        return False
        
def isnparray(data):
    try:
        abs(data[0][0])
        return True
    except:
        return False

def isinteger(val):
    if val%1==0:
        return True
    else:
        return False
    
#%%
def get_beat_data(data,columns,seconds='last',starteqend=False,preloadduration=0.3):
    """Given a numpy array, or a panda data frame, assuming that the first
    column is time, or that time goes by the name 'X' (for panda), it returns 
    the requested columns for the seconds requested (by default only the last 
    second), and if desired, it modifies the first 0.1s so that the values at 
    the end are the same as the values at the beginning.
    Seconds can be 'last', [initial time, final time], beat# (integer)
    """
    if ispanda(data) and isastr(columns[0]):
        time=data.as_matrix(['X'])
        data=data.as_matrix(columns)
    elif isnparray(data) and isanum(columns[0]):
        data=np.array(data)
        time=data[:,[0]].copy()
        data=data[:,columns].copy()
    else:
        return None
    time=time.transpose()[0]
    if str(seconds)=='last':
        seconds=[time[-1]-1,time[-1]]
    elif isanum(seconds):
        if len(np.array([seconds]))>1:
            pass
        #now check if we wanted a beat#
        elif isinteger(seconds):
            pld=preloadduration
            seconds=[seconds-1+pld,seconds+pld]
        else:
            return None
    #start row(sr) and end row (er)
    sr=np.argmin(abs(time-seconds[0]))
    er=np.argmin(abs(time-seconds[-1]))
    data=data[sr:er+1]
    timeabs=time[sr:er+1].copy()
    timerel=timeabs-timeabs[0]
    if starteqend:
        if timerel[-1]<0.05:
            return None
        #fifty ms row
        fiftymsr=np.argmin(abs(timerel-0.05))
        #time as a column again, multiplied horizontally to reach the desired dim
        t=np.array([timerel[:fiftymsr+1]]).T 
        t=np.tile(t,(1,data.shape[1]))
        #vf/vi (relationship between final value (vf) and initial value (vi))
        vf_vi=np.tile(data[-1]/data[0],(fiftymsr+1,1))
        adj_mat=(1-vf_vi)/0.05*t+vf_vi
        data[:fiftymsr+1,:]=data[:fiftymsr+1,:]*adj_mat
    return data,np.array([timeabs]).T,np.array([timerel]).T
        