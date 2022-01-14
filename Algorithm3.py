import math
import random

points = []
NUMBER_OF_POINTS = 100
X_MIN_AREA = 0
Y_MIN_AREA = 0
X_MAX_AREA = 200
Y_MAX_AREA = 200
r = 10
for i in range(0,NUMBER_OF_POINTS):
    x = random.randint(X_MIN_AREA,X_MAX_AREA)
    y = random.randint(Y_MIN_AREA,Y_MAX_AREA)
    points.append([x,y])

points.sort()
#print(points)

circle = 0
disks = []
while(len(points) > 0):
    circle += 1
    #coveredPointsIndexes = []
    #coveredPointsIndexes.append(0)
    startCoord = [points[0][0],points[0][1]-r]

    checkThisPoints = []
    for i in range(1,len(points)):
        if(round(math.sqrt((points[0][0] - points[i][0])**2 + (points[0][1]-points[i][1])**2),3) <= 2*r):
            checkThisPoints.append(i)
    #print(checkThisPoints)
    maxPointCount = 0
    maxPointsCovered = []
    circlePointX = 0
    circlePointY = 0
    for i in range(0,181,5):
    
        newCoordinate = [((startCoord[0]-points[0][0])*math.cos(math.radians(i))) - ((startCoord[1]-points[0][1])*math.sin(math.radians(i))) ,
                        (((startCoord[0]-points[0][0])*math.sin(math.radians(i)))) + ((startCoord[1]-points[0][1])*math.cos(math.radians(i)) )
                        ]
        
        uzunluk = math.sqrt((0 - newCoordinate[0])**2 + (0 - newCoordinate[1])**2)
        newCoordinate[0] = round(newCoordinate[0],5)
        newCoordinate[1] = round(newCoordinate[1],5)
        #print(round(uzunluk,3))
        
        coveredPointsIndex = []
        count = 0
        for k in range(0,len(checkThisPoints)):
            
            if(round(math.sqrt((newCoordinate[0]- (points[checkThisPoints[k]][0]-points[0][0]))**2 + (newCoordinate[1]-(points[checkThisPoints[k]][1]-points[0][1]))**2),3) <= r):
                
                count += 1
                coveredPointsIndex.append(checkThisPoints[k])

        if(count > maxPointCount):
            maxPointsCovered = coveredPointsIndex.copy()
            maxPointCount = count
            circlePointX = newCoordinate[0]
            circlePointY = newCoordinate[1]

    ## append disk
    disks.append([circlePointX+points[0][0],circlePointY+points[0][1]])
    #print(newCoordinate)
    #uzunluk = round(uzunluk,3)
    ## kendi noktayıda ekleyelim
    maxPointCount += 1
    maxPointsCovered.append(0)
    #print(maxPointCount)
    newPoints = []
    for i in range(0,len(points)):
        if(not(i in maxPointsCovered)):
            newPoints.append(points[i])
    #print(points)
    points = newPoints.copy()
    

print("bitti")
print(disks)
print(circle)
#point = [2,2]
#r = 2

#startFrom = [0,point[1]-r-2]

#(x.cosa – y.sina, x.sina + y.cosa)
## Rotating 180 degree
#count = 0
#for i in range(0,181):
#    newCoordinate = [(startFrom[0]*math.cos(math.radians(i))) - (startFrom[1]*math.sin(math.radians(i))) +2,
#                    ((startFrom[0]*math.sin(math.radians(i)))) + (startFrom[1]*math.cos(math.radians(i)) +2)
#                    ]
    #print(newCoordinate)
#    uzunluk = math.sqrt((point[0] - newCoordinate[0])**2 + (point[1] - newCoordinate[1])**2)
#    uzunluk = round(uzunluk,3)
#    print(uzunluk)
#    if(uzunluk == 2):
#        count += 1                

#print(count)