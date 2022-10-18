
# (C) Harith Manoj 2021
import pathlib
import matplotlib.pyplot as plt

from DataForms import *

def read(file, graph, inputVal, aux):
    
    isHeader = False

    f = open(file, "r", encoding = 'utf-8')

    freq = 0
    head = []

    state = 0
    counter = 0

    for l in f:
        if(l != "\n"):
            print(l)
            if(state == 0):
                if l.startswith("t"):
                    freq = None
                else:
                    freq = float(l)
                state += 1
            elif (state == 1):
                head = l.split()
                state += 1

                for i in range(1, len(head)):
                    aux.append(RawData(1,1, ""))
                    aux[i - 1].name = head[i] + " : " + aux[i - 1].name
                    
            else:
                valList = l.split()
                value = float(valList[0])
                for (g, i) in zip(graph, inputVal):
                    if(i == -1):
                        g.update(value)
                    else:
                        g.update(graph[i].top())
                '''tapMarks.update(graphs[1].top())'''

                for iter in range(1, len(valList)):
                    value = float(valList[iter])
                    aux[iter - 1].update(value)
    return (freq, head[0])


graphs = [RawData(1,1, "rawInput")]
aux = [RawData(1, 1), RawData(1, 1), RawData(1, 1), RawData(1,4096), RawData(1,1*4096), RawData(1,1)]
auxName = ["firstOrder", "secondOrder", "thirdOrder", "fallPulse", "risePulse", "tapcount"]
print(read('dataLogs/sensortest1.log', graphs, [-1], aux))


for ax in aux:
    print(ax.getData())

print(graphs[0].getData())

plt.plot(graphs[0].getData())

for ax in aux:
    plt.plot(ax.getData())

plt.legend(["pressure"] + auxName)

plt.show()

