# Author: OMKAR PATHAK
# Source: https://github.com/OmkarPathak/Data-Structures-using-Python/blob/master/Queue/Queue.py

class Queue(object):
    def __init__(self, limit):
        self.queue = []
        self.front = None
        self.rear = None
        self.limit = limit
        self.size = 0

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    # to check if queue is empty
    def isEmpty(self):
        return self.size <= 0

    # to add an element from the rear end of the queue
    def enqueue(self, data):
        if self.size >= self.limit:
            return -1          # queue overflow
        else:
            self.queue.append(data)

        # assign the rear as size of the queue and front as 0
        if self.front is None:
            self.front = self.rear = 0
        else:
            self.rear = self.size

        self.size += 1

    # to pop an element from the front end of the queue
    def dequeue(self):
        if self.isEmpty():
            return -1          # queue underflow
        else:
            self.queue.pop(0)
            self.size -= 1
            if self.size == 0:
                self.front = self.rear = 0
            else:
                self.rear = self.size - 1

    def getSize(self):
        return self.size
