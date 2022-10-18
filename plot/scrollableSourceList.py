
# Scrollable Source list
# (C) Harith Manoj 2021

import tkinter as tk
from tkinter.constants import END, GROOVE, SINGLE


class SourceList:

    def __init__(self, root, title, loadData, row, col, span):

        self.loadData = loadData
        self.root = root
        self.frame = tk.Frame(self.root, relief = GROOVE, bd = 2)
        self.frame.grid(row = row, column = col, columnspan = span)

        self.titleLabel = tk.Label(self.frame, text = title)
        self.titleLabel.grid(row = 0, column = 0, columnspan = 2)
        self.titleLabel.config(font = ("Courier", 20))

        self.frame.grid_rowconfigure(0, minsize = 10)
        
        self.source = tk.Listbox(self.frame, selectmode = SINGLE)
        self.source.grid(row = 1, column = 0)

        self.sourceScroll = tk.Scrollbar(self.frame)
        self.sourceScroll.grid(row = 1, column = 1)

        self.source.config(yscrollcommand = self.sourceScroll.set)

        self.sourceScroll.config(command  = self.source.yview)

        self.reload = tk.Button(self.frame, text = "reload", command = lambda: self.setSources(self.loadData()))
        self.reload.grid(row = 2, column = 0, columnspan = 2)

        self.setSources(self.loadData())

    def setSources(self, sources):
        self.source.delete(0, END)
        for i in sources:
            self.source.insert(END, i)

        self.source.selection_set(0)

    def get(self):
        return self.source.get(self.source.curselection())

