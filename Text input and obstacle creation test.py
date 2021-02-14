

def grouper(n, iterable):
    args = [iter(iterable)] * n 
    return zip(*args) 

def matrix_creation():
    #Each grid square size
    g_dim = int((max(SS_L, SS_W)) / (max(BB_L, BB_W)))

    #Once figured out the distance the buttbot can cover, add duration variables to use for Motor Driver function calls

    num_rows = math.floor(SS_L / g_dim)
    num_cols = math.floor(SS_W / g_dim)

    #Matrix creation
    SS = [['X' for i in range(num_rows)] for j in range(num_cols)]
    
    
text = input("Enter Rows and Columns of Obstacle Spaces (r,c): ")
print("Obstacles are at: ", text)
obstacles = tuple(text[x:x + 2]
    for x in range(0, len(text), 2))
print(obstacles)

