import time as TIME
import psutil

dx = [0, 0, -1, 1]
dy = [1, -1, 0, 0]
moves = "rludRLUD"

# Get information in the file
def readMap(matrix, file_name):
    
    # Get information from file to matrix
    with open(file_name, 'r') as file_input:
        for line in file_input:
            # Get information from each line in file
            matrix.append(line)

    # Get weight of stones
    weights = matrix[0].split() 

    # Get width and height of map
    height = len(matrix)
    width = max([len(line) for line in matrix])

    # Get information in matrix
    player_pos = ()
    stones_pos = []
    switches_pos = []
    walls_pos = []

    # Count number of stone or switch
    count = 0
    
    for i in range(1, height):
        for j in range(len(matrix[i])-1):
            if matrix[i][j] == '$': #-> stone
                # Add position and cost of stone
                stones_pos.append((i, j, int(weights[count])))
                count += 1
            elif matrix[i][j] == '@': #-> player
                player_pos = (i, j)
            elif matrix[i][j] == '.': #-> switch
                switches_pos.append((i, j))
            elif matrix[i][j] == '#': #-> wall
                walls_pos.append((i, j))
            elif matrix[i][j] == '*': #-> switch and stone
                stones_pos.append((i, j, int(weights[count])))
                count += 1
                switches_pos.append((i, j))
            elif matrix[i][j] == '+': #-> player and switch
                switches_pos.append((i, j))
                player_pos = (i, j)

    return player_pos, stones_pos, switches_pos, walls_pos

# Check switch have filled by stone
def checkAllSwitch(stones_pos, switches_pos):
    remain = [x for x in stones_pos if (x[0], x[1]) not in switches_pos]
    return len(remain) == 0

# Action of player
def typeOfAction(direction, player_pos, stones_pos, walls_pos):
    """
        1: blocked 
        4: can push
        0: no obstacle
    """
    # blocked by wall
    if tuple(player_pos) in walls_pos:
        return 1 
    
    # check if any stone is pushed
    for i in stones_pos:
        # Player on stone location
        if tuple(player_pos) == (i[0], i[1]):
            # Change location of stone
            pushed_stones = (i[0] + dx[direction], i[1] + dy[direction])
            
            # If new location is wall
            if pushed_stones in walls_pos: 
                return 1
            
            # If new location is not stone
            if pushed_stones not in ((j[0], j[1]) for j in stones_pos):
                return 4 
            # If it is stone
            else:
                return 1
            
    # no obstacle
    return 0

def dfs(file_name):
    """
    actions: chuỗi các hành động, biểu diễn bằng các ký tự uldr: đi bình thường, ULDR: đẩy
    steps: số bước đi
    weight: tổng trọng số đã đẩy
    node: số node của cây mà thuật toán đã tạo ra
    time: thời gian chạy thuật toán (ms)
    memory: bộ nhớ mà thuật toán đã dùng (MB)
    """
    process = psutil.Process()
    actions, steps, weight, node, time, memory = '', 0, 0, 0, 0, 0
    memory = process.memory_info().rss
    # Code
    matrix = []
    
    # Get input from file
    player, stones, switches, walls = readMap(matrix, file_name)
    
    visited = list()
    
    frontier = list()
    frontier.append((player, stones, weight, actions))

    time = TIME.time()
    max_memory = memory

    while len(frontier) != 0:
        top = frontier.pop()
        player = top[0]
        stones = top[1]
        weight = top[2]
        actions = top[3]

        # Check goal reaching
        if checkAllSwitch(stones, switches):
            time = TIME.time() - time
            max_memory = max(max_memory, process.memory_info().rss)
            memory = max_memory - memory
            break


        if (player, stones) in visited:
            continue

        visited.append((player, stones))

        for i in range(4):
            x = player[0] + dx[i]
            y = player[1] + dy[i]
            t = typeOfAction(i, [x, y], stones, walls)

            # If blocked
            if t == 1:
                continue

            new_stones = stones
            new_weight = weight

            # If player can push stone
            if t == 4:
                
                pushed_stones_weight = int([stone for stone in new_stones if (stone[0], stone[1]) == (x, y)][0][-1])
                
                new_stones = list(stone for stone in new_stones if (stone[0], stone[1]) != (x, y))

                # add new location
                new_stones.append((x + dx[i], y + dy[i], pushed_stones_weight))
                new_weight += pushed_stones_weight
            new_stones = sorted(new_stones, key = lambda x:(x[0], x[1]))

            if ((x, y), new_stones) in visited:
                continue
            
            node += 1
            frontier.append(((x, y), new_stones, new_weight, actions + moves[i+t]))
        steps = len(actions)
    return actions, steps , weight, node, time, memory

if __name__ == '__main__':
    file_name = 'input-01.txt'
    actions, steps, weight, node, time, memory = dfs(file_name)
    f = open(file_name.replace('in', 'out'), 'w')
    f.write('DFS\n')
    sep = '\n'
    f.write(f"Steps: {steps}{sep}Weight: {weight}{sep}Nodes: {node}{sep}Time (ms): {time * 1000:.2f}{sep}Memory (MB): {memory / 1e6:.2f}{sep}{actions}")