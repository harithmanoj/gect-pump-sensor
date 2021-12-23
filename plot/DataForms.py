

class GraphData:
    
    def __init__(self, axsFrom: float, axsTo: float, name = ""):

        self.axesFrom = axsFrom
        self.axesTo = axsTo
        self.name = name

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

    def getName(self):
        return self.name

class RawData(GraphData):

    def __init__(self, axsFrom: float, axsTo: float, name = ""):

        super().__init__(axsFrom, axsTo, name)
        self.name = "Raw Data " + name

    def update(self, value: float):
        self.value.append(value * self.axesTo / self.axesFrom)

class MovingAverage(GraphData):

    def __init__(self, axsFrom: float, axsTo: float, averageSize: int, getPopValue, name = ""):

        self.averagingSize = averageSize
        self.sum: float = 0.0
        self.getPopValue = getPopValue

        super().__init__(axsFrom, axsTo)
        self.name = "Moving Average " + name

    def update(self, value: float):

        if(len(self.value) >= (self.averagingSize)):
            self.sum -= self.getPopValue(self.averagingSize)
            self.sum += value
            self.value.append(self.sum / self.averagingSize)
        else:
            self.sum += value
            self.value.append(self.sum / (len(self.value)+ 1 ))

class BlockedAverage(GraphData):

    def __init__(self, axsFrom: float, axsTo: float, averagingSize: int, name) -> None:
        
        self.averagingSize = averagingSize
        self.sum: float = 0.0
        self.last: float = 0.0
        self.count: int = 0

        super().__init__(axsFrom, axsTo)
        self.name = "Blocked Average " + name

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

class StepDetector(GraphData):

    def __init__(self, windowSize: int, getValues, threshold, name):

        self.windowSize = windowSize
        self.getPlotValues = getValues
        self.prevSum = 0.0
        self.nextSum = 0.0
        self.lastDifference = 0.0
        self.evaluationIndex = 0
        self.descFlag = False
        self.threshold = threshold
        

        super().__init__(1, 1)
        self.name = "Step Detect " + name

    def update(self, value: float):

        self.evaluationIndex += 1
        val = self.getPlotValues(self.windowSize)
        self.prevSum -= val[0]
        self.prevSum += val[1]
        self.nextSum -= val[2]
        self.nextSum += value

        diff = abs(self.prevSum - self.nextSum) / self.windowSize

        #print(self.evaluationIndex, value, val,  self.prevSum, self.nextSum, diff, self.lastDifference, self.descFlag, sep= ' ')

        rise = diff - self.lastDifference

        if(rise > (self.threshold / 10)):
            self.descFlag = True
        else:
            if(self.descFlag):
                if(diff > self.threshold):
                    self.value.append(self.evaluationIndex - 1 - self.windowSize)
                self.descFlag = False
                

        self.lastDifference = diff
    


            




