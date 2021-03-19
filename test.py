search_space = [[0,0,0],[0,0,0],[0,0,0]]

for i in range(3):
    for j in range(3):
        search_space[i][j] = 255

print(search_space)
test = [(0,1), (2,2)]
print(len(test))
for i in range(len(test)):
    search_space[test[i][0]][test[i][1]] = 0

print(search_space)