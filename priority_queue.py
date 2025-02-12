import itertools
from heapq import heappush, heappop


class PriorityQueue:
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.counter = itertools.count()

    def __len__(self):
        return len(self.pq)

    def add_task(self, priority, task):
        if task in self.entry_finder:
            self.update_priority(priority, task)
            return self
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def update_priority(self, priority, task):
        entry = self.entry_finder[task]
        count = next(self.counter)
        entry[0], entry[1] = priority, count

    def pop_task(self):
        while self.pq:
            priority, count, task = heappop(self.pq)
            del self.entry_finder[task]
            return priority, task
        raise KeyError('pop from an empty priority queue')

