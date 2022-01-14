import random

f = open("pointFile.txt", "a")
plane = 800
f.write(str(plane))
f.write("\n")
numberOfPoints = 100

for i in range(0,100):
    x = random.randint(0,800)
    y = random.randint(0,800)
    f.write(str(x))
    f.write(",")
    f.write(str(y))
    f.write("\n")
f.close()