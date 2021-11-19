# Python to plot pressure data collected

import matplotlib.pyplot as plt

def read(file):

    f = open(file, "r")

    data = []

    for line in f:
        if(line != "\n"):
            data.append(float(line) * 3.3 / 1024)

    f.close()

    return data


def main():

    idleData = read("idleNotConnected.log")
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
    pOn.set_ylim(2.5, 3.4)

    plt.show()


if __name__ == "__main__":

    main()