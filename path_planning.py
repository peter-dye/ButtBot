# I'm thinking we make each grid square the size of the bots largest dimension
# Bot wanders until obstacle detected or butt detected, enters collision avoidance or butt pickup
import math
import re
import motor_driver
#import butt_relative_distance as rel_dist
#import servo_driver as sd
from constants import *

#User input search space dimensions
ss_l = 100 
ss_wd = 100 

def matrix_creation(ss_l, ss_wd, BB_L, BB_W):
    #Each grid square size
    g_dim = int((max(ss_l, ss_wd)) / (max(BB_L, BB_W)))

    #Once figured out the distance the buttbot can cover, add duration variables to use for Motor Driver function calls

    num_rows = math.floor(ss_l / g_dim)
    num_cols = math.floor(ss_wd / g_dim)

    #Matrix creation
    matrix = [['X' for i in range(num_rows)] for j in range(num_cols)]

    obstacles = []
    print('Grid is ', num_rows-1, ' tall by ', num_cols-1, ' wide.\n')
    line = input('Enter location of obstacles (r,c):\n') 

    temp = re.findall(r'\d+', line) 
    res = list(map(int, temp)) 

    i = 0
    while i < len(res):
        obstacles.append((res[i],res[i+1]))
        i += 2
    print(obstacles)

    for j in range(len(obstacles)):
        matrix[obstacles[j][0]][obstacles[j][1]] = 'E'
    print_matrix(matrix)
    return matrix, num_rows, num_cols

#Pretty print matrix
def print_matrix(matrix) :
	for row in range(len(matrix)-1,-1,-1):
		print(("[{0}]".format(', '.join(map(str, matrix[row])))))

#Traverse rows left to right
def scan_right(matrix, curr_position, mc):
    count = 0
    while count != num_cols:
        count += 1
        if SS[curr_position[0]][curr_position[1]] == 'X':
            mc.fwd_bwd(curr_speed, 1, 'fwd') #dur will be how long it takes to traverse 1 grid
            SS[curr_position[0]][curr_position[1]] = 'O'
            print_matrix(SS)
            print('\n')
        if SS[curr_position[0]][curr_position[1]] == 'E':
            collision_avoidance(curr_position)
        if curr_position[1] != num_cols - 1:
            curr_position[1] += 1

#Traverse rows right to left
def scan_left(matrix, curr_position, mc):
    count = 0
    while count != num_cols:
        count += 1
        if SS[curr_position[0]][curr_position[1]] == 'X':
            mc.fwd_bwd(curr_speed, 1, 'fwd') #dur will be how long it takes to traverse 1 grid
            SS[curr_position[0]][curr_position[1]] = 'O'
            print_matrix(SS)
            print('\n')
        if curr_position[1] != 0:
            curr_position[1] -= 1

#Move up by 1 after traversing a row
def wander(matrix, mc, curr_position):
    count = 0
    while (count != num_rows):
        if (curr_position[0] % 2 == 0): #move right every even row
            mc.pivot_right_left(1, 'right') #duration will need to be however long for 90deg
            mc.fwd_bwd(curr_speed, 1, 'fwd')
            mc.pivot_right_left(1, 'right') #duration will need to be however long for 90deg
            scan_right(matrix, curr_position, mc)
            curr_position[0] += 1
            count += 1
        else:
            mc.pivot_right_left(1, 'left')    #duration will need to be however long for 90deg
            mc.fwd_bwd(curr_speed, 1, 'fwd')
            mc.pivot_right_left(1, 'left')    #duration will need to be however long for 90deg
            scan_left(matrix, curr_position, mc)
            curr_position[0] += 1
            count += 1

#Want to go around known obstacles, under it, where we have already been
# Edge cases are if obstacle in first or last column, or top row
def collision_avoidance():
    # If obstacle in first column on approach, move up to next row. If first column still blocked turn right and traverse row
    # If first column not blocked, move camera to look at it for butt, then mark visited and traverse row to right
    if next_position[1] == 0:
        mc.pivot_right_left(1, 'right') #duration will need to be however long for 90deg
        mc.fwd_bwd(curr_speed, 1, 'fwd')
        current_position[0] += 1
        next_position[0] += 1
        if SS[next_position[0]][next_position[1]] == "E":
            mc.pivot_right_left(1, 'right')
            return
        else:
            #sd.camera_pan(IMG_WD, butt_x, 'left')
            pass
            
#def butt_alignment():
#    distance, angle, direction = rel_dist.calc_dist(butt_x, butt_y)
#    mc.pivot_right_left(angle, direction)
#    mc.fwd_bwd(1, distance, 'fwd')

if __name__ == "__main__":

    mc = motor_driver.MotorDriver()

    SS, num_rows, num_cols = matrix_creation(ss_l, ss_wd, BB_L, BB_W)

    curr_position = [0,0]

    while curr_position != [(num_rows -1), (num_cols -1)]:

        wander(SS, mc, curr_position)

    #return_home()
