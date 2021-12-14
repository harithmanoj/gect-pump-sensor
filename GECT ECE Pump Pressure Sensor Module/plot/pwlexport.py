# PWL Export

# (C) Harith Manoj 2021

def read(file):

    f = open(file, "r", encoding = 'utf-8')

    data = []

    for line in f:
        if(line != "\n"):
            data.append(float(line) * 3.3 / 1024)
            
            
    f.close()

    return data

def main():

    file = input("File name :")

    sampling = float(input("Sampling freq :"))

    data = read(file)

    f = open(file + ".pwl", 'w', encoding = 'utf-8')

    for i in range(len(data)):
        f.write(str(float(i) / sampling) + "," + str(data[i]) + "\n")

    f.write('\n')


if __name__ == "__main__":
    main()



    