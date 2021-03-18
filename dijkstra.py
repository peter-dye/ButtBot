import math
import queue
import copy
import cv2
import matplotlib.pyplot as plt
import numpy as np
import heapq

num_cols = 10
num_rows = 10

picture = np.empty([num_rows, num_cols])
for i in range(num_rows):
    for j in range(num_cols):
        picture[i][j] = 255
#picture[0][1] = 0
picture[0][2] = 0
picture[1][0] = 0
#picture[1][1] = 0
#picture[1][2] = 0
picture[2][1] = 0
picture[2][0] = 0

print(picture)
class Vertex:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.d=float('inf') #distance from source
        self.parent_x=None
        self.parent_y=None
        self.processed=False
        self.index_in_queue=None

def bubble_up(queue, index):
    if index <= 0:
        return queue
    p_index=(index-1)//2
    if queue[index].d < queue[p_index].d:
            queue[index], queue[p_index]=queue[p_index], queue[index]
            queue[index].index_in_queue=index
            queue[p_index].index_in_queue=p_index
            queue = bubble_up(queue, p_index)
    return queue

def bubble_down(queue, index):
    length=len(queue)
    lc_index=2*index+1
    rc_index=lc_index+1
    if lc_index >= length:
        return queue
    if lc_index < length and rc_index >= length: #just left child
        if queue[index].d > queue[lc_index].d:
            queue[index], queue[lc_index]=queue[lc_index], queue[index]
            queue[index].index_in_queue=index
            queue[lc_index].index_in_queue=lc_index
            queue = bubble_down(queue, lc_index)
    else:
        small = lc_index
        if queue[lc_index].d > queue[rc_index].d:
            small = rc_index
        if queue[small].d < queue[index].d:
            queue[index],queue[small]=queue[small],queue[index]
            queue[index].index_in_queue=index
            queue[small].index_in_queue=small
            queue = bubble_down(queue, small)
    return queue

def get_neighbors(mat,r,c):
    shape=mat.shape
    neighbors=[]
    #ensure neighbors are within image boundaries
    if r > 0 and not mat[r-1][c].processed:
        neighbors.append(mat[r-1][c])
    if r < shape[0] - 1 and not mat[r+1][c].processed:
        neighbors.append(mat[r+1][c])
    if c > 0 and not mat[r][c-1].processed:
        neighbors.append(mat[r][c-1])
    if c < shape[1] - 1 and not mat[r][c+1].processed:
        neighbors.append(mat[r][c+1])
    return neighbors

def get_distance(img,u,v):
    return 0.1 + (float(img[v])-float(img[u]))**2

def print_matrix(matrix) :
	for row in range(len(matrix)-1,-1,-1):
		print(("[{0}]".format(', '.join(map(str, matrix[row])))))

#dijkstra's
def find_shortest_path(matrix, src, dst):
    pq = [] #min heap priority queue returns smallest value next
    num_rows, num_cols = matrix.shape[0], matrix.shape[1]
    source_row = src[0]
    source_col = src[1]
    print('trying to get from: ', source_row, source_col)
    dest_row = dst[0]
    dest_col = dst[1]
    print('to: ', dest_row, dest_col)
    matrix = np.full((num_rows, num_cols), None) #access by matrix[row][col]

    for r in range(num_rows):
        for c in range(num_cols):
            matrix[r][c] = Vertex(r,c)
            matrix[r][c].index_in_queue = len(pq)
            pq.append(matrix[r][c])

    matrix[source_row][source_col].d=0 #set distance to start node to 0
    pq=bubble_up(pq, matrix[source_row][source_col].index_in_queue)

    while len(pq) > 0:
        u=pq[0]
        u.processed=True
        pq[0]=pq[-1]
        pq[0].index_in_queue=0
        pq.pop()
        pq=bubble_down(pq,0)
        neighbors = get_neighbors(matrix,u.row,u.col)
        for v in neighbors:
            dist=get_distance(picture,(u.row,u.col),(v.row,v.col))
            if u.d + dist < v.d:
                v.d = u.d+dist
                v.parent_x=u.row
                v.parent_y=u.col
                idx=v.index_in_queue
                pq=bubble_down(pq,idx)
                pq=bubble_up(pq,idx)
    path=[]
    iter_v=matrix[dest_row][dest_col]
    while(iter_v.row!=source_row or iter_v.col!=source_col):
        path.append([iter_v.row,iter_v.col])
        iter_v=matrix[iter_v.parent_x][iter_v.parent_y]
    
    #path.append([source_row,source_col])
    path.reverse()
    path.pop() #remove the last spot cause we get it from plan path function
    return path

def open_spots(matrix):
    num_locations = 0
    global num_cols
    global num_rows
    for i in range (num_rows):
        for j in range (num_cols):
            if matrix[i][j] == 255:
                num_locations += 1
    return num_locations #return number of locations that must be visited

