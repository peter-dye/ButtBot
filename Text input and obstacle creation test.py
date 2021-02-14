import re
import math

def matrix_creation(SS_L, SS_W, BB_L, BB_W):
    #Each grid square size
    g_dim = int((max(SS_L, SS_W)) / (max(BB_L, BB_W)))

    #Once figured out the distance the buttbot can cover, add duration variables to use for Motor Driver function calls

    num_rows = math.floor(SS_L / g_dim)
    num_cols = math.floor(SS_W / g_dim)

    #Matrix creation
    SS = [['X' for i in range(num_rows)] for j in range(num_cols)]

    obstacles = []
    print('Grid is ', num_rows, ' tall by ', num_cols, ' wide.\n')
    line = input('Enter location of obstacles (r,c):\n') 

    temp = re.findall(r'\d+', line) 
    res = list(map(int, temp)) 

    i = 0
    while i < len(res):
        obstacles.append((res[i],res[i+1]))
        i += 2
    print(SS)
    for i in range(len(obstacles)):
        SS[obstacles[i][0]][obstacles[i][1]] = 'O'
        i += 1
    print(SS)

matrix_creation(100, 100, 10, 10)