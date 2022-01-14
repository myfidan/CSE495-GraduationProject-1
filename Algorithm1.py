import random
import math
import time

points = []
hexagons = []
marked_hexagons = []
NUMBER_OF_POINTS = 500
X_MIN_AREA = 0
Y_MIN_AREA = 0
X_MAX_AREA = 200
Y_MAX_AREA = 200
r = 10
y_hex_count = 0
x_hex_count = 0
for i in range(0,NUMBER_OF_POINTS):
    x = random.randint(X_MIN_AREA,X_MAX_AREA)
    y = random.randint(Y_MIN_AREA,Y_MAX_AREA)
    points.append([x,y,-1,-1])


def Regular_Tessellation(points,r,hexagons):
    hex_x_coord = r/2
    hex_y_coord = r/2*math.sqrt(3)
    
   
    hexagon_x_index = 0
    ## X cord
    count_x = 0
    while True:

        if(hexagon_x_index % 2 == 0):
            hex_y_coord = r/2*math.sqrt(3)
        else:
            hex_y_coord = 0

        hexagons.append([])
        ## Y cord
        count_y = 0
        while True:
            hexagons[hexagon_x_index].append([hex_x_coord,hex_y_coord])
            count_y += 1
            if(hex_y_coord >= Y_MAX_AREA):
                if(count_y % 2 != 0):
                    hex_y_coord += r*math.sqrt(3)
                    hexagons[hexagon_x_index].append([hex_x_coord,hex_y_coord])
                break
            hex_y_coord += r*math.sqrt(3)

        hexagon_x_index += 1
        count_x += 1
        if(hex_x_coord + r/2 > X_MAX_AREA):
            if(count_x % 2 == 0):
                break
        hex_x_coord += 3*r/2


def Find_hexagons_foreach_point(points,r,hexagons):
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
        p[2] = x_rank
        p[3] = y_rank
        return

    #check (𝑥 rank + 1, 𝑦 rank)
    hex = hexagons[x_rank+1][y_rank]
    hex_x = hex[0]
    hex_y = hex[1]
    result = math.sqrt(((p_x_coord-hex_x)**2) + ((p_y_coord-hex_y)**2))
    if(result <= r):
        p[2] = x_rank+1
        p[3] = y_rank
        return

    if(x_rank % 2 == 0):
        #check (𝑥 rank + 1, 𝑦 rank + 1)
        hex = hexagons[x_rank+1][y_rank+1]
        hex_x = hex[0]
        hex_y = hex[1]
        result = math.sqrt(((p_x_coord-hex_x)**2) + ((p_y_coord-hex_y)**2))
        if(result <= r):
            p[2] = x_rank+1
            p[3] = y_rank+1
            return
           
    else:
        #check (𝑥 rank + 1, 𝑦 rank − 1)
        hex = hexagons[x_rank+1][y_rank-1]
        hex_x = hex[0]
        hex_y = hex[1]
        result = math.sqrt(((p_x_coord-hex_x)**2) + ((p_y_coord-hex_y)**2))
        if(result <= r):
            p[2] = x_rank+1
            p[3] = y_rank-1
            return
           

    print("!!!!!!!!!!!!!!!!!!!")



def Minimum_Geometric_Disk_Cover(points,r,hexagons):
    global y_hex_count
    global x_hex_count
    global marked_hexagons

    x = 0
    y = 0
    while(x < x_hex_count):
        y = 0
        while( y < y_hex_count):
            ## Take combination of all 4 hexagons
            comb_list = [[x,y],[x,y+1],[x+1,y],[x+1,y+1]]

            ret = [[]]
            for n in comb_list:
                ret += [r + [n] for r in ret]
            
            ret[3], ret[4] = ret[4],ret[3]
            ret[4], ret[8] = ret[8],ret[4]
            ret[7],ret[12] = ret[12],ret[7]
            point_list = []
            find_points_onThose_hex(point_list,x,y,points)

            ## find hexagons for each 
            for i in ret:
                temp_list = []
                chosen_hex = []
                for j in i:
                    hex = hexagons[j[0]][j[1]]
                    check_hex = False
                    for k in point_list:
                        if (not([k[0],k[1]] in temp_list) and math.sqrt(((hex[0]-k[0])**2) + ((hex[1]-k[1])**2)) <= r):
                            temp_list.append([k[0],k[1]])
                            check_hex = True
                    if(check_hex):
                         chosen_hex.append(hex)
                if(len(temp_list) == len(point_list)):
                    marked_hexagons.append(chosen_hex)
                    break



            #print("*******************")
            #print(point_list)
            #print(ret)
            #print("-------------------")

            y += 2
        x += 2
        y = 0
    ## 0,0 0,1
    ## 1,0 1,1

    ## 0,2 0,3
    ## 1,2 1,3

    ## to up => y = y+2
    ## to right => x = x+2 and make y = 0

def find_points_onThose_hex(point_list,x,y,points):
    for i in points:
        # take the coord of point
        point_coord = [i[2],i[3]]
        if(point_coord == [x,y] or point_coord == [x+1,y] or point_coord == [x,y+1] or point_coord == [x+1,y+1]):
            point_list.append(i)


start_time = time.time()

Regular_Tessellation(points,r,hexagons)
Find_hexagons_foreach_point(points,r,hexagons)

## Print y hex and x hex count
y_hex_count = len(hexagons[0])
x_hex_count = len(hexagons)
#print(y_hex_count)
#print(x_hex_count)
# y = 13, x = 14
Minimum_Geometric_Disk_Cover(points,r,hexagons)
#14
#13
#for i in points:
#    print(i)

end_time = (time.time() - start_time)

count = 0
for i in marked_hexagons:
    for j in i:
        print(j)
        count += 1

print('{0} points covered by using {1} disk'.format(NUMBER_OF_POINTS, count))
#print(% " points covered" % count)

print("Run time: --- %s seconds ---" % end_time)