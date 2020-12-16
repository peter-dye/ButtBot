# I'm thinking we make each grid square the size of the bots largest dimension
# Bot just 
import math

BB_L = 10 #length of vehicle in cm
BB_W = 10 #width of vehicle in cm

SS_L = 100 #length of search space in cm
SS_W = 100 #width of search space in cm

g_dim = int((max(SS_L, SS_W)) / (max(BB_L, BB_W)))

num_rows = math.floor(SS_L / g_dim)
num_cols = math.floor(SS_W / g_dim)

SS = [['X' for i in range(num_rows)] for j in range(num_cols)]


def print_matrix(matrix) :
	for row in range(len(matrix)-1,-1,-1):
		print(("[{0}]".format(', '.join(map(str, matrix[row])))))

print_matrix(SS)