from PriorityQueue import PriorityQueue
import sys

def visualize():
    print('visualize')

def runAll():
    print('run all case')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        assert len(sys.argv) == 2, "Invalid number of arguments"
        assert sys.argv[1] in ['-y', '-n', '-Y', '-N'], "Invalid arguments"
        visualize() if sys.argv[1] in ['-y', '-Y'] else runAllCase()
    else:
        runAll()