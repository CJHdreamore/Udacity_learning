# Hello! It's time for us to realize a stack in python!
# Do you find it a little easier to start?
# Stack can also be realized in python using class list[]
# Keep in mind, it is FILO.

class Stack(object):
    def __init__(self,size):
        self.stack = []
        self.size = size
        self.top = -1

    def set_size(self,size):
        if self.top >= size:
            raise Exception("StackWillOverFlow")
        self.size = size

    # The big point is the top of the stack is not static,it's changeble
    # while push(),in other word,self.top will increase

    def isFull(self):
        return True if self.size == self.top + 1 else False

    def isEmpty(self):
        return True if self.top == -1 else False

    def pop(self):
        if self.isEmpty():
            return None
        self.top -= 1     # why the expert writes
        return self.stack.pop()  # -- does it mean we pick out the bottom number?



    def push(self,data):
        if self.isFull():
            raise Exception('StackOverflow')
            return
        self.stack.append(data)
        self.top += 1

    def stacktop(self):
        if self.isEmpty():
            raise Exception('StackIsEmpty')
            return
        return self.stack[self.top]


    def show(self):
        print self.stack


if __name__ == '__main__':
    S = Stack(10)
    for i in range(0,4):
        S.push(i)
    print S.stacktop()





