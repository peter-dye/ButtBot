# I'm thinking we make each grid square the size of the bots largest dimension
# Bot wanders until obstacle detected or butt detected, enters collision avoidance or butt pickup
import math
import motor_driver
import butt_relative_distance as rel_dist

#Two different speeds to run the motors at
HI_SPEED = 1
LO_SPEED = 0.25
curr_speed = HI_SPEED
#Buttbot dimensions
BB_L = 10 
BB_W = 10 

#User input search space dimensions
SS_L = 100 
SS_W = 100 

#Each grid square size
g_dim = int((max(SS_L, SS_W)) / (max(BB_L, BB_W)))

#Once figured out the distance the buttbot can cover, add duration variables to use for Motor Driver function calls

num_rows = math.floor(SS_L / g_dim)
num_cols = math.floor(SS_W / g_dim)

#Matrix creation
SS = [['X' for i in range(num_rows)] for j in range(num_cols)]

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
        if (curr_position[0] % 2 == 0):
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

def collision_avoidance():
    None

def butt_alignment():
    distance, angle, direction = rel_dist.calc_dist(butt_x, butt_y)
    mc.pivot_right_left(angle, direction)
    mc.fwd_bwd(1, distance, 'fwd')

if __name__ == "__main__":

    mc = motor_driver.MotorDriver()

    curr_position = [0,0]

    while curr_position != [(num_rows -1), (num_cols -1)]:

        wander(SS, motor_controller, curr_position)

    #return_home()
