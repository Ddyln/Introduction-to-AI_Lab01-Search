from PriorityQueue import PriorityQueue
from a_star import a_star
from dfs import dfs
from ucs import ucs
import visualize as vsl
import sys
import os

def visualize():
    vsl.run()

def runAll():
    for i in range(1, 11):
        ch = ('0' if i < 10 else '') + str(i)
        file_name = 'input-' + ch + '.txt'
        if os.path.isfile(file_name):
            actions, steps, weight, node, time, memory = a_star(file_name)
            f = open(file_name.replace('in', 'out'), 'w')
            f.write('A*\n')
            sep = ', '
            f.write(f"Steps: {steps}{sep}Weight: {weight}{sep}Nodes: {node}{sep}Time (ms): {time * 1000:.2f}{sep}Memory (MB): {memory / 1e6:.2f}\n{actions}\n")

            actions, steps, weight, node, time, memory = ucs(file_name)
            f = open(file_name.replace('in', 'out'), 'a')
            f.write('UCS\n')
            sep = ', '
            f.write(f"Steps: {steps}{sep}Weight: {weight}{sep}Nodes: {node}{sep}Time (ms): {time * 1000:.2f}{sep}Memory (MB): {memory / 1e6:.2f}\n{actions}\n")

            # actions, steps, weight, node, time, memory = dfs(file_name)
            # f = open(file_name.replace('in', 'out'), 'a')
            # f.write('DFS\n')
            # sep = ', '
            # f.write(f"Steps: {steps}{sep}Weight: {weight}{sep}Nodes: {node}{sep}Time (ms): {time * 1000:.2f}{sep}Memory (MB): {memory / 1e6:.2f}\n{actions}\n")
                
if __name__ == '__main__':
    if len(sys.argv) > 1:
        assert len(sys.argv) == 2, "Invalid number of arguments"
        assert sys.argv[1] == '-v', "Invalid arguments"
        visualize()
    else:
        runAll()