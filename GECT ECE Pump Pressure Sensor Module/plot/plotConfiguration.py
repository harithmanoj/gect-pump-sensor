# Plot Configuration class


# (C) Harith Manoj 2021

import tkinter as tk
from GraphData import Graphs
from tkinter.constants import GROOVE

class GraphInfo:

    def __init__(self, root, row, col, span, index: int, inputs: list[tk.StringVar]):

        self.root = root


        self.frame = tk.Frame(master = self.root, relief = GROOVE, bd = 2)
        self.frame.grid(row = row, column = col, columnspan = span)

        self.enable = tk.IntVar(self.frame)
        self.enableTick = tk.Checkbutton(master = self.frame, text = "Raw Plot",
            variable = self.enable, onvalue = 1, offvalue = 0)
        self.enableTick.grid(row = 0, column = 0)
        self.enable.set(1)

        self.nameVar = tk.StringVar(self.frame)
        self.nameEntry = tk.Entry(self.frame, textvariable = self.nameVar)
        self.nameEntry.grid(row = 0, column = 1)
        self.nameVar.set(str(index))

        self.typeVar = tk.StringVar(self.frame)
        self.typeSel = tk.OptionMenu(self.frame, self.typeVar, *Graphs)
        self.typeSel.grid(row = 0, column = 2)
        self.typeVar.set(Graphs[0])

        self.arg1 = tk.DoubleVar(self.frame)
        self.arg1Entry = tk.Entry(self.frame)
        self.arg1Entry.grid(row = 0, column = 3)
        self.arg1.set(10)

        self.inputGraph = tk.StringVar(self.frame)
        self.inputList = []
        self.inputs = inputs
        self.index = index

        for i in range(0, index):
            self.inputList.append(inputs[i].get())

        self.inputGraphDrop = tk.OptionMenu(self.frame, self.inputGraph, *self.inputList)
        self.inputGraphDrop.grid(row = 0, column = 4)
        self.inputGraph.set(inputs[index - 1])

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

        


class PlotSettings:

    def __init__(self, root, row, col, span) -> None:
        
        self.root = root

        self.frame = tk.Frame(master = self.root, relief = GROOVE, bd = 2)
        self.frame.grid(row = row, column = col, columnspan = span)

        self.titleLabel = tk.Label(master = self.frame, text = "Settings")
        self.titleLabel.grid(row = 0, column = 0, columnspan = 3)
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

        self.

        self.plotButton = tk.Button(self.frame, text = "Plot")

        self.plotButton.grid(row = 7, column = 0, columnspan = 3)