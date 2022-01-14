import random
import math
import time

points = []
hexagons = []
marked_hexagons = set()
NUMBER_OF_POINTS = 500
X_MIN_AREA = 0
Y_MIN_AREA = 0
X_MAX_AREA = 200
Y_MAX_AREA = 200
r = 10
for i in range(0,NUMBER_OF_POINTS):
    x = random.randint(X_MIN_AREA,X_MAX_AREA)
    y = random.randint(Y_MIN_AREA,Y_MAX_AREA)
    points.append([x,y])


def Regular_Tessellation(points,r,hexagons):
    hex_x_coord = r/2
    hex_y_coord = r/2*math.sqrt(3)
    
   
    hexagon_x_index = 0
    ## X cord
    while True:

        if(hexagon_x_index % 2 == 0):
            hex_y_coord = r/2*math.sqrt(3)
        else:
            hex_y_coord = 0

        hexagons.append([])
        ## Y cord
        while True:
            hexagons[hexagon_x_index].append((hex_x_coord,hex_y_coord))
            if(hex_y_coord >= Y_MAX_AREA):
                break
            hex_y_coord += r*math.sqrt(3)

        hexagon_x_index += 1
        if(hex_x_coord + r/2 > X_MAX_AREA):
            break
        hex_x_coord += 3*r/2

def Minimum_Geometric_Disk_Cover(points,r,hexagons):
    
    for i in points:
        x_rank = int(i[0]/(r*3/2))
        y_rank = 0
        if(x_rank % 2 == 0):
            y_rank = int(i[1]/(r*math.sqrt(3)))
        else:
            y_rank = int((i[1]+(math.sqrt(3)/2*r))/(r*math.sqrt(3)))
        
        #Find the hexagon containing 𝑝 by comparing the distances from 𝑝 to the centers of hexagons with indices
        #(𝑥 rank, 𝑦 rank), (𝑥 rank + 1, 𝑦 rank), and [(𝑥 rank + 1, 𝑦 rank + 1) if 𝑥 rank is even or (𝑥 rank + 1, 𝑦 rank − 1)
        #if 𝑥 rank is odd]. Ties are broken in favor of the marked hexagon, otherwise broken arbitrary
        Find_Hexagon(i,r,hexagons,x_rank,y_rank)

def Find_Hexagon(p,r,hexagons,x_rank,y_rank):
    global marked_hexagons
    p_x_coord = p[0]
    p_y_coord = p[1]

    #check (x rank, y rank)
    hex = hexagons[x_rank][y_rank]
    hex_x = hex[0]
    hex_y = hex[1]
    result = math.sqrt(((p_x_coord-hex_x)**2) + ((p_y_coord-hex_y)**2))
    if(result <= r):
        if hexagons[x_rank][y_rank] in marked_hexagons:
            return
        else:
            marked_hexagons.add(hexagons[x_rank][y_rank])
            return

    #check (𝑥 rank + 1, 𝑦 rank)
    hex = hexagons[x_rank+1][y_rank]
    hex_x = hex[0]
    hex_y = hex[1]
    result = math.sqrt(((p_x_coord-hex_x)**2) + ((p_y_coord-hex_y)**2))
    if(result <= r):
        if hexagons[x_rank+1][y_rank] in marked_hexagons:
            return
        else:
            marked_hexagons.add(hexagons[x_rank+1][y_rank])
            return

    if(x_rank % 2 == 0):
        #check (𝑥 rank + 1, 𝑦 rank + 1)
        hex = hexagons[x_rank+1][y_rank+1]
        hex_x = hex[0]
        hex_y = hex[1]
        result = math.sqrt(((p_x_coord-hex_x)**2) + ((p_y_coord-hex_y)**2))
        if(result <= r):
            if hexagons[x_rank+1][y_rank+1] in marked_hexagons:
                return
            else:
                marked_hexagons.add(hexagons[x_rank+1][y_rank+1])
                return
    else:
        #check (𝑥 rank + 1, 𝑦 rank − 1)
        hex = hexagons[x_rank+1][y_rank-1]
        hex_x = hex[0]
        hex_y = hex[1]
        result = math.sqrt(((p_x_coord-hex_x)**2) + ((p_y_coord-hex_y)**2))
        if(result <= r):
            if hexagons[x_rank+1][y_rank-1] in marked_hexagons:
                return
            else:
                marked_hexagons.add(hexagons[x_rank+1][y_rank-1])
                return

    print("!!!!!!!!!!!!!!!!!!!")

start_time = time.time()

Regular_Tessellation(points,r,hexagons)
Minimum_Geometric_Disk_Cover(points,r,hexagons)

end_time = (time.time() - start_time)

for i in marked_hexagons:
        print(i)
#print(len(marked_hexagons))
print('{0} points covered by using {1} disk'.format(NUMBER_OF_POINTS, len(marked_hexagons)))
print("--- %s seconds ---" % end_time)
#print(hexagons)
#print(hexagons[0][0])

