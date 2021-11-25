# Python to plot pressure data collected

import matplotlib.pyplot as plt

def read(file, averaging = 1):

    f = open(file, "r", encoding = 'utf-8')

    data = []
    buffer = []

    for line in f:
        if(line != "\n"):
            buffer.append(float(line) * 3.3 / 1024)
            if(len(buffer) == averaging):
                sum = 0
                for item in buffer:
                    sum = sum + item
                buffer.clear()
                sum = float(sum) / float(averaging)
                data.append(sum)
            
    f.close()

    return data


def main():

    """ idleData = read("idleNotConnected.log")
    pumpoff = read("pump off.log")
    pumpOnInit = read("pump on init.log")

    fig, (idle, pOn, pOff) = plt.subplots(3)

    plt.subplots_adjust(left = 0.03, right = 0.97, bottom = 0.03, top = 0.97)

    idle.set_title("Idle")
    idle.plot(idleData, 'tab:red')

    pOff.set_title("Pump OFF")
    pOff.plot(pumpoff, 'tab:blue')
    pOn.set_ylim(2.5, 3.4)

    pOn.set_title("Pump ON")
    pOn.plot(pumpOnInit, 'tab:green')
    pOn.set_ylim(2.5, 3.4) """

    idleLargeData = read("idle2.log")
    print(len(idleLargeData))
    idleAvgData = read("idle2.log", 10)
    print(len(idleAvgData))

    onLargeData = read("pumpon2.log")
    print(len(onLargeData))
    onAvgData = read("pumpon2.log", 10)
    print(len(onAvgData))

    large, (lidle, lidleavg, lOnavg, lOn) = plt.subplots(4)

    plt.subplots_adjust(left = 0.03, right = 0.989, bottom = 0.03, top = 0.97, wspace = 0.202, hspace = 0.324)

    lidle.set_title("Idle 10 samples ps")
    lidle.plot(idleLargeData, 'tab:red')
    lidle.set_ylim(0.035, 0.040)
    lidle.set_xlim(0, len(idleLargeData))

    lidleavg.set_title("Idle average 10:1 samples ps")
    lidleavg.plot(idleAvgData, 'tab:green')
    lidleavg.set_ylim(0.035, 0.040)
    lidleavg.set_xlim(0, len(idleAvgData))

    lOn.set_title("Line Pressure 10 samples ps")
    lOn.plot(onLargeData, 'tab:blue')
    lOn.set_ylim(3.05, 3.15)
    lOn.set_xlim(0, len(onLargeData))

    lOnavg.set_title("Line Pressure 10:1 samples ps")
    lOnavg.plot(onAvgData, 'tab:purple')
    lOnavg.set_ylim(3.05, 3.15)
    lOnavg.set_xlim(0, len(onAvgData))


    plt.show()


if __name__ == "__main__":

    main()