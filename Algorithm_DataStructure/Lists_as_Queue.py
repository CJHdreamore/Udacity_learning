#-------------Buit-in Class-----------------------------
#from collections import deque
#queue = deque(['Eric','John','Michael'])
#queue.append('Terry')
#queue.append('Graham')
#print queue.popleft()  # the first to arrive now leaves
#print queue
#--------------------------------------------------------

class Queue:
    def __init__(self,head = None):
        self.storage = [head]

    def enqueue(self,new_element):
        self.storage.append(new_element)

    def peek(self):
        return self.storage[0]

    def dequeue(self):
        if self.storage:
            out_element = self.storage[0]
            del self.storage[0]
            return out_element
            # return self.storage.pop(0)
        else:
            return None

q = Queue(1)
q.enqueue(2)
q.enqueue(3)
print q.peek()
print q.dequeue()
q.enqueue(4)
print q.dequeue()









