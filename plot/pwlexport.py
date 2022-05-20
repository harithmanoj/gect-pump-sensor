# PWL Export

# (C) Harith Manoj 2021

def read(file, conv):

    f = open(file, "r", encoding = 'utf-8')

    data = []

    for line in f:
        if(line != "\n"):
            data.append(line)
    fltdata = []

    for i in range(2, len(data)):
        fltdata.append(float(data[i]) * conv    )
    f.close()

    return fltdata

def main():

    file = input("File name: ")

    sampling = float(input("Sampling freq: "))

    conv = float(input("Conversion Factor: "))

    data = read(file, conv)

    f = open(file + ".pwl", 'w', encoding = 'utf-8')

    for i in range(len(data)):
        f.write(str(float(i) / sampling) + "," + str(data[i]) + "\n")

    f.write('\n')


if __name__ == "__main__":
    main()



    