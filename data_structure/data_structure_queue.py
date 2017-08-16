# Think about how to construct a queue in C
# a queue belongs to linear list, thus it has two types of storage-- array & linklist
# the characteristic of a queue is FIFO
# in a queue,we need to consider actions: enter a queue,leave a queue

# But how to achieve queue in python?

# we've known that in python sequence is just the concept of linear list.
# List [] tuple (,)  range  string all belong to sequence
#Intuitively, list and tuple may both can be used to achieve a queue.
#Let's try!


class Queue(object):
    def __init__(self,size): # the length of the queue
        self.queue =[]           # it's a list
        self.size = size         # size = 8
        self.front = 0
        self.rear = -1

    def isFull(self): # the function to judge a queue is full
        return True if self.rear == self.size - 1 else False

    def isEmpty(self):
        return True if self.rear == -1 else False  # list[-1] means the last place

    def push(self,data):
        if self.isFull():
            raise Exception('QueueOverFlow')
        self.queue.append(data)
        self.rear += 1  # rear = rear + 1

    def pop(self):
        if self.isEmpty():
            raise Exception('QueueEmpty')
        self.rear -= 1
        return self.queue.pop(self.front)  # take out front element

    # Is there something to heed up about the order of these languages?
    # when push: we append data first,and then rear= rear + 1
    # when pop: we firstly make rear = rear - 1;then pop out list[front]

    def first(self):
        return self.queue[self.front]  # take out the front element of the queue

    def last(self):
        return self.queue[self.rear]  # take out the rear element

    def show(self):
        print self.queue


# Summary: 1. In order to use the same structure in other files, we def class to realize a queue
#             Class can involve: the node structure of queue & the conducting function in queue
#             So it's just like an envelop!

#          2. the essence of queue is the same, no matter we code in python or C.
#             That's to say, first we need to construct a queue.
#             In C, we can use an array[] or * sqrt as a linklist; In python, we just use a list []
#             Once we have a queue:
#             We will try to judge its empty/ full; We will push,pop elements from queue
#             Those actions involve how to change our front and rear. And this is a little bit different in different languages.

