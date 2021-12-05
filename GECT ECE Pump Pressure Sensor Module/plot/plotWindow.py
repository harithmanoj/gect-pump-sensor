# Python Application to plot line feed seperated values.


from logging import root
from sys import api_version
from typing import List

from matplotlib.figure import Figure
from scrollableSourceList import SourceList
from plotSettings import PlotSettings
import pathlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

import tkinter as tk

from DataForms import *

def loadData():

    files = []

    for path in pathlib.Path('dataLogs').rglob('*.log'):
        files.append(path.name)

    return files

def read(file):

    f = open(file, "r", encoding = 'utf-8')

    data = []

    for line in f:
        if(line != "\n"):
            data.append(float(line) * 3.3 / 1024)
            
            
    f.close()

    return data

xMax = 0

def plotFunction(
                rawEnable, movingEnable, blockedEnable,
                movingAverageSize, blockingAverageSize,
                fromValue, toValue, source, fig, canvas
            ):

    graphs: list[GraphData] = []

    if(rawEnable == 1):
        graphs.append(RawData(fromValue, toValue))
        fromValue = 1
        toValue = 1
    
    if(movingEnable == 1):
        graphs.append(MovingAverage(fromValue, toValue, movingAverageSize))
        fromValue = 1
        toValue = 1

    if(blockedEnable == 1):
        graphs.append(BlockedAverage(fromValue, toValue, blockingAverageSize))

    f = open(source(), "r", encoding = 'utf-8')

    for line in f:
        if(line != "\n"):
            value = float(line)
            for g in graphs:
                g.update(value)
                value = g.top()
    plt.clf()

    axes = fig().add_subplot(111)

    legend = []

    for g in graphs:
        axes.plot(g.getData())
        legend.append(g.getName())

    axes.legend(legend)

    global xMax
    xMax = graphs[0].getLength()
    
    canvas().draw()

def main():

    rootWindow = tk.Tk()

    titleString = "Plot From File { line feed seperated values }"

    rootWindow.title(titleString)

    title = tk.Label(rootWindow, text = titleString)
    title.grid(row = 0, column = 0, columnspan = 4)
    title.config(font = ("Courier", 40))

    rootWindow.grid_columnconfigure(0, minsize = 20)

    quitBtn = tk.Button(rootWindow, text = "Quit", command = rootWindow.destroy)
    quitBtn.grid(row = 1, column = 0)

    frame = tk.Frame(rootWindow)
    frame.grid(row = 2, column = 3)

    fig = plt.figure(figsize=(12,7.5), dpi = 100)
    
    canvas = FigureCanvasTkAgg(fig,
                               master = frame)  
    canvas.draw()
    
  
    canvas.get_tk_widget().pack()
  
    toolbar = NavigationToolbar2Tk(canvas,
                                   frame)
    toolbar.update()
  
    canvas.get_tk_widget().pack()

    sourceFiles = SourceList(rootWindow, "Files", loadData, 2, 1, 1)
    plotSettings = PlotSettings(
        rootWindow, 2, 2, 1, plotFunction, 
        lambda: "dataLogs/" + sourceFiles.get(), 
        lambda: (fig), 
        lambda: (canvas)
        )

    tk.mainloop()

if __name__ == "__main__":
    main()