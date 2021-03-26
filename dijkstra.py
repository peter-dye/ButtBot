import math
import queue
import copy
import numpy as np
import heapq
import time

class PathPlanning():

    def __init__(self, num_rows, num_cols, obstacles):
        
        self.num_rows = num_rows
        self.num_cols = num_cols 
        self.obstacles = obstacles 
        self.start_heading = 'right' #bot always starts pointing to the right
        self.coordinate_list = [] #list of coordinates for search path
        self.direction_list = [] #list of up, down, left, right directions for search path
        self.path_home = [] #list of coordinates for return home path
        self.direction_list_home = [] #list of up, down, left, right directions for return home path
        self.instructions_home = [] #list of turns angles and distances for return home path

        self.search_space = np.empty([self.num_rows, self.num_cols])
        self.search_space_copy = np.empty([self.num_rows, self.num_cols])

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.search_space[i][j] = 255
                self.search_space_copy[i][j] = 255
      
        if self.obstacles is not None:
            self.add_obstacles()

        self.route = self.plan_path() #list of coordinates for search path including obstacle avoidance
        self.get_directions() #list of right, left, up, down in order
        
        self.instructions = [] #list of turn angles and travel distances for search path

    def get_instructions(self):
        count = 1
        self.direction_list.insert(0,self.start_heading)
        for i in range(len(self.direction_list)-1):
            curr_direction = self.direction_list[i]
            suiv_direction = self.direction_list[i+1]
            degrees = self.get_degrees(curr_direction, suiv_direction)
            self.instructions.append(degrees)
            self.instructions.append(count)
        return self.instructions

    def add_obstacles(self):
        for i in range(len(self.obstacles)):
            self.search_space[self.obstacles[i][0]][self.obstacles[i][1]] = 0
            self.search_space_copy[self.obstacles[i][0]][self.obstacles[i][1]] = 0

    class Vertex:
        def __init__(self, row, col):
            self.row = row
            self.col = col
            self.d=float('inf') #distance from source
            self.parent_x=None
            self.parent_y=None
            self.processed=False
            self.index_in_queue=None

    def bubble_up(self, queue, index):
        if index <= 0:
            return queue
        p_index=(index-1)//2
        if queue[index].d < queue[p_index].d:
                queue[index], queue[p_index]=queue[p_index], queue[index]
                queue[index].index_in_queue=index
                queue[p_index].index_in_queue=p_index
                queue = self.bubble_up(queue, p_index)
        return queue

    def bubble_down(self, queue, index):
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
                queue = self.bubble_down(queue, lc_index)
        else:
            small = lc_index
            if queue[lc_index].d > queue[rc_index].d:
                small = rc_index
            if queue[small].d < queue[index].d:
                queue[index],queue[small]=queue[small],queue[index]
                queue[index].index_in_queue=index
                queue[small].index_in_queue=small
                queue = self.bubble_down(queue, small)
        return queue

    def get_neighbors(self, r, c):
        shape=self.search_space.shape
        neighbors=[]
        #ensure neighbors are within image boundaries
        if r > 0 and not self.search_space[r-1][c].processed:
            neighbors.append(self.search_space[r-1][c])
        if r < shape[0] - 1 and not self.search_space[r+1][c].processed:
            neighbors.append(self.search_space[r+1][c])
        if c > 0 and not self.search_space[r][c-1].processed:
            neighbors.append(self.search_space[r][c-1])
        if c < shape[1] - 1 and not self.search_space[r][c+1].processed:
            neighbors.append(self.search_space[r][c+1])
        return neighbors

    def get_distance(self, u, v):
        return 0.1 + (float(self.search_space_copy[v])-float(self.search_space_copy[u]))**2

    def print_matrix(self) :
        for row in range(len(self.search_space)-1,-1,-1):
            print(("[{0}]".format(', '.join(map(str, self.search_space_copy[row])))))

    #dijkstra's
    def find_shortest_path(self, src, dst):
        pq = [] #min heap priority queue returns smallest value next
        self.num_rows, self.num_cols = self.search_space.shape[0], self.search_space.shape[1]
        source_row = src[0]
        source_col = src[1]
        dest_row = dst[0]
        dest_col = dst[1]
        self.search_space = np.full((self.num_rows, self.num_cols), None) #access by self.search_space[row][col]

        for r in range(self.num_rows):
            for c in range(self.num_cols):
                self.search_space[r][c] = self.Vertex(r,c)
                self.search_space[r][c].index_in_queue = len(pq)
                pq.append(self.search_space[r][c])

        self.search_space[source_row][source_col].d=0 #set distance to start node to 0
        pq=self.bubble_up(pq, self.search_space[source_row][source_col].index_in_queue)

        while len(pq) > 0:
            u=pq[0]
            u.processed=True
            pq[0]=pq[-1]
            pq[0].index_in_queue=0
            pq.pop()
            pq=self.bubble_down(pq,0)
            neighbors = self.get_neighbors(u.row,u.col)
            for v in neighbors:
                dist=self.get_distance((u.row,u.col),(v.row,v.col))
                if u.d + dist < v.d:
                    v.d = u.d+dist
                    v.parent_x=u.row
                    v.parent_y=u.col
                    idx=v.index_in_queue
                    pq=self.bubble_down(pq,idx)
                    pq=self.bubble_up(pq,idx)
        path=[]
        iter_v=self.search_space[dest_row][dest_col]
        while(iter_v.row!=source_row or iter_v.col!=source_col):
            path.append([iter_v.row,iter_v.col])
            iter_v=self.search_space[iter_v.parent_x][iter_v.parent_y]
    
        path.reverse()
        path.pop() #remove the last spot cause we get it from plan path function
        return path

    def open_spots(self):
        num_locations = 0
        for i in range (self.num_rows):
            for j in range (self.num_cols):
                if self.search_space_copy[i][j] == 255:
                    num_locations += 1
        return num_locations #return number of locations that must be visited

    def avoid_obstacle(self, curr_position, prev_position):
        source = copy.deepcopy(prev_position)
        while self.search_space_copy[curr_position[0]][curr_position[1]] != 255: #look for next open spot
            if curr_position[0]%2 == 0:
                if curr_position[1] != self.num_cols-1:
                    curr_position[1] += 1
                else:
                    curr_position[0] += 1
            else:
                if curr_position[1] != 0:
                    curr_position[1] -= 1
                else:
                    curr_position[0] += 1
        destination = copy.deepcopy(curr_position)
        path = self.find_shortest_path(source, destination) #use source, dest in dijkstra's
        return destination, path

    def plan_path(self):
        full_path = []
        curr_position = [0,0]
        visited_spots = 0
        num_locations = self.open_spots() #find num spots we need to visit till done
        while visited_spots != num_locations: #while not done
            if curr_position[0]%2 == 0: #if in even row move right
                if self.search_space_copy[curr_position[0]][curr_position[1]] == 255: #if spot available
                    full_path.append(copy.deepcopy(curr_position)) #add spot to path
                    visited_spots += 1
                    if curr_position[1] != self.num_cols-1: #if not at row end
                        prev_position = copy.deepcopy(curr_position) 
                        curr_position[1] += 1 #move right
                    else:
                        prev_position = copy.deepcopy(curr_position) #if at row end
                        curr_position[0] += 1 #move up row
                else:
                    #find start and end for dijkstra's
                    curr_position, path_around_obstacle = self.avoid_obstacle(copy.deepcopy(curr_position), copy.deepcopy(prev_position))
                    full_path.extend(copy.deepcopy(path_around_obstacle))
            else: #in odd row so move left
                if self.search_space_copy[curr_position[0]][curr_position[1]] == 255: #if spot available
                    full_path.append(copy.deepcopy(curr_position)) #add spot to path
                    visited_spots += 1
                    if curr_position[1] != 0: #if not at row end
                        prev_position = copy.deepcopy(curr_position)
                        curr_position[1] -= 1 #move left
                    else: #if at row end
                        prev_position = copy.deepcopy(curr_position)
                        curr_position[0] += 1 #move up row
                else:
                    #find start and end for dijkstra's
                    curr_position, path_around_obstacle = self.avoid_obstacle(copy.deepcopy(curr_position), copy.deepcopy(prev_position))
                    full_path.extend(copy.deepcopy(path_around_obstacle))
        self.coordinate_list.extend(full_path)
        return full_path

    def get_directions(self):
        for i in range(len(self.route)-1):
            curr = self.route[i]
            suiv = self.route[i+1]
            if(suiv[1]-curr[1] == 1):
                self.direction_list.append('right')
            elif(suiv[1]-curr[1] == -1):
                self.direction_list.append('left')
            elif(suiv[0]-curr[0] == 1):
                self.direction_list.append('up')
            else:
                self.direction_list.append('down')


    def get_degrees(self, curr_direction, suiv_direction):
        if curr_direction == 'right':
            if suiv_direction == 'right':
                return 0
            elif suiv_direction == 'up':
                return -90
            elif suiv_direction == 'left':
                return 180
            else:
                return 90
        elif curr_direction == 'left':
            if suiv_direction == 'right':
                return 180
            elif suiv_direction == 'up':
                return 90
            elif suiv_direction == 'left':
                return 0
            else:
                return -90
        if curr_direction == 'up':
            if suiv_direction == 'right':
                return 90
            elif suiv_direction == 'up':
                return 0
            elif suiv_direction == 'left':
                return -90
            else:
                return 180
        if curr_direction == 'down':
            if suiv_direction == 'right':
                return -90
            elif suiv_direction == 'up':
                return 180
            elif suiv_direction == 'left':
                return 90
            else:
                return 0

    def get_instructions_home(self):
        start = self.coordinate_list[-1]
        #start = [self.num_rows-1, self.num_cols-1]
        end = [0,0]
        self.path_home = self.find_shortest_path(start, end) #find shortest path from end location to (0,0)
        self.path_home.append(end)
        self.path_home.insert(0,start)
        for i in range(len(self.path_home)-1): #create list of up, down, left, right directions to get home
            curr = self.path_home[i]
            suiv = self.path_home[i+1]
            if(suiv[1]-curr[1] == 1):
                self.direction_list_home.append('right')
            elif(suiv[1]-curr[1] == -1):
                self.direction_list_home.append('left')
            elif(suiv[0]-curr[0] == 1):
                self.direction_list_home.append('up')
            else:
                self.direction_list_home.append('down')
        count = 1
        realign = self.get_degrees(self.direction_list[-1], self.direction_list_home[0]) #add first turn angle to instruction list
        self.instructions_home.append(realign)
        for i in range(len(self.direction_list_home)-1): #convert direction list into instructions with turn angles and distances
            curr_direction = self.direction_list_home[i]
            suiv_direction = self.direction_list_home[i+1]
            if curr_direction == suiv_direction:
                count += 1
            else:
                self.instructions_home.append(count)
                degrees = self.get_degrees(curr_direction, suiv_direction)
                self.instructions_home.append(degrees)
                count = 1
            if i == len(self.direction_list_home)-2:
                self.instructions_home.append(count)
        
        return self.instructions_home

