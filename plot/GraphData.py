# File to define classes to encapsulate 
# different Data Graphing Transforms.

# (C) Harith Manoj 2021


from typing import List, Literal


class GraphData:
    
    def __init__(self, axsFrom: float, axsTo: float, name = ""):

        self.axesFrom = axsFrom
        self.axesTo = axsTo
        self.name = name

        self.data = []

    def update(self, value: float):
        self.data.append(value * self.axesTo / self.axesFrom)

    def getData(self):
        return self.data

    def getLength(self):
        return len(self.data)

    def getValue(self, i):
        return self.data[i]

    def top(self):
        if(len(self.data) == 0):
            return 0.0
        else:
            return self.data[self.getLength() - 1]

    def getName(self):
        raise NotImplementedError()

    def getSubList(self, lastSize):
        if(self.getLength() >= lastSize):
            return self.data[(self.getLength() - lastSize):]
        else:
            return self.data

    def getSubListRange(self, lastSize):
        if(self.getLength() >= lastSize):
            return (self.getLength() - lastSize, self.getLength())
        else:
            return (0, self.getLength())

    def getName(self):
        return self.name

class MovingAverageGraph(GraphData):

    def __init__(self, axsFrom : float,
             axsTo : float, averageWindow : int, 
             inputGraph : GraphData, name = ""):

        self.averagingWindow = averageWindow
        self.inputData = inputGraph
        self.sum: float = 0.0

        super().__init__(axsFrom, axsTo, name)

    def update(self, value: float):
        len: int = 0
        
        if(self.inputData.getLength() > self.averagingWindow):

            self.sum -= self.inputData.getValue(self.inputData.getLength() - 1 - self.averagingWindow)
            len = self.averagingWindow
        else:
            len = self.inputData.getLength()
        
        self.sum += value

        super().update(self.sum / len)

    def update(self):
        self.update(self.inputData.top())

    def getName(self):

        return self.name + " | Moving Average {" + str(self.averagingWindow) + "} of " + self.inputData.name

class BlockedAverageGraph(GraphData):

    def __init__(self, axsFrom: float, axsTo: float, 
            averagingWindow: int, inputGraph: GraphData, name = ""):

        self.averagingWindow = averagingWindow
        self.inputData = inputGraph
        self.last: float = 0.0
        self.counter: int = 0
        self.sum: float = 0.0

        super().__init__(axsFrom, axsTo, name)

    def update(self, value: float):
        
        if(self.inputData.getLength() < self.averagingWindow):
            self.last = value

        self.sum += value
        self.counter += 1

        if(self.counter == self.averagingWindow):
            self.last = self.sum / self.averagingWindow
            self.sum = 0.0
            self.counter = 0
        
        super().update(self.last)

    def update(self):
        self.update(self.inputData.top())

    def getName(self):

        return self.name + " | Blocked Average {" + str(self.averagingWindow) + "} of " + self.inputData.name

class Gradient(GraphData):

    def __init__(self, axsFrom: float, axsTo: float, inputGraph: GraphData, name = ""):

        self.inputData = inputGraph
        super().__init__(axsFrom, axsTo, name)
  

    def update(self, value: float):

        if(self.inputData.getLength() < 2):
            super().update(value)
        else:
            super().update(value - self.inputData.getValue(self.inputData.getLength() - 2))

    def update(self):
        self.update(self.inputData.top())

    def getName(self):
        
        return self.name + " | Gradient of " + self.inputData.name
class AverageGradient(GraphData):

    def __init__(self, axsFrom: float, axsTo: float, 
            averagingWindow: float, inputGraph: GraphData, name=""):

        self.averagingWindow = averagingWindow
        self.inputData = inputGraph
        
        self.prevBlock = 0.0
        self.currBlock = 0.0

        super().__init__(axsFrom, axsTo, name=name)

    def update(self, value: float):
        
        if(self.inputData.getLength() < (self.averagingWindow * 2 + 1)):
            self.evaluationIndex = self.averagingWindow

            if(self.inputData.getLength() < self.averagingWindow):
                self.prevBlock += value
            elif(self.inputData.getLength() != self.averagingWindow):
                self.currBlock += value
                super().update(0)
        
            return None


        self.prevBlock -= self.inputData.getValue(self.inputData.getLength() - (self.averagingWindow * 2 + 2))
        self.prevBlock += self.inputData.getValue(self.inputData.getLength() - (self.averagingWindow + 2))
        self.currBlock -= self.inputData.getValue(self.inputData.getLength() - (self.averagingWindow + 1))
        self.currBlock += value

        super().update(self.currBlock - self.prevBlock)

    def update(self):
        self.update(self.inputData.top())

    def getName(self):
        
        return self.name + " | Average Distance {" + str(self.averagingWindow) + "} of " + self.inputData.name

        
Graphs = [
    "Raw Data", "Moving Average", "Blocked Average", "Average Gradient"
]
