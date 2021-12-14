

import matplotlib.pyplot as plt
import math


def main():

    value = ([], [])

    R = 47000
    C = 10 * (10**-6)

    fc = 1 / (2 * math.pi * R *C)
    print(fc)

    for i in range(1, 7000):
        x = float(i) / 1000.0
        value[0].append((x))
        value[1].append(fc / math.sqrt((fc*fc) + (x*x)))
    
    plt.plot(value[0], value[1])
    plt.show()

if __name__ == "__main__":
    main()