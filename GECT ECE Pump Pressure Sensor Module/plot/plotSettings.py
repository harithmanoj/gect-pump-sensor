# Plot Settings class

import tkinter as tk
from tkinter.constants import GROOVE

from matplotlib.pyplot import text



class PlotSettings:

    def __init__(self, root, row, col, span, plotFunction, source, fig, canvas) -> None:
        
        self.root = root
        self.plotFunction = plotFunction
        self.source = source
        self.plotfig = fig
        self.plotCanvas = canvas

        self.frame = tk.Frame(master = self.root, relief = GROOVE, bd = 2)
        self.frame.grid(row = row, column = col, columnspan = span)

        self.titleLabel = tk.Label(master = self.frame, text = "Settings")
        self.titleLabel.grid(row = 0, column = 0, columnspan = 3)
        self.titleLabel.config(font = ("Courier", 20))

        self.frame.grid_rowconfigure(0, minsize = 20)

        self.rawEnable = tk.IntVar(self.frame)
        self.rawTick = tk.Checkbutton(master = self.frame, text = "Raw Plot",
            variable = self.rawEnable, onvalue = 1, offvalue = 0)
        self.rawTick.grid(row = 1, column = 0, columnspan = 3)
        self.rawEnable.set(1)

        self.movingEnable = tk.IntVar(self.frame)
        self.movingTick = tk.Checkbutton(master = self.frame, text = "Moving Average", 
            variable = self.movingEnable, onvalue = 1, offvalue = 0)
        self.movingTick.grid(row = 2, column = 0, columnspan = 2)
        self.movingEnable.set(1)

        self.movingAverageSize = tk.IntVar(self.frame)
        self.movingSize = tk.Entry(self.frame, textvariable = self.movingAverageSize)
        self.movingSize.grid(row = 2, column = 2)
        self.movingAverageSize.set(10)

        self.blockedEnable = tk.IntVar(self.frame)
        self.blockedTick = tk.Checkbutton(master = self.frame, text = "Blocked Average",
            variable = self.blockedEnable, onvalue = 1, offvalue = 0)
        self.blockedTick.grid(row = 3, column = 0, columnspan = 2)
        self.blockedEnable.set(1)

        self.blockingAverageSize = tk.IntVar(self.frame)
        self.blockingSize = tk.Entry(self.frame, textvariable = self.blockingAverageSize)
        self.blockingSize.grid(row = 3, column = 2)
        self.blockingAverageSize.set(10)

        self.axisScaleLabel = tk.Label(self.frame, text = "Axis Scale")
        self.axisScaleLabel.grid(row = 4, column = 0, columnspan = 3)

        self.fromValue = tk.DoubleVar(self.frame)
        self.fromEntry = tk.Entry(self.frame, textvariable = self.fromValue)
        self.fromEntry.grid(row = 5, column = 0)
        self.fromValue.set(1024)

        self.seperator = tk.Label(self.frame, text = " : ")
        self.seperator.grid(row = 5, column = 1)

        self.toValue = tk.DoubleVar(self.frame)
        self.toEntry = tk.Entry(self.frame, textvariable = self.toValue)
        self.toEntry.grid(row = 5, column = 2)
        self.toValue.set(3.3)

        self.plotButton = tk.Button(self.frame, text = "Plot", 
            command = lambda: self.plotFunction(
                self.rawEnable.get(), self.movingEnable.get(), self.blockedEnable.get(),
                self.movingAverageSize.get(), self.blockingAverageSize.get(),
                self.fromValue.get(), self.toValue.get(), self.source,
                self.plotfig, self.plotCanvas
            ))

        self.plotButton.grid(row = 7, column = 0, columnspan = 3)