def avoid_obstacle(matrix, curr_position, prev_position):
    print('avoiding obstacle')
    source = copy.deepcopy(prev_position)
    print('source = ', source)
    while matrix[curr_position[0]][curr_position[1]] != 255: #look for next open spot
        if curr_position[0]%2 == 0:
            if curr_position[1] != num_cols-1:
                curr_position[1] += 1
            else:
                curr_position[0] += 1
        else:
            if curr_position[1] != 0:
                curr_position[1] -= 1
            else:
                curr_position[0] += 1
    destination = copy.deepcopy(curr_position)
    path = find_shortest_path(matrix, source, destination) #use source, dest in dijkstra's
    return destination, path

def plan_path(matrix):
    global num_cols
    full_path = []
    curr_position = [0,0]
    visited_spots = 0
    num_locations = open_spots(matrix) #find num spots we need to visit till done
    print('num locations = ', num_locations)
    while visited_spots != num_locations: #while not done
        if curr_position[0]%2 == 0: #if in even row move right
            print('in even row: ', curr_position[0])
            if matrix[curr_position[0]][curr_position[1]] == 255: #if spot available
                print('adding ', curr_position, 'to path ', full_path)
                full_path.append(copy.deepcopy(curr_position)) #add spot to path
                print('path so far is: ', full_path)
                visited_spots += 1
                print('visited spots = ', visited_spots)
                if curr_position[1] != num_cols-1: #if not at row end
                    prev_position = copy.deepcopy(curr_position) 
                    curr_position[1] += 1 #move right
                    print('move right to current position = ', curr_position)
                else:
                    prev_position = copy.deepcopy(curr_position) #if at row end
                    curr_position[0] += 1 #move up row
                    print('move up row to current position = ', curr_position)
            else:
                #find start and end for dijkstra's
                curr_position, path_around_obstacle = avoid_obstacle(matrix, copy.deepcopy(curr_position), copy.deepcopy(prev_position))
                full_path.extend(copy.deepcopy(path_around_obstacle))
        else: #in odd row so move left
            print('in odd row: ', curr_position[0])
            if matrix[curr_position[0]][curr_position[1]] == 255: #if spot available
                full_path.append(copy.deepcopy(curr_position)) #add spot to path
                print('path so far is: ', full_path)
                visited_spots += 1
                print('visited spots = ', visited_spots)
                if curr_position[1] != 0: #if not at row end
                    prev_position = copy.deepcopy(curr_position)
                    curr_position[1] -= 1 #move left
                    print('move left to current position = ', curr_position)
                else: #if at row end
                    prev_position = copy.deepcopy(curr_position)
                    curr_position[0] += 1 #move up row
                    print('move up row current position = ', curr_position)
            else:
                #find start and end for dijkstra's
                curr_position, path_around_obstacle = avoid_obstacle(matrix, copy.deepcopy(curr_position), copy.deepcopy(prev_position))
                full_path.extend(copy.deepcopy(path_around_obstacle))
    return full_path

def get_directions(route):
    direction_list = []
    for i in range(len(route)-1):
        curr = route[i]
        suiv = route[i+1]
        if(suiv[1]-curr[1] == 1):
            direction_list.append('right')
        elif(suiv[1]-curr[1] == -1):
            direction_list.append('left')
        elif(suiv[0]-curr[0] == 1):
            direction_list.append('up')
        else:
            direction_list.append('down')
    return direction_list

route = plan_path(picture)
print(route)

direction_list = get_directions(route)

def get_degrees(curr_direction, suiv_direction):
    if curr_direction == 'right':
        if suiv_direction == 'right':
            return 0
        elif suiv_direction == 'up':
            return 90
        elif suiv_direction == 'left':
            return 180
        else:
            return -90
    elif curr_direction == 'left':
        if suiv_direction == 'right':
            return 180
        elif suiv_direction == 'up':
            return -90
        elif suiv_direction == 'left':
            return 0
        else:
            return 90
    if curr_direction == 'up':
        if suiv_direction == 'right':
            return -90
        elif suiv_direction == 'up':
            return 0
        elif suiv_direction == 'left':
            return 90
        else:
            return 180
    if curr_direction == 'down':
        if suiv_direction == 'right':
            return 90
        elif suiv_direction == 'up':
            return 180
        elif suiv_direction == 'left':
            return -90
        else:
            return 0

instructions = []
count = 1
for i in range(len(direction_list)-1):
    curr_direction = direction_list[i]
    suiv_direction = direction_list[i+1]
    if curr_direction == suiv_direction:
        count += 1
    else:
        instructions.append(count)
        degrees = get_degrees(curr_direction, suiv_direction)
        instructions.append(degrees)
        print('direction = ', curr_direction, 'distance = ', count)
        count = 1
    if i == len(direction_list)-2:
        instructions.append(count)
        print('direction = ', suiv_direction, 'distance = ', count)
print(instructions)

