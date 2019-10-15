# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 14:05:52 2019

@author: Binh
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 10:41:05 2018

@author: Binh
"""
import matplotlib 
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
#from skimage import io
#from skimage.io import imread
#from skimage.io._plugins import pil_plugin
#from skimage.io import use_plugin
#use_plugin('pil', 'imread')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import tkinter as tk    

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import font
from tkinter import filedialog

import time
import OpenOPC

import psutil as p



def prepare_cpu_usage():
         
         """helper function to return CPU usage info"""
         # get the CPU times using psutil module
         t = p.cpu_times()
         # return only the values we're interested in
         print(t)
         return t.user

def get_cpu_usage():
         global before

         """Compute CPU usage comparing previous and current
        measurements"""
         # take the current CPU usage information
         now = prepare_cpu_usage()

         return now
# Total number of iterations
         
def update_clock():
        global user,MAXITERS, l_user,fig,cnt,ax
        now = time.strftime("%H:%M:%S")
        window.after(500, update_clock)

        """Custom timerEvent code, called at timer event receive""" # get the cpu percentage usage
        result = get_cpu_usage()
        # append new data to the datasets
        user.append(result)
        # update lines data using the lists with new data
        l_user.set_data(range(len(user)), user)
        ax.set_xlim(0,cnt)
        # force a redraw of the Figure
        fig.canvas.draw()
        # if we've done all the iterations
        cnt += 1
        maxdata=max(user)
        mindata=min(user)
#        print(user)
        ax.set_ylim(mindata*0.90, maxdata*1.1)





class CPUMonitor():
 """Matplotlib Figure widget to display CPU utilization"""
 def __init__():
         global before,user,MAXITERS, l_user,fig,cnt,ax
         # save the current CPU info (used by updating algorithm)
         before = prepare_cpu_usage()
         # first image setup
         fig,ax = plt.subplots(1,figsize=(4,5))

         ax.set_autoscale_on(False)
         # generates first "empty" plots
         user=[]
         l_user, = ax.plot([],user, label='User %')

         # add legend to plot
         ax.legend()
         # force a redraw of the Figure
         fig.canvas.draw()
         # initialize the iteration counter
         cnt = 0
         # call the update method (to speed-up visualization)
         update_clock()

         








def initialize()
     opc = OpenOPC.client()
     opc.connect('UNICORN_OPC.System0.1')
    count = 0
    CPUMonitor.__init__()

    fig.show()



        
def settingChange(var=None):
    global threshfactor,minArea,colorIndex,intensityMode,widthFraction,relHeight
    global lambdaPara,pPara,selectedStrip,count,prominenceVal,distanceVal


def kill():
     plt.close("all")
     window.destroy()

MAXITERS = 30
     
window = tk.Tk()  
window.title("LFA Analysis")
window.geometry("700x900+0+0")
#canvas = FigureCanvasTkAgg(fig1, master=window)
#plot_widget = canvas.get_tk_widget()
appHighlightFont = tk.font.Font(family='Helvetica', size=8)
#window.size(10,10)


SampleIDsEntry = tk.Entry(window,width=30, font=appHighlightFont)
SampleIDsEntry.grid(row=24,column=3,columnspan=5)

exitBtn=tk.Button(window, text = "EXIT", command = kill, font=appHighlightFont)
openBnt=tk.Button(window,text="Open File",command=initialize, font=appHighlightFont)

openBnt.grid(row=2, column=3,columnspan=2)
exitBtn.grid(row=3, column=3,columnspan=2)
window.mainloop()
    


if __name__ == '__main__':
    import sys
from PyQt5 import QtWidgets
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)
else:
    app = QtWidgets.QApplication.instance() 

app.exec_()