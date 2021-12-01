# live plot pressure data

from typing import List
from serialCommunication import SerialCommunication

import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

import numpy
    
def display(data, ymin, ymax, title, color):

    ySpan = ymax - ymin

    ymin = ymin - ySpan * 0.1
    ymax = ymax + ySpan * 0.1

    plt.suptitle(title)
    axis = plt.plot(data, color)

    return axis

rawData = []
rawMin = 0
rawMax = 0
movingAverage = []
movMin = 0
movMax = 0
cutDown = []
cutMin = 0
cutMax = 0

figure = plt.figure()

rawLine = plt.plot(rawData, 'tab:red')
avgLine = plt.plot(movingAverage, 'tab:green')
cutLine = plt.plot(cutDown, 'tab:blue')

plt.legend(["raw", "moving Average", "blocked average"])

averagingWindow = 10.0


def update(value : float):
    
    global rawData
    global rawMin
    global rawMax
    global movingAverage
    global movMin
    global movMax
    global cutDown
    global cutMin
    global cutMax

    if(value > rawMax):
        rawMax = value
    elif(value < rawMin):
        rawMin = value
    
    #value = float(value) * 3.3 / 1024.0
    rawData.append(value)
    i = len(rawData) - 1

    mov = 0.0
    cut = 0.0

    while(i > 0) and (i > (len(rawData) - 1 - averagingWindow)):
        print(str(mov) + " " + str(rawData[i]))
        mov = mov + rawData[i]
        i -= 1

    if( len(rawData) < averagingWindow):
        mov /= len(rawData)
    else:
        mov /= averagingWindow
    print(mov)
    if(mov > movMax):
        movMax = mov
    elif (mov < movMin):
        movMin = mov

    movingAverage.append(mov)

    if( (len(rawData) % averagingWindow) == 0):
        i = len(movingAverage) - 1
        while(i > 0) and (i > len(movingAverage) - 1 - averagingWindow):
            cut += movingAverage[i]
            i -= 1

        cut /= averagingWindow

        if(cut > cutMax):
            cutMax = cut
        elif(cut < cutMin):
            cutMin = cut

        cutDown.append(cut)
    else:
        if(len(cutDown) != 0):
            cutDown.append(cutDown[len(cutDown) - 1])
        else:
            cutDown.append(0)

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

    x = range(len(rawData))
    print(x)
    rawLine[0].set_data(x, rawData)
    avgLine[0].set_data(x, movingAverage)
    cutLine[0].set_data(x, cutDown)

    figure.gca().relim()
    figure.gca().autoscale_view()

        

def main():
    
    global com
    rate = 9600
    port = SerialCommunication.acquirePortsWith("CH340")

    com = SerialCommunication(port, rate, 1)

    anim = FuncAnimation(figure, draw, interval = 200)

    plt.show()

    f = open("file.log", "w")

    for item in rawData:
        f.write(str(item) + "\n")

    f.close()



if __name__ == "__main__":
    main()
    


