# -*- coding: utf-8 -*-
"""
Created on Thu Aug 04 09:51:03 2016

@author: eta2
"""

import os
os.chdir('C:/users/eta2/Documents/Dymola/LPM_Enric')
from my_functions import *
os.chdir('D:/users/eta2/own_mat2/')
import matplotlib.pyplot as plt
import pandas as pd

#%% Get files to read
rootf=os.getcwd().replace('\\','/')+'/'
filesindir=os.listdir(rootf)
relevantfiles=[]
for candidate in filesindir:
    if 'hC' in candidate and '.txt' in candidate:
        relevantfiles.append(candidate)

# XV_data is a tuple full of dictionaries. 
# The key of the dictionaries is the beat number
RV_data=[]
LV_data=[]
RV_columns=['P3','V3']
LV_columns=['P6','V6']
for i,filename in enumerate(relevantfiles):
    rawd=pd.read_csv(filename)
    rawd_cl=rawd.drop_duplicates(subset='X',keep='last')
    RV_beatdata={}
    LV_beatdata={}
    for beat in range(1,2): #Beat 1
        RV_matrix,t_abs,t_rel=get_beat_data(rawd_cl,RV_columns)
        RV_beatdata[beat]=np.c_[t_rel,RV_matrix]
        LV_matrix,t_abs,t_rel=get_beat_data(rawd_cl,LV_columns)
        LV_beatdata[beat]=np.c_[t_rel,LV_matrix]
    RV_data.append(RV_beatdata)
    LV_data.append(LV_beatdata)

#%% Safety feature
creategraphs=False
#%% What to do
which_to_analyze='RV'
wta=which_to_analyze
if which_to_analyze=='LV':
    data=LV_data
    xlim=[60,160]
    ylim=[0,150]
elif which_to_analyze=='RV':
    data=RV_data
    xlim=[90,200]
    ylim=[0,50]
#%% Plot PV Loops
if creategraphs:
    for i,run_dict in enumerate(data):
        plt.clf()
        for beat in range(1,2): #Beat 1
            plt.plot(run_dict[beat][:,2]/1000,run_dict[beat][:,1]*7500)
        plt.xlim(xlim)
        plt.ylim(ylim)
        plt.savefig('./images/'+wta+'_PV_Loop_'+relevantfiles[i][:-4]+
                    '.png',dpi=250)
    #plt.show()

#%% Analyze data
#P_conv=[]
#V_conv=[]
#for i,run_dict in enumerate(data):
#    P_min_diff=np.min(run_dict[8][:,1])-np.min(run_dict[9][:,1])
#    P_max_diff=np.max(run_dict[8][:,1])-np.max(run_dict[9][:,1])
#    P_conv.append((abs(P_min_diff)+abs(P_max_diff))/2*7500)
#    V_min_diff=np.min(run_dict[8][:,2])-np.min(run_dict[9][:,2])
#    V_max_diff=np.max(run_dict[8][:,2])-np.max(run_dict[9][:,2])
#    V_conv.append((abs(V_min_diff)+abs(V_max_diff))/2/1000)
#
#P_conv=np.array(P_conv).T
#V_conv=np.array(V_conv).T

#%%
#f=open(wta+'PVconv.txt','w')
#np.savetxt(f,np.c_[P_conv,V_conv],fmt='%.5e',delimiter=',')
#f.close()

#%% Plot P and V over same plot

if creategraphs:
    for i,run_dict in enumerate(data):
        plt.clf()
        fig,ax1=plt.subplots()
        ax2=ax1.twinx()
        for beat in range(1,2): #Beats 8 & 9
            ax1.plot(run_dict[beat][:,0],run_dict[beat][:,1]*7500,'b-')
            ax2.plot(run_dict[beat][:,0],run_dict[beat][:,2]/1000,'r-')
#        ax1.plot(data[-1][beat][:,0],data[-1][beat][:,1]*7500,c=[0.5,0.5,1],linewidth=0.1)
#        ax2.plot(data[-1][beat][:,0],data[-1][beat][:,2]/1000,c=[1,0.5,0.5],linewidth=0.1)
        ax1.set_ylim(ylim)
        ax2.set_ylim(xlim)
        ax1.set_ylabel('P [mmHg]')
        ax2.set_ylabel('V [ml]')
        ax1.set_xlim([0,1])
        for tl in ax1.get_yticklabels():
            tl.set_color([0.3,0.3,0.8])
        for tl in ax2.get_yticklabels():
            tl.set_color([0.8,0.3,0.3])
        plt.savefig('./images/'+wta+'_P_V_'+relevantfiles[i][:-4]+
                    '.png',dpi=250)

#%% Plot all beats
creategraphs=False
if creategraphs:
    for i,run_dict in enumerate(data):
        plt.clf()
        fig,ax1=plt.subplots()
        ax2=ax1.twinx()
        for beat in range(1,10): #Beats 1 to 9
            ax1.plot(run_dict[beat][:,0]+beat-1,run_dict[beat][:,1]*7500,'b-',linewidth=0.5)
            ax2.plot(run_dict[beat][:,0]+beat-1,run_dict[beat][:,2]/1000,'r-',linewidth=0.5)
            ax1.plot(data[-1][beat][:,0]+beat-1,data[-1][beat][:,1]*7500,c=[0.5,0.5,1],linewidth=0.1)
            ax2.plot(data[-1][beat][:,0]+beat-1,data[-1][beat][:,2]/1000,c=[1,0.5,0.5],linewidth=0.1)
        ax1.set_ylim(ylim)
        ax2.set_ylim(xlim)
        ax1.set_ylabel('P [mmHg]')
        ax2.set_ylabel('V [ml]')
        ax1.set_xlim([0,9])
        for tl in ax1.get_yticklabels():
            tl.set_color([0.3,0.3,0.8])
        for tl in ax2.get_yticklabels():
            tl.set_color([0.8,0.3,0.3])
        plt.savefig('./images/'+wta+'_all_P_V_base&num_'+relevantfiles[i][-8:-4]+
                    '.png',dpi=250)

#%%

#bla=np.arange(0,100,0.1)
#fig,ax1=plt.subplots()
#ax1.plot(bla,bla*10)
#ax2=ax1.twinx()
#ax2.plot(bla,-bla)
#plt.show()
