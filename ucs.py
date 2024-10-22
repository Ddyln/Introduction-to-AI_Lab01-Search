from PriorityQueue import PriorityQueue
import time as TIME
# import psutil

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
    stones_info = ()
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
                stones_info += ((i, j, stones_cost[cnt]), )
                cnt += 1
            elif matrix[i][j] == '@': # ares
                matrix[i][j] = 3
                player_pos = (i, j)
            elif matrix[i][j] == '.': # switches
                matrix[i][j] = 4
                switches_pos += ((i, j), )
            elif matrix[i][j] == '*': # stones + switches
                matrix[i][j] = 5
                stones_info += ((i, j, stones_cost[cnt]), )
                cnt += 1
                switches_pos += ((i, j), )
            elif matrix[i][j] == '+': # ares + switches
                matrix[i][j] = 6
                player_pos = (i, j)
    return player_pos, stones_info, switches_pos, walls_pos

def typeOfAction(direction, player_pos, stones_info, switches_pos, walls_pos):
    # blocked by wall
    if tuple(player_pos) in walls_pos:
        return 1 
    
    # check if any stone is pushed
    for i in stones_info:
        if tuple(player_pos) == (i[0], i[1]):
            pushed_stones = (i[0] + dx[direction], i[1] + dy[direction])
            if pushed_stones in walls_pos: return 1
            return 4 if pushed_stones not in ((j[0], j[1]) for j in stones_info) else 1
    
    # no obstacle
    return 0

def checkAllSwitch(stones_info, switches_pos):
    remain = [x for x in stones_info if (x[0], x[1]) not in switches_pos]
    return len(remain) == 0

matrix = [[]] 
player_pos, stones_info, switches_pos, walls_pos = readMap(matrix, 'input.txt')

actions, steps, stones_weight, node, time, memory = '', 0, 0, 0, 0, 0

frontier = PriorityQueue(typeOfHeap=False)  # Min heap for UCS

frontier.push((player_pos, stones_info, stones_weight, actions, 0), 0)

explored = set()

while not frontier.is_empty():
    topQueue = frontier.pop()
    player_pos = topQueue[0]
    stones_info = topQueue[1]
    stones_weight = topQueue[2]
    actions = topQueue[3]
    oldcost = topQueue[4]

    if (player_pos, stones_info) in explored:
        continue

    if checkAllSwitch(stones_info, switches_pos):
        break
    
    explored.add((player_pos, stones_info))

    for i in range(4):
        x = dx[i] + player_pos[0]
        y = dy[i] + player_pos[1]

        status = typeOfAction(i, (x, y), stones_info, switches_pos, walls_pos)
        
        if status == 1:
            continue
        
        pushed_stone_weight = 0
        new_stones_infor = stones_info
        move_cost = 1

        if status == 4:
            new_stones_infor = ()
            for stone in stones_info:
                if (stone[0], stone[1]) == (x, y):
                    # print(type(stone))
                    pushed_stone_weight = stone[2]
                else:
                    new_stones_infor += (stone, )
            move_cost += pushed_stone_weight

            # pushed_stone_infor = [i for i in stones_info if (i[0], i[1]) == (x, y)][0][-1]
            # not_pushed_stone_infor = tuple(i for i in stones_info if (i[0], i[1]) != (x, y))

            new_stones_infor += ((x + dx[i], y + dy[i], pushed_stone_weight), )
        
        if ((x, y), new_stones_infor) in explored:
            continue

        frontier.push(((x, y), 
                       new_stones_infor, 
                       stones_weight + pushed_stone_weight, 
                       actions + actionsMap[i + status],
                       oldcost + stones_weight + move_cost), 
                       oldcost + stones_weight + move_cost)

print(actions)