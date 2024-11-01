from PriorityQueue import PriorityQueue
import time    # Library to measure time
import psutil  # Library to monitor memory usage

# Define movements: up, right, down, left
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# Each action is mapped to a corresponding character
actionsMap = 'urdlURDL'     # With uppercase characters is moving to push the rock
                            # With normal write characters as normal moves

def readMap(matrix, file_name):
    """
    Reads the map from a file and parses the positions of the player, stones, switches, and walls.
    """
    inp = open(file_name).read().split('\n')         # Read the file and split it into lines
    stones_cost = list(map(int, inp[0].split()))     # Read stone costs from the first line
    inp = inp[1:]                                    # Remove the first line
    w = max([len(line) for line in inp])             # Find the maximum width
    h = len(inp)                                     # Height of the map
    matrix = [i for i in inp]                        # Create the matrix from lines
    matrix = [','.join(i).split(',') for i in matrix]   # Split each line into characters

    player_pos = ()     # Position of the player
    stones_info = ()    # Information about the stones
    switches_pos = ()   # Positions of the switches
    walls_pos = ()      # Positions of the walls
    cnt = 0             # Counter for the number of stones
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            # Classify characters in the matrix
            if matrix[i][j] == '#': # walls
                walls_pos += ((i, j), )
            elif matrix[i][j] == '$': # stones
                stones_info += ((i, j, stones_cost[cnt]), )
                cnt += 1
            elif matrix[i][j] == '@': # Player position
                player_pos = (i, j)
            elif matrix[i][j] == '.': # switches
                switches_pos += ((i, j), )
            elif matrix[i][j] == '*': # stones + switches
                stones_info += ((i, j, stones_cost[cnt]), )
                cnt += 1
                switches_pos += ((i, j), )
            elif matrix[i][j] == '+': # Player + Switch
                player_pos = (i, j)
                switches_pos += ((i, j), )
    return player_pos, stones_info, switches_pos, walls_pos

def typeOfAction(direction, player_pos, stones_info, switches_pos, walls_pos):
    """
    Checks if the movement action is valid.
    """
    # Check if the player position collides with a wall
    if tuple(player_pos) in walls_pos:
        return 1 
    
    # Check if any stone is being pushed
    for i in stones_info:
        if tuple(player_pos) == (i[0], i[1]):
            pushed_stones = (i[0] + dx[direction], i[1] + dy[direction])
            if pushed_stones in walls_pos: 
                return 1 # Cannot push stone into wall
            return 4 if pushed_stones not in ((j[0], j[1]) for j in stones_info) else 1
    
    # No obstacle
    return 0

def checkAllSwitch(stones_info, switches_pos):
    """
    Checks if all switches have been activated.
    """
    remain = [x for x in stones_info if (x[0], x[1]) not in switches_pos]
    return len(remain) == 0 # If no stones are not on switches, return True

def ucs(file_name = 'input.txt'):
    """
    actions: chuỗi các hành động, biểu diễn bằng các ký tự uldr: đi bình thường, ULDR: đẩy
    steps: số bước đi
    stones_weight: tổng trọng số đã đẩy
    node: số node của cây mà thuật toán đã tạo ra
    time_taken: thời gian chạy thuật toán (ms)
    memory_consumed: bộ nhớ mà thuật toán đã dùng (MB)
    """
    # Initialize to track memory information
    process = psutil.Process()

    actions, stones_weight, node = '', 0, 0

     # Initial memory usage
    initial_memory = process.memory_info().rss 
  
    matrix = [[]] 

    # Read the map from the file
    player_pos, stones_info, switches_pos, walls_pos = readMap(matrix,file_name)

    frontier = PriorityQueue(typeOfHeap=False)  # Min heap for UCS

    # Add the initial state to the priority queue
    frontier.push((player_pos, stones_info, stones_weight, actions, 0), 0)

    explored = set()    # Set of explored states

    # Start measuring time
    start_time = time.time()

    while not frontier.is_empty():
        topQueue = frontier.pop()    # Get the state with the lowest cost
        player_pos = topQueue[0]
        stones_info = topQueue[1]
        stones_weight = topQueue[2]
        actions = topQueue[3]
        oldcost = topQueue[4]

        # If the state has already been explored, skip it
        stones_info = tuple(sorted(stones_info, key = lambda x: (x[0], x[1])))
        if (player_pos, stones_info) in explored:
            continue
        
        # If all switches have been activated, stop the algorithm
        if checkAllSwitch(stones_info, switches_pos):
            break
        explored.add((player_pos, stones_info))  # Mark the state as explored

        # Check all possible actions
        for i in range(4):
            x = dx[i] + player_pos[0]
            y = dy[i] + player_pos[1]

            # Check the action
            status = typeOfAction(i, (x, y), stones_info, switches_pos, walls_pos)
            
            if status == 1: # If blocked, skip
                continue
            
            pushed_stone_weight = 0
            new_stones_infor = stones_info
            move_cost = 1   # Normal move cost

            # If a stone is pushed
            if status == 4:
                new_stones_infor = ()   # Initialize new stone information
                for stone in stones_info:
                    if (stone[0], stone[1]) == (x, y):
                        # print(type(stone))
                        pushed_stone_weight = stone[2]  # Record the weight of the pushed stone ((0, 1): position; 2: weight)
                    else:
                        new_stones_infor += (stone, )   # Add non-pushed stones
                move_cost = pushed_stone_weight        # Update move cost

                new_stones_infor += ((x + dx[i], y + dy[i], pushed_stone_weight), ) # Add new stone to information
            
            # If the state has already been explored, skip it
            new_stones_infor = tuple(sorted(new_stones_infor, key = lambda x: (x[0], x[1])))
            
            if ((x, y), new_stones_infor) in explored:
                continue

            node += 1   # Increment the node count

            # Add the new state to the priority queue
            frontier.push(((x, y), 
                        new_stones_infor, 
                        stones_weight + pushed_stone_weight, 
                        actions + actionsMap[i + status],
                        oldcost + move_cost), 
                        oldcost + move_cost)
            
    # Stop measuring time
    end_time = time.time()
    # Stop measuring memory
    final_memory = process.memory_info().rss  # Final memory usage

    # Calculate time and memory consumed
    time_taken = end_time - start_time
    memory_consumed = final_memory - initial_memory

    steps = len(actions)    # Calculate the number of steps

    return actions, steps, stones_weight, node, time_taken, memory_consumed

if __name__ == '__main__':
    file_name = 'input-03.txt'
    actions, steps, weight, node, time_taken, memory_consumed = ucs(file_name)
    f = open(file_name.replace('in', 'out'), 'w')
    f.write('UCS\n')
    sep = '\n'
    f.write(f"Steps: {steps}{sep}Weight: {weight}{sep}Nodes: {node}{sep}Time (ms): {time_taken * 1000:.2f}{sep}Memory (MB): {memory_consumed / 1e6:.2f}{sep}{actions}")