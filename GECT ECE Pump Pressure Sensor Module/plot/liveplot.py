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

figure = plt.figure()

rawLine = plt.plot(rawData.getSubList(windowSize), 'tab:red')
avgLine = plt.plot(movingAverage.getSubList(windowSize), 'tab:green')
cutLine = plt.plot(cutDown.getSubList(windowSize), 'tab:blue')

plt.legend(["raw", "moving Average", "blocked average"])


def update(value : float):
    
    global rawData
    global movingAverage
    global cutDown

    rawData.update(value)
    save.update(value)
    movingAverage.update(rawData.top())
    cutDown.update(movingAverage.top())

com = None

def draw(i):
    
    global com
    while com.waiting() != 0:
        str_ = com.readline()
        update(float(str_))

    global rawLine
    global avgLine
    global cutLine
    global figure    
    windowBound = rawData.getSubListRange(windowSize)
    windowRange = range(windowBound[0], windowBound[1])
    print(rawData.getLength(), movingAverage.getLength(), cutDown.getLength(), sep = ' ')
    rawLine[0].set_data(windowRange, rawData.getSubList(windowSize))
    avgLine[0].set_data(windowRange, movingAverage.getSubList(windowSize))
    cutLine[0].set_data(windowRange, cutDown.getSubList(windowSize))

    figure.gca().relim()
    figure.gca().autoscale_view()

        

def main():
    
    global com
    rate = 9600
    port = SerialCommunication.acquirePortsWith("CH340")

    com = SerialCommunication(port, rate, 1)
    
    anim = FuncAnimation(figure, draw, interval = 200)

    plt.show()

    file = "dataLogs/25msDataPot5to3"
    ext = ".log"

    while Path(file + ext).is_file():
        file += str(1)
    

    f = open(file + ext, "w")

    for item in rawData.value:
        f.write(str(item) + "\n")

    f.close()



if __name__ == "__main__":
    main()
    
