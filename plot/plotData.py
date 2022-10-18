# Python to plot pressure data collected

# (C) Harith Manoj 2021

import matplotlib.pyplot as plt

def read(file):

    f = open(file, "r", encoding = 'utf-8')

    data = []

    for line in f:
        if(line != "\n"):
            data.append(float(line) * 3.3 / 1024)
            
            
    f.close()

    return data

def constrained(lower, value, diff):
    if(lower + diff > value):
        return lower
    else:
        return (value - diff)

def blockedAverage(data, averagingSize : float, shouldPreserve : bool):

    ret = []
    value = 0.0
    last = 0.0
    count = 0
    for i in data:
        if(count != (averagingSize)):
            value += i
            if shouldPreserve:
                ret.append(last)
            count += 1
        else:
            value /= averagingSize
            last = value
            ret.append(value)
            value = i
            count = 1
    return ret

def movingAverage(data, averagingSize : float):

    ret = []
    value = 0.0

    for i in range(0, len(data)):
        if(i >= averagingSize):
            value -= data[i - averagingSize]
        value += data[i]
        div = averagingSize
        if(i < averagingSize):
            div = i + 1
        ret.append(value / div)

    return ret



def main():

    data = read("dataLogs/filelive.log")
    mov = movingAverage(data, 10)
    block = blockedAverage(mov, 10, True)

    plt.plot(data)
    plt.plot(mov)
    plt.plot(block)

    plt.legend(["raw", "moving Average", "blocked average"])


    plt.show()
   

if __name__ == "__main__":

    main()