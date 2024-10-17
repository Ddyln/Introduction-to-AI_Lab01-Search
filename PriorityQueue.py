import heapq

class PriorityQueue:
    def __init__(self, typeOfHeap: bool = True):
        """type = true -> max heap
        """
        self.heap = []
        self.type = typeOfHeap

    def push(self, item, priority):
        heapq.heappush(self.heap, (-priority if self.type == True else priority, item))

    def pop(self):
        return heapq.heappop(self.heap)[1]

    def peek(self):
        return self.heap[0][1] if self.heap else None

    def is_empty(self):
        return len(self.heap) == 0