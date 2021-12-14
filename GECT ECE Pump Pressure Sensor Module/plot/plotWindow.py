# Python Application to plot line feed seperated values.


from logging import root
from sys import api_version
from typing import Any, List

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
            data.append(float(line))
            
            
    f.close()

    return data

xMax = 0


def getLastValue(x, graphs):

    return graphs[1].getValue(graphs[1].getLength() - (x + 1))

def getTripletValues(x, graphs):

    if(graphs[0].getLength() < (2 * x + 1)):
        return (0, 0, 0)
    else:
        return (getLastValue(2*x + 1, graphs), getLastValue(x + 1, graphs), getLastValue(x, graphs))

def plotFunction(
                rawEnable, movingEnable, blockedEnable,
                movingAverageSize, blockingAverageSize,
                fromValue, toValue, source, fig, canvas
            ):

    graphs : list[GraphData] = []
    inputValue : list[int] = []

    orig = (fromValue, toValue)

    if(rawEnable == 1):
        graphs.append(RawData(fromValue, toValue))
        inputValue.append(-1)
        fromValue = 1
        toValue = 1
    
    if(movingEnable == 1):
        graphs.append(
            MovingAverage(fromValue, toValue, movingAverageSize, 
            lambda x, graphs = graphs: graphs[0].getValue(graphs[0].getLength() - (x + 1)), str(movingAverageSize)))
        inputValue.append(0)
        fromValue = 1
        toValue = 1

    if(blockedEnable == 1):
        graphs.append(BlockedAverage(fromValue, toValue, blockingAverageSize, "of mov " + str(movingAverageSize)))
        inputValue.append(len(graphs) - 2)

    '''if(movingEnable == 1):
        graphs.append(
            MovingAverage(fromValue, toValue, movingAverageSize * 2, 
            lambda x, graphs = graphs: graphs[0].getValue(graphs[0].getLength() - (x + 1)), str(movingAverageSize * 2)))
    
        inputValue.append(0)
'''
    tapMarks = StepDetector(
        blockingAverageSize,
        lambda x, graphs = graphs: (getTripletValues(x, graphs)), 25 * 3.3 / 1024.0, " Moving Average Tap Detection"
        )
    
    f = open(source(), "r", encoding = 'utf-8')

    for line in f:
        if(line != "\n"):
            value = float(line)
            for (g, i) in zip(graphs, inputValue):
                if(i == -1):
                    g.update(value)
                else:
                    g.update(graphs[i].top())
            tapMarks.update(graphs[1].top())
    plt.clf()

    axes = fig().add_subplot(111)

    legend = []

    for g in graphs:
        axes.plot(g.getData())
        legend.append(g.getName())

    for x in tapMarks.getData():
        axes.annotate('Tap', xy = (x, graphs[1].getValue(x) + 0.1), xytext = (x, graphs[1].getValue(x) + 0.2), 
            arrowprops = dict(facecolor = 'green', shrink = 0.05 ))

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