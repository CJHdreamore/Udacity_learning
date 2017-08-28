# Binary Search Tree
# This shows us we can achieve our goal either by an iteration ( while function)
# or by a recursive function.
class Node(object):
    def __init__(self,value):
        self.value = value
        self.left = None
        self.right = None

class BST(object):
    def __init__(self,root):
        self.root = Node(root)

    def insert(self, new_val):
        start = self.root
        return self.bst_insert(start,new_val)

    def bst_insert(self,start,new_val):
        if start:
            if start.value > new_val:
                if start.left == None:
                    start.left = Node(new_val)
                else:
                    self.bst_insert(start.left,new_val)

            elif start.value < new_val:
                if start.right == None:
                      start.right = Node(new_val)
                else:
                    self.bst_insert(start.right,new_val)
        else:
            return -1

    def search(self,find_val):
        '''Binary search tree'''
        start = self.root
        while (start):
            if start.value < find_val:
                start = start.right
            elif start.value > find_val:
                start = start.left
            elif start.value == find_val:
                return True
        return False

    def insert2(self,new_val):
        start = self.root
        while start:
            if start.value > new_val:
                if (start.left != None):
                    start = start.left
                else:
                    start.left = Node(new_val)
                    return
            if start.value < new_val:
                if (start.right != None):
                    start = start.right
                else:
                    start.right = Node(new_val)
                    return
        start = Node(new_val)

    def preorder_print(self,start,traversal):
        if start:
            traversal.append(start.value)
        if start.left:
            self.preorder_print(start.left,traversal)
        if start.right:
            self.preorder_print(start.right,traversal)
        return traversal

    def print_tree(self):
        '''Print out all tree nodes as they are visited in a
        pre-order traversal'''
        start = self.root
        traversal = []
        self.preorder_print(start,traversal)
        string = ''
        for nodes in traversal:
            string = string + str(nodes) + '-'
        return string[0:-1]



# Set up tree
tree = BST(4)

# Insert elements
tree.insert(2)
tree.insert(1)
tree.insert(3)
tree.insert(5)
# Check search
print tree.search(4)
print tree.search(6)
print tree.print_tree()