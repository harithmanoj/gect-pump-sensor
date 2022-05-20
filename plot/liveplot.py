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

rawData = RawData(1, 1)
movingAverage = MovingAverage(1, 1, averagingWindow, 
    lambda x: rawData.getValue(rawData.getLength() - (x + 1)), str(averagingWindow))
cutDown = BlockedAverage(1, 1, averagingWindow, "of mov 10")

auxCount = 6

aux = [RawData(1, 1), RawData(1, 1), RawData(1, 1), RawData(1,3*4096), RawData(1,3*4096), RawData(1,0.5*4096)]
auxName = ["firstOrder", "secondOrder", "thirdOrder", "fallPulse", "risePulse", "tapCount"]

figure = plt.figure()

rawLine = plt.plot(rawData.getSubList(windowSize), 'tab:red')
avgLine = plt.plot(movingAverage.getSubList(windowSize), 'tab:green')
cutLine = plt.plot(cutDown.getSubList(windowSize), 'tab:blue')

auxLine = []

for ax in aux:
    auxLine.append(plt.plot(ax.getSubList(windowSize)))

plt.legend(["raw", "moving Average", "blocked average"] + auxName)


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
    
    print(splitflt)

    updateFlt(splitflt[0],splitflt[1:])

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
    
    for (ln, ax) in zip(auxLine, aux):
        ln[0].set_data(windowRange, ax.getSubList(windowSize))


    figure.gca().relim()
    figure.gca().autoscale_view()

        

def main():
#     global cm

#     for i in range(0,1000):
#         cm.append(str(i) + " " + str(i+1) + " " + str(i+2))

#     cm.reverse()
    global com
    rate = 115200
    port = SerialCommunication.acquirePortsWith("CP210x")

    com = SerialCommunication(port, rate, 1)
    
    anim = FuncAnimation(figure, draw, interval = 200)

    plt.show()

    file = "dataLogs/multitest"
    ext = ".log"

    if Path(file + ext).is_file():
        count = 1
        while Path(file + str(count) + ext).is_file():
            count += 1
        file = file + str(count)


    f = open(file + ext, "w")
    f.write(str(20) + "\n")

    head = "Pressure "

    for hd in auxName:
        head += hd + ' '

    head += "\n"

    f.write(head)
    for i in range(save.getLength()):
        strVal = str(save.getValue(i))

        strVal += ' '

        for ax in aux:
            strVal += str(ax.getValue(i)) + ' '
        
        f.write(strVal + "\n")

    f.close()



if __name__ == "__main__":
    main()
    
