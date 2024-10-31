from PriorityQueue import PriorityQueue
import time as TIME
from collections import deque
import psutil
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
    player_pos = []
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
                player_pos = [i, j]
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
                player_pos = [i, j]
    return player_pos, stones_pos, switches_pos, walls_pos

def heuristicCost(stones_pos, switches_pos):
    return 0

def typeOfAction(direction, player_pos, stones_pos, switches_pos, walls_pos):
    if tuple(player_pos) in walls_pos:
        return 1 # blocked

    # check if any stone is pushed
    for i in stones_pos:
        if tuple(player_pos) == (i[0], i[1]):
            pushed_stones = (i[0] + dx[direction], i[1] + dy[direction])
            # print(pushed_stones, walls_pos)
            # print(pushed_stones in walls_pos + stones_pos)
            if pushed_stones in walls_pos: return 1
            return 4 if pushed_stones not in ((j[0], j[1]) for j in stones_pos) else 1

    # no obstacle
    return 0

def checkAllSwitch(stones_pos, switches_pos):
    remain = [x for x in stones_pos if (x[0], x[1]) not in switches_pos]
    return len(remain) == 0

def bfs(file_name):
    """
    BFS algorithm
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
    matrix = [[]]

    # Read the map and initialize positions
    player_pos, stones_pos, switches_pos, walls_pos = readMap(matrix, file_name)

    # Use a standard queue for BFS instead of PriorityQueue
    frontier = deque()
    frontier.append((player_pos, steps, stones_pos,weight, actions))

    # Keep track of explored states
    explored_set = set()
    time = TIME.time()
    max_memory = memory

    while frontier:
        # Queue the first element (FIFO)
        player_pos, steps, stones_pos,weight , actions = frontier.popleft()

        if (tuple(player_pos), stones_pos) in explored_set:
            continue

       # position visited
        explored_set.add((tuple(player_pos), stones_pos))

        # Check if the goal (all switches activated) is reached
        if checkAllSwitch(stones_pos, switches_pos):
            time = TIME.time() - time
            max_memory = max(max_memory, process.memory_info().rss)
            memory = max_memory - memory
            break

        # Expanding the current node
        for i in range(4):
            x = dx[i] + player_pos[0]
            y = dy[i] + player_pos[1]

            t = typeOfAction(i, [x, y], stones_pos, switches_pos, walls_pos)
            if t == 1:  # Blocked action
                continue

            new_stones_pos = stones_pos
            new_weight = weight
            if t == 4:  # Stone is pushed
                pushed_stones_weight = [i for i in new_stones_pos if (i[0], i[1]) == (x, y)][0][-1]
                new_stones_pos = tuple(i for i in new_stones_pos if (i[0], i[1]) != (x, y))

                # add new stones position
                new_stones_pos += ((x + dx[i], y + dy[i], pushed_stones_weight),)

                # add weight
                new_weight += pushed_stones_weight

            # Sort the stones' positions for consistency in explored states
            new_stones_pos = tuple(sorted(new_stones_pos, key=lambda x: (x[0], x[1])))

            # Check if the new state has been explored
            if ((x, y), tuple(new_stones_pos)) in explored_set:
                continue

            node += 1  # Count the number of nodes created
            frontier.append(([x, y], steps + 1, new_stones_pos, new_weight, actions + actionsMap[i + t]))

    return actions, steps, weight, node, time, memory

if __name__ == '__main__':
    file_name = 'input-03.txt'
    actions, steps, weight, node, time, memory = bfs(file_name)
    print(actions)
    f = open(file_name.replace('in', 'out'), 'w')
    f.write('BFS\n')
    sep = '\n'
    f.write(f"Steps: {steps}{sep}Weight: {weight}{sep}Nodes: {node}{sep}Time (ms): {time * 1000:.2f}{sep}Memory (MB): {memory / 1e6:.2f}{sep}{actions}")