obstacles = [(0,1),(3,2),(3,3),(3,4),(4,2),(4,4),(4,5)]
cmd = PathPlanning(7,7, obstacles)
print('Search instructions: ', cmd.get_instructions(), ', Number of instructions = ', len(cmd.instructions))
print('Search path coordinate list: ', cmd.coordinate_list)
instructions_home = cmd.get_instructions_home()
print('Instructions home: ', instructions_home)
print('Return home path coordinate list: ', cmd.path_home)

'''
visual_matrix = np.full((cmd.num_rows, cmd.num_cols), None)
for i in range(len(cmd.search_space_copy)):
    for j in range(len(cmd.search_space_copy)):
        if cmd.search_space_copy[i][j] == 255:
            visual_matrix[i][j] = 'O'
        else:
            visual_matrix[i][j] = 'X'

search_and_return = []
search_and_return.extend(cmd.coordinate_list)
search_and_return.extend(cmd.path_home)

for coord in search_and_return:
    #print('coord = ', coord)
    temp = copy.deepcopy(visual_matrix)
    temp[coord[0]][coord[1]] = 'B'
    for row in range(len(temp)-1,-1,-1):
        print(("[{0}]".format(', '.join(map(str, temp[row])))))
    print('\n')
    time.sleep(0.4)
print('Calculated search path is: ', cmd.coordinate_list)
print('Calculated return path is: ', cmd.path_home)
'''
