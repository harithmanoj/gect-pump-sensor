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

def loadData():

    files = []

    for path in pathlib.Path('dataLogs').rglob('*.log'):
        files.append(path.name)

    return files

class GraphData:
    
    def __init__(self, axsFrom: float, axsTo: float):

        self.axesFrom = axsFrom
        self.axesTo = axsTo

        self.value = []

    def update(self, value: float):
        raise NotImplementedError()

    def getData(self):
        return self.value

    def getLength(self):
        return len(self.value)

    def getValue(self, i):
        return self.value[i]

    def top(self):
        if(len(self.value) == 0):
            return 0.0
        else:
            return self.value[self.getLength() - 1]

    def getName(self):
        raise NotImplementedError()

class RawData(GraphData):

    def __init__(self, axsFrom: float, axsTo: float):

        super().__init__(axsFrom, axsTo)

    def update(self, value: float):
        self.value.append(value * self.axesTo / self.axesFrom)

    def getName(self):
        return "Raw Data"

class MovingAverage(GraphData):

    def __init__(self, axsFrom: float, axsTo: float, averageSize: int):

        self.averagingSize = averageSize
        self.sum: float = 0.0

        super().__init__(axsFrom, axsTo)

    def update(self, value: float):

        if(len(self.value) >= (self.averagingSize)):
            self.sum -= self.value[len(self.value) - self.averagingSize]
            self.sum += value
            self.value.append(self.sum / self.averagingSize)
        else:
            self.sum += value
            self.value.append(self.sum / (len(self.value)+ 1 ))

    def getName(self):
        return "Moving Average"

class BlockedAverage(GraphData):

    def __init__(self, axsFrom: float, axsTo: float, averagingSize: int) -> None:
        
        self.averagingSize = averagingSize
        self.sum: float = 0.0
        self.last: float = 0.0
        self.count: int = 0

        super().__init__(axsFrom, axsTo)

    def update(self, value: float):

        self.sum += value
        self.count += 1
        
        if(self.count == self.averagingSize):
            self.last = self.sum / self.averagingSize
            self.sum = 0.0
            self.count = 0
        
        self.value.append(self.last)

    def getName(self):
        return "Blocked Average"
    

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