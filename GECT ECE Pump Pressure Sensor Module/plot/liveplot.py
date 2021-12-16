# live plot pressure data

from pathlib import Path
from typing import List
from serialCommunication import SerialCommunication

import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

import math

from DataForms import *


def display(data, ymin, ymax, title, color):

    ySpan = ymax - ymin

    ymin = ymin - ySpan * 0.1
    ymax = ymax + ySpan * 0.1

    plt.suptitle(title)
    axis = plt.plot(data, color)

    return axis

averagingWindow: int = 10
windowSize: int = 300

save = RawData(1,1)

rawData = RawData(1024, 3.3)
movingAverage = MovingAverage(1, 1, averagingWindow, 
    lambda x: rawData.getValue(rawData.getLength() - (x + 1)), str(averagingWindow))
cutDown = BlockedAverage(1, 1, averagingWindow, "of mov 10")

auxCount = 2

aux = [RawData(1,3), RawData(1,3)]

figure = plt.figure()

rawLine = plt.plot(rawData.getSubList(windowSize), 'tab:red')
avgLine = plt.plot(movingAverage.getSubList(windowSize), 'tab:green')
cutLine = plt.plot(cutDown.getSubList(windowSize), 'tab:blue')

plt.legend(["raw", "moving Average", "blocked average"])


def updateFlt(value: float, auxVal: list[float]):
    
    global rawData
    global movingAverage
    global cutDown
    global aux

    rawData.update(value)
    movingAverage.update(rawData.top())
    save.update(value)
    cutDown.update(movingAverage.top())
    for (val, a) in zip(auxVal, aux):
        a.update(val)

def update(strVal: str):
    splitVal = strVal.split()
    splitflt = []

    for sp in splitVal:
        splitflt.append(float(sp))

    updateFlt(splitflt[0], splitflt[1:])

com = None
#cm: list[str] = []

def draw(i):
    
    global com
    while com.waiting() != 0:
        str_ = com.readline()
        update(str_)
    #for i in range(0,10):
    #    update(strVal = cm.pop())

    global rawLine
    global avgLine
    global cutLine
    global figure    
    windowBound = rawData.getSubListRange(windowSize)
    windowRange = range(windowBound[0], windowBound[1])
    rawLine[0].set_data(windowRange, rawData.getSubList(windowSize))
    avgLine[0].set_data(windowRange, movingAverage.getSubList(windowSize))
    cutLine[0].set_data(windowRange, cutDown.getSubList(windowSize))

    figure.gca().relim()
    figure.gca().autoscale_view()

        

def main():
#     global cm

#     for i in range(0,1000):
#         cm.append(str(i) + " " + str(i+1) + " " + str(i+2))

#     cm.reverse()
    global com
    rate = 9600
    port = SerialCommunication.acquirePortsWith("CH340")

    com = SerialCommunication(port, rate, 1)
    
    anim = FuncAnimation(figure, draw, interval = 200)

    plt.show()

    file = "dataLogs/sample"
    ext = ".log"

    count = 1
    while Path(file + str(count) + ext).is_file():
        count += 1
    

    f = open(file + str(count) + ext, "w")
    f.write(str(40) + "\n")
    f.write("Pressure_2nd fallingPulse risingPulse\n")
    for i in range(save.getLength()):
        strVal = str(save.getValue(i))
        for a in aux:
            strVal = strVal + " " + str(a.getValue(i))
        f.write(strVal + "\n")

    f.close()



if __name__ == "__main__":
    main()
    
