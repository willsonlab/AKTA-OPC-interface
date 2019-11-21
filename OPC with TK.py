# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 10:41:05 2018

@author: Binh
"""
import matplotlib 
#matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk    
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import font

#from tkinter import filedialog

import time
import OpenOPC

#def stat(data,windowsize):
#    rollingAvg=pd.rolling_mean(data,windowsize)
    
def switch_valve():
        global valvepos
        opc.write(('System 1\INSTRUCTION\Flowpath\ColumnPosition\Position',valvepos))
        opc.write(('System 1\INSTRUCTION\Flowpath\ColumnPosition\ColumnPosition_Exe',1))
        print("current valve is ",valvepos)
#        opc.write((r'System 1\INSTRUCTION\Other\SetMark\Name','column switched'))
#        opc.write((r'System 1\INSTRUCTION\Other\SetMark\SetMark_Exe',1))

def get_OPC_values():
         global before
         OPCString=opc.read('System 1\EVENT\ANALOG\AD900')
         OPCdata=float(OPCString[0])
         print(OPCdata)
         return OPCdata
         
def update_clock():
        global data,Avg, windowsize,l_data,fig,cnt,ax,threshold,windowsizeEntry,activate_status,rollingAvg,l_average
        global average,StandardDev, connection_status

        now = time.strftime("%H:%M:%S")
        window.after(500, update_clock)
        """Custom timerEvent code, called at timer event receive""" 
        if (connection_status):
            result = get_OPC_values()
            # append new data to the datasets
            data.append(result)
        # update lines data using the lists with new data
        l_data.set_data(range(len(data)), data)
        ax.set_xlim(0,cnt)
        # force a redraw of the Figure
        # if we've done all the iterations
        cnt += 1
        windowsize=int(windowsizeEntry.get())
        maxdata=max(data)
        mindata=min(data)
        if len(data)>(windowsize+1):
            average=np.average(data[len(data)-windowsize:])
            StandardDev=np.std(data[len(data)-windowsize:])
            rollingAvg.append(average)
            Avg.set(str(average))
            STD.set(str(StandardDev))
            l_average.set_data(range(len(rollingAvg)), rollingAvg)
            window.update_idletasks()

#        print(data)
            
        ax.set_ylim(mindata*0.90, maxdata*1.1)
        fig.canvas.draw()
        
        if (activate_status==True):
            if (result > threshold):
                print("Threshold reached")
                switch_valve()    
                activate_status=False
                v.set(False)
            

    


class OPC_control():
 def __init__():
         global before,data, l_data,fig,cnt,ax,rollingAvg,l_average
         before = get_OPC_values()
         # first image setup
         fig,ax = plt.subplots(1,figsize=(8,4))
         ax.set_autoscale_on(False)
         # generates first "empty" plots
         data=[]
         rollingAvg=[]
         l_data, = ax.plot([],data, label='AD900')
         l_average, =ax.plot([],rollingAvg, label='Avg')
         # add legend to plot
         ax.legend()
         # force a redraw of the Figure
         fig.canvas.draw()
         # initialize the iteration counter
         cnt = 0
         # call the update method (to speed-up visualization)
         update_clock()



def initialize():
    global opc,activate_status,connection_status
    activate_status=False
    if not(connection_status):
        connection_status=True
        opc.connect('UNICORN_OPC.System0.1')
        OPC_control.__init__()
    fig.show()



        
#def settingChange(var=None):
#    global threshfactor,minArea,colorIndex,intensityMode,widthFraction,relHeight
#    global lambdaPara,pPara,selectedStrip,count,prominenceVal,distanceVal
def activate():
        global activate_status,threshold,valvepos
        
        print("Threshold: ", threshold, "Valve: ", valvepos)

        if not(str(ThresholdEntry.get())==''):
            threshold=float(str(ThresholdEntry.get()) )  
        else: 
            threshold=0
        if not (str(ValvePosEntry.get())==''):   
            valvepos=int(ValvePosEntry.get())
        if (abs(threshold)>0 and valvepos>0):
            activate_status=True
        else:
            v.set(False)

        
def deactivate():
        global activate_status,threshold,valvepos
        activate_status=False


def kill():
     global opc
     if (connection_status):
        opc.close()
     plt.close("all")
     window.destroy()
     
def calThreshold():
    global average,StandardDev
    threshold=average+ (3*StandardDev)
    ThresholdEntry.delete(0,END)
    ThresholdEntry.insert(0,str(threshold))

    
def disconnectOPC():
    global opc,connection_status
    if (connection_status):
        opc.close()
        connection_status=False

def Switch():
    global opc,ValvePosEntry,valvepos
    if not (str(ValvePosEntry.get())==''):   
        valvepos=int(ValvePosEntry.get())
        switch_valve()


connection_status=False
opc = OpenOPC.client()
threshold=0
valvepos=0   
windowsize=10
window = tk.Tk()  
window.title("OPC controller")
window.geometry("300x300+0+0")
#canvas = FigureCanvasTkAgg(fig1, master=window)
#plot_widget = canvas.get_tk_widget()
appHighlightFont = tk.font.Font(family='Helvetica', size=8)
tk.Label(window, text="Threshold", font=appHighlightFont).grid(row=8,column=2,columnspan=2)

ThresholdEntry = tk.Entry(window,width=30, font=appHighlightFont)
ThresholdEntry.grid(row=8,column=5,columnspan=3)

windowsizeEntry  = tk.Entry(window,width=30, font=appHighlightFont)
windowsizeEntry.grid(row=3,column=5,columnspan=3)
windowsizeEntry.insert(0,'10')

tk.Label(window, text="Valve Position", font=appHighlightFont).grid(row=9,column=2,columnspan=2)
Avg = StringVar()
Avg.set('--')
tk.Label(window, text="Average    ", font=appHighlightFont).grid(row=5,column=2,columnspan=3)
tk.Label(window, text="Window Size", font=appHighlightFont).grid(row=3,column=2,columnspan=3)
tk.Label(window, text="STD        ", font=appHighlightFont).grid(row=6,column=2,columnspan=3)

STD = StringVar()
STD.set('--')
AvgLabel=tk.Label(window, textvariable= Avg, font=appHighlightFont).grid(row=5,column=5,columnspan=4)
StdLabel= tk.Label(window, textvariable=STD, font=appHighlightFont).grid(row=6,column=5,columnspan=2)

ValvePosEntry = tk.Entry(window,width=30, font=appHighlightFont)
ValvePosEntry.grid(row=9,column=5,columnspan=1)

CalculateBtn=tk.Button(window, text = "Calculate Threshold", command = calThreshold , font=appHighlightFont)
CalculateBtn.grid(row=7, column=3,columnspan=2)

v = IntVar()
v.set(False)
activateBtn=tk.Radiobutton(window, text = "Activate", command = activate, variable=v, value=True, font=appHighlightFont)
deactivateBtn=tk.Radiobutton(window, text = "Deactivate", command = deactivate, variable=v, value=False, font=appHighlightFont)

activateBtn.grid(row=11, column=3,columnspan=1)
deactivateBtn.grid(row=12, column=3,columnspan=1)

exitBtn=tk.Button(window, text = "EXIT", command = kill, font=appHighlightFont)
openBtn=tk.Button(window,text="Open Connection",command=initialize, font=appHighlightFont)
disconnectBtn=tk.Button(window,text="Disconnet OPC",command=disconnectOPC, font=appHighlightFont)
disconnectBtn.grid(row=13, column=3,columnspan=2)
PositionBtn=tk.Button(window,text="Valve Switch",command=Switch, font=appHighlightFont)
PositionBtn.grid(row=10, column=5,columnspan=2)
openBtn.grid(row=2, column=3,columnspan=2)
exitBtn.grid(row=14, column=3,columnspan=3)
window.mainloop()
    


#if __name__ == '__main__':
#    import sys
#from PyQt4 import QtWidgets
#if not QtWidgets.QApplication.instance():
#    app = QtWidgets.QApplication()
#else:
#    app = QtWidgets.QApplication.instance() 

#app.exec_()
