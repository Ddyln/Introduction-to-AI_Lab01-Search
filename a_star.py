from PriorityQueue import PriorityQueue
import time as TIME
import psutil
from itertools import permutations 

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
actionsMap = 'urdlURDL'

def readMap(matrix, file_name):
    inp = open(file_name).read().split('\n')
    w = list(map(int, inp[0].split()))
    stones_cost = list(map(int, inp[0].split()))
    inp = inp[1:]
    w = max([len(line) for line in inp])
    h = len(inp)
    matrix = [i for i in inp]
    matrix = [','.join(i).split(',') for i in matrix]
    player_pos = ()
    stones_pos = ()
    switches_pos = ()
    walls_pos = ()
    cnt = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == ' ': matrix[i][j] = 0 # space
            elif matrix[i][j] == '#': # walls
                matrix[i][j] = 1
                walls_pos += ((i, j), )
            elif matrix[i][j] == '$': # stones
                matrix[i][j] = 2
                stones_pos += ((i, j, stones_cost[cnt]), )
                cnt += 1
            elif matrix[i][j] == '@': # ares
                matrix[i][j] = 3
                player_pos = (i, j)
            elif matrix[i][j] == '.': # switches
                matrix[i][j] = 4
                switches_pos += ((i, j), )
            elif matrix[i][j] == '*': # stones + switches
                matrix[i][j] = 5
                stones_pos += ((i, j, stones_cost[cnt]), )
                cnt += 1
                switches_pos += ((i, j), )
            elif matrix[i][j] == '+': # ares + switches
                matrix[i][j] = 6
                player_pos = (i, j)
                switches_pos += ((i, j), )
    return player_pos, stones_pos, switches_pos, walls_pos

def heuristicCost(stones_pos, switches_pos):
    # return 0
    h = 1e18
    temp = permutations(switches_pos)
    for a in temp:
        temp_h = 0
        for i in range(len(a)):
            temp_h += (abs(stones_pos[i][0] - a[i][0]) + abs(stones_pos[i][1] - a[i][1])) * stones_pos[i][2]
        h = min(h, temp_h)
    return h

def typeOfAction(direction, player_pos, stones_pos, switches_pos, walls_pos):
    # blocked by wall
    if player_pos in walls_pos:
        return 1 
    
    # check if any stone is pushed
    for i in stones_pos:
        if player_pos == (i[0], i[1]):
            pushed_stones = (i[0] + dx[direction], i[1] + dy[direction])
            if pushed_stones in walls_pos: return 1
            return 4 if pushed_stones not in ((j[0], j[1]) for j in stones_pos) else 1
    
    # no obstacle
    return 0

def checkAllSwitch(stones_pos, switches_pos):
    remain = [x for x in stones_pos if (x[0], x[1]) not in switches_pos]
    return len(remain) == 0

def a_star(file_name = 'input-01.txt'):
    """
    actions: chuỗi các hành động, biểu diễn bằng các ký tự uldr: đi bình thường, ULDR: đẩy
    steps: số bước đi
    weight: tổng trọng số đã đẩy
    node: số node của cây mà thuật toán đã tạo ra
    time: thời gian chạy thuật toán (ms)
    memory: bộ nhớ mà thuật toán đã dùng (MB)
    """
    process = psutil.Process()
    actions, weight, node, time, memory = '', 0, 0, 0, 0
    memory = process.memory_info().rss
    # Code
    matrix = [[]]
    player_pos, stones_pos, switches_pos, walls_pos = readMap(matrix, file_name)
    frontier = PriorityQueue(0)
    frontier.push((player_pos, stones_pos, actions, weight, 0), 0)    
    explored_set = set()
    time = TIME.time()
    max_memory = memory
    steps = 0
    while frontier.is_empty() == False:
        topQueue = frontier.pop()
        player_pos = topQueue[0]
        stones_pos = topQueue[1]
        actions = topQueue[2]
        weight = topQueue[3]
        g = topQueue[4]
        if (player_pos, stones_pos) in explored_set:
            continue
        # print(actions, player_pos, stones_pos)
        
        explored_set.add((player_pos, stones_pos))

        # Check goal reaching
        if checkAllSwitch(stones_pos, switches_pos):
            time = TIME.time() - time
            max_memory = max(max_memory, process.memory_info().rss)
            memory = max_memory - memory
            steps = len(actions)
            break
        
        # Expanding
        for i in range(4):
            x = dx[i] + player_pos[0]
            y = dy[i] + player_pos[1]
            t = typeOfAction(i, (x, y), stones_pos, switches_pos, walls_pos)
            if t == 1:
                continue
            new_stones_pos = stones_pos
            new_weight = weight
            pushed_stones_weight = 0.01
            if t == 4:
                pushed_stones_weight = [i for i in new_stones_pos if (i[0], i[1]) == (x, y)][0][-1]
                new_stones_pos = tuple(i for i in new_stones_pos if (i[0], i[1]) != (x, y))
                new_stones_pos += ((x + dx[i], y + dy[i], pushed_stones_weight), )
                new_weight += pushed_stones_weight
            new_stones_pos = tuple(sorted(new_stones_pos, key = lambda x: (x[0], x[1])))
            if ((x, y), new_stones_pos) in explored_set:
                continue
            node += 1
            new_g = g + pushed_stones_weight
            frontier.push(((x, y), 
                            new_stones_pos, 
                            actions + actionsMap[i + t],
                            new_weight,
                            new_g), 
                            new_g + heuristicCost(new_stones_pos, switches_pos))
    return actions, steps, weight, node, time, memory

if __name__ == '__main__':
    file_name = 'input-05.txt'
    actions, steps, weight, node, time, memory = a_star(file_name)
    f = open(file_name.replace('in', 'out'), 'w')
    f.write('A*\n')
    sep = ', '
    f.write(f"Steps: {steps}{sep}Weight: {weight}{sep}Nodes: {node}{sep}Time (ms): {time * 1000:.2f}{sep}Memory (MB): {memory / 1e6:.2f}\n{actions}")
    f.close()