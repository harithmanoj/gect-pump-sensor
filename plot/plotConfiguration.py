# Plot Configuration class


# (C) Harith Manoj 2021

import tkinter as tk
from GraphData import Graphs
from tkinter.constants import GROOVE

class GraphInfo:

    def __init__(self, root, row, index: int, inputs: list[tk.StringVar]):

        self.frame = root
        self.row = row

        self.enable = tk.IntVar(self.frame)
        self.enableTick = tk.Checkbutton(master = self.frame, text = "Raw Plot",
            variable = self.enable, onvalue = 1, offvalue = 0)
        self.enableTick.grid(row = self.row, column = 0)
        self.enable.set(1)

        self.nameVar = tk.StringVar(self.frame)
        self.nameEntry = tk.Entry(self.frame, textvariable = self.nameVar)
        self.nameEntry.grid(row = self.row, column = 1)
        self.nameVar.set(str(index))

        self.typeVar = tk.StringVar(self.frame)
        self.typeSel = tk.OptionMenu(self.frame, self.typeVar, *Graphs)
        self.typeSel.grid(row = self.row, column = 2)
        self.typeVar.set(Graphs[0])

        self.arg1 = tk.DoubleVar(self.frame)
        self.arg1Entry = tk.Entry(self.frame, textvariable = self.arg1)
        self.arg1Entry.grid(row = self.row, column = 3)
        self.arg1.set(10)

        self.inputGraph = tk.StringVar(self.frame)
        self.inputList = []
        self.inputs = inputs
        self.index = index

        for i in range(0, index):
            self.inputList.append(inputs[i].get())

        self.inputGraphDrop = tk.OptionMenu(self.frame, self.inputGraph, *self.inputList)
        self.inputGraphDrop.grid(row = self.row, column = 4)
        self.inputGraph.set(inputs[index - 1])

        self.outputRow = tk.IntVar(self.frame)
        self.outputRowEntry = tk.Entry(self.frame, textvariable = self.outputRow)
        self.outputRowEntry.grid(row = self.row, column = 5)

        self.outputCol = tk.IntVar(self.frame)
        self.outputColEntry = tk.Entry(self.frame, textvariable = self.outputCol)
        self.outputColEntry.grid(row = self.row, column = 6)

    def shouldShow(self):
        return (self.enable.get() == 1)
    
    def getName(self):
        return self.nameVar

    def getType(self):
        return self.typeVar
    
    def getArg1(self):
        return self.arg1

    def getInputSelect(self):
        return self.inputGraph

    def getGraphPosition(self):
        return (self.outputRow, self.outputCol)

    def getColumnOrder():
        return ("Show", "Name", "Type", "Argument", "Input", "Graph Row", "Graph Column")

    def destroy(self):

        
        self.enableTick.destroy()

        self.nameEntry.destroy()

        self.typeSel.destroy()

        self.arg1Entry.destroy()

        self.inputGraphDrop.destroy()

        self.outputRowEntry.destroy()

        self.outputColEntry.destroy()

        


class PlotSettings:

    def __init__(self, root, row, col, span, plotFunction) -> None:
        
        self.root = root

        self.frame = tk.Frame(master = self.root, relief = GROOVE, bd = 2)
        self.frame.grid(row = row, column = col, columnspan = span)

        self.titleLabel = tk.Label(master = self.frame, text = "Settings")
        self.titleLabel.grid(row = self.row, column = 0, columnspan = 3)
        self.titleLabel.config(font = ("Courier", 20))

        self.frame.grid_rowconfigure(0, minsize = 20)

        self.frame.grid_columnconfigure(1, minsize = 10)

        self.graphList: list[GraphInfo] = []
        self.graphNames: list[tk.StringVar] = []

        self.row = 1

        self.fromValue = tk.DoubleVar(self.frame)
        self.fromEntry = tk.Entry(self.frame, textvariable = self.fromValue)
        self.fromEntry.grid(row = self.row, column = 0)
        self.fromValue.set(1024)

        self.seperator = tk.Label(self.frame, text = " : ")
        self.seperator.grid(row = self.row, column = 1)

        self.toValue = tk.DoubleVar(self.frame)
        self.toEntry = tk.Entry(self.frame, textvariable = self.toValue)
        self.toEntry.grid(row = self.row, column = 2)
        self.toValue.set(3.3)

        self.row += 1

        self.graphPropertyFrame = tk.Frame(self.frame)
        self.graphPropertyFrame.grid(row = self.row, column = 0, columnspan = 3)
        self.row +=1

        self.graphInfoTitle: list[tk.Label] = []
        for i in len(GraphInfo.getColumnOrder()):
            self.graphInfoTitle.append(tk.Label(self.graphPropertyFrame, text = GraphInfo.getColumnOrder()[i]))
            self.graphInfoTitle[i].grid(row = 0, column = i)

        self.graphList.append(GraphInfo(self.graphPropertyFrame, 1, 0, self.graphNames))
        self.graphNames.append(self.graphList[0].getName())

        self.addButton = tk.Button(self.frame, text = "+", command = self.addGraph())
        self.addButton.grid(row = self.row, column = 0)
        
        self.delButton = tk.Button(self.frame, text = "-", command = self.redGraph())
        self.delButton.grid( row = self.row, column = 2)

        self.row += 1

        self.plotButton = tk.Button(self.frame, text = "Plot", command = self.plot())

        self.plotButton.grid(row = 7, column = 0, columnspan = 3)

        self.plotFunction = plotFunction

    
    def addGraph(self):
        self.graphList.append(GraphInfo(self.graphPropertyFrame, len(self.graphList) + 1, len(self.graphList), self.graphNames))
        self.graphNames.append(self.graphList[len(self.graphList) -1].getName())

    def redGraph(self):
        if(len(self.graphList) == 1):
            return
        self.graphNames.pop()
        self.graphList[len(self.graphList) - 1].destroy()
        self.graphList.pop()

    def plot(self):
        self.plotFunction()