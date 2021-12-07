
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

    def getSubList(self, lastSize):
        if(self.getLength() >= lastSize):
            return self.value[(self.getLength() - lastSize):]
        else:
            return self.value

    def getSubListRange(self, lastSize):
        if(self.getLength() >= lastSize):
            return (self.getLength() - lastSize, self.getLength())
        else:
            return (0, self.getLength())

class RawData(GraphData):

    def __init__(self, axsFrom: float, axsTo: float):

        super().__init__(axsFrom, axsTo)

    def update(self, value: float):
        self.value.append(value * self.axesTo / self.axesFrom)

    def getName(self):
        return "Raw Data"

class MovingAverage(GraphData):

    def __init__(self, axsFrom: float, axsTo: float, averageSize: int, getPopValue):

        self.averagingSize = averageSize
        self.sum: float = 0.0
        self.getPopValue = getPopValue

        super().__init__(axsFrom, axsTo)

    def update(self, value: float):

        if(len(self.value) >= (self.averagingSize)):
            self.sum -= self.getPopValue(self.averagingSize)
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

        if(self.getLength() == 0):
            self.last = value
        
        if(self.count == self.averagingSize):
            self.last = self.sum / self.averagingSize
            self.sum = 0.0
            self.count = 0
        
        self.value.append(self.last)

    def getName(self):
        return "Blocked Average"
